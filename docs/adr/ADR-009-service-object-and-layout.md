# ADR-009: One Service object and one layout for every service

**Status:** Proposed (2026-11-11)
**Relates to:** ADR-007 (signal broker), ADR-008 (hosting several services in one container), cynthus-shared issue 93
(refactor shared model classes). The tenant, organization and workspace vocabulary is left to a separate decision
(see "Not decided here").

## Context

The execution path through a Cynthus service is hard for a person to follow because the same thing is built in
different ways in different places. Reading the five domain services and shared issue 93 on 2026-11-11:

1. **"Service" means three things.** `cynthus.core.service.Service` (issue 93) is the identity of a service
   (`id_`, `name`, `domain`). `ServiceApplication` and `ServiceModule` (cynthus-shared) are what runs. And
   `inventory.services.ItemService`, `ShelfService` and the like are per-aggregate operations classes. A reader cannot
   tell from the word which one is meant.
2. **A service has no single definition.** Each package builds its parts as module-level singletons
   (`core_database`, `signal_access`, `request_handler`) in `signal_handler.py`, a free function
   (`handle_public_signal`) and an `initialize()` that hands them to `ServiceApplication` as separate arguments. To
   learn what Inventory is, you read four files and assemble it.
3. **One concept, four shapes.** A location exists as `core.resource.StorageLocation` (issue 93), a SQLAlchemy model,
   pydantic read and write schemas, and a messaging payload. The conversions between them are written by hand in each
   service.
4. **The identity of the actor is thin.** Facts a service publishes carry `actor_id` of the user who asked. The service
   that acted has no identity on the wire, although issue 93 already models it (`InventoryService` has a fixed id and
   `EventRequest.requestor` may be a `System`).

Issue 93 solves the first and third problems in the data model: one layout for pydantic classes (`id_`, frozen
identity for singletons, one class per file), and a `Service`, `System`, `Resource` and `Event` family. It is not yet
connected to the running code, and it is unfinished (`InventoryService.build_event` raises `NameError`;
`Service.publish_message` is a stub).

## Decision

A service is one **Service object**, defined in one place, with the same shape in every repository.

### The Service object

- **Identity (data, in `cynthus.core.service`).** `Service` keeps the shape in issue 93: `id_` (a fixed UUID per service,
  frozen), `name`, `domain`. `InventoryService`, `ProfileService` and the rest subclass it with their fixed values.
  This part is pure data: no IO, no web framework, no database. It can be serialized (`model_dump`) for health
  bodies, registries, audit signals and logs.
- **Runtime (in `cynthus.service`).** `ServiceModule` (ADR-008) takes the identity: `ServiceModule(service=InventoryService(),
  routers=..., subscription=..., handler=..., database=..., signal_access=...)`. Its `name` is `service.name`. The
  health body, the Domain registry and the logs use `service.id_` and `service.name`, never a free string.
- **Layering rule.** `cynthus.core` does not import `cynthus.service`, FastAPI, SQLAlchemy or the broker. The runtime
  imports the data, never the reverse. This is what lets the same object describe a service to any code that uses it.
- **One entry point per package.** Each service package exposes `service`: the `ServiceModule` built from its identity
  and parts. `inventory.service` is the answer to "what is Inventory". The package's `app` is
  `ServiceApplication(name, modules=[service])`, and the Domain container loads `package.service`. This replaces the
  `service_module()` factory added in ADR-008 step 2, which is the one seam to change.

### One layout for every service package

```text
containers/<service>/src/<service>/
    __init__.py        exposes `service` and `app`
    service.py         the only place the Service object and its parts are assembled
    handler.py         handle(signal, publisher): dispatch to operations
    routes/            FastAPI routers (event routes)
    models/            SQLAlchemy persistence models (one class per file)
    schemas/           request and response schemas (one class per file)
    operations/        the per-aggregate classes now in `services/` (ItemOperations or similar)
```

- `services/` is renamed `operations/` so that "service" means only the Service object.
- `signal_handler.py` becomes `handler.py`; its module-level singletons move into `service.py`, which builds them once and
  hands them to the handler explicitly. A reader opens `service.py` to see every part and `handler.py` to see the flow.
- Services with no database or no migrations (Logistics) simply omit those parts; the files that exist have the same
  names everywhere.
- A new service starts from this layout; the Domain container, health, logging and registries need no special case for it.

### One representation, converted in one place

- A `Resource` class from `cynthus.core.resource` is the in-memory form of a thing (a location, a shelf, an item).
  Persistence models and wire payloads are converted to and from it by methods on the model or schema
  (`to_resource()`, `from_resource()`), not by code in each handler.
- An `Event` (issue 93) converts to and from the signal messages in `cynthus.messaging` in one adapter, so a handler can
  work with the data model and publish through one call. The signal contract on the wire does not change in this ADR.
- Serialization is pydantic's: `model_dump(mode='json')` and `model_validate_json`. No hand-built dicts.

### The service as an actor

Facts and audit signals published by a service name the service as the actor (`service.id_`) in addition to the user who
asked, using the `User | System` requestor of issue 93. Where this needs a signal field that does not exist, it is added
as an optional field (additive, no schema break; see cynthus-shared issue 102 for the schema version).

## Not decided here

- **Tenant, organization and workspace.** Issue 93 models `Tenant` (personal or organizational) and `Workspace`; the
  signals and tokens carry `organization_id`. Which word is the boundary, what an organization is, and how tenants
  collaborate is a separate decision (a following ADR). This ADR does not depend on it: the Service object is the same
  either way.
- **Moving the existing signal vocabulary** (`lifecycle_action`, `actor_id`) onto the `Event` model's vocabulary
  (`EventAction`). The adapter above hides the difference until that is decided.

## Options considered

1. **Leave each service as it is and write the standard down.** Cheapest, but the layout is already inconsistent and a
   document does not make the next service follow it. Rejected.
2. **Make the issue 93 `Service` carry the runtime parts too.** One class, but then `cynthus.core` imports the web
   framework and the database, and the object can no longer be serialized or used by code that only needs identity.
   Rejected: the layering rule is what keeps the object the same for every user of it.
3. **Identity in `core`, runtime in `service`, joined by `ServiceModule` (this ADR).** Keeps issue 93's data model and
   ADR-008's hosting, and adds only the join.

## Consequences

- Issue 93 must land first as a proper change: fix `InventoryService`, finish or remove the stubs, add the other services'
  identities, add tests for the layering rule. It is the first piece of work.
- Every service package is touched once to adopt the layout. Done a service at a time, behind unchanged signals and
  routes, with each service's suite unchanged in what it asserts.
- `ServiceModule` gains a required `service` argument; the single-module arguments of `ServiceApplication` stay until the
  last package has moved.
- The `operations/` rename changes import paths inside each package only.

## Work plan (each piece is its own issue, PR and test run in the dev environment)

1. cynthus-shared: land issue 93 (data model), fix the known defects, add identities for every service, test the layering.
2. cynthus-shared: `ServiceModule` takes `service`; health and the Domain registry use it.
3. cynthus-core: move one service (Logistics, the smallest) to the layout and the `service` entry point; check it runs alone
   and inside the Domain container. Then Shopping, Profile, Inventory, Recipe.
4. The same layout for the services in the other repositories (trust, intelligence, health, commerce, engine).
5. The `Resource` and `Event` conversions, one aggregate at a time, starting with Inventory.
6. Update the engineering standards with the layout.

## Review triggers

- A service cannot follow the layout without a special case: fix the layout, not the service.
- The Event adapter needs a signal change: raise it with the schema version (issue 102).

## Sources

- cynthus-shared issue 93, branch `93-refactor-shared-model-classes` (read on 2026-11-11).
- ADR-007, ADR-008.
