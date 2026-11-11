# ADR-010: Tenants, parent tenants, owners and billing accounts

**Status:** Proposed (2026-11-11)
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
3. cynthus-trust: parent tenant creation; owner-claim rule with tests.
4. Services, one at a time: read `tenant_id`; rename columns by migration when the schema next changes.
5. Billing accounts: entity, API and screens (own design).
6. Remove `organization_id` after one release.

## Review triggers

- A case needs more than one level of parent tenants.
- A real organization needs rights across its tenants that the explicit grant cannot express.

## Sources

- The owner's decisions of 2026-11-11.
- cynthus-shared issue 93 (branch `93-refactor-shared-model-classes`), issue 102.
