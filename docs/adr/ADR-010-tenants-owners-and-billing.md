# ADR-010: Tenants, parent tenants, owners and billing accounts

**Status:** Proposed (2026-11-11), amended 2026-11-12
**Relates to:** ADR-009 (the Service object and one layout), cynthus-shared issue 93 (core model classes), cynthus-shared
issue 102 (signal schema version).

## Context

The signals and access tokens carry `organization_id`, and the model in shared issue 93 has a `Tenant` (personal or
organizational) and a `Workspace`. Three things were unclear, and the owner settled them on 2026-11-11:

1. **The word.** "Organization" reads awkwardly for a personal tenant. A real organization (for example Tech-Clusive
   Solutions, LLC) may also want more than one tenant, which would make it several Cynthus "organizations".
2. **How one owner's tenants relate.** A user who owns several tenants needs one place that ties them together without
   doing any work of its own.
3. **Who pays, and who may do what.** Billing and rights were not separated from the tenant, and a token issued to a
   collaborator must never carry more rights than they have.

## Decision

### The tenant is the boundary

A **tenant** is the unit of data ownership, isolation and access. It has a `type` of `personal` or `organizational`. The
word "organization" is retired from the model: there is no separate Organization entity. A real organization is a user
(the owner) with one or more organizational tenants under a parent tenant.

### Parent tenants

- A user's first tenant stands alone. When the same owner creates a second tenant, a **parent tenant** is created
  automatically and becomes the parent of both. Tenants T00001 and T00002 then have parent T00003.
- A parent tenant has **no workspaces** and no resources: no work is done in it. It is the bridge that groups the owner's
  tenants for administration and billing.
- A parent tenant has **the same owner** as its children.
- Each further tenant the owner creates is added under the same parent.
- *Proposed, to confirm with the owner:* a tenant has at most one parent, and a parent has no parent of its own (one
  level). Deeper nesting is not allowed until a case needs it.

### Owner, members and rights

- One user can be the owner and a member of several tenants.
- **Owner** is a property of the tenant, held by the user who owns it. It is not a role that can be granted.
- A token issued to another user to work in someone's tenants **never carries owner rights**. It can carry **super admin**
  (and any lesser role) but owner only when the subject is the owner. The authorization check that turns a token into a
  decision must compare the subject with the tenant's owner and refuse an owner claim from anyone else.
- Working with another tenant is **explicit access**, a grant from the tenant (or its owner) to a user or group, not
  something a membership implies. The form of the grant (what it covers, for how long) is not decided here.

### Billing accounts

- Billing is separate from the tenant. An owner has **one or more billing accounts**.
- The owner chooses which billing account is attached to each tenant. Several tenants may share one account, or each may
  have its own.
- **Each billing account sets its own options** (for example payment method and invoicing). The list of options is not
  decided here.
- Keeping billing separate per tenant is therefore the choice of attaching different accounts. *Proposed, to confirm with the
  owner:* by default every new tenant is attached to the owner's first (default) account.
- A parent tenant is attached to a billing account like any other, so the owner can see one bill for a group of tenants by
  attaching them all to one account.

### Names on the wire and in the model

- **`tenant_id`** replaces `organization_id` in signals, tokens and the model. The value is the same: what is called
  `organization_id` today already identifies the tenant.
- The change is **additive**: `tenant_id` is added beside `organization_id` with the same value, `organization_id` is
  accepted and written for one release as a deprecated alias, then removed. It is tied to the signal schema version
  (cynthus-shared issue 102).
- Database columns named `organization_id` keep their names until their schemas next change, then are renamed by a
  migration. The service code uses `tenant_id`.
- The model in shared issue 93 gains `parent` (a `Tenant` or its id, empty for a parent or a stand-alone tenant) and
  `billing_account_id` on `Tenant`, and a `BillingAccount` class (`id_`, `owner`, `name`, `options`). `Workspace` is
  unchanged: it belongs to a tenant that is not a parent.

## Amendment (2026-11-12): the Auth schema

Settled with the owner while designing the Auth records for ADR-013. It refines the model above; where they differ, this
section wins.

### Tables

- `tenant_types`: `id`, `name` (`personal`, `organizational`, `parent`). Replaces the `bridge` flag: a parent tenant is a tenant of type `parent`.
- `roles`: `id`, `name` (for example `super_admin`, `admin`, `member`, `viewer`). A check constraint refuses the name `owner`.
- `tenants`: `id`, `name`, `type_id`, `parent_id` (empty for a stand-alone or parent tenant), `owner_id` (user), `billing_account_id`, `deleted_at`
- `workspaces`: `id`, `name`, `tenant_id`, `owner_id` (user), `deleted_at`
- `workspace_roles`: `id`, `workspace_id`, `user_id`, `role_id`, `status` (`pending`, `active`, `revoked`, `expired`), `deleted_at`

- A workspace belongs to **exactly one tenant** (`workspaces.tenant_id`). A join table between tenants and workspaces is
  not used: it would allow a workspace in several tenants.
- A workspace in a parent tenant is refused: the service reads the tenant's type when it creates the workspace.

### Owner stays a column

- `owner_id` is on `tenants` and on `workspaces`, `NOT NULL`, with a foreign key to the user. Every tenant and workspace
  has exactly one owner by construction, and "is this subject the owner?" is a column compare on every request, not a
  join.
- Owner is not a row of `workspace_roles`, and `roles` cannot hold it. This keeps the rule above: owner is a property,
  not a role that can be granted.
- Transfer of ownership is one update of `owner_id`; the previous owner may be given an ordinary role in the same
  transaction. The rule that unregistering is refused while other members exist ("transfer first") stands.
- *Alternative kept open:* ownership as a row of a mapping table (history of past owners). It would need a unique index of
  one live owner per workspace and would drop the rule that no role is `owner`. It is a separate migration if a case for
  ownership history appears.

### A token and the workspace

- A workspace is **not created automatically**. A new user has a tenant and no workspace and creates one explicitly.
- A token carries a `workspace_id`. Until the user has one, the token carries the **nil workspace id**
  (`00000000-0000-0000-0000-000000000000`), and services answer 409 `workspace_required` for anything that needs a
  workspace.
- **Creating a workspace**, and **switching to another workspace**, each return a new token carrying that workspace id.
- Auth issues a token for a workspace only if the user **owns it or holds an active `workspace_roles` row** in it. The
  check is made when the token is issued.
- Access to somebody else's workspace is a `workspace_roles` row created by an access request (ADR-013): status `pending`
  until the owner approves it.

## Amendment 2 (2026-11-12): roles and the privilege matrix

The `roles` table holds five rows. Each role has a set of actions over three kinds of resource: **content** (what the
services keep: inventory, recipes, shopping lists, profiles), **members** (who has access to the workspace) and
**settings** (the workspace's name, defaults and billing link).

- `viewer`
  - Content: create: no
  - list: yes
  - read: yes
  - write: no
  - Members: grant: no
  - Settings: read
- `contributor`
  - Content: create: yes
  - list: yes
  - read: yes
  - write: yes
  - Members: grant: no
  - Settings: read
- `manager`
  - Content: create: yes
  - list: yes
  - read: yes
  - write: yes
  - Members: grant: no
  - Settings: read
- `admin`
  - Content: create: no
  - list: yes
  - read: yes (non-private)
  - write: no
  - Members: grant: up to `contributor`
  - Settings: read, write
- `super_admin`
  - Content: create: yes
  - list: yes
  - read: yes (private too)
  - write: yes
  - Members: grant: up to `super_admin`
  - Settings: read, write

- **Write includes soft delete** (ADR-011).
- **Private content** is readable only by its owner and by `super_admin`. Every other role reads non-private content
  only. Content has no `private` flag yet; adding it is its own change.
- **Grant:** nobody grants a role above their own, and nobody grants `owner` (ADR-013). A decision that grants a role is
  checked against the role of the person deciding.
- **Owner** is not a role. The owner holds every privilege in their own tenant and workspace and is the only one who can
  transfer ownership.
- **Own resources:** a user can always read and write their own profile and the resources they created, whatever their
  role (as today).
- **`admin` and `manager`:** an `admin` administers the people and settings of a workspace and reads its non-private
  content, but does not change it. A `manager` works on the content on behalf of the owner (for example, placing orders
  for the owner's shopping list), and cannot grant access.
- **Mapping from the roles Auth uses today:** `workspace_administrator` becomes `super_admin`, `team_member` becomes
  `contributor`, and `client_contributor` becomes `viewer` with the own-resources rule. The migration changes the stored
  names, and `role_permissions.py` maps the new names to the service permissions (`inventory:read` and the rest).

## Not decided here

- What a parent tenant lets its owner do across the children beyond seeing them and their billing (for example reporting).
- What an inter-tenant grant covers and how it ends.
- The billing account options and the integration with a payment provider.
- Transfer of ownership, and what happens to a parent when its last child is deleted.
- Whether a stand-alone tenant gets a parent only on the second tenant (as here) or from the start.

## Options considered

1. **Keep `organization_id` and add a parent concept.** No wire change, but the word stays awkward for personal tenants and
   "an organization has several organizations" remains. Rejected.
2. **A separate Organization entity above the tenants.** Matches the real world, but adds a second kind of parent beside
   the bridge the owner already uses. Rejected: the parent tenant does the job.
3. **Tenant as the boundary, parent tenant as the bridge, billing accounts apart (this ADR).** One boundary word, one
   grouping mechanism, billing chosen per tenant.

## Consequences

- Every place that reads `organization_id` (tokens, signals, the services' tables, the Core API, Auth, the web and mobile
  clients) must move to `tenant_id`. Done a service at a time behind the alias.
- Auth must create the parent tenant when a second tenant is created, and must refuse an owner claim for a non-owner.
- Billing needs its own entity and screens; nothing in the current services depends on it yet.
- Tests for the owner rule come first, because it is a security boundary.

## Work plan (each piece is its own issue, PR and test run in the dev environment)

1. cynthus-shared: `tenant_id` beside `organization_id` in the signal base and the token claims (additive), with the schema
   version from issue 102.
2. cynthus-shared issue 93: add `parent`, `billing_account_id`, `BillingAccount`; fix the known defects.
3. cynthus-trust: tenant and workspace records, the nil workspace id and new-token rule, parent tenant creation, owner-claim rule with tests (the amendment above); then the ADR-013 records.
4. Services, one at a time: read `tenant_id`; rename columns by migration when the schema next changes.
5. Billing accounts: entity, API and screens (own design).
6. Remove `organization_id` after one release.

## Review triggers

- A case needs more than one level of parent tenants.
- A real organization needs rights across its tenants that the explicit grant cannot express.

## Sources

- The owner's decisions of 2026-11-11.
- cynthus-shared issue 93 (branch `93-refactor-shared-model-classes`), issue 102.
