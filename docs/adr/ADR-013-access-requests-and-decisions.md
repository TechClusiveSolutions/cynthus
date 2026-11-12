# ADR-013: Access requests, event request decisions and conditions

**Status:** Proposed (2026-11-12)
**Relates to:** ADR-009 (the Service object), ADR-010 (tenants, owners and billing), ADR-011 (soft deletes, workflow
tests), cynthus-shared issue 93 (the event model).

## Context

The core model has `EventRequest`, `EventRequestResponse` and a decision made of an answer, a reason and a condition.
They can be built and are tested, but nothing uses them. Access today is recorded by the `audit.identity.access.*`
signals, and there is no workspace role and no way to ask for access. The owner described the cases to settle:

- **Jill asks for access to Jack's workspace.** A `public.auth.workspace_role.created` signal. The requestor is Jill, the
  resource is the workspace role, the owner is Jack, the action is created. The role record exists with the status
  *pending*, and the decision is approved conditionally.
- **Jack approves.** A new event, `public.auth.workspace_role.updated`, with its own event request (requestor Jack,
  action updated).
- **A grant is revoked.** Another change to the same role.
- **A user acts on their own resource.** The decision is approved, reason permitted, with no condition.
- **A manager of Jack's shopping list places an order for him.** The *order created* event is conditionally approved until
  a payment method is created and linked.
- **Several conditions may be needed at once**, so conditions need a table of their own.
- **Pending requests expire:** 5 days for an access request, 7 days for a collaboration or participation request, by
  type of condition.
- **A user can never grant a privilege they do not already have.** They can still create resources.

The open question was whether the first decision is updated when the approval comes, or whether the answer is left empty
until then, or the decision and its answer are split into two tables.

## Decision

### A decision is an immutable fact; the approval is a new request with its own decision

Decisions are append-only. The first decision (*approved conditionally, waiting for Jack*) is never changed. Jack's
approval is a new event request with its own decision. Revoking a grant is a further event request and a further
decision. What changes over time is the **status of the resource** (the workspace role is pending, then active, then
revoked), which the service holds on the resource and which can always be rebuilt from the sequence of decisions.

This rejects leaving the answer empty (the row would be updated later and the audit trail of who decided what, when,
would be lost) and keeps the decision and its answer in one row (they are never separated in time).

### The records

| Record | Holds |
|---|---|
| `event_request` | `id`, the event (type, action, resource type and id, tenant, workspace), `requestor_id` (user or system), `reason` (text), `requested_on`, `in_reply_to` (the request it answers, empty for the first) |
| `decision` | `id`, `event_request_id`, `answer` (`approved`, `approved_conditionally`, `denied`, `denied_conditionally`), `reason`, `determined_by` (the service), `determined_on` |
| `decision_condition` | `id`, `decision_id`, `condition` (its type), `status` (`open`, `satisfied`, `waived`, `expired`), `expires_at`, `satisfied_by_decision_id`, `satisfied_on` |

A decision has zero or more conditions. A request is **in effect** when its latest decision is approved, or approved
conditionally with every condition satisfied or waived. A condition that expires without being satisfied closes the
request.

### What reason and condition mean

- The **condition** is what must happen before the request takes effect (for example `authorization_required`: the owner
  must approve).
- The **reason** is why the decision is what it is (for example `insufficient_privileges`: Jill is not the owner;
  `permitted`: the owner is acting on their own resource; `authorization_granted`: the owner approved; `expired`).

*To confirm with the owner:* the example in the discussion had the reason as `authorization_required` and the condition
as `authorization_granted`. This ADR reads them the other way round, which is how the existing enumerations are named
(`authorization_required` is a condition; `authorization_granted` is a reason). A reason `expired` is new.

### The walk-through

1. Jill requests access. Auth creates the workspace role with status *pending* and publishes
   `public.auth.workspace_role.created`. Request: actor Jill, resource the role, owner Jack, action created. Decision:
   `approved_conditionally`, reason `insufficient_privileges`, one condition `authorization_required`, `expires_at` five
   days out, status *open*.
2. Jack approves. A new request: actor Jack, resource the role, owner Jack, action updated, `in_reply_to` the first.
   Decision: `approved`, reason `authorization_granted`. The condition of the first decision becomes *satisfied*, with
   `satisfied_by_decision_id` pointing here. The role becomes *active*. `public.auth.workspace_role.updated`.
3. Jack revokes later. A new request (action updated or deleted) and a decision `approved`, reason `permitted`. The
   role becomes *revoked*; its earlier decisions stay as they were. `public.auth.workspace_role.deleted` for a delete.
4. Nobody answers within five days. A scheduled job marks the condition *expired*, the role *expired*, and records a
   decision `denied`, reason `expired`, determined by Auth. A signal announces it.
5. Jack creates a resource of his own. The decision is `approved`, reason `permitted`, no condition.

### Privileges: nobody grants what they do not hold

- A decision that grants a privilege is valid only if the person deciding already holds that privilege in that
  workspace. Checked when the decision is made, not when the request is made.
- The **owner** privilege cannot be granted at all (ADR-010). A workspace role is never `owner`; a database check says so.
- A super admin may grant any role up to and including super admin, never owner.
- Anyone may **create** a resource they are allowed to create without being able to grant access to it. The manager of a
  shopping list can create an order. The order is conditionally approved until a payment method exists and is linked;
  the condition `payment_method_required` is satisfied by the decision that records the link, whoever makes it.

### Expiry

- Every condition has an `expires_at`, set from its type: **5 days** for an access request, **7 days** for a
  collaboration or participation request. The expiry for other condition types is set when they are introduced; a type
  may have none.
- A scheduled job (the Scheduler) finds open conditions past their time, expires them and publishes the result. Expiry
  is therefore a recorded decision, not a silent deletion (soft deletes, ADR-011).

### Where it lives

- The model classes stay in `cynthus.core.event`: `EventRequest` gains `in_reply_to`, a `DecisionCondition` class
  (`condition`, `status`, `expires_at`, `satisfied_by`) replaces the single `condition` on `EventRequestDecision`, and
  `EventRequestDecisionReason` gains `expired`. Factories and fixtures follow.
- Auth owns the records for access requests (`event_requests`, `decisions`, `decision_conditions`, `workspace_roles`) in
  its own database, until a Billing or Access service takes tenant management (the owner's decision of 2026-11-12).
  Other services keep their own conditions (the order's payment method) in their schemas, with the same shape.

## Options considered

1. **Leave the answer empty until the approval (A).** One row to update; loses history; a decision that is later
   edited cannot be audited. Rejected.
2. **Decision and answer in separate tables (B).** The answer is never separate from its decision in time, so the split
   buys nothing. Rejected. What does need a table of its own is the **condition**.
3. **Append-only decisions, conditions as their own records (this ADR).** History is kept; several conditions per
   decision; conditions can expire and be satisfied independently.

## Consequences

- Access requests, approvals and revocations are all auditable by replaying decisions.
- Resources carry a status that follows the decisions, so a read does not need to replay them.
- The Scheduler gains an expiry job; Auth gains tables, a migration and endpoints; the workflow tests gain a scenario.
- A condition type needs a rule for who may satisfy it and how long it lasts; this ADR sets the two for access and
  collaboration requests.

## Work plan (each its own issue and PR)

1. cynthus-shared: `in_reply_to`, `DecisionCondition`, reason `expired`; factories, fixtures, docs.
2. Auth: tables and migration for the records and `workspace_roles` (no `owner` role), the privilege check, the
   endpoints (request access, approve, reject, revoke) and the signals.
3. Scheduler: the expiry job.
4. Workflow tests: the scenario "Jill asks for access to Jack's workspace" in the mocked API test and in the database
   test (`test_auth` schema), including approval, revocation and expiry, then the manager's order with a payment-method
   condition.
5. The engineering standards: how a service records a conditional decision.

## Not decided here

- The expiry of the payment-method condition on an order, and of other condition types.
- Whether Jack is notified (email or in-app) and how; the signal is the contract.
- Whether a rejected request can be made again at once, or only after a delay.
- Delegation: whether Jack can let a super admin approve for him within the privilege rule above.

## Review triggers

- A decision needs more than the four answers.
- A condition needs a rule that does not fit its type (for example a different expiry per request).
