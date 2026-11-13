# ADR-007: A selectable signal broker (Azure Service Bus or RabbitMQ)

**Status:** Proposed (2026-11-10)
**Supersedes:** the rejection of RabbitMQ in ADR-006. ADR-006 otherwise stands: Azure Service Bus remains the default
broker, and the `SignalPublisher` and `SignalSubscriber` interfaces are unchanged.

## Context

ADR-006 chose Azure Service Bus and rejected "switch the backbone to RabbitMQ/NATS/Kafka" because it contradicted
ADD v6 and the Azure deployment. Four things have changed:

1. **The emulator cannot run the stack.** Microsoft's emulator allows 10 concurrent connections and has said the
   limit will not change (Azure/azure-service-bus-emulator-installer#58). Eleven services use the bus, so even one
   connection per process (cynthus-core#139) exceeds the cap. A spike on 2026-11-10 showed that a link-routing
   multiplexer does not help either: the emulator accepts one `$cbs` authorization link per connection.
2. **Production may not be Azure.** The hosting cost analysis (2026-11-10) puts the stack at about $210 to $460 a
   month on Azure Container Apps and about $25 to $60 a month on a single VPS.
3. **The interfaces already exist.** Application code depends on `SignalPublisher` and `SignalSubscriber`
   (ADR-006, standards section 6), and `InMemorySignalBus` already implements both for tests. A second broker is
   one more implementation, not a rewrite.
4. **What we use is small.** An audit of the code on 2026-11-10 found: publish to one topic, a subscription per
   service, complete on success, dead-letter on a handler error, per-message properties (`message_id`,
   `correlation_id`, the `authorization` token), and a delivery limit and TTL in the emulator configuration. We do
   not use abandon or defer, lock renewal, scheduled enqueue, sessions or duplicate detection.

## Decision

The broker is chosen by the environment, and Azure Service Bus remains the default.

- `SIGNAL_BROKER` is `servicebus` (default), `rabbitmq` or `memory`.
- `RABBITMQ_URL` holds the RabbitMQ connection (`amqp://user:password@host:5672/vhost`). It is a secret and lives in
  an untracked `.env`, like `SERVICE_BUS_CONNECTION_STRING`.
- Service code never names a broker. `ServiceApplication` and the service factories ask a `SignalBroker` factory
  (in cynthus-shared) for the connection, publisher and subscriber. This replaces the two places that name Service
  Bus today: `ServiceApplication._lifespan` and the per-service `from_environment()` calls.
- The RabbitMQ implementation talks to the broker with `aio-pika` directly, as the Service Bus implementation talks
  to the Azure SDK directly. FastStream is not involved (its Azure broker is a community package; its RabbitMQ broker
  is not needed behind our interfaces).

### RabbitMQ topology

RabbitMQ 4.x with quorum queues. Every service declares what it needs at start-up; the declarations are idempotent.

- Topic (`cynthus-events-topic`): A durable topic exchange with the topic's name
- Event type (`audit.identity.user.rejected`): The routing key. The dotted names already fit topic routing.
- Subscription (`cynthus-profile-sub`): A durable quorum queue of that name, bound to the exchange with `#` (all events)
- Subscription filter (scheduler): Binding keys on the queue instead of `#`
- Complete: Ack
- Dead-letter on a handler error: Reject without requeue, to a dead-letter exchange; a `<subscription>.dlq` queue keeps the message and its `x-death` history
- `MaxDeliveryCount` (10): `x-delivery-limit` 10 on the quorum queue; the broker dead-letters at the limit
- TTL (`PT1H`): `x-message-ttl` 3,600,000 ms
- Message properties: Standard properties: `message_id`, `correlation_id`, `type` (the event type), `content_type`; headers carry `authorization`
- Accepted by the broker: Publisher confirms on the channel
- Peek-lock: Prefetch with manual ack: an unacked message returns to the queue if the channel closes

The `authorization` token travels in a header, never in the body, exactly as it travels as an application property on
Service Bus. Log lines carry the event type and correlation id only.

### Behaviour that must match

- `publish` does not return before the broker confirms the message, and raises `SignalBusUnavailable` when it cannot.
  The same limits apply: 5 seconds per attempt, then a 15-second cool-down in which callers fail at once, and the
  `on_unavailable` hook fires (it feeds `ServiceOutage` and the Service Unavailable page).
- A handler that returns settles its signal; a handler that raises dead-letters it, and later signals are not blocked.
- Cancelling `run()` stops delivery without settling the signals in hand; the broker redelivers them.
- A process holds one broker connection (`aio-pika` robust connection) with a channel for publishing and a channel for
  consuming, so the connection count stays at one per process. RabbitMQ has no connection cap of the emulator's kind.

### Differences the services must accept

- RabbitMQ has no scheduled enqueue, sessions, duplicate detection or lock renewal. Nothing uses them. Idempotency
  stays in the services (`processed_requests`).
- Redeclaring a queue with different arguments fails. Changing the delivery limit or TTL means a new queue name or a
  deliberate delete, and the adapter reports the mismatch clearly.
- Dev and production may use different brokers. The shared test suite runs against the in-memory bus and, when
  `RABBITMQ_URL` is set, against a real RabbitMQ; a service's behaviour must not depend on the broker.

## Options considered

- Keep Service Bus only and stop services to fit the emulator: Status quo. Blocks running the whole stack in dev.
- Multiplex connections with Qpid Dispatch: Tried; failed on one `$cbs` link per connection. Possible with a custom CBS responder, but costly and Azure-only.
- Kafka: No per-message dead-lettering, heavier, poor fit for subscription-per-service. Rejected.
- ActiveMQ Artemis (AMQP 1.0): Closest to Service Bus semantics, but a heavy JVM broker and still needs its own adapter. Not chosen.
- **RabbitMQ behind the existing interfaces, selected by environment**: **Chosen.**

## Consequences

- Dev can run the full stack without the emulator's cap. Production may run on a VPS with RabbitMQ or on Azure with
  Service Bus.
- Two adapters to keep in step. The shared tests run both through the same cases so a gap shows up in CI.
- cynthus-shared gains the dependency `aio-pika` and a minor release (v0.11.0). Services adopt the factory in their own
  pull requests and then pin the new tag. Services with their own startup (the Core API, the Celery worker and
  scheduler, Auth) are converted separately.
- Engineering standards section 6 is updated to say the broker is selectable.

## Review triggers

Revisit this decision if RabbitMQ and Service Bus behaviour diverge in a way tests cannot hide; if production settles on
one broker for good (then retire the other adapter); or if a third broker is proposed.

## Sources

- Azure/azure-service-bus-emulator-installer#58 (connection limit; "no plans to increase").
- Spike notes, 2026-11-10 briefing: link routing fails on the single `$cbs` link per connection.
- Hosting cost analysis, 2026-11-10.
- RabbitMQ 4.x documentation: quorum queues (delivery limit, dead-letter strategies), dead letter exchanges, publisher
  confirms.
