# Partner service list request (public.partner.service_list.requested)

Type: application feature. Repositories: cynthus-commerce (Partner service), cynthus-shared, cynthus-trust, cynthus.
Tracking issue: cynthus#98. Slices: cynthus-shared#176 to #181 and #186 to #188, cynthus-trust#87, cynthus-commerce#15, cynthus#99.
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
- F19 (cynthus ADR-013 and cynthus-shared `core/event`): a request is decided. `EventRequest`, `EventRequestDecision`
  (answer, answer reason, conditions), `DecisionCondition` (exact-match settling, expiry) and `EventRequestResponse`
  (`approve`, `conditionally_approve`, `deny`, `in_effect`) exist; decisions are append-only; an owner on their own
  resource is `approved` with the reason `permitted`; a request that needs approval is `approved_conditionally` with
  `approval_required` and a condition `approval_granted` that expires; a requester without the privilege is `denied`
  with `insufficient_privileges`. The enumeration has no reason for an automatic approval by role. Verified.
- F20 (cynthus-shared `EventRequest`): it holds an `Event` (full Tenant, Workspace and User objects) and a `User | System`
  requestor, so it cannot hold a `SignalEvent` or an id-only requestor. Verified.
- F21 (cynthus-shared `SignalAccess.authorize`): it verifies the token and also refuses a missing permission with
  `Forbidden`, so a denial can never become a decision. Verified.
- F22 (cynthus-trust `auth/decision_store.py`, `access_requests.py`): only Auth makes decisions today, for access
  requests, in its own tables. No other service creates a decision. Verified.

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
- D7 (2026-11-25): every request is decided as ADR-013 describes. An owner on their own resource is `approved` with
  `permitted`. A requester with access through a role (contributor, manager, admin) is approved automatically, with the
  new reason `access_permitted`. A requester who needs authorization is `approved_conditionally` with
  `approval_required`. A requester without the privilege is `denied` with `insufficient_privileges`.
- D8 (2026-11-25): the partner list is a platform-owned registry: a token with `partner:read` is approved with
  `access_permitted`, any other is denied. The approval flow exists in the code but this feature never takes it.
- D9 (2026-11-25): decisions are published as their own signals, so the audit engine (not built yet) and every
  subscriber see them as they happen: `public.decision.event_request.approved`, `.approved_conditionally`, `.denied` and
  `.denied_conditionally`. The responded signal keeps its status and gains 202 for a conditional approval.
- D10 (2026-11-25): decisions are not stored in per-service storage (this overrides the ADR-013 line that other
  services keep their own records). They are cached for short-term retrieval.

## Assumptions (confirm or change)

- A1: names are exactly `public.partner.service_list.requested` and `public.partner.service_list.responded` (domain
  `partner`, aggregate `service_list`). "Service list" means the list of `Partner` rows.
- A2: the request has `schema_version` (default 1) and `filters.name` (optional, case-insensitive contains). No filter
  returns all partners ordered by name. No paging.
- A3: the response has `schema_version`, `status` (200, 202, 401, 403 or 422), `result` (a list of `{id, name}`) and
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
- A13: the decision rules (`DecisionPolicy`), in order: the claims lack the permission, `denied` with
  `insufficient_privileges`; a platform-owned resource (no tenant), `approved` with `access_permitted`; the resource
  tenant is the token tenant and the token is the owner's, `approved` with `permitted`; the same tenant, `approved` with
  `access_permitted`; another tenant, `approved_conditionally` with `approval_required` and one condition
  `approval_granted` that expires in 5 days (ADR-013). The "another tenant" rule is provisional (R8).
- A14: a token that is forged, for another tenant, workspace or actor, or without a workspace is not decided: it is
  refused with the existing errors and an audit record, because there is no identity to decide about.
- A15: a decision signal is published on the public topic without an access token, with the lifecycle action
  `created`, and carries the request id, the requested event type and action, the requestor, the answer, the reason,
  the conditions and who decided.
- A16: the decision cache keeps a decision for 24 hours by default (configurable), and for a conditional decision until
  its latest open condition expires, if that is later. It is a cache, not a store: a restart may lose it, and the
  decision signal is the durable record once the audit engine exists.

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

### Revision 2026-11-25: decisions (S10 to S12, and the revised S6 and S8)

The `Authorizer`, `authorize` and `read_event` of the design above are replaced by one dependency, `decided_request`,
and the handler of S8 follows the decision flow. Everything else above stands.

- S10 (cynthus-shared): `EventRequest.event` is `Event | SignalEvent` and `requestor` is `User | System | UUID` (with the
  property `requestor_id`); `EventRequestAnswerReason.ACCESS_PERMITTED`; `SignalAccess.authenticate(message,
  signal_message)`, the checks of `authorize` without the permission check; `cynthus.service.DecisionPolicy(
  determined_by, approval_expiry, clock)` with `decide(request, claims, *, permission, resource_tenant_id=None) ->
  EventRequestResponse` following A13.
- S11 (cynthus-shared): `SignalDomainType.DECISION`; the signal actions `approved`, `approved_conditionally` and
  `denied_conditionally`; the four signals above with one payload (`EventRequestDecisionPayload`) and four messages;
  the core events `EventRequestApprovedEvent`, `EventRequestApprovedConditionallyEvent`, `EventRequestDeniedEvent` and
  `EventRequestDeniedConditionallyEvent` (a base `EventRequestDecisionEvent` with `deciding(request, decision)` that picks
  the subclass); `DecisionSignalGenerator` in the default registry.
- S12 (cynthus-shared): `cynthus.service.DecisionCache(redis, ttl)` with `put(response)` and `get(event_request_id)`
  over `RedisClient`, storing the decision data as JSON under `decision:<id>`; a Redis failure is logged, never raised.
- S6 (revised): `SignalRouter` injection and `dependency_overrides` as before, plus a handler may return a list or tuple
  of results that are published in order; `SignalRequest` (event, claims, message, request, response, decision event);
  `decided_request(event_class, permission, access, policy, resource_tenant=None, cache=None, registry=None)`: parse the
  message, `access.authenticate`, read the event, build the `EventRequest`, `policy.decide`, build the decision event,
  cache the decision, return the `SignalRequest`.
- S8 (revised): the handler uses `Depends(decided_request(PartnerServiceListRequestedEvent, 'partner:read',
  signal_access, policy, cache=cache))`; when the decision is in effect it queries and answers 200; a conditional
  decision answers 202 and a denial 403, without a query; it returns `[request.decision_event, response_event]`; the hooks
  fire for the request event, the decision event and the response event. The `TokenError` handler publishes a 401
  response and no decision.

## Slices

All issues use P2 - Medium and status Planned.

- S1 (cynthus-shared#176) cynthus-shared, M, Infrastructure, Shared: signals, payloads, messages, factories, docs. No dependencies.
- S2 (cynthus-shared#177) cynthus-shared, M, Infrastructure, Shared: `SignalEvent` and `EventHooks`. No dependencies.
- S3 (cynthus-shared#178) cynthus-shared, M, Infrastructure, Shared: `SignalEventReader` and `SignalEventMismatch`. Depends on S2.
- S4 (cynthus-shared#179) cynthus-shared, M, Infrastructure, Shared: partner events, data models, `PartnerSignalGenerator`, registry entry.
  Depends on S1, S2 (S3 for the read tests).
- S5 (cynthus-shared#180) cynthus-shared, M, Infrastructure, Shared: `SignalRouter`, `UnknownSignalError`, exception handlers, publishing of
  the returned value. Depends on S2.
- S6 (cynthus-shared#181) cynthus-shared, M, Infrastructure, Shared: injection, `dependency_overrides`, result lists, `SignalRequest`
  and `decided_request` (revised). Depends on S3, S5, S10, S11 and S12.
- S7 (cynthus-trust#87) cynthus-trust, XS, Application, Trust: `partner:read` and its role grants. No dependencies.
- S8 (cynthus-commerce#15) cynthus-commerce, M, Application, Platform: pin bump, `service.py`, `dependencies.py`, `routes/event.py`, tests,
  CHANGELOG (revised: decisions). Depends on the shared release (S1 to S6, S10 to S12) and S7 for a live token.
- S9 (cynthus#99) cynthus, XS, Infrastructure, Docs: Signal Catalog entries. Depends on S1.
- S10 (cynthus-shared#186) cynthus-shared, M, Infrastructure, Shared: decision model for id-based events (`EventRequest`
  with `SignalEvent`, `access_permitted`, `SignalAccess.authenticate`, `DecisionPolicy`). No dependencies.
- S11 (cynthus-shared#187) cynthus-shared, M, Infrastructure, Shared: decision signals, events and generator. Depends on S4
  (the generator takes a `SignalEvent`).
- S12 (cynthus-shared#188) cynthus-shared, S, Infrastructure, Shared: `DecisionCache`. Depends on S11 (the data model).

Order (revised 2026-11-25): S1 to S3, S5, S7 and S9 are done. S4 and S10 run in parallel; S11 follows S4 and S12
follows S11 (S12 can start on the data model once S11 is specified); S6 follows S10, S11 and S12; the owner merges the
shared slices and cuts v0.20.0; then S8. The decision signals also need Signal Catalog entries (a follow-up issue in
this repository).

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
  (also when it raises); `dependency_overrides` replaces a dependency for that router only; a returned list or tuple
  publishes each result in order; handlers must name their parameters `signal`, `publisher` and `error`.
- AC13 (unit, S10): `EventRequest` accepts a `SignalEvent` and a UUID requestor; `SignalAccess.authenticate` returns the
  claims for a genuine matching token and raises `TokenError` or `Forbidden('workspace_required')` otherwise, without
  a permission check; each rule of A13 gives the stated answer, reason and conditions, with a fixed clock.
- AC14 (unit and feature integration, S11): the four decision signals have exactly the names in D9; `deciding` returns the
  event that matches each answer; the generator gives an equal message for an equal event with the conditions in the
  payload; an approved, a conditional and a denied decision published through `EventMessagePublisher` give three distinct
  signals.
- AC15 (unit, S12): `put` then `get` returns an equal decision; an unknown id returns `None`; the TTL is 24 hours, or until
  the latest condition expires when later; a Redis error is logged and not raised.
- AC7 (unit, S7): `partner:read` is in the permissions of the roles in A5 and in no other role; a member's issued token
  carries it.
- AC8 (unit, S8): with fake dependencies, a request without a filter builds a statement with no `where`; with
  `name='acme'` the compiled `where` filters on name; an approved decision gives a responded event with status 200,
  the request's correlation id and the items; `hooks.fire` is called for the request event, the decision event and the
  response event; the handler returns the decision event and then the response event.
- AC9 (unit, S8): a denied decision gives a published `denied` decision event and a 403 response without using the
  session; a conditional decision gives 202; a forged token gives a 401 response and no decision; an invalid payload gives
  422; a response is always published.
- AC10 (feature integration, S8): against the testing schema (`test_partner`, role `partner_test`) with two partners, no
  filter returns both ordered by name, a name filter returns the match, an empty table returns 200 and an empty list.
- AC11 (system integration, S8): a requested message with a genuine `partner:read` token published on the bus (in
  memory in CI; RabbitMQ on the Cynthus VM as a manual check recorded in the PR) reaches the Partner service; the
  `approved` decision signal and a responded message with the same correlation id come back, and the decision is cached.
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
- R8: the rule for a request on another tenant's resource (A13, the approval case) is the owner's to refine; it lives
  only in `DecisionPolicy` and this feature never takes it.
- R9: `EventRequest` gains alternatives in its types (S10); Auth uses its own SQL models for decisions, so it is not
  affected, but a type check in an unseen caller could be: stop and report.
- R10: a cache is not a store (A16). Until the audit engine exists, a decision signal nobody consumes is the only record;
  the owner accepted this on 2026-11-25.

## Out of scope

- A route or service that publishes the request (A8): a follow-up plan.
- Paging, other filters, partner create, update and delete signals and events, soft deletes on Partner (the model has no
  `deleted_at`): follow-up plans.
- Events that write to the database (A11, R2).
- Moving the query behind a repository (cynthus#71).
- Decision tables per service, and the audit engine that consumes the decision signals.
- The approval reply flow for a conditional decision (the owner is told and answers with a new request), and the
  notification of the owner: no resource of this feature needs it.

## Issue plan

- Tracking: cynthus#98 (label Feature, size XL, priority P2 - Medium), with this document.
- S1 cynthus-shared#176 "Partner service list signals" (M); S2 cynthus-shared#177 "SignalEvent and EventHooks" (M); S3
  cynthus-shared#178 "SignalEventReader: events from received signals" (M); S4 cynthus-shared#179 "Partner events and
  signal generator" (M); S5 cynthus-shared#180 "SignalRouter" (M); S6 cynthus-shared#181 "Router dependency injection
  and decided_request" (M); S7 cynthus-trust#87 "partner:read permission" (XS); S8 cynthus-commerce#15 "Answer
  public.partner.service_list.requested" (M); S9 cynthus#99 "Signal Catalog: partner service list" (XS);
  S10 cynthus-shared#186 "Decision model for id-based events" (M); S11 cynthus-shared#187 "Decision signals" (M); S12
  cynthus-shared#188 "DecisionCache" (S).
- All are Task issues in milestone "Cynthus 1.0 - Platform Foundation Complete", status Planned.
