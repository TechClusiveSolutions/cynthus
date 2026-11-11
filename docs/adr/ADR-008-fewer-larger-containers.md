# ADR-008: Run the domain services as fewer, larger containers

**Status:** Proposed (2026-11-11)
**Relates to:** ADR-007 (selectable signal broker); ADR-009 (the Service object and one layout), which replaces the
`service_module()` factory described here with a `service` entry point per package. Core issue 184 asked for this design.

## Context

The core stack runs one container per domain service: inventory, profile, recipe, shopping and logistics, besides the
API, Session, web, Scheduler and Worker. Measured on JMac on 2026-11-11, with the stack on RabbitMQ:

| Container | Idle CPU | Memory |
|---|---|---|
| inventory, profile, recipe, shopping | 4 to 5 % of a core each | 109 to 120 MB each |
| core API, Session | about 2.5 % each | about 114 MB each |
| auth | 7 % | 137 MB |
| analysis, chat | 2.5 % each | 99 to 106 MB each |
| scheduler, worker | under 1 % | 92 MB, 271 MB |
| RabbitMQ (replacing the Service Bus emulator at 647 MB) | under 1 % | 117 MB |

Most of each Python service's memory is the interpreter, FastAPI, SQLAlchemy and the shared library, which every
container loads again. Four of the five domain services (inventory, profile, shopping, logistics) have the same shape:
`ServiceApplication`, one subscription, one handler, one schema in the shared core database. Recipe has the same shape
plus an importer that fetches web pages and reads images.

What is already true:

- **One database.** The domain services share the core Postgres; each owns a schema and its own Alembic version table
  (`version_table_schema`). Nothing to merge.
- **One Redis** per group (core, auth, intelligence), already.
- **The signal contract is per subscription.** Each service has its own subscription (queue), so which process reads it
  does not change what the other services see.
- **Both broker implementations take several subscriptions.** `subscribe(topic, subscription, handler)` can be called
  many times before `run()`, over one connection.

What would be gained, and what would not. Folding four services into one process saves about 3 interpreters' worth,
roughly 300 to 350 MB and 3 idle CPU slices, out of a stack of about 2 GB. That is real on a small VPS and
irrelevant on a large host. The larger savings already happened with ADR-007: dropping the Service Bus emulator
saves 530 MB. The second benefit is **broker connections**: with every service running there are 11 (one per
process); hosting inventory, profile, shopping and logistics in one process makes it 8. That is under the Service Bus
emulator's cap of 10 again, which matters if Azure Service Bus stays a supported choice.

## Decision

Build the domain services into **one image that hosts several modules, chosen by `SERVICES`**. The grouping is a
deployment choice, not a code choice.

- `SERVICES=inventory,profile,shopping,logistics` starts those modules in one process. `SERVICES=recipe` starts one
  module. The same image, started twice with different values, gives two containers. Dev runs one container; a
  production host can split it when it needs to scale or isolate a module.
- A module keeps everything it has today: package, models, schema, migrations, subscription, handler, tests. The
  signal contract does not change.
- `ServiceApplication` gains a **module** concept. A module is `name`, `routers`, `subscription`, `handler`,
  `signal_access`, `database`. `ServiceApplication` takes one module (what it does today) or a list. For a list it
  opens Redis, the token verifier and the broker once, calls `subscribe` once per module, and runs one subscriber.
  A service passing the current arguments keeps working unchanged (a shared minor release).
- **Kept separate**, as proposed in core issue 184: Auth (the security boundary and its own database), the Session
  gateway, web (nginx), Analysis and Chat (different resources and an isolated network), the Core API (public edge),
  and one Celery container for the Worker and Beat.
- **Recipe is not in the default group.** It fetches arbitrary web pages and decodes uploaded images; a slow or
  failing import must not stall inventory or shopping handlers that share its event loop. It stays its own container
  by default (`SERVICES=recipe`), and the setting lets us change that later.

### How the open questions are settled

- **Failure isolation.** All modules in a container share its fate if the process dies, and share one event loop. To
  keep one module's handler from starving the others, a module's handler runs under the subscriber's existing
  per-message error handling (a raise dead-letters that one signal) and a per-handler timeout (new, default 60 s,
  `SIGNAL_HANDLER_TIMEOUT_SECONDS`; the first draft said 30 s, raised so the Recipe import cannot be cut off). A module whose subscriber task stops is reported unhealthy; the container is
  restarted by its orchestrator, as a single service is today.
- **Health.** `/signal/health` answers for the container: 200 only while every module's subscription is being read and
  the database answers. The body lists each module (`{"modules": {"inventory": "ok", ...}}`), and
  `/signal/health/{module}` answers for one, so a person can see which module failed. The container health check
  keeps using `/`.
- **Independent scaling.** Scale the container; every module in it scales together. To scale one module alone, run a
  second container with only that module in `SERVICES` and take it out of the first. Queues are per subscription, so
  two consumers of one queue share its work (competing consumers); no change to the broker.
- **Migration order.** At start-up each selected module runs its own `alembic upgrade head`, one after another, in the
  order of `SERVICES`. A failure stops the container with the module named. Schemas are independent, so the order
  does not matter for correctness. `<MODULE>_RUN_MIGRATIONS=false` keeps working per module.
- **Test layout.** Module code and tests stay where they are (`containers/<module>/src`, `containers/<module>/test`),
  and each module's suite and coverage gate stay as they are. The hosting image adds a small `containers/domain`
  package (module registry, entry point, Dockerfile) with its own tests: the registry, `SERVICES` parsing, the
  aggregated health and a start-up test that loads all modules in one process.
- **Package names.** Several modules in one interpreter share one import namespace. `profile` is also a standard
  library module, and `inventory`, `recipe`, `shopping` and `logistics` are generic names. The image installs each
  module under its own name and loads it through the registry; the first step of the work is a check that all five
  import side by side. If a name clashes, that module is renamed (a package rename, not a behaviour change).
- **Build.** The module sources live in different directories, so the image builds from the repository root and copies
  the selected modules' `src`, `migrations` and requirements (the union, with one shared pin set).
- **Redis event routers.** Each module's `routes/event.py` builds its own Redis router from the `CACHE_*` settings.
  These are placeholders today. In the hosting process they connect to the same Redis; they are kept as they are and
  reviewed when real event routes arrive.

*Amended 2026-11-11 after steps 1 and 2:* the subscriber is shared, so if it stops every hosted service is unavailable;
only the database check is per service. The first draft implied a per-service subscriber check.

## Options considered

1. **Keep one container per service (status quo).** Simplest to reason about and to scale. Costs about 330 MB and
   three idle CPU slices more than needed, and leaves the stack at 11 broker connections. Remains correct on a large
   host.
2. **Merge the services into one codebase and one package.** Smallest runtime, but it ends independent ownership of
   schemas, tests and release, and is hard to undo. Rejected: the same savings come from hosting, without merging.
3. **One image, modules chosen by `SERVICES` (this ADR).** Same savings, modules stay independent, and the grouping can
   change per environment without code changes.
4. **Move to a serverless platform that bills per request.** Outside this ADR; the hosting cost analysis covers it.

## Consequences

- The default dev stack runs three containers fewer (inventory, profile, shopping and logistics become one) and the
  broker sees three connections fewer.
- A fault that kills the process takes down all modules in that container. Splitting by `SERVICES` is the remedy.
- `ServiceApplication` is more complex; the single-module path must stay unchanged and covered by its existing tests.
- Compose, the hosting cost analysis and the standards (section on containers) are updated when the work lands.

## Work plan (each piece is its own issue, PR and test run in the dev environment)

1. **cynthus-shared:** `ServiceApplication` accepts several modules; the handler timeout; aggregated and per-module
   health. Release as a minor version.
2. **cynthus-core:** check that the five packages import side by side; add `containers/domain` (registry, entry point,
   image, tests); add a compose service `domain` under a profile, beside the existing ones.
3. **Dev environment:** run the end-to-end scripts against `domain` (the existing containers stopped), with the broker
   stopped and started, and with a poison message. Compare memory, CPU and connection counts with this ADR.
4. **Switch the default** in compose to `domain`, keep the old services available under a profile for one release, then
   remove them.
5. Update the hosting cost analysis and the standards.

## Review triggers

- A module needs to scale or fail independently of the others: move it to its own container.
- A module's imports clash with another's and cannot be renamed cheaply.
- The measured saving is under 200 MB: stop after step 3 and keep the status quo.

## Sources

- Measurements: `docker stats` on JMac, 2026-11-11, stack on RabbitMQ with the Service Bus emulator stopped.
- ADR-007, core issue 184, the hosting cost analysis of 2026-11-10.
