# Plan: signal broker reconnect (retry forever, exponential backoff, max 1 hour)

Status: approved by the owner 2026-11-16. Tracking issue: cynthus#88. Slice 1 is cynthus-shared#161; slices 2 to 6 are cynthus-core#249, #250, #251, cynthus-trust#85 and cynthus-intelligence#37.

## Intent
Every Cynthus service that holds a signal broker connection must recover by itself when the broker is away at start or
goes away later, with exponential backoff capped at one hour and no limit on attempts. The logic lives once, in
cynthus-shared. Each of the eight services is tested on its own, in its own repository.

## Survey (verified 2026-11-16 on origin/dev unless marked)
- F1. `SignalConsumer.run()` (cynthus-shared `src/cynthus/service/signal_consumer.py`) opens its receiver once and has no
  reconnect. Only the Azure SDK's short internal retry applies. If it raises, the listener task ends.
- F2. `RabbitMqSignalSubscriber._read` (`messaging/subscriber/rabbitmq_signal_subscriber.py`) opens a channel once; a
  failure ends the task. `RabbitMqConnection` uses `aio_pika.connect_robust`, which reconnects after a first successful
  connect but raises if the first connect fails.
- F3. `ServiceBusSignalPublisher` already fails fast: 5 s per attempt, a 15 s cool-down, then `SignalBusUnavailable`,
  and calls `on_unavailable` (the API reports an outage flag in Redis). `RabbitMqSignalPublisher` also raises
  `SignalBusUnavailable`. This is the request-path behaviour the owner chose to keep.
- F4. `SignalBroker.from_environment()` builds the one connection and the publisher and subscriber. It has no state a
  health check can read.
- F5. `ServiceApplication` (shared) already serves `/signal/health`: 503 while the subscriber task is not running or the
  database does not answer. It is the only shared health route; whether the api, worker, scheduler, domain and recipe
  containers all use it: not verified.
- F6. The scheduler runs the listener on a thread and touches an alive file every 10 s from a separate task; the
  container health check reads the file's age. The worker listener thread has no alive file (core
  `worker/tasks/ingress/signal_listener.py`). Both call `subscriber.run()` once and let it end.
- F7. The api starts `subscriber.run()` with `asyncio.create_task` in `api/__init__.py`; auth builds a broker and a
  publisher (trust `auth/__init__.py`); analysis and chat come from `ServiceApplication` or the same pattern (not
  verified for each).
- F8. The spike of 2026-11-15: the VM worker's listener died at start (host unreachable), never retried, and the
  container stayed healthy. This is the failure this plan removes.
- F9. cynthus-shared tests live under `test/unit/...`; CI runs ruff, pytest with coverage and `check_coverage.py`.
  Versions: `pyproject.toml` is `0.0.0`; how the service repos pick up a shared change (branch pin, release): not verified.

## Decisions (owner, answered 2026-11-16)
- D1. Tests are per repository only: shared tests the logic; each service repo tests its own service. No cynthus-testing
  suite in this plan.
- D2. A request that publishes while the broker is down fails fast with 503 as today; retries run in the background.
- D3. Health reports the broker state in the body and stays healthy (HTTP 200) while the service is alive and retrying.
- D4. Network errors and rejected credentials retry forever; missing or malformed configuration fails at start.

## Assumptions (confirm or change)
- A1. Delays: first 1 s, doubling, capped at 3600 s, each with up to 20 percent random reduction (so never above the
  cap). The delay resets to 1 s after the connection has stayed up for 60 s.
- A2. Every attempt logs one warning line (attempt number, next delay, exception class name only: the message can name
  the namespace or hold a URL). Once the cap is reached it logs once per hour, not per attempt.
- A3. A message the handler raises on is still dead-lettered (not retried by this plan).
- A4. Sleeping in 1-second steps is not needed: the loop sleeps the whole delay but wakes at once on cancellation.
  The scheduler's alive file keeps its own task, so it keeps touching while the loop sleeps.
- A5. The fake broker for tests is a public module of cynthus-shared (`cynthus.service.fake_broker`), as the in-memory
  bus already is, so each service repo can write its test without a second fake.
- A6. Size, priority and milestone as the board values: size XS S M L XL; priority P0 to P3 (P2 here); milestone
  "Cynthus 1.0 - Platform Foundation Complete".
- A7. One cynthus-shared release gates slices 2 to 6; each service repo pins it the way it pins shared today.

## Design
In cynthus-shared (`src/cynthus/service/`, one class per module):
- `backoff.py`: `Backoff(base=1.0, factor=2.0, cap=3600.0, jitter=0.2, random=...)` with `next_delay()` and `reset()`.
- `broker_state.py`: `BrokerState` with `connected`, `since`, `attempts`, `last_error` (class name), `mark_connected()`,
  `mark_disconnected(error)`. Held as `SignalBroker.state`.
- `reconnecting_loop.py`: `ReconnectingLoop(state, backoff, errors, sleep=asyncio.sleep, stable_after=60.0)` with
  `async run(open_and_read)`: calls it; on one of `errors` marks disconnected, logs, sleeps the delay, tries again;
  on `CancelledError` stops; any other exception (configuration, a bug) propagates and ends the task loudly.
- `SignalConsumer.run()` and `RabbitMqSignalSubscriber._read` wrap their body in `ReconnectingLoop`. The receiver and
  channel are opened inside the loop, so a first-time failure is the same as a later one.
- Publishers call `state.mark_disconnected` on `SignalBusUnavailable` and `mark_connected` on a successful send. They
  keep fail-fast (D2).
- `ServiceApplication._module_health` adds `signal_broker` (`connected` or `disconnected`), `since` and `attempts`; the
  status is `degraded` with HTTP 200 while disconnected and the task is alive (D3). A dead task is still 503.
- `fake_broker.py`: `FlakyServiceBusClient` and `FlakyRabbitMqConnection`: fail the first N opens (or drop after M
  messages), then work; deliver scripted messages; no network.
- Docs: `docs/cynthus/messaging/broker.md` (behaviour, delays, log lines, health fields) and CHANGELOG.
In each service repository: bump shared; make sure the listener task is started inside the supervised path (api,
worker, scheduler, domain, recipe, auth, analysis, chat); surface `signal_broker` in its health answer where it does
not use `ServiceApplication`; keep the alive file or add one for the worker; the per-service test.

## Slices
- S1 (M, cynthus-shared, issue #161): Backoff, BrokerState, ReconnectingLoop, consumer and subscriber wiring, publisher
  state, health fields, fake broker, docs. Release gates S2 to S6.
- S2 (S, cynthus-core): api and scheduler.
- S3 (S, cynthus-core): worker (listener thread in the main Celery process; add the alive file or an equivalent signal
  the container health reads).
- S4 (S, cynthus-core): domain (one connection for its services) and recipe.
- S5 (S, cynthus-trust): auth.
- S6 (S, cynthus-intelligence): analysis and chat.
Order: S1, then S2 to S6 in parallel. Each of S2 to S6 follows the spec of its issue with the same test shape.

## Acceptance criteria
Shared (S1):
1. (unit) `Backoff`: delays double from 1 s, never exceed 3600 s even with the largest jitter, jitter stays within 20
   percent below, `reset()` returns to 1 s, 1000 consecutive `next_delay()` calls never raise.
2. (unit, fake clock) `ReconnectingLoop`: 1000 failures in a row are retried with no limit; a success followed by 60 s of
   uptime resets the delay; a drop before 60 s does not; cancellation during a sleep stops it at once; a configuration
   error (`ValueError`) is not retried and propagates; a rejected-credentials error is retried.
3. (feature integration, fake broker) `SignalConsumer` and `RabbitMqSignalSubscriber` with a broker that is down at start
   then up: they subscribe and deliver the queued signal; with a broker that drops after two messages: they resume and
   deliver the rest; a handler that raises is dead-lettered and the loop continues.
4. (unit) `BrokerState` and `/signal/health`: `disconnected` with HTTP 200 and `degraded` while retrying, `connected`
   and `ok` after, 503 only when the subscriber task is not running.
5. (unit) No log line in a retry contains the connection string, the URL or the exception message (checked with a
   connection string and URL containing a marker).
6. (lint, CI) ruff clean, one class per module, 100 percent line and branch on the new modules, markdown checks.
Per service (S2 to S6, each in its own repository, no network):
7. (feature integration) With the broker down at start, the service starts, its health answers 200 with
   `signal_broker: disconnected`; when the fake broker comes up it subscribes to its own subscription and a published
   signal reaches its handler; health answers `connected`. One such test for each of the eight services: api, worker,
   scheduler, domain, recipe, auth, analysis, chat.
8. (feature integration) A request that publishes while down returns the same 503 as today within the existing 5 s limit
   (api and auth at least; the other services where they publish).
9. (unit) The alive file of the scheduler and worker keeps being touched while the listener sleeps in a back-off.

## Risks and unknowns
- A container is healthy while its listener is down (D3): nothing stops a broken broker from going unnoticed except the
  state field and the logs. A later change to `cynthus-env run` can read the field (separate issue, not here).
- Retrying rejected credentials forever (D4) logs one warning per hour at the cap: a wrong password is visible but slow
  to notice. The first attempts log every time.
- The Azure SDK has its own internal retries and timeouts, so the first delays are longer than 1 s in practice.
- How shared changes reach each service repo (A7) is not verified.
- Domain hosts several services over one connection: one loop per subscription means several loops marking one state.
  The state is the connection's, so it uses the last transition; the test for S4 covers two subscriptions.

## Out of scope
Changing the dead-letter rules, per-segment credentials (cynthus#87), the 10 connection limit, publisher
wait-and-retry in requests, `cynthus-env` reading the state, system tests in cynthus-testing, any live run on the VM.

## Issue plan
- Tracking issue: cynthus#88 (Feature, XL, P2, Planned).
- S1: cynthus-shared#161 (retitle and rewrite acceptance to criteria 1 to 6).
- S2 to S6: new issues in cynthus-core (three), cynthus-trust, cynthus-intelligence, each Infrastructure subtype, size S,
  Planned, with criteria 7 to 9 for their services.
- cynthus-core#248, cynthus-trust#84 and cynthus-intelligence#36 stay cancelled and are linked from the tracking issue.
