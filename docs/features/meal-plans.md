# Meal plans (create, share, template, recur and make private)

Type: application feature. Repositories: cynthus-core (module `meal`), cynthus-shared, cynthus-trust, cynthus. Tracking issue: cynthus#90.
Walked through with the owner section by section, 2026-11-18 to 2026-11-20. Slices: cynthus#91, cynthus-shared#162 and #163,
cynthus-trust#86, cynthus-core#252 to #257. Follow-up plans: cynthus#92 (invitations), #93 (Places in Logistics), #94 (web pages),
#95 (tokens and entitlements).

## Intent (binding)

The owner's request, kept as stated:

- A user can create, update, retrieve, list and delete meal plans.
- Plans have predefined and custom meal frequencies.
- Plans have predefined and custom durations.
- A user can create meal plan templates.
- A user can share their meal plans with other users.
- A user can invite other users to view, contribute to, and/or manage their meal plans.
- A user can make their plans private.

Problem: there is no meal service, no plan table and no plan API. Only the plan created, updated and deleted signal
classes exist. Sharing and privacy have no model below the workspace.

Clarifications by the owner (binding):

- A plan is workspace-scoped and carries a `workspace_id`. The plan's owner is chosen at creation. `owner_id` is
  optional in the create request and defaults to the caller. A caller may create as the workspace owner only if their
  workspace role is `super_admin` or `manager`; a `contributor` or `admin` creates only as themselves. The service
  checks the value against the token and never trusts the body alone. A plan's owner deletes it and answers its
  access requests, as does the workspace owner and a `super_admin`.
- Joining a workspace gives no right to create or change resources.
- Default: a new plan is listable and viewable (contents included) to everyone in its workspace.
- Share means: listable in the workspace, and the owner allows or denies access requests (ADR-013 flow, 5-day expiry).
- Editing by someone else needs a role on the plan, from an allowed access request.
- Plan roles: viewer (reads), contributor (edits meals), admin (meals, frequency, duration), manager (admin plus
  making the plan private). Only the owner deletes. Managers cannot delete. An admin cannot make a plan private.
- A user with no workspace gets a confirmation page that a workspace will be created for them; on confirm the client
  calls `POST /auth/workspaces`, otherwise nothing is created. The meal module answers `workspace_required`.
- Invitations (the owner sending a view, contribute or manage request, and invitations to a meal or a series of meals
  such as lunch every Thursday from Dec 1 to Dec 31, with cancel and response per occurrence or per series) are their
  own story sequence after this plan. This plan designs for them.

## Survey: what exists

Verified in the code and documents on 2026-11-18 to 2026-11-20, clones on `dev` after `git pull`.

- F1 (cynthus-documentation, docs/features/feature-registry.md): FT-MP-004 "Create a Meal Plan" (day, week or month;
  High; Phase 1) is the only plan feature. No entry exists for templates, sharing, invitations or privacy of plans.
  Recipe libraries have roles (FT-RM-001, Phase 2). Engagements and groups are FT-EM and FT-GM (Phase 2).
- F2 (docs/signals/signal-catalog.md): `public.meal.plan.created`, `.updated` and `.deleted` are published by
  `cynthus-core-api` and consumed by analysis, scheduler and audit. No request, response, share or invitation signal.
- F3 (cynthus-shared, src/cynthus/messaging/component/meal; the GitHub repository cynthus-messaging-core now redirects to
  cynthus-shared, and the local clone cynthus-messaging-core is stale): `MealPlanCreatedPayload` has `plan_id`, `horizon`,
  `start_date`, `end_date`, `meal_count`, `astri_assisted`. No frequency, visibility or owner. Dates are `datetime` in
  the class and `date` in the docs. The recipe component has `recipe_requested.py` and `recipe_responded.py`; the meal
  component has no equivalent.
- F4 (cynthus-core, containers/): api, cache, db, domain, inventory, logistics, profile, recipe, scheduler, session,
  shopping, web, worker. No `meal` module. Recipe is the pattern: `request_handler.py`, `operations/recipe_service.py`,
  `models/` (with `owner_id` beside the workspace), `schemas/`, Alembic migrations, and
  `api/src/api/routes/recipe_request.py` (publishes a request signal, acknowledges with a correlation id; the answer
  arrives on the websocket).
- F5 (cynthus-core issue #130, open): asks for plans with a period, meals per day (1 to 48), a default plan, "the last
  plan cannot be deleted", meals and the web pages. Overlaps this request on plans, durations and frequencies.
  #13, #133 and #134 touch the same area.
- F6 (ADR-008, ADR-009; containers/domain/src/domain/modules.py): domain services run as modules of one image chosen
  by `SERVICES`. `MODULES` lists inventory, profile, shopping, logistics and recipe; recipe runs on its own by default.
  cynthus-shared `core/service` has one class per service with a fixed `SERVICE_ID`; there is no `MealService`.
- F7 (ADR-014): each segment keeps its own database and cache; segments meet only through signals and the Auth keys.
- F8 (ADR-011): every delete is a soft delete; `SoftDeletable` exists in cynthus-shared.
- F9 (ADR-010 amendment 2): roles viewer, contributor, manager, admin, super_admin; private content is readable only
  by its owner and super_admin; the private flag does not exist yet; nobody grants a role above their own.
- F10 (ADR-013): access requests are requestor-initiated, with append-only decisions and conditions; expiry 5 days for
  access, 7 days for collaboration. `EventRequest`, `EventRequestDecision` and `DecisionCondition` exist in
  cynthus-shared `core/event`. No owner-initiated invitation exists. Not verified: that the expiry job is built.
- F11 (cynthus-trust, auth/role_permissions.py): permissions are inventory, profile, recipe and shopping read and
  write. No `meal:*`.
- F12 (cynthus-trust, auth/tenancy.py, routes/token.py): the token's `owner` claim means the subject owns the tenant of
  the token. Only a tenant's owner can create a workspace in it. The workspace's `owner_id` is only in Auth's
  database. `TokenClaims` has `organization_id` (tenant), `workspace_id`, `roles`, `permissions`, `owner`; it has no
  subscription tier and no workspace owner id.
- F13 (cynthus-core, inventory/lookup.py): a record in another workspace is reported as not found, never forbidden.
- F14 (cynthus-trust, routes/workspace.py): `POST /auth/workspaces` and `POST /auth/workspaces/switch` exist and return
  a new token. cynthus-shared `security/require_permission.py` and `service/signal_access.py` already answer
  `workspace_required`. Registration gives a user a tenant and no workspace.
- F15 (cynthus-shared core/resource): `Place`, `Engagement` and `Attendee` classes exist; there are no tables or
  service for them. `StorageLocation` exists. No meal plan classes. cynthus-shared core/event has inventory event
  classes and no meal event classes. `LifecycleAction` has created, updated, deleted, snapshot; `EventAction` also has
  added, removed, retrieved.
- F16 (cynthus-core containers/logistics): a stub with no database, no access decisions and only an event route.
- F17 (cynthus-intelligence containers/analysis): the handler logs signal types and validates the profile snapshot; it
  stores nothing. ARCHITECTURE section on Astri context has cynthus-core-api assemble the context on demand.
- F18 (cynthus-web, cynthus-core containers/web): the web client exists; no plan page exists.
- F19 (CI): each repository's CI, lint and boundary rules were not read for this plan. Not verified.

Findings that changed the design: F5 (the split with #130), F9 and F13 (private plans and plan roles need an ADR and a
rule for who reads what), F10 (access requests exist; invitations do not), F12 (the token does not name the workspace
owner), F14 (workspace creation needs no new Trust work), F16 (Places in Logistics start from nothing).

## Decisions (owner)

- D1 (2026-11-18): A new `meal` module in the cynthus-core image (ADR-008). #130 is narrowed to meals inside a plan
  and the web pages.
- D2 (2026-11-18, superseded by D5 then D11): sharing reached only workspace members. In this plan a plan is reached
  only from inside its workspace.
- D3 (2026-11-18): A new plan is visible to its workspace by default; the owner (or a manager) can make it private.
- D4 (2026-11-18, superseded by D11): invite, accept, 7-day expiry.
- D5 (2026-11-18, moved by D11): a per-plan grant that works from the invitee's own workspace, with a user lookup by
  email and a reviewed exception to the workspace check. Goes to the invitations sequence.
- D6 (2026-11-18): A user with no workspace sees a confirmation page; on confirm the client calls `POST /auth/workspaces`.
  No Trust change and no ADR-010 amendment. The meal module answers `workspace_required`.
- D7 (2026-11-19): The `meal` module joins the default domain group.
- D8 (2026-11-19): Plans recur (`none` or `repeat` with `until` or `count`); the Scheduler creates the next plan 7 days
  before it starts.
- D9 (2026-11-19): `place_id` is nullable on plans and meals, with no foreign key. Places are a core object handled in
  the Logistics module, as their own plan.
- D10 (2026-11-19): Meals per slot are limited by a setting the service reads (default 1; a subscription lookup
  supplies more later). 409 `slot_full`. Meals half.
- D11 (2026-11-19): All invitations are their own story sequence after this plan.
- D12 (2026-11-20): S3 adds one claim, `workspace_owner_id`. `home_*` and `current_*` claims, the entitlements lookup,
  the client cache and the write-behind cache are a later plan with an ADR on token claims.
- Confirmed 2026-11-19: ADR-015 comes before any sharing slice; the sizes and groupings of the slices; the
  follow-up plan stubs are filed as issues now.

## Assumptions (confirmed by the owner 2026-11-20)

- A1: Frequency means meals per day. Predefined `one_a_day`, `two_a_day`, `three_a_day` (Breakfast, Lunch, Dinner),
  `three_and_snacks` (5 slots). Custom is 1 to 48 slots, each with a label and an optional `HH:MM` time of day.
- A2: Duration predefined `day`, `week`, `two_weeks`, `month` (the calendar month of the start date), `year`. Custom
  is 1 to 366 days. `end_date` is derived and stored.
- A3: Plan record: `name` (1 to 100 characters), `workspace_id`, `owner_id` (chosen at creation, default the caller),
  `created_by`, `duration`, `frequency`, `start_date`, `end_date`, `visibility`, `recurrence`, `series_id`,
  `series_index`, `place_id`, `deleted_at`. The default plan and the last-plan rule stay in #130. Overlapping plans
  are allowed.
- A4: `workspace` visibility: every member lists and reads. `private`: the owner, a workspace `super_admin` and members
  with a plan role read it. This is an exception to ADR-010, recorded in ADR-015.
- A5: Plan role capabilities: viewer reads; contributor edits meals; admin edits meals and changes settings other than
  visibility; manager does what admin does and sets visibility. Settings are name, duration, frequency, recurrence and
  place. Only a plan's owner, the workspace owner and a `super_admin` delete. A `super_admin` does everything the
  owner can except transfer ownership. Who answers an access request: the plan's owner and a `super_admin` grant any
  plan role; a manager grants up to manager.
- A6: A plan role comes only from an allowed access request in this plan (invitations add a second source later). A
  workspace role alone gives no write access to anyone else's plan.
- A7: Auth adds `meal:read` and `meal:write` to every role. The permission means "may call the API"; the plan role
  decides what happens, and only `PlanAccess` decides it.
- A8: Templates hold name, duration, frequency, slots and place; no dates or recurrence; same two visibility values;
  edited by the owner, the creator and a `super_admin`; no roles of their own. A plan can be saved as a template and
  created from one. Meals are copied once #130 meals exist.
- A9: No web pages in this plan (they follow in a web plan with WCAG 2 AA and screen reader checks), including the
  workspace confirmation page and the owner dropdown.
- A10: Board mapping: Size XS S M L XL as is; Priority high is P1, medium P2, low P3; milestone "Cynthus 1.0 - Platform
  Foundation Complete". Tracking issue Feature, XL, P1. Slices P1 except S0 and S9 (P2).
- A11: Signals: created, updated and deleted gain `owner_id`, `frequency`, `visibility` and `series_id` (additive,
  schema version bump). New: `public.meal.plan.requested` and `.responded`, `.access_requested`, `.access_answered`,
  `.access_revoked`. Invitation signal names are reserved, not built.
- A12: An unanswered access request expires after 5 days.
- A13: With the nil workspace id the module answers 409 `workspace_required` with a plain-sentence message.
- A14: A request's token already proves workspace membership, so the meal module keeps no members table of its own and
  does not need the Auth membership signals.
- A15: A recurrence `count` is 1 to 100.

## Design

### cynthus-shared (a tagged release gates the core slices)

- `cynthus.core.resource.MealPlan(WorkspaceResource, SoftDeletable)`: `name`, `owner_id`, `created_by`, `duration`,
  `frequency`, `start_date`, `end_date`, `visibility`, `recurrence`, `series_id`, `place_id`.
- `PlanDuration` with `PlanDurationKind`, `MealFrequency` with `MealFrequencyKind` and `MealSlot(label, position,
  time_of_day)`; value objects that validate themselves and raise `InvalidPlanDuration` and `InvalidMealFrequency`.
- `PlanVisibility` (`workspace`, `private`); `PlanRole` (`viewer`, `contributor`, `admin`, `manager`) with
  `can_edit_meals`, `can_edit_settings`, `can_set_visibility` and `may_grant(target)`; `PlanRecurrence` (`none` or
  `repeat` with `until` or `count`; raises `InvalidRecurrence`).
- `MealPlanMember` (`plan`, `user_id`, `role`, `source`, `granted_by`, `status`) and `MealPlanTemplate`.
- Access requests reuse `EventRequest`, `EventRequestDecision` and `DecisionCondition` (ADR-013). No new decision
  answer types or lifecycle actions.
- Event and data classes for plan, member and access request created, updated and deleted, following the inventory
  pattern. `MealService` with a fixed `SERVICE_ID`, domain `CORE`. Fixtures beside the classes.

### cynthus-shared, messaging package (the same tagged release train as the model classes)

- `public.meal.plan.requested` and `.responded` (copying the recipe files); `.access_requested`, `.access_answered`,
  `.access_revoked`; additive fields on created, updated and deleted; invitation signal names reserved.

### cynthus-trust

- `role_permissions.py`: `meal:read` and `meal:write` on every role.
- The token carries `workspace_owner_id` (additive; `TokenClaims` and the issuer).

### cynthus-core, module `meal` (in the default domain group)

- Schema `meal`; every table has `organization_id`, `workspace_id` and `deleted_at`. Tables: `plans`, `plan_slots`,
  `plan_members`, `event_requests`, `decisions`, `decision_conditions` (the ADR-013 shape with a generic
  `subject_type` and `subject_id` so invitations can reuse them), `templates`, `template_slots`,
  `processed_requests`. Indexes: one live member per plan and user; one open request per plan and user; one plan per
  `(series_id, series_index)`.
- `PlanService`: create, get, list, update, delete, `create_next`. `TemplateService`: CRUD, `from_plan`,
  `create_plan`. `AccessService`: request, answer, revoke, change role, leave, list members. `RequestHandler`, as in
  recipe.
- `PlanAccess` is the only place that decides who may read, edit meals, edit settings, set visibility or delete. It
  has one function, `PlanAccess.in_workspace`, that compares workspace ids, so the invitations sequence changes one
  place.
- List results carry `my_role` and `can_request_access`. A private plan the caller cannot read is absent.
- Routes in `api/src/api/routes/meal_request.py`: `/api/v1/meal-plans`, `/{id}/access-requests`, `/{id}/members`,
  `/{id}/series`, and `/api/v1/meal-plan-templates`. Each publishes a request signal and acknowledges with a
  correlation id.
- The Scheduler publishes two internal signals, `internal.meal.plan.recurrence_due` and
  `internal.meal.plan.access_expiry_due`; the meal module handles them. The Scheduler never touches schema `meal`.
- Recurrence: the next plan is created 7 days before the current one starts, copying duration, frequency, slots,
  visibility and place (never members or requests). It stops at `until` or `count`. A series edit changes this plan
  and the plans that have not started. Deleting one plan leaves the others; `DELETE .../series` deletes the unstarted
  ones. A repeated signal creates one plan, by the unique index.
- Failure types: `PlanNotFound` (404, also for a private plan the caller cannot read), `PlanForbidden` (403),
  `InvalidPlanDuration`, `InvalidMealFrequency`, `InvalidRecurrence` (422), `PlanRoleNotGrantable` (403),
  `AccessRequestNotPending` and `AccessAlreadyHeld` (409), `WorkspaceRequired` (409, `workspace_required`).
- Rules: only `PlanAccess` decides access; routes publish only the request signal; only the handler publishes facts;
  no SQL delete and no `session.delete` in the module; no module outside `meal` imports `meal.models`; every query
  filters `deleted_at IS NULL`.

## Slices

No slice is bigger than M. Subtype is Infrastructure for documentation and Application for the rest.

- S0 cynthus-documentation, size S, applies to Docs: ADR-015 (plan roles, private-plan exception to ADR-010,
  access-request flow, recurrence, seams for invitations), registry and Signal Catalog entries, and the #130 re-scope
  text. Gates S6 and S7.
- S1 cynthus-shared (messaging package), size S, applies to Shared: the signals and payload fields. A tagged release gates S4 to S8.
- S2 cynthus-shared, size M, applies to Shared: the classes, events, `MealService`, fixtures. A tagged release gates
  S4 to S8.
- S3 cynthus-trust, size S, applies to Trust: `meal:read`, `meal:write` and the `workspace_owner_id` claim.
- S4 cynthus-core, size M, applies to Core: module skeleton and registration, migration 0001, `PlanService`,
  `PlanAccess` (owner and visibility), handler, routes, signals, soft delete, create-as rules, `workspace_required`,
  lint and boundary rules. Depends on S1, S2, S3.
- S5 cynthus-core, size S: templates. Depends on S4.
- S6 cynthus-core, size M: `plan_members`, the four roles in `PlanAccess`, the private rule, members list, change
  role, revoke, leave, `my_role` and `can_request_access`. Depends on S0 and S4.
- S7 cynthus-core with the Scheduler, size M: access requests, answers, append-only decisions, 5-day expiry through
  `internal.meal.plan.access_expiry_due`, signals. Depends on S6.
- S8 cynthus-core with the Scheduler, size M: recurring plans (`recurrence_due`, `create_next`, series edit and
  delete, idempotency). Depends on S4.
- S9 cynthus-core tests/integration, size S: the end-to-end scenario. Depends on S5, S7, S8.

Order: S0, S1, S2, S3 in parallel; then S4; then S5, S6 and S8 in parallel; then S7; then S9. S1 and S2 are in the same repository and each needs a
tagged release (or one release covers both) and a pin bump in cynthus-core (core pins `cynthus-shared@v0.16.0` per container); S3 needs a Trust
deploy. Each deploy needs the owner's explicit yes.

## Acceptance criteria (testable)

- AC1 (unit, S2): `PlanDuration` returns the right `end_date` for each predefined kind and custom 1 to 366 days (a month
  starting 15 February ends 14 March). 0 and 367 raise `InvalidPlanDuration`.
- AC2 (unit, S2): `MealFrequency` accepts the four predefined and 1 to 48 custom slots with unique consecutive
  positions and an optional `HH:MM` time. 0 slots, 49 slots and a bad time raise `InvalidMealFrequency`.
- AC3 (unit, S2): `PlanRole`, a table-driven test of every role against edit meals, edit settings and set visibility.
  Delete is never granted by a role. `may_grant` refuses anything above the granter's role.
- AC4 (unit, S2): `PlanRecurrence` requires `until` or `count` for `repeat`, never both; refuses an `until` before the
  start; `count` is 1 to 100.
- AC5 (unit, S3): `RolePermissions.for_roles` returns `meal:read` and `meal:write` for every role and nothing for an
  unknown role. The token carries `workspace_owner_id`; a token without it still verifies.
- AC6 (feature integration, S4): create, get, list, update and delete through the handler against a real Postgres
  schema. Delete sets `deleted_at` and leaves the row. `owner_id` defaults to the caller. A `super_admin` or manager
  may create with `owner_id` = workspace owner; a contributor or admin doing so, or any other `owner_id`, is refused
  with 403 `PlanForbidden`.
- AC7 (feature integration, S4): every predefined and a custom frequency, duration and recurrence is stored and
  returned with `end_date`. An invalid one answers 422 with the named error and a plain-sentence message.
- AC8 (feature integration, S4): a plan in another workspace, a deleted plan and a private plan the caller cannot read
  answer 404, and the list omits them.
- AC9 (feature integration, S4): created, updated and deleted signals carry the new fields. A request is acknowledged
  with a correlation id and answered exactly once.
- AC10 (feature integration, S4): repeating a request id does not process it twice.
- AC11 (feature integration, S4): a token with the nil workspace id answers 409 `workspace_required` with a plain
  message and creates nothing.
- AC12 (feature integration, S5): a template saved from a plan and a plan created from it (with a start date) have the
  same duration, frequency, slots and place. A template has no dates or recurrence. Deleting a template leaves plans
  made from it.
- AC13 (feature integration, S6): a new plan is `workspace` visibility. Any member lists and reads it; a member with no
  role is refused edits (403). After `private`, a member with no role gets 404 and does not see it listed; the owner,
  a `super_admin` and role holders still read it.
- AC14 (feature integration, S6): a table-driven test of viewer, contributor, admin, manager and owner against read,
  edit meals, edit settings, set visibility and delete. A manager cannot delete. An admin cannot set private. A
  contributor cannot change frequency or duration. A `super_admin` does anything the owner can except transfer
  ownership.
- AC15 (feature integration, S6): revoking a role, or the holder leaving, removes access at once. A list shows
  `my_role` and `can_request_access` correctly.
- AC16 (feature integration, S7): a request is pending. Allowing it grants the role and records `source =
  access_request` and `granted_by`. Denying closes it. Only the plan's owner, the workspace owner, a `super_admin` or a
  manager within the grant rule may answer. A decision is never updated (a test that tries fails). A second open
  request and a role already held answer 409.
- AC17 (feature integration, S7): with the clock injected, an unanswered request expires after 5 days through
  `internal.meal.plan.access_expiry_due`. A decision with reason `expired` is recorded and a later answer gets
  `AccessRequestNotPending`.
- AC18 (feature integration, S8): `recurrence_due` creates the next plan 7 days before the start, copying duration,
  frequency, slots, visibility and place but no members or requests. A repeated signal creates one plan. It stops at
  `until` or `count`. A series edit changes only plans that have not started. Deleting one plan leaves the others, and
  `DELETE .../series` deletes the unstarted ones.
- AC19 (lint, S4 to S8): a rule fails on `DELETE` SQL or `session.delete(...)` in the meal module. The exception list is
  empty.
- AC20 (import boundary, S4 to S8): a test fails if routes, handler or services decide access outside `PlanAccess`, if
  routes publish anything but the request signal, or if anything outside `meal` imports `meal.models`.
- AC21 (unit and import boundary, S6 to S7): member rows record `source` and `granted_by`. The invitation signal names
  are reserved and unused. `PlanAccess.in_workspace` is the only function that compares workspace ids.
- AC22 (system integration, S9): Jack owns a workspace and Jill is a member. Jack creates a weekly plan with three meals
  a day and Jill lists and reads it. Jill's edit is refused. She requests contributor, Jack allows it, and she edits
  meals. Jack marks the plan private; Sam (no role) gets 404 and Jill still reads. Jack revokes Jill and she gets 404.
  An unanswered request expires. The next plan of the series appears at its lead time. Jack deletes the plan and
  nobody sees it. Real `test_meal` schema, in-memory signal bus, injected clock.
- AC23 (CI): each repository's lint, type and test jobs pass; coverage does not fall below its threshold (not
  verified: the threshold; the coder reads it). S4 runs the full suites of inventory, profile, shopping and logistics
  because the default group shares one image.
- AC24 (documentation): ADR-015, the registry, the Signal Catalog, the module README and the API reference list the
  operations, fields, roles and errors. Each repository's CHANGELOG has a line. `check_markdown.py` and
  `check_line_endings.py` pass.
- AC25 (accessibility): not applicable here, because no page is built (D6, A9). A test asserts every error has a
  non-empty plain-sentence message that a page can show unchanged. The web plan carries the WCAG 2 AA and screen
  reader checks.

## Risks and unknowns

When a risk happens the coder stops and reports; the coordinator brings it to the owner.

- R1: #130 overlap. If work on #130 has started, stop and ask. #130 is edited first after approval (owner sees the
  text before it is saved).
- R2 (closed by D12): the token did not name the workspace owner; S3 adds `workspace_owner_id`.
- R3: The ADR-013 expiry job may not exist (not verified). If missing, S7 builds the generic expiry job and may grow
  beyond M; the coder stops and reports.
- R4: A plan role can raise a member above their workspace role for that plan only. Confirmed by the owner; recorded
  in ADR-015.
- R5: A private plan readable by role holders contradicts the letter of ADR-010. Recorded in ADR-015; S0 gates S6.
- R6: Consumers of plan signals (analysis, scheduler, audit) may reject unknown fields. S1 checks each parser first.
- R7: A calendar month varies, so a 28 or 30 day custom duration differs from `month`. Both `kind` and `end_date`
  are stored.
- R8: Wire date type (`date` or `datetime`) differs between the class and the docs. S1 picks one and fixes the other.
- R9: Adding `meal` to the default group changes `MODULES`, compose and the image. Every deploy needs the owner's yes.
- R10: One definition of today is needed for "7 days before" and "5 days to expire". Use the UTC date; dates are
  stored as dates. No workspace time zone exists.
- R11: Not verified that the Scheduler can publish a daily internal signal for each job. S7 and S8 check first.
- R12: Concurrency: two answers to one request, two recurrence signals. Unique indexes, a transaction and a test each.
- R13: The default group is one image, so bumping the `cynthus-shared` pin for `meal` bumps it for the other four
  modules too. S4 runs their suites.

## Out of scope

- Meals inside a plan (recipe, ad hoc, status, notes, date, time and place, several meals per slot, the slot limit,
  `slot_full`), the default plan and "last plan cannot be deleted": the re-scoped #130.
- All invitations, plan-access and meal, with series, per-occurrence cancel and response, cross-workspace grants and
  the user lookup by email: the invitations sequence.
- Places (tables and service in Logistics, a place's scope for providers and partners, the `place_id` check): a Places
  plan.
- Web pages (plan list and page, forms, templates, members and access requests, the workspace confirmation page, the
  owner dropdown): the web plan, with accessibility checks.
- `home_*` and `current_*` claims, the entitlements lookup, the client cache and the write-behind cache: a tokens and
  entitlements plan with an ADR.
- Asking a workspace owner for permission to create plans: a follow-up request type.
- Astri behavior and meal-time checks (duplicate meals, profile conflicts, inventory and schedule factors, the
  planned-meals signal, whether Analysis accumulates history): #14, #100 and the meals plan.
- Notification delivery and per-user settings; billing limits (plans per tier, subscription lookup for the slot
  limit); sharing individual templates and copying meals into templates; a workspace time zone.

## Issue plan

Tracking issue (cynthus-documentation): "Meal plans: create, share, template, recur and make private". Feature, XL, P1,
milestone "Cynthus 1.0 - Platform Foundation Complete", task list of S0 to S9.

Slice issues (status Planned; seed in each body): S0 to S9 as in Slices, with sizes S, S, M, S, M, S, M, M, M, S.

Follow-up stubs (cynthus-documentation, Feature, status Planned, size XL as a placeholder): Invitations; Places in
Logistics; Web: meal plan pages and the workspace confirmation page; Tokens and entitlements.

Other: #130 is rewritten to the narrowed scope after the owner sees the text. Design document
`docs/features/meal-plans.md` in cynthus-documentation on branch `<N>-meal-plans-design`, linked from
`docs/README.md`, with a CHANGELOG line; the PR says "Part of #N"; no Copilot review; the owner's explicit yes before
merge.
