# Partner service list request (public.partner.service_list.requested)

Type: application feature. Repositories: cynthus-commerce (Partner service), cynthus-shared, cynthus-trust, cynthus.
Tracking issue: cynthus#98. Slices: cynthus-shared#176 to #181, cynthus-trust#87, cynthus-commerce#15, cynthus#99.
Planned with the owner on 2026-11-25. The owner's request, kept verbatim:

> Now, let's set up a `@broker.subscriber(...)` endpoint in containers/partner/src/partner/routes/event.py. The service should listen for a "public.partner.service_list.requested" event. The request handler should call `session.query(Partner).where(...).all()`. Once the results are retrieved from the database, the partner list should be serialized and publishedvia a signal message object. This will require the appropriate event and signal classes to be created. Please open the corresponding GitHub issues.

The owner then replaced the first sketch with this design: handlers take a session and an authorizer through
dependency injection, turn the signal into an event, return an unauthorized response when the check fails, look up with
`select(Partner).where(...)` and return a response event. The shared libraries hold the common logic and the Partner
specific logic lives in the router handler methods. Events exist so event hooks can be added later and so create, update
and delete events can later serialize themselves to the database.

## Intent (binding)

The Partner service (cynthus-commerce) listens on the signal bus for `public.partner.service_list.requested`. Each
request becomes a domain event, is authorized, reads the matching partners from the service's own database, and the
answer is published as a signal message generated from a response event. The events exist so that hooks can be attached
to them later; the signal and event classes this needs are created. First thoughts on approach (the handler shape, the
router, the dependencies) go in Design.

## Survey: what exists

- F1 (cynthus-commerce, partner/routes/event.py): a copy of core's Redis FastStream router with a placeholder
  `item.added` subscriber; it names no signal. Verified.
- F2 (cynthus ADR-007): service code never names a broker; services register a `subscription` and `handler` on
  `ServiceModule`; `SignalBroker` gives the publisher and subscriber. Verified.
- F3 (cynthus-shared `ServiceModule`): `routers` (FastAPI routers), `subscription` and `handler` together,
  `signal_access`, `database`. The handler is called with `(signal, publisher)`. Verified.
- F4 (cynthus-shared): `PartnerApiPublicSubscription` exists. Verified.
- F5 (cynthus-shared `messaging`): a signal is a definition class, a payload class and a message class; requests and
  responses come in pairs (inventory). `SignalDomainType` has no `PARTNER`; there is no `component/partner`. Verified.
- F6 (cynthus-shared `docs/signal-generators.md`, `core/event`, `messaging/generator`): an `Event` is a pure record
  (tenant, workspace, resource, action, data validated by an optional `data_model`); a `SignalGenerator` with
  `SignalContract`s turns one event into one message; `EventMessagePublisher` publishes through a
  `SignalGeneratorRegistry`; the generator must be pure. The direction is event to message only: nothing turns a
  received message into an event. Verified.
- F7 (cynthus-shared `Event`, `UserEvent`, `Service.build_event`): an event needs full `Tenant`, `Workspace`,
  `Resource` and (for `UserEvent`) `User` objects; a `Tenant` needs a name, a type and an owner `User` with first
  name, last name and email. A request signal and the token carry only ids (`TokenClaims`: subject,
  tenant, workspace, roles, permissions, owner). Verified.
- F8 (cynthus-shared): no hook or listener mechanism for events exists. Verified (grep).
- F9 (cynthus-core inventory `handler.py`, `request_handler.py`): the current pattern: `SignalAccess.authorize`, an
  inline `select`, a `...RespondedMessage` with `status`, `result`, `error`, ids copied from the request. It builds
  messages directly, not events. Verified.
- F10 (cynthus-shared `Database` v0.19.0): `get_session(env, service)` returns an `AsyncSession` with no `.query()`;
  each call opens a session from a cached engine, so the `Database` object must be one per process. Verified.
- F11 (cynthus-shared, `fast-depends` 3.0.11 in the Partner image): `fast_depends.inject` resolves `Depends`,
  including `yield` dependencies, and validates with pydantic; FastStream is built on it. Verified (installed).
- F12 (cynthus-shared `SignalAccess.authorize`): async; raises `Forbidden` (403) or `TokenError` (401); records an
  audit decision. Verified.
- F13 (cynthus-commerce Partner model): `Partner(Base)` with `id` and `name`; no tenant, workspace or `deleted_at`.
  Verified.
- F14 (cynthus-trust `auth/role_permissions.py`): permissions are strings per role; no `partner:read`. Verified.
- F15 (cynthus Signal Catalog, Feature Registry): no `public.partner.service_list.*` entry, and no feature id found
  (grep only). Not verified beyond that.
- F16 (cynthus docs/features/persistence-layer.md): the approved plan puts persistence in separate pure serializers
  (`to_record` and `from_record`), not in methods on events or ORM models, and is not built yet. The owner's idea of an
  event method or an ORM `deserialize` that writes the database differs from it. Not needed for a read-only list; see
  Risks. Verified (plan text).
- F18 (session briefing 2026-11-14, multi-agent pilot; searched all design docs and briefings): the "signal-to-event
  direction" is listed as not done, and no document designs a signal reader, an id-based event or event hooks. The same
  briefing lists an open item: an event class does not check its action (relevant to `SignalEvent`, see A9). No work in
  progress was found. Verified (grep of docs, plans and briefings).
- F17 (cynthus-shared CI): ruff, one class per module with a unit test module each, coverage gate 90 and 80 percent.
  Verified.

## Decisions (owner)

- D1 (2026-11-25): the subscriber is a decorator on a shared `SignalRouter` (`@router.subscriber(signal_name)`),
  dispatching through `ServiceModule` and `SignalBroker`; not a literal FastStream broker.
- D2 (2026-11-25): the query is async: `(await session.execute(select(Partner).where(...))).scalars().all()`.
- D3 (2026-11-25): the caller must be authenticated and hold a new `partner:read` permission.
- D4 (2026-11-25): handlers use dependency injection (`Depends`) for the session, the authorizer and the events; the
  authorizer raises and the router maps the exception to a responded status; a handler returns the response event.
- D5 (2026-11-25): signals become domain events, so hooks can attach later. A new id-based `SignalEvent` base carries
  tenant, workspace and actor ids; the existing `Event` is unchanged.
- D6 (2026-11-25): a minimal `EventHooks` (`register`, `fire`) is built now; nothing is registered yet.

## Assumptions (confirm or change)

- A1: names are exactly `public.partner.service_list.requested` and `public.partner.service_list.responded` (domain
  `partner`, aggregate `service_list`). "Service list" means the list of `Partner` rows.
- A2: the request has `schema_version` (default 1) and `filters.name` (optional, case-insensitive contains). No filter
  returns all partners ordered by name. No paging.
- A3: the response has `schema_version`, `status` (200, 401, 403 or 422), `result` (a list of `{id, name}`) and
  `error`; ids and the correlation id are copied from the request.
- A4: partners are not tenant-scoped (F13); tenant and workspace are used for the access check and recorded on the
  events only.
- A5: `partner:read` goes to the same roles as `inventory:read`.
- A6: the `item.added` scaffold is removed from the Partner `event.py`.
- A7: the shared slices release together as v0.20.0; the Partner slice bumps its pin to it.
- A8: who publishes the request is a follow-up (not in this feature).
- A9: `SignalEvent` has `id_`, `correlation_id`, `occurred_on`, `tenant_id`, `workspace_id`, `actor_id`,
  `service_id`, `action`, `data` and an optional `data_model` like `Event`, and the same `event_type` rule; it is not a
  subclass of `Event`. A subclass may declare the actions it allows and the event rejects any other (the open
  action-check item in F18).
- A10: event hooks run after the event is built and before the response is published; a hook that raises is logged and
  does not change the response (decided now so the first hook cannot break answers; revisit with the first real hook).
- A11: events that create, update or delete (and write to the database) are a later plan; see F16 and the Risks.
- A12: board values: Size XS S M L XL; Priority P2 - Medium; milestone "Cynthus 1.0 - Platform Foundation Complete";
  status Planned.

## Design

cynthus-shared:
- Signals (S1): `SignalDomainType.PARTNER`, `PublicPartnerSignalBase`, `PublicPartnerServiceListSignalBase`
  (aggregate `service_list`), `PublicPartnerServiceListRequestedSignal` and `...RespondedSignal`; in
  `cynthus.messaging.component.partner`: payloads `PartnerServiceListRequestedPayload` (`filters:
  PartnerServiceListFilters`), `PartnerServiceListItem`, `PartnerServiceListRespondedPayload`; messages
  `PartnerServiceListRequestedMessage` and `PartnerServiceListRespondedMessage`; test factories.
- `cynthus.core.event.SignalEvent` (S2): the id-based event base described in A9. `cynthus.core.event.EventHooks` (S2):
  `register(event_class, hook)` (async callable), `fire(event)` awaits the hooks registered for the class of the event
  and its bases, in registration order, logging and swallowing a hook's exception (A10).
- `cynthus.messaging.generator.SignalEventReader` (S3): `read(message, claims, event_class)` builds the event from a
  received message and the verified `TokenClaims`: ids from the claims (they must equal the ids in the message; a
  mismatch raises `SignalEventMismatch`), `data` from the payload fields the contract maps to `data.*` (the contract
  `sources` read in reverse), `correlation_id` and `id_` from the message.
- Partner events and generator (S4): `PartnerEvent(SignalEvent)`, `PartnerServiceListRequestedEvent` with
  `PartnerServiceListRequestedData` (`name: str | None`), `PartnerServiceListRespondedEvent` with
  `PartnerServiceListRespondedData` (`status`, `items`, `error`); `PartnerSignalGenerator` with a contract for each
  signal, added to `SignalGeneratorRegistry.default()`. The generator is pure (docs/signal-generators.md).
- `cynthus.service.SignalRouter` (S5): `subscriber(signal_name)` registers an async function; `dispatch(signal,
  publisher)` runs the function registered for `signal.event_type`, then publishes what it returns (an `Event` or a
  `SignalEvent` through `EventMessagePublisher`, a message directly, `None` publishes nothing);
  `exception_handler(ExceptionType)` registers a function that turns an exception into the returned event; an
  unregistered signal raises `UnknownSignalError` so the broker dead-letters it; a type registered twice raises
  `ValueError`. `ServiceModule(handler=router.dispatch)` is the wiring.
- Injection (S6): `dispatch` calls handlers through `fast_depends.inject`. Handlers may declare `signal:
  ReceivedSignal`, `publisher: SignalPublisher` and any `Depends(...)`, including `yield` dependencies;
  `router.dependency_overrides` replaces a dependency in tests. `cynthus.service.Authorizer` is a dependency factory:
  `authorize('partner:read')` returns `TokenClaims` or raises `Forbidden` or `TokenError`, recording the audit
  decision through `SignalAccess` (F12). `read_event(EventClass)` is a dependency that uses `SignalEventReader` with the
  claims and parses the signal body.

cynthus-trust (S7): `PARTNER_READ = 'partner:read'` in `auth/role_permissions.py`, granted as in A5.

cynthus-commerce (S8), containers/partner/src/partner:
- `service.py`: one `partner_database = Database()`, `signal_access`, `hooks = EventHooks()`, and
  `ServiceModule(subscription=PartnerApiPublicSubscription(), handler=event.dispatch, signal_access=signal_access,
  database=partner_database)`.
- `dependencies.py`: `partner_session()`, a `yield` dependency that opens `partner_database.get_session(environ.get('ENV'),
  'partner')`, rolls back on error and always closes.
- `routes/event.py`: `event = SignalRouter()`; `@event.exception_handler(Forbidden)` returns a responded event with
  status 403, `TokenError` 401, `ValidationError` 422; and the handler:


```text
@event.subscriber(PublicPartnerServiceListRequestedSignal.name)
async def handle_service_list_requested(
    claims: TokenClaims = Depends(authorize('partner:read')),
    request: PartnerServiceListRequestedEvent = Depends(read_event(PartnerServiceListRequestedEvent)),
    session: AsyncSession = Depends(partner_session),
    hooks: EventHooks = Depends(partner_hooks),
) -> PartnerServiceListRespondedEvent:
    await hooks.fire(request)
    statement = select(Partner).order_by(Partner.name)
    if request.data.name: statement = statement.where(Partner.name.ilike(f'%{request.data.name}%'))
    partners = (await session.execute(statement)).scalars().all()
    response = PartnerServiceListRespondedEvent.answering(request, items=[...], status=200)
    await hooks.fire(response)
    return response
```

cynthus (S9): Signal Catalog entries for both signals; this design document.

## Slices

All issues use P2 - Medium and status Planned.

- S1 (cynthus-shared#176) cynthus-shared, M, Infrastructure, Shared: signals, payloads, messages, factories, docs. No dependencies.
- S2 (cynthus-shared#177) cynthus-shared, M, Infrastructure, Shared: `SignalEvent` and `EventHooks`. No dependencies.
- S3 (cynthus-shared#178) cynthus-shared, M, Infrastructure, Shared: `SignalEventReader` and `SignalEventMismatch`. Depends on S2.
- S4 (cynthus-shared#179) cynthus-shared, M, Infrastructure, Shared: partner events, data models, `PartnerSignalGenerator`, registry entry.
  Depends on S1, S2 (S3 for the read tests).
- S5 (cynthus-shared#180) cynthus-shared, M, Infrastructure, Shared: `SignalRouter`, `UnknownSignalError`, exception handlers, publishing of
  the returned value. Depends on S2.
- S6 (cynthus-shared#181) cynthus-shared, M, Infrastructure, Shared: injection, `dependency_overrides`, `Authorizer`/`authorize`,
  `read_event`. Depends on S3 and S5.
- S7 (cynthus-trust#87) cynthus-trust, XS, Application, Trust: `partner:read` and its role grants. No dependencies.
- S8 (cynthus-commerce#15) cynthus-commerce, M, Application, Platform: pin bump, `service.py`, `dependencies.py`, `routes/event.py`, tests,
  CHANGELOG. Depends on the shared release (S1 to S6) and S7 for a live token.
- S9 (cynthus#99) cynthus, XS, Infrastructure, Docs: Signal Catalog entries. Depends on S1.

Order: S1, S2, S7, S9 in parallel; then S3 and S5 in parallel; then S4 and S6; the owner merges S1 to S6 and cuts
v0.20.0; then S8. Seven slices are shared-library work; the Partner handler itself is S8.

## Acceptance criteria (testable)

- AC1 (unit, S1): the signal classes' names equal `public.partner.service_list.requested` and `.responded`; each
  message `event_type` equals its signal name; payloads validate and round-trip through JSON; a non-string `name`
  filter is rejected.
- AC2 (unit, S2): `SignalEvent` has the fields in A9, derives `event_type` like `Event`, checks `data` against
  `data_model`, and rejects an unknown data key. `EventHooks.fire` calls the hooks for the event's class and its bases
  in registration order; a hook that raises is logged and the next hook still runs; firing with no hooks does nothing.
- AC3 (unit, S3): `SignalEventReader.read` gives an event whose ids come from the claims, whose `data` equals the
  payload fields mapped by the contract, and whose `correlation_id` matches the message; claims with a different
  tenant, workspace or actor than the message raise `SignalEventMismatch`.
- AC4 (unit, S4): `PartnerSignalGenerator` gives an equal message for an equal event (purity), with the event id as
  `event_id`; the registry default includes both partner events; an event of a class with no generator raises
  `UnknownEventError`.
- AC5 (unit, S5): `dispatch` calls the function registered for the type and publishes an event it returns through
  `EventMessagePublisher`; a raised exception with a registered handler publishes that handler's event; an unregistered
  signal raises `UnknownSignalError`; a duplicate registration raises `ValueError`; `None` publishes nothing.
- AC6 (unit, S6): a handler's `Depends` are resolved, including a `yield` dependency that is closed after the handler
  (also when it raises); `dependency_overrides` replaces a dependency; `authorize('partner:read')` returns claims for a
  token with the permission, raises `Forbidden` without it and `TokenError` for a forged token, and each case records an
  audit decision.
- AC7 (unit, S7): `partner:read` is in the permissions of the roles in A5 and in no other role; a member's issued token
  carries it.
- AC8 (unit, S8): with fake dependencies, a request without a filter builds a statement with no `where`; with
  `name='acme'` the compiled `where` filters on name; the handler returns a responded event with status 200, the
  request's correlation id and the items; `hooks.fire` is called for the request event and for the response event.
- AC9 (unit, S8): the exception handlers give status 403 for `Forbidden`, 401 for `TokenError` and 422 for an invalid
  payload, the session is never used in those cases, and a response is always published.
- AC10 (feature integration, S8): against the testing schema (`test_partner`, role `partner_test`) with two partners, no
  filter returns both ordered by name, a name filter returns the match, an empty table returns 200 and an empty list.
- AC11 (system integration, S8): a requested message with a genuine `partner:read` token published on the bus (in
  memory in CI; RabbitMQ on the Cynthus VM as a manual check recorded in the PR) reaches the Partner service and a
  responded message with the same correlation id comes back.
- AC12 (lint, CI, all slices): `ruff check .`, the coverage gate, one class per module with a test module each and
  `markdownlint` pass; S9 lists both signals in the Signal Catalog (checked by `check_markdown.py`). Accessibility: not
  applicable, there is no user interface.

## Risks and unknowns

- R1: the dependency layer replaces the `(signal, publisher)` handler shape only inside `SignalRouter`; other services
  keep their handlers. If `fast_depends` behaves differently for async generators in this loop, stop and report.
- R2: F16: the owner wants events that serialize to the database (or ORM `deserialize`), while the approved
  persistence-layer plan keeps serializers separate from business code. Not needed here (read only); the first create,
  update or delete feature needs a decision between them. Do not start persistence methods in these slices.
- R3: whether a hook failure should ever abort the request (A10) is decided only by the first real hook.
- R4: `SignalEventReader` reads the contract `sources` in reverse; if a contract maps a payload field from `resource`,
  `user` or `env`, reading it cannot give data: stop and report.
- R5: the shared release gates S8; the owner approves each merge and the tag.
- R6: if `SignalConsumer` completes instead of dead-lettering an exception from `dispatch`, stop and report before
  changing the consumer.
- R7: scope. Seven shared slices for one read-only list is a large foundation; it is the owner's chosen design (D4 to
  D6) and later features reuse it.

## Out of scope

- A route or service that publishes the request (A8): a follow-up plan.
- Paging, other filters, partner create, update and delete signals and events, soft deletes on Partner (the model has no
  `deleted_at`): follow-up plans.
- Events that write to the database (A11, R2).
- Moving the query behind a repository (cynthus#71).

## Issue plan

- Tracking: cynthus#98 (label Feature, size XL, priority P2 - Medium), with this document.
- S1 cynthus-shared#176 "Partner service list signals" (M); S2 cynthus-shared#177 "SignalEvent and EventHooks" (M); S3
  cynthus-shared#178 "SignalEventReader: events from received signals" (M); S4 cynthus-shared#179 "Partner events and
  signal generator" (M); S5 cynthus-shared#180 "SignalRouter" (M); S6 cynthus-shared#181 "Router dependency injection
  and Authorizer" (M); S7 cynthus-trust#87 "partner:read permission" (XS); S8 cynthus-commerce#15 "Answer
  public.partner.service_list.requested" (M); S9 cynthus#99 "Signal Catalog: partner service list" (XS).
- All are Task issues in milestone "Cynthus 1.0 - Platform Foundation Complete", status Planned.
