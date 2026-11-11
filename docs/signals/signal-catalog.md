# Cynthus Life Ecosystem — Signal Catalog

**Document Version:** 1.0 (June 2026)
**Status:** Active
**Companion Documents:** Cynthus Feature Registry v1.4, Cynthus ADD V6

---

## Conventions

### Signal Namespace Format

```
{visibility}.{domain}.{entity}.{action}
```

- `public.*` — Domain facts published to `cynthus-topic-public`. Any authorized downstream service may consume.
- `internal.*` — Infrastructure and choreography signals published to `cynthus-topic-internal`. Consumed by specific services only.
- `audit.*` — Write-once compliance events published to `cynthus-topic-audit`. Consumed exclusively by `cynthus-audit`.

### Envelope

Every signal is wrapped in `SignalMessageEnvelope[T]` (defined in ADD V6):

```python
SignalMessageEnvelope[T](
    signal_id=<UUIDv4>,
    correlation_id=<UUIDv4>,          # Trace ID across service hops
    timestamp=<UTC datetime>,
    sender_service="cynthus-{service}",
    schema_version="1.0.0",
    topic="cynthus-topic-{public|internal|audit}",
    organization_id="org_{id}",
    workspace_id="ws_{id}",
    payload=<T>                        # Domain-specific payload shown in each entry below
)
```

Payload samples below show **only the `payload` field content**. The full envelope always wraps it.

### Read-Only Operations

Features that are purely synchronous read/query operations (Browse, Search, Report queries) do not produce Service Bus signals. These are noted inline with `— synchronous gRPC query; no async signal —`.

---

## Domain: Meal Planning

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-MP-001 | `public.meal.suggestion.requested` | public | `cynthus-core-api` | `cynthus-chat`, `cynthus-audit` | User initiated an on-demand meal suggestion; context bundle reference included |
| FT-MP-001 | `public.meal.suggestion.generated` | public | `cynthus-chat` | `cynthus-core-api`, `cynthus-notification`, `cynthus-audit` | Astri produced a meal suggestion and returned it to the user |
| FT-MP-001, FT-MP-005 | `public.meal.suggestion.accepted` | public | `cynthus-core-api` | `cynthus-chat`, `cynthus-analysis`, `cynthus-audit` | User accepted a suggestion; stored for preference model training |
| FT-MP-001, FT-MP-005 | `public.meal.suggestion.denied` | public | `cynthus-core-api` | `cynthus-chat`, `cynthus-analysis`, `cynthus-audit` | User denied a suggestion; triggers follow-up suggestion from Astri |
| FT-MP-002 | `internal.meal.suggestion_schedule.configured` | internal | `cynthus-core-api` | `cynthus-scheduler` | User set or changed their scheduled suggestion cadence |
| FT-MP-002 | `internal.meal.suggestion_schedule.triggered` | internal | `cynthus-scheduler` | `cynthus-core-api` | Scheduler fired a due suggestion event; core assembles context and forwards to chat |
| FT-MP-003 | *(synchronous gRPC query; no async signal)* | — | — | — | Browse meals by category is a read-only query |
| FT-MP-004 | `public.meal.plan.created` | public | `cynthus-core-api` | `cynthus-analysis`, `cynthus-scheduler`, `cynthus-audit` | A new meal plan was created for a workspace |
| FT-MP-004 | `public.meal.plan.updated` | public | `cynthus-core-api` | `cynthus-analysis`, `cynthus-scheduler`, `cynthus-audit` | An existing meal plan was modified |
| FT-MP-004 | `public.meal.plan.deleted` | public | `cynthus-core-api` | `cynthus-analysis`, `cynthus-scheduler`, `cynthus-audit` | A meal plan was removed |
| FT-MP-006 | `public.meal.recipes.associated` | public | `cynthus-core-api` | `cynthus-recipe`, `cynthus-analysis`, `cynthus-audit` | Multiple recipe IDs linked to a composite meal entry |
| FT-MP-007 | `public.meal.vote.initiated` | public | `cynthus-core-api` | `cynthus-messaging`, `cynthus-notification`, `cynthus-audit` | A group meal vote was opened; push alerts sent to group members |
| FT-MP-008 | `public.meal.vote.cast` | public | `cynthus-core-api` | `cynthus-analysis`, `cynthus-messaging`, `cynthus-audit` | A group member submitted their vote |
| FT-MP-009 | `public.meal.vote.resolved` | public | `cynthus-core-api` | `cynthus-chat`, `cynthus-notification`, `cynthus-audit` | Vote concluded with a winning choice |
| FT-MP-010 | `internal.meal.vote.stalemate_detected` | internal | `cynthus-analysis` | `cynthus-chat` | Split vote detected; Astri asked to act as tiebreaker |
| FT-MP-010 | `public.meal.vote.auto_resolved` | public | `cynthus-chat` | `cynthus-core-api`, `cynthus-notification`, `cynthus-audit` | Astri resolved a stalemate based on history and expiry data |
| FT-MP-011 | `internal.profile.energy_level.updated` | internal | `cynthus-profile` | `cynthus-chat`, `cynthus-core-api` | User updated their current Energy Banker spoon budget |

### Sample Payloads — Meal Planning

```json
// public.meal.suggestion.requested
{
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "context_bundle_id": "ctx_7g8h9i",
  "trigger": "on_demand",
  "energy_level": 7,
  "requested_at": "2027-01-15T12:04:00Z"
}

// public.meal.suggestion.generated
{
  "suggestion_id": "sug_j1k2l3",
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "context_bundle_id": "ctx_7g8h9i",
  "meal_name": "Lemon Herb Roasted Chicken",
  "recipe_ids": ["rec_m1n2o3"],
  "rationale": "Uses the chicken thighs expiring in 2 days and matches your low-effort preference.",
  "spoon_cost": 3,
  "estimated_cost_usd": 8.50
}

// public.meal.suggestion.accepted
{
  "suggestion_id": "sug_j1k2l3",
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "meal_name": "Lemon Herb Roasted Chicken",
  "accepted_at": "2027-01-15T12:05:22Z"
}

// public.meal.suggestion.denied
{
  "suggestion_id": "sug_j1k2l3",
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "reason": "not_in_mood",
  "denied_at": "2027-01-15T12:05:10Z"
}

// internal.meal.suggestion_schedule.configured
{
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "cadence": "daily",
  "preferred_time": "08:00",
  "timezone": "America/Chicago"
}

// internal.meal.suggestion_schedule.triggered
{
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "cadence": "daily",
  "due_at": "2027-01-16T08:00:00Z"
}

// public.meal.plan.created
{
  "plan_id": "pln_p3q4r5",
  "workspace_id": "ws_d4e5f6",
  "created_by": "usr_a1b2c3",
  "horizon": "week",
  "start_date": "2027-01-20",
  "end_date": "2027-01-26",
  "meal_count": 14,
  "astri_assisted": true
}

// public.meal.vote.initiated
{
  "vote_id": "vot_s6t7u8",
  "workspace_id": "ws_d4e5f6",
  "group_id": "grp_v9w0x1",
  "initiated_by": "usr_a1b2c3",
  "proposed_meal": "Tacos al Pastor",
  "recipe_id": "rec_y2z3a4",
  "expires_at": "2027-01-15T18:00:00Z"
}

// public.meal.vote.cast
{
  "vote_id": "vot_s6t7u8",
  "voter_id": "usr_b5c6d7",
  "workspace_id": "ws_d4e5f6",
  "group_id": "grp_v9w0x1",
  "vote": "yes",
  "cast_at": "2027-01-15T14:23:00Z",
  "current_tally": { "yes": 2, "no": 1, "pending": 1 }
}

// public.meal.vote.auto_resolved
{
  "vote_id": "vot_s6t7u8",
  "workspace_id": "ws_d4e5f6",
  "group_id": "grp_v9w0x1",
  "resolution": "Tacos al Pastor",
  "recipe_id": "rec_y2z3a4",
  "tiebreak_rationale": "Highest group preference score; chicken thighs expiring tonight.",
  "resolved_by": "astri",
  "resolved_at": "2027-01-15T18:01:00Z"
}

// internal.profile.energy_level.updated
{
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "previous_level": 8,
  "new_level": 4,
  "updated_at": "2027-01-15T09:00:00Z"
}
```

---

## Domain: Inventory Management

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-IM-001 | `public.inventory.location.created` | public | `cynthus-inventory` | `cynthus-core-cache`, `cynthus-audit` | A new named inventory location was created |
| FT-IM-001 | `public.inventory.location.updated` | public | `cynthus-inventory` | `cynthus-core-cache`, `cynthus-audit` | Location metadata (name, type, config) was changed |
| FT-IM-001 | `public.inventory.location.deleted` | public | `cynthus-inventory` | `cynthus-core-cache`, `cynthus-shopping`, `cynthus-audit` | Location was removed; shopping service clears any procurement links |
| FT-IM-001 | `public.inventory.shelf.created` | public | `cynthus-inventory` | `cynthus-core-cache`, `cynthus-audit` | A new shelf was created within a location |
| FT-IM-001 | `public.inventory.shelf.updated` | public | `cynthus-inventory` | `cynthus-core-cache`, `cynthus-audit` | Shelf name or position was changed |
| FT-IM-001 | `public.inventory.shelf.deleted` | public | `cynthus-inventory` | `cynthus-core-cache`, `cynthus-audit` | Shelf was removed along with its items and owners |
| FT-IM-002 | `audit.inventory.location.role_assigned` | audit | `cynthus-core-api` | `cynthus-audit` | RBAC role granted on an inventory location |
| FT-IM-002 | `audit.inventory.location.role_revoked` | audit | `cynthus-core-api` | `cynthus-audit` | RBAC role revoked on an inventory location |
| FT-IM-003 | `public.inventory.item.added` | public | `cynthus-inventory` | `cynthus-core-cache`, `cynthus-scheduler`, `cynthus-audit` | Item added to a location; cache updated; scheduler registers expiry watch |
| FT-IM-003 | `public.inventory.item.updated` | public | `cynthus-inventory` | `cynthus-core-cache`, `cynthus-scheduler`, `cynthus-audit` | Item quantity or metadata changed |
| FT-IM-003 | `public.inventory.item.removed` | public | `cynthus-inventory` | `cynthus-core-cache`, `cynthus-scheduler`, `cynthus-audit` | Item removed from location |
| FT-IM-001 | `public.inventory.owner.added` | public | `cynthus-inventory` | `cynthus-audit` | A user was made an owner of a shelf |
| FT-IM-001 | `public.inventory.owner.removed` | public | `cynthus-inventory` | `cynthus-audit` | A user stopped being an owner of a shelf |
| FT-IM-001 | `public.inventory.location.requested` | public | `cynthus-core-api` | `cynthus-inventory`, `cynthus-audit` | A caller asked to create, get, list, update or delete a location; the API acknowledges the client at once and hands the request, with the caller token as a message property, to the Inventory service |
| FT-IM-001 | `public.inventory.location.responded` | public | `cynthus-inventory` | `cynthus-core-api`, `cynthus-audit` | The Inventory service's answer with an HTTP-style status and the result or error; the API relays it to the waiting client over its websocket |
| FT-IM-001 | `public.inventory.shelf.requested` | public | `cynthus-core-api` | `cynthus-inventory`, `cynthus-audit` | A caller asked to create, get, list, update or delete a shelf; the API acknowledges the client at once and hands the request, with the caller token as a message property, to the Inventory service |
| FT-IM-001 | `public.inventory.shelf.responded` | public | `cynthus-inventory` | `cynthus-core-api`, `cynthus-audit` | The Inventory service's answer with an HTTP-style status and the result or error; the API relays it to the waiting client over its websocket |
| FT-IM-003 | `public.inventory.item.requested` | public | `cynthus-core-api` | `cynthus-inventory`, `cynthus-audit` | A caller asked to create, get, list, update or delete an item; the API acknowledges the client at once and hands the request, with the caller token as a message property, to the Inventory service |
| FT-IM-003 | `public.inventory.item.responded` | public | `cynthus-inventory` | `cynthus-core-api`, `cynthus-audit` | The Inventory service's answer with an HTTP-style status and the result or error; the API relays it to the waiting client over its websocket |
| FT-IM-002 | `public.inventory.owner.requested` | public | `cynthus-core-api` | `cynthus-inventory`, `cynthus-audit` | A caller asked to create, get, list, update or delete a shelf owner; the API acknowledges the client at once and hands the request, with the caller token as a message property, to the Inventory service |
| FT-IM-002 | `public.inventory.owner.responded` | public | `cynthus-inventory` | `cynthus-core-api`, `cynthus-audit` | The Inventory service's answer with an HTTP-style status and the result or error; the API relays it to the waiting client over its websocket |
| FT-IM-005 | `public.inventory.list.requested` | public | `cynthus-core-api` | `cynthus-inventory`, `cynthus-audit` | A caller asked for the inventory listing; the API acknowledges the client at once and hands the request, with the caller token as a message property, to the Inventory service |
| FT-IM-005 | `public.inventory.list.updated` | public | `cynthus-inventory` | `cynthus-core-api`, `cynthus-audit` | The Inventory service's answer with an HTTP-style status and the result or error; the API relays it to the waiting client over its websocket |
| FT-IM-004 | `internal.inventory.location.subscription_created` | internal | `cynthus-core-api` | `cynthus-notification`, `cynthus-audit` | User subscribed to alerts for a specific location |
| FT-IM-004 | `internal.inventory.location.subscription_removed` | internal | `cynthus-core-api` | `cynthus-notification`, `cynthus-audit` | User unsubscribed from location alerts |
| FT-IM-005, FT-IM-006 | `public.inventory.item.low` | public | `cynthus-scheduler` | `cynthus-notification`, `cynthus-chat`, `cynthus-shopping`, `cynthus-audit` | Item quantity crossed below the user-defined minimum threshold; notification fans out to owner and location subscribers; shopping service auto-appends to active procurement list |
| FT-IM-007, FT-IM-008 | `public.inventory.item.expiry_approaching` | public | `cynthus-scheduler` | `cynthus-notification`, `cynthus-chat`, `cynthus-analysis`, `cynthus-audit` | Item is within configured days-before-expiry window |
| FT-IM-007, FT-IM-008 | `public.inventory.item.expired` | public | `cynthus-scheduler` | `cynthus-notification`, `cynthus-chat`, `cynthus-audit` | Item has reached or passed its registered expiry date |
| FT-IM-009 | `public.inventory.order.initiated` | public | `cynthus-core-api` | `cynthus-partner-api`, `cynthus-billing-api`, `cynthus-audit` | User triggered a reorder through a third-party vendor |
| FT-IM-009 | `public.inventory.order.submitted` | public | `cynthus-partner-api` | `cynthus-notification`, `cynthus-audit` | Order successfully handed off to external fulfillment provider |
| FT-IM-009 | `public.inventory.order.failed` | public | `cynthus-partner-api` | `cynthus-notification`, `cynthus-audit` | Order handoff to external provider failed |
| FT-IM-011 | `internal.inventory.scan.receipt_submitted` | internal | `cynthus-core-api` | `cynthus-worker` | Receipt image queued for OCR/batch-add processing |
| FT-IM-011 | `internal.inventory.scan.completed` | internal | `cynthus-worker` | `cynthus-core-api` | OCR complete; structured item list ready to be batch-added to location |
| FT-IM-012 | `public.inventory.mutation.recorded` | public | `cynthus-core-api` | `cynthus-core-cache`, `cynthus-audit` | Canonical immutable ledger entry for every inventory state change (add, update, move, consume) |
| FT-IM-013 | `internal.inventory.item.prioritized_for_expiry` | internal | `cynthus-scheduler` | `cynthus-core-api` | Near-expiry items flagged for elevation in next context assembly payload sent to Astri |

**Request and response.** Every interaction between the Core API and the Inventory service uses signals: the request carries the operation (`create`, `get`, `list`, `update`, `delete`), the target ids, filters and data; the response carries the same operation, a status (`200`, `201`, `204`, `401`, `403`, `404`, `405`, `409`, `422`, `500`) and the result or error. They are joined by the envelope `correlation_id`. The facts above follow a successful change.

### Sample Payloads — Inventory Management

```json
// public.inventory.location.created
{
  "location_id": "loc_e1f2g3",
  "workspace_id": "ws_d4e5f6",
  "created_by": "usr_a1b2c3",
  "name": "Kitchen Pantry",
  "type": "ambient",
  "created_at": "2027-04-10T10:00:00Z"
}

// public.inventory.item.added
{
  "item_id": "itm_h4i5j6",
  "location_id": "loc_e1f2g3",
  "workspace_id": "ws_d4e5f6",
  "added_by": "usr_a1b2c3",
  "name": "Whole Milk",
  "quantity": 1,
  "unit": "gallon",
  "low_threshold": 0.25,
  "expiry_date": "2027-04-17",
  "barcode": "041303004105",
  "catalog_item_id": "cat_k7l8m9"
}

// public.inventory.item.low
{
  "item_id": "itm_h4i5j6",
  "location_id": "loc_e1f2g3",
  "workspace_id": "ws_d4e5f6",
  "name": "Whole Milk",
  "current_quantity": 0.2,
  "unit": "gallon",
  "low_threshold": 0.25,
  "owner_id": "usr_a1b2c3",
  "location_subscribers": ["usr_b5c6d7"],
  "detected_at": "2027-04-14T07:00:00Z"
}

// public.inventory.item.expiry_approaching
{
  "item_id": "itm_h4i5j6",
  "location_id": "loc_e1f2g3",
  "workspace_id": "ws_d4e5f6",
  "name": "Whole Milk",
  "expiry_date": "2027-04-17",
  "days_remaining": 3,
  "owner_id": "usr_a1b2c3"
}

// public.inventory.order.initiated
{
  "order_id": "ord_n0o1p2",
  "workspace_id": "ws_d4e5f6",
  "initiated_by": "usr_a1b2c3",
  "items": [
    { "catalog_item_id": "cat_k7l8m9", "name": "Whole Milk", "quantity": 2, "unit": "gallon" }
  ],
  "preferred_vendor_id": "vnd_q3r4s5",
  "fulfillment_platform": "instacart",
  "initiated_at": "2027-04-14T08:30:00Z"
}

// public.inventory.order.submitted
{
  "order_id": "ord_n0o1p2",
  "workspace_id": "ws_d4e5f6",
  "external_order_reference": "IC-88291042",
  "fulfillment_platform": "instacart",
  "estimated_delivery": "2027-04-14T12:00:00Z",
  "submitted_at": "2027-04-14T08:31:15Z"
}

// internal.inventory.scan.receipt_submitted
{
  "job_id": "job_t6u7v8",
  "workspace_id": "ws_d4e5f6",
  "submitted_by": "usr_a1b2c3",
  "target_location_id": "loc_e1f2g3",
  "image_blob_uri": "https://cynthus-storage.blob.core.windows.net/receipts/job_t6u7v8.jpg",
  "submitted_at": "2027-04-10T10:05:00Z"
}

// internal.inventory.scan.completed
{
  "job_id": "job_t6u7v8",
  "workspace_id": "ws_d4e5f6",
  "items_parsed": 14,
  "unrecognized_items": 1,
  "structured_items": [
    { "name": "Whole Milk", "quantity": 1, "unit": "gallon", "catalog_item_id": "cat_k7l8m9", "expiry_date": "2027-04-17" }
  ],
  "completed_at": "2027-04-10T10:05:42Z"
}

// public.inventory.mutation.recorded
{
  "mutation_id": "mut_w9x0y1",
  "location_id": "loc_e1f2g3",
  "workspace_id": "ws_d4e5f6",
  "actor_id": "usr_a1b2c3",
  "mutation_type": "item_added",
  "item_id": "itm_h4i5j6",
  "delta": { "quantity": 1, "unit": "gallon" },
  "timestamp": "2027-04-10T10:05:43Z"
}

// internal.inventory.item.prioritized_for_expiry
{
  "workspace_id": "ws_d4e5f6",
  "prioritized_items": [
    { "item_id": "itm_h4i5j6", "name": "Whole Milk", "expiry_date": "2027-04-17", "days_remaining": 3 },
    { "item_id": "itm_z2a3b4", "name": "Greek Yogurt", "expiry_date": "2027-04-16", "days_remaining": 2 }
  ],
  "context_assembly_hint": "elevate_expiry_items",
  "computed_at": "2027-04-14T06:00:00Z"
}
```

---

## Domain: Recipe Management

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-RM-001 | `public.recipe.library.created` | public | `cynthus-recipe` | `cynthus-audit` | Recipe library created with initial RBAC configuration |
| FT-RM-001 | `public.recipe.library.updated` | public | `cynthus-recipe` | `cynthus-audit` | Library name, description, or RBAC changed |
| FT-RM-001 | `public.recipe.library.deleted` | public | `cynthus-recipe` | `cynthus-audit` | Library and all contained recipes removed |
| FT-RM-001 | `audit.recipe.library.role_assigned` | audit | `cynthus-recipe` | `cynthus-audit` | RBAC role granted on a recipe library |
| FT-RM-001 | `audit.recipe.library.role_revoked` | audit | `cynthus-recipe` | `cynthus-audit` | RBAC role revoked on a recipe library |
| FT-RM-002 | `public.recipe.created` | public | `cynthus-recipe` | `cynthus-core-api`, `cynthus-analysis`, `cynthus-audit` | New recipe added to a library; core-api updates context availability |
| FT-RM-002 | `public.recipe.updated` | public | `cynthus-recipe` | `cynthus-core-api`, `cynthus-analysis`, `cynthus-audit` | Recipe content or metadata changed |
| FT-RM-002 | `public.recipe.deleted` | public | `cynthus-recipe` | `cynthus-core-api`, `cynthus-audit` | Recipe removed from a library |
| FT-RM-003 | *(synchronous gRPC query; no async signal)* | — | — | — | Recipe search is a read-only filtered query |
| FT-RM-004 | `internal.recipe.import.url_submitted` | internal | `cynthus-recipe` | `cynthus-worker` | URL queued for web-scraping and recipe extraction |
| FT-RM-004 | `internal.recipe.import.completed` | internal | `cynthus-worker` | `cynthus-recipe` | Scraped and cleaned recipe ready for library insertion |
| FT-RM-004 | `internal.recipe.import.failed` | internal | `cynthus-worker` | `cynthus-recipe`, `cynthus-notification` | URL scrape or parse failed; user notified |
| FT-RM-005 | `internal.recipe.modification.clinically_suggested` | internal | `cynthus-chat` | `cynthus-recipe`, `cynthus-audit` | Astri produced a clinically driven ingredient modification (PHI context involved; audit required) |
| FT-RM-006 | `public.recipe.scaled` | public | `cynthus-recipe` | `cynthus-core-api`, `cynthus-analysis`, `cynthus-audit` | Recipe scaled to target portion count; updated ingredient quantities and procurement manifest emitted |
| FT-RM-007 | `internal.recipe.pricing.updated` | internal | `cynthus-recipe` | `cynthus-core-api` | Price-per-portion recalculated after inventory cost change; updated estimate propagated to recipe metadata |
| FT-RM-008 | `internal.recipe.ocr.image_submitted` | internal | `cynthus-recipe` | `cynthus-worker` | Recipe card or printed menu image queued for OCR processing |
| FT-RM-008 | `internal.recipe.ocr.completed` | internal | `cynthus-worker` | `cynthus-recipe` | OCR result ready; structured recipe object awaiting library insertion |
| FT-RM-009 | `internal.recipe.scrape.url_submitted` | internal | `cynthus-recipe` | `cynthus-worker` | Blog URL queued for backstory-stripped recipe extraction (reuses import worker path) |
| FT-RM-009 | `internal.recipe.scrape.completed` | internal | `cynthus-worker` | `cynthus-recipe` | Cleaned recipe extracted from blog URL; ready for insertion |
| FT-RM-010 | `internal.recipe.nutrition.enriched` | internal | `cynthus-worker` | `cynthus-recipe` | USDA FoodData Central nutritional data matched and injected into recipe ingredient array |
| FT-RM-011 | `public.recipe.substitution.requested` | public | `cynthus-core-api` | `cynthus-chat`, `cynthus-audit` | User selected an ingredient for substitution; context bundle dispatched to Astri |
| FT-RM-011 | `public.recipe.substitution.suggested` | public | `cynthus-chat` | `cynthus-recipe`, `cynthus-audit` | Astri returned one or more substitution alternatives with technique notes |
| FT-RM-011 | `public.recipe.variant.saved` | public | `cynthus-recipe` | `cynthus-core-api`, `cynthus-audit` | User saved an Astri-suggested modification as a named variant alongside the original |

### Sample Payloads — Recipe Management

```json
// public.recipe.created
{
  "recipe_id": "rec_c5d6e7",
  "library_id": "lib_f8g9h0",
  "workspace_id": "ws_d4e5f6",
  "created_by": "usr_a1b2c3",
  "name": "Classic Beef Tacos",
  "tags": ["dinner", "mexican", "quick"],
  "spoon_cost": 2,
  "prep_time_minutes": 20,
  "difficulty": "easy",
  "allergens": ["dairy", "gluten"],
  "nutritional_enriched": false,
  "created_at": "2027-04-10T11:00:00Z"
}

// public.recipe.scaled
{
  "recipe_id": "rec_c5d6e7",
  "library_id": "lib_f8g9h0",
  "workspace_id": "ws_d4e5f6",
  "scaled_by": "usr_a1b2c3",
  "base_portions": 4,
  "target_portions": 40,
  "scale_factor": 10.0,
  "procurement_manifest": [
    { "ingredient": "Ground Beef", "quantity": 10, "unit": "lbs" },
    { "ingredient": "Corn Tortillas", "quantity": 80, "unit": "count" }
  ],
  "estimated_cost_usd": 185.00,
  "scaled_at": "2027-10-15T09:00:00Z"
}

// internal.recipe.nutrition.enriched
{
  "recipe_id": "rec_c5d6e7",
  "workspace_id": "ws_d4e5f6",
  "per_portion": {
    "calories": 520,
    "protein_g": 32,
    "fat_g": 24,
    "carbohydrates_g": 45
  },
  "allergens_detected": ["dairy", "gluten"],
  "usda_matched_ingredients": 8,
  "unmatched_ingredients": 0,
  "enriched_at": "2027-04-10T11:00:45Z"
}

// public.recipe.substitution.requested
{
  "substitution_request_id": "sub_i1j2k3",
  "recipe_id": "rec_c5d6e7",
  "workspace_id": "ws_d4e5f6",
  "requested_by": "usr_a1b2c3",
  "target_ingredient": "Whole Milk",
  "user_prompt": "I'm lactose intolerant — what would give the same creaminess?",
  "context_bundle_id": "ctx_l4m5n6",
  "requested_at": "2027-04-10T11:05:00Z"
}

// public.recipe.substitution.suggested
{
  "substitution_request_id": "sub_i1j2k3",
  "recipe_id": "rec_c5d6e7",
  "workspace_id": "ws_d4e5f6",
  "original_ingredient": "Whole Milk",
  "suggestions": [
    {
      "substitute": "Full-Fat Oat Milk",
      "quantity_adjustment": "1:1 ratio",
      "technique_note": "Add 1 tsp cornstarch per cup to improve body.",
      "flavor_impact": "Slight oat sweetness; nearly neutral in savory dishes."
    },
    {
      "substitute": "Cashew Cream",
      "quantity_adjustment": "Use 3/4 cup per 1 cup milk",
      "technique_note": "Blend soaked cashews with water to desired consistency.",
      "flavor_impact": "Richer and slightly nuttier; complements cream sauces well."
    }
  ],
  "suggested_at": "2027-04-10T11:05:08Z"
}

// public.recipe.variant.saved
{
  "variant_id": "rec_o7p8q9",
  "base_recipe_id": "rec_c5d6e7",
  "library_id": "lib_f8g9h0",
  "workspace_id": "ws_d4e5f6",
  "variant_name": "Classic Beef Tacos (Dairy-Free)",
  "substitutions_applied": [{ "original": "Whole Milk", "substitute": "Full-Fat Oat Milk" }],
  "saved_by": "usr_a1b2c3",
  "saved_at": "2027-04-10T11:06:00Z"
}
```

---

## Domain: Shopping List

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-SL-001 | `public.shopping_list.created` | public | `cynthus-shopping` | `cynthus-audit` | Named shopping list (notebook) created |
| FT-SL-001 | `public.shopping_list.updated` | public | `cynthus-shopping` | `cynthus-audit` | List name, archive status, or metadata changed |
| FT-SL-001 | `public.shopping_list.deleted` | public | `cynthus-shopping` | `cynthus-audit` | List removed; purchase history retained per retention policy |
| FT-SL-002 | `public.shopping_list.item.added` | public | `cynthus-shopping` | `cynthus-analysis`, `cynthus-audit` | Item manually or automatically added to list |
| FT-SL-002 | `public.shopping_list.item.updated` | public | `cynthus-shopping` | `cynthus-analysis`, `cynthus-audit` | Item quantity, unit, or notes changed |
| FT-SL-002 | `public.shopping_list.item.checked_off` | public | `cynthus-shopping` | `cynthus-analysis`, `cynthus-audit` | Item marked as purchased in-store; updates purchase history used by Astri |
| FT-SL-002 | `public.shopping_list.item.removed` | public | `cynthus-shopping` | `cynthus-audit` | Item removed from list without being purchased |
| FT-SL-003 | `audit.shopping_list.role_assigned` | audit | `cynthus-shopping` | `cynthus-audit` | RBAC role granted on a shopping list |
| FT-SL-003 | `audit.shopping_list.role_revoked` | audit | `cynthus-shopping` | `cynthus-audit` | RBAC role revoked on a shopping list |
| FT-SL-004 | `internal.shopping_list.procurement_target.set` | internal | `cynthus-shopping` | `cynthus-core-api`, `cynthus-scheduler` | A list designated as the active procurement target for auto-append of low-inventory signals |
| FT-SL-005 | `internal.shopping_list.item.vendor_preference_set` | internal | `cynthus-shopping` | `cynthus-chat`, `cynthus-partner-api` | Vendor preference tagged to a shopping list line item; used by Astri for fulfillment routing |
| FT-SL-006 | `audit.shopping_list.management_delegated` | audit | `cynthus-shopping` | `cynthus-audit` | Manager-level delegation granted to a user or group |
| FT-SL-006 | `audit.shopping_list.management_revoked` | audit | `cynthus-shopping` | `cynthus-audit` | Management delegation removed |
| FT-SL-007 | `public.shopping_list.access_requested` | public | `cynthus-shopping` | `cynthus-notification`, `cynthus-audit` | User submitted a request to access another user's list |
| FT-SL-007 | `public.shopping_list.access_request_withdrawn` | public | `cynthus-shopping` | `cynthus-notification`, `cynthus-audit` | Requester cancelled a pending access request before owner responded |
| FT-SL-008 | `public.shopping_list.access_granted` | public | `cynthus-shopping` | `cynthus-notification`, `cynthus-identity`, `cynthus-audit` | List owner approved an access request; permissions provisioned immediately |
| FT-SL-008 | `public.shopping_list.access_denied` | public | `cynthus-shopping` | `cynthus-notification`, `cynthus-audit` | List owner denied an access request |
| FT-SL-009 | `internal.shopping_list.generation.requested` | internal | `cynthus-core-api` | `cynthus-chat` | Astri-assisted list generation triggered; context bundle (history, meal plan, inventory gaps) forwarded |
| FT-SL-009 | `internal.shopping_list.generation.completed` | internal | `cynthus-chat` | `cynthus-shopping` | Astri returned generated item list ready for user review before saving |
| FT-SL-009 | `internal.shopping_list.promotional_data.requested` | internal | `cynthus-chat` | `cynthus-partner-api` | Astri queried active promotional data from the user's opted-in vendors |
| FT-SL-010 | `internal.shopping_list.autopurchase.schedule_configured` | internal | `cynthus-shopping` | `cynthus-scheduler` | User configured a recurring auto-purchase cadence for a list item |
| FT-SL-010 | `internal.shopping_list.autopurchase.reminder_due` | internal | `cynthus-scheduler` | `cynthus-notification`, `cynthus-chat` | Grace period reminder dispatched to user before scheduled auto-purchase executes |
| FT-SL-010 | `public.shopping_list.autopurchase.confirmed` | public | `cynthus-shopping` | `cynthus-partner-api`, `cynthus-billing-api`, `cynthus-audit` | User confirmed order (or grace period elapsed silently); order submitted to vendor |
| FT-SL-010 | `public.shopping_list.autopurchase.cancelled` | public | `cynthus-shopping` | `cynthus-scheduler`, `cynthus-audit` | User cancelled a pending scheduled purchase during the grace period |
| FT-SL-010 | `public.shopping_list.autopurchase.modified` | public | `cynthus-shopping` | `cynthus-scheduler`, `cynthus-audit` | User changed quantity, vendor, or frequency during the grace period |
| FT-SL-011 | `internal.shopping_list.meal_gap.detected` | internal | `cynthus-scheduler` | `cynthus-notification`, `cynthus-chat` | Lookahead cross-check found missing ingredients for meals planned within the configured window |

### Implemented names (phase 1)

The signal classes in `cynthus-shared` repeat the aggregate in the name, as the other domains do (`public.recipe.recipe.created`), so three rows above exist under a longer name. The item signals already had four parts. The Core API asks the Shopping service for list and item work with a request and a response signal (one pair for both, because items belong to the list).

| Catalog name | Implemented name | Class (in `cynthus.messaging.common`) |
|---|---|---|
| `public.shopping_list.created` | `public.shopping_list.list.created` | `PublicShoppingListListCreatedSignal` |
| `public.shopping_list.updated` | `public.shopping_list.list.updated` | `PublicShoppingListListUpdatedSignal` |
| `public.shopping_list.deleted` | `public.shopping_list.list.deleted` | `PublicShoppingListListDeletedSignal` |
| `public.shopping_list.item.added` | same | `PublicShoppingListItemAddedSignal` |
| `public.shopping_list.item.updated` | same | `PublicShoppingListItemUpdatedSignal` |
| `public.shopping_list.item.checked_off` | same | `PublicShoppingListItemCheckedOffSignal` |
| `public.shopping_list.item.removed` | same | `PublicShoppingListItemRemovedSignal` |
| (not in the first catalog) | `public.shopping_list.list.requested` | `PublicShoppingListListRequestedSignal` |
| (not in the first catalog) | `public.shopping_list.list.responded` | `PublicShoppingListListRespondedSignal` |

`requested` is published by `cynthus-core-api` and consumed by `cynthus-shopping`; `responded` is published by `cynthus-shopping` and consumed by `cynthus-core-api`, which relays it to the waiting client. The rest of this domain (access requests, delegation, procurement target, vendor preference, auto-purchase and generation) is still to be built. The Shopping design adds list orders, procurement batches and a planner, each with signals of their own; see [../architecture/shopping-design.md](../architecture/shopping-design.md).

### Sample Payloads — Shopping List

```json
// public.shopping_list.created
{
  "list_id": "sl_r0s1t2",
  "workspace_id": "ws_d4e5f6",
  "created_by": "usr_a1b2c3",
  "name": "Weekly Groceries",
  "linked_procurement": false,
  "created_at": "2027-10-01T09:00:00Z"
}

// public.shopping_list.item.added
{
  "list_id": "sl_r0s1t2",
  "item_id": "sli_u3v4w5",
  "workspace_id": "ws_d4e5f6",
  "added_by": "usr_a1b2c3",
  "name": "Whole Milk",
  "quantity": 2,
  "unit": "gallon",
  "notes": "Organic if available",
  "source": "manual",
  "catalog_item_id": "cat_k7l8m9",
  "preferred_vendor_id": null,
  "added_at": "2027-10-01T09:05:00Z"
}

// public.shopping_list.item.checked_off
{
  "list_id": "sl_r0s1t2",
  "item_id": "sli_u3v4w5",
  "workspace_id": "ws_d4e5f6",
  "checked_off_by": "usr_a1b2c3",
  "name": "Whole Milk",
  "quantity_purchased": 2,
  "unit": "gallon",
  "vendor_id": "vnd_q3r4s5",
  "checked_off_at": "2027-10-02T11:20:00Z"
}

// internal.shopping_list.procurement_target.set
{
  "list_id": "sl_r0s1t2",
  "workspace_id": "ws_d4e5f6",
  "set_by": "usr_a1b2c3",
  "previous_target_id": null,
  "set_at": "2027-10-01T09:01:00Z"
}

// internal.shopping_list.generation.requested
{
  "generation_request_id": "gen_x6y7z8",
  "list_id": "sl_r0s1t2",
  "workspace_id": "ws_d4e5f6",
  "requested_by": "usr_a1b2c3",
  "mode": "restock",
  "include_promotions": true,
  "purchase_history_window_days": 90,
  "context_bundle_id": "ctx_a9b0c1",
  "requested_at": "2027-10-01T09:10:00Z"
}

// internal.shopping_list.generation.completed
{
  "generation_request_id": "gen_x6y7z8",
  "list_id": "sl_r0s1t2",
  "workspace_id": "ws_d4e5f6",
  "generated_items": [
    { "name": "Whole Milk", "quantity": 2, "unit": "gallon", "rationale": "Purchased weekly; currently low" },
    { "name": "Greek Yogurt", "quantity": 4, "unit": "cup", "rationale": "On sale at Kroger this week" }
  ],
  "promotion_hits": 2,
  "completed_at": "2027-10-01T09:10:05Z"
}

// internal.shopping_list.autopurchase.reminder_due
{
  "schedule_id": "asc_d2e3f4",
  "list_id": "sl_r0s1t2",
  "workspace_id": "ws_d4e5f6",
  "user_id": "usr_a1b2c3",
  "items": [
    { "item_id": "sli_u3v4w5", "name": "Whole Milk", "quantity": 2, "unit": "gallon", "estimated_price_usd": 7.98 }
  ],
  "vendor_id": "vnd_q3r4s5",
  "vendor_name": "Kroger",
  "execute_at": "2027-10-05T08:00:00Z",
  "grace_period_ends_at": "2027-10-05T08:00:00Z",
  "reminder_sent_at": "2027-10-02T08:00:00Z"
}

// public.shopping_list.autopurchase.confirmed
{
  "schedule_id": "asc_d2e3f4",
  "list_id": "sl_r0s1t2",
  "workspace_id": "ws_d4e5f6",
  "confirmed_by": "system",
  "confirmation_reason": "grace_period_elapsed",
  "items": [
    { "item_id": "sli_u3v4w5", "name": "Whole Milk", "quantity": 2, "unit": "gallon" }
  ],
  "vendor_id": "vnd_q3r4s5",
  "confirmed_at": "2027-10-05T08:00:01Z"
}

// internal.shopping_list.meal_gap.detected
{
  "workspace_id": "ws_d4e5f6",
  "user_id": "usr_a1b2c3",
  "lookahead_days": 3,
  "gaps": [
    {
      "meal_plan_entry_id": "pln_g5h6i7",
      "meal_name": "Lemon Herb Roasted Chicken",
      "planned_date": "2027-10-04",
      "missing_ingredients": [
        { "name": "Fresh Thyme", "quantity": 1, "unit": "bunch" },
        { "name": "Lemons", "quantity": 2, "unit": "count" }
      ]
    }
  ],
  "active_list_id": "sl_r0s1t2",
  "detected_at": "2027-10-01T06:00:00Z"
}
```

---

## Domain: Group Management

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-GM-001 | `public.group.created` | public | `cynthus-core-api` | `cynthus-identity`, `cynthus-audit` | Group workspace created; identity service provisions workspace-scoped token claims |
| FT-GM-001 | `public.group.updated` | public | `cynthus-core-api` | `cynthus-audit` | Group name, settings, or metadata changed |
| FT-GM-001 | `public.group.deleted` | public | `cynthus-core-api` | `cynthus-identity`, `cynthus-messaging`, `cynthus-audit` | Group removed; identity revokes workspace claims; messaging removes channels |
| FT-GM-002 | `public.group.member_added` | public | `cynthus-core-api` | `cynthus-identity`, `cynthus-notification`, `cynthus-audit` | User added to group with assigned role; JWT claims updated |
| FT-GM-002 | `public.group.member_role_changed` | public | `cynthus-core-api` | `cynthus-identity`, `cynthus-audit` | Member's group role changed; JWT refreshed to reflect new permissions |
| FT-GM-002 | `public.group.member_removed` | public | `cynthus-core-api` | `cynthus-identity`, `cynthus-notification`, `cynthus-audit` | Member removed from group; workspace access revoked |
| FT-GM-003 | `public.group.join_requested` | public | `cynthus-core-api` | `cynthus-notification`, `cynthus-audit` | User submitted a join request or accepted a group invite |
| FT-GM-003 | `public.group.join_approved` | public | `cynthus-core-api` | `cynthus-identity`, `cynthus-notification`, `cynthus-audit` | Group manager approved the join; member provisioned |

### Sample Payloads — Group Management

```json
// public.group.created
{
  "group_id": "grp_v9w0x1",
  "workspace_id": "ws_d4e5f6",
  "created_by": "usr_a1b2c3",
  "name": "The Martinez Family",
  "account_type": "residential",
  "member_limit": 5,
  "created_at": "2027-10-15T10:00:00Z"
}

// public.group.member_added
{
  "group_id": "grp_v9w0x1",
  "workspace_id": "ws_d4e5f6",
  "added_by": "usr_a1b2c3",
  "member_id": "usr_b5c6d7",
  "role": "member",
  "added_at": "2027-10-15T10:05:00Z"
}

// public.group.join_requested
{
  "request_id": "jrq_j1k2l3",
  "group_id": "grp_v9w0x1",
  "workspace_id": "ws_d4e5f6",
  "requester_id": "usr_c8d9e0",
  "invite_code_used": "INV-XK92M",
  "requested_at": "2027-10-16T09:00:00Z"
}
```

---

## Domain: Engagement Management

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-EM-001 | `public.engagement.created` | public | `cynthus-core-api` | `cynthus-chat`, `cynthus-notification`, `cynthus-audit` | Engagement event created; Astri notified to begin planning assist |
| FT-EM-001 | `public.engagement.updated` | public | `cynthus-core-api` | `cynthus-chat`, `cynthus-notification`, `cynthus-audit` | Engagement details (attendees, date, venue, materials) changed |
| FT-EM-001 | `public.engagement.deleted` | public | `cynthus-core-api` | `cynthus-notification`, `cynthus-audit` | Engagement cancelled; attendees notified |
| FT-EM-002 | `public.engagement.attendee_joined` | public | `cynthus-core-api` | `cynthus-chat`, `cynthus-profile`, `cynthus-audit` | User RSVP'd; their dietary constraints shared with engagement host |
| FT-EM-002 | `public.engagement.attendee_declined` | public | `cynthus-core-api` | `cynthus-notification`, `cynthus-audit` | User declined RSVP |
| FT-EM-003 | `audit.engagement.manager_assigned` | audit | `cynthus-core-api` | `cynthus-audit` | Co-host delegation granted for an engagement |

### Sample Payloads — Engagement Management

```json
// public.engagement.created
{
  "engagement_id": "eng_m4n5o6",
  "workspace_id": "ws_d4e5f6",
  "created_by": "usr_a1b2c3",
  "name": "Birthday Dinner — Sofia",
  "scheduled_date": "2028-02-14",
  "location": "Home",
  "estimated_attendees": 8,
  "created_at": "2028-01-20T15:00:00Z"
}

// public.engagement.attendee_joined
{
  "engagement_id": "eng_m4n5o6",
  "workspace_id": "ws_d4e5f6",
  "attendee_id": "usr_b5c6d7",
  "dietary_constraints_shared": true,
  "constraint_summary": { "allergens": ["peanuts"], "preferences": ["vegetarian"] },
  "joined_at": "2028-01-21T10:00:00Z"
}
```

---

## Domain: Live Companion

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-LC-001 | `public.live_session.started` | public | `cynthus-core-api` | `cynthus-messaging`, `cynthus-audit` | Live peer-to-peer or user-to-provider session initiated |
| FT-LC-001 | `public.live_session.ended` | public | `cynthus-core-api` | `cynthus-audit` | Live session terminated; duration and participant record closed |
| FT-LC-001 | `internal.live_session.step_advanced` | internal | `cynthus-chat` | `cynthus-messaging` | Astri advanced to next step in real-time guided cooking session |

### Sample Payloads — Live Companion

```json
// public.live_session.started
{
  "session_id": "lss_p7q8r9",
  "workspace_id": "ws_d4e5f6",
  "initiator_id": "usr_a1b2c3",
  "participant_id": "usr_b5c6d7",
  "participant_type": "peer",
  "context": "recipe_guidance",
  "recipe_id": "rec_c5d6e7",
  "started_at": "2029-01-15T18:30:00Z"
}

// internal.live_session.step_advanced
{
  "session_id": "lss_p7q8r9",
  "workspace_id": "ws_d4e5f6",
  "recipe_id": "rec_c5d6e7",
  "current_step": 3,
  "total_steps": 7,
  "step_description": "Add the diced onions to the pan and sauté until translucent, about 4 minutes.",
  "advanced_at": "2029-01-15T18:35:00Z"
}
```

---

## Domain: AI Companion

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-AI-001 | `internal.intelligence.chat.session_started` | internal | `cynthus-core-api` | `cynthus-chat`, `cynthus-audit` | User initiated an Astri conversation session |
| FT-AI-001 | `internal.intelligence.chat.session_ended` | internal | `cynthus-chat` | `cynthus-core-api`, `cynthus-audit` | Astri conversation session closed |
| FT-AI-002 | `internal.intelligence.context.assembled` | internal | `cynthus-core-api` | `cynthus-chat` | Context bundle (inventory snapshot + profile constraints + filtered recipes) assembled and dispatched to Intelligence subnet; for the chat flow the bundle travels inside `internal.intelligence.chat.message_requested`, because Chat has no route to Core |
| FT-AI-001, FT-AI-002 | `internal.intelligence.chat.message_requested` | internal | `cynthus-core-api` | `cynthus-chat` | User message and the assembled context dispatched to the Intelligence subnet; not sent to audit because the payload holds health data; the answer streams on the Chat websocket |
| FT-AI-001 | `internal.intelligence.chat.message_generated` | internal | `cynthus-chat` | `cynthus-core-api`, `cynthus-audit` | An answer is complete; records the model configuration hash, token counts and the hard-constraint check; carries no answer text |
| FT-AI-003 | *(internal cynthus-chat processing; no Service Bus signal)* | — | — | — | Screen-reader linearization is an in-process formatting step within the Intelligence subnet |
| FT-AI-004 | *(hot path WebSocket stream; no Service Bus signal)* | — | — | — | TTS token streaming operates on a direct WebSocket channel, bypassing Service Bus |
| FT-AI-005 | `internal.intelligence.chat.interaction_recorded` | internal | `cynthus-chat` | `cynthus-core-api`, `cynthus-audit` | Astri received a real-world state disclosure from user (e.g., "I just used the last of the milk"); downstream services independently mutate their state |

### Sample Payloads — AI Companion

```json
// internal.intelligence.context.assembled
{
  "context_bundle_id": "ctx_a9b0c1",
  "workspace_id": "ws_d4e5f6",
  "user_id": "usr_a1b2c3",
  "inventory_snapshot_id": "inv_snap_s2t3u4",
  "hard_constraints": ["peanuts", "tree_nuts"],
  "soft_preferences": { "cuisines": ["mexican", "italian"], "energy_level": 4 },
  "recipe_candidate_count": 12,
  "allergen_filtered_count": 3,
  "assembled_at": "2027-01-15T12:04:01Z"
}

// internal.intelligence.chat.message_requested (the access token travels as the authorization message property)
{
  "session_id": "ses_y8z9a0",
  "message_id": "msg_k1l2m3",
  "text": "What can I cook tonight?",
  "context": {
    "context_bundle_id": "ctx_a9b0c1",
    "hard_constraints": ["peanuts", "tree_nuts"],
    "soft_preferences": { "cuisines": ["mexican", "italian"], "energy_level": 4 },
    "inventory_snapshot": [ { "name": "whole milk", "quantity": 1, "unit": "gallon", "expiry_date": "2027-01-20" } ],
    "recipe_candidates": [ { "recipe_id": "rcp_p4q5r6", "title": "Black bean tacos", "ingredients": ["black beans", "tortillas"], "minutes": 25, "energy_cost": 3 } ],
    "recipe_candidate_count": 12,
    "allergen_filtered_count": 3,
    "conversation_history": [],
    "assembled_at": "2027-01-15T12:04:01Z"
  }
}

// internal.intelligence.chat.message_generated
{
  "session_id": "ses_y8z9a0",
  "message_id": "msg_k1l2m3",
  "provider": "ollama",
  "model": "phi4-mini:latest",
  "model_configuration_hash": "36f158577e6b05f1603430ebbe8e46ae0a1020abedcf74a8bbff90eeec57bf6c",
  "finish_reason": "stop",
  "prompt_tokens": 812,
  "completion_tokens": 143,
  "generation_seconds": 21.4,
  "constraint_check": "passed",
  "regenerations": 0
}

// internal.intelligence.chat.interaction_recorded
{
  "interaction_id": "int_v5w6x7",
  "session_id": "ses_y8z9a0",
  "workspace_id": "ws_d4e5f6",
  "user_id": "usr_a1b2c3",
  "interaction_type": "state_disclosure",
  "natural_language": "I just finished the last of the whole milk.",
  "inferred_mutations": [
    { "entity": "inventory_item", "item_id": "itm_h4i5j6", "action": "depleted", "quantity": 0 }
  ],
  "recorded_at": "2027-01-15T12:10:00Z"
}
```

---

## Domain: Messaging

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-MS-001 | `public.messaging.message.sent` | public | `cynthus-messaging` | `cynthus-notification`, `cynthus-audit` | Text message sent to a group channel |
| FT-MS-001 | `public.messaging.message.deleted` | public | `cynthus-messaging` | `cynthus-audit` | Message removed from a channel |
| FT-MS-002 | *(triggered by domain signals; no dedicated signal)* | — | — | — | Interactive cards are rendered by `cynthus-messaging` when it consumes signals such as `public.meal.vote.initiated` or `public.inventory.item.low`; no separate card signal is published |
| FT-MS-003 | `public.messaging.recipe.shared` | public | `cynthus-messaging` | `cynthus-audit` | Recipe rich-link card shared into a group channel |
| FT-MS-003 | `public.messaging.inventory_item.shared` | public | `cynthus-messaging` | `cynthus-audit` | Inventory item rich-link card shared into a group channel |

### Sample Payloads — Messaging

```json
// public.messaging.message.sent
{
  "message_id": "msg_b1c2d3",
  "channel_id": "chn_e4f5g6",
  "group_id": "grp_v9w0x1",
  "workspace_id": "ws_d4e5f6",
  "sender_id": "usr_a1b2c3",
  "body": "Should we do tacos tonight or the chicken?",
  "sent_at": "2027-10-15T17:30:00Z"
}

// public.messaging.recipe.shared
{
  "message_id": "msg_h7i8j9",
  "channel_id": "chn_e4f5g6",
  "group_id": "grp_v9w0x1",
  "workspace_id": "ws_d4e5f6",
  "shared_by": "usr_a1b2c3",
  "recipe_id": "rec_c5d6e7",
  "recipe_name": "Classic Beef Tacos",
  "shared_at": "2027-10-15T17:31:00Z"
}
```

---

## Domain: Clinical Monitoring

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-CL-001 | `internal.health.telemetry.snapshot_recorded` | internal | `cynthus-analysis` | `cynthus-audit` | Warm-path biometric snapshot committed after aggregation from the hot-path time-series buffer; raw stream bypasses Service Bus entirely |
| FT-CL-002 | `audit.health.provider_data_access` | audit | `cynthus-health-api` | `cynthus-audit` | Provider read a patient's health dataset; immutable record per HIPAA |
| FT-CL-003 | `public.health.biometric.anomaly_detected` | public | `cynthus-analysis` | `cynthus-notification`, `cynthus-chat`, `cynthus-health-api`, `cynthus-audit` | Biometric telemetry breached a threshold; alert dispatched to user and forwarded to provider triage if consented |
| FT-CL-004 | `internal.health.analysis.correlation_completed` | internal | `cynthus-analysis` | `cynthus-chat`, `cynthus-health-api` | Correlation model linked dietary patterns to biometric anomalies or reported symptoms; surfaced as Astri insight |
| FT-CL-005 | `internal.health.rpm.transmission_logged` | internal | `cynthus-health-api` | `cynthus-billing-api`, `cynthus-audit` | Qualifying physiologic data transmission event recorded for CPT billing cycle |
| FT-CL-005 | `internal.health.rpm.clinician_interaction_logged` | internal | `cynthus-health-api` | `cynthus-billing-api`, `cynthus-audit` | Clinician interaction time recorded for RPM billing compliance |

### Sample Payloads — Clinical Monitoring

```json
// internal.health.telemetry.snapshot_recorded
{
  "snapshot_id": "snp_k0l1m2",
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "window_start": "2029-06-01T08:00:00Z",
  "window_end": "2029-06-01T09:00:00Z",
  "metrics": {
    "avg_heart_rate_bpm": 72,
    "avg_glucose_mg_dl": 98,
    "systolic_bp_mmhg": 122,
    "diastolic_bp_mmhg": 78
  },
  "source": "apple_healthkit",
  "recorded_at": "2029-06-01T09:01:00Z"
}

// public.health.biometric.anomaly_detected
{
  "anomaly_id": "anm_n3o4p5",
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "metric": "glucose_mg_dl",
  "observed_value": 195,
  "threshold": 160,
  "severity": "high",
  "consented_provider_ids": ["prv_q6r7s8"],
  "snapshot_id": "snp_k0l1m2",
  "detected_at": "2029-06-01T09:01:05Z"
}

// internal.health.rpm.transmission_logged
{
  "log_id": "rpm_t9u0v1",
  "patient_id": "usr_a1b2c3",
  "provider_id": "prv_q6r7s8",
  "workspace_id": "ws_d4e5f6",
  "cpt_category": "99454",
  "data_type": "glucose_continuous",
  "billing_cycle": "2029-06",
  "logged_at": "2029-06-01T09:01:06Z"
}
```

---

## Domain: Service and Resource Management

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-SR-001 | `public.service_registry.created` | public | `cynthus-partner-api` | `cynthus-audit` | Service registry created by a provider or supplier |
| FT-SR-001 | `public.service_registry.updated` | public | `cynthus-partner-api` | `cynthus-audit` | Registry content or availability updated |
| FT-SR-001 | `public.service_registry.deleted` | public | `cynthus-partner-api` | `cynthus-audit` | Registry removed |
| FT-SR-002 | `audit.service_registry.management_delegated` | audit | `cynthus-partner-api` | `cynthus-audit` | Staff member granted management rights on a service registry |
| FT-SR-003 | `public.promotion.created` | public | `cynthus-partner-api` | `cynthus-notification`, `cynthus-chat`, `cynthus-audit` | Promotion published; delivered only to users with active opt-in subscription to that vendor |
| FT-SR-003 | `public.promotion.updated` | public | `cynthus-partner-api` | `cynthus-notification`, `cynthus-audit` | Promotion terms or dates changed |
| FT-SR-003 | `public.promotion.expired` | public | `cynthus-scheduler` | `cynthus-notification`, `cynthus-partner-api`, `cynthus-audit` | Promotion reached its end date; removed from active listings |
| FT-SR-004 | `public.device_registry.device_listed` | public | `cynthus-partner-api` | `cynthus-audit` | Partner registered a hardware device for user discovery |
| FT-SR-004 | `public.device_registry.device_removed` | public | `cynthus-partner-api` | `cynthus-audit` | Device delisted from the partner device registry |
| FT-SR-006 | `public.vendor.subscription_created` | public | `cynthus-core-api` | `cynthus-notification`, `cynthus-partner-api`, `cynthus-chat`, `cynthus-audit` | User explicitly opted in to receive promotional notifications from a specific vendor |
| FT-SR-006 | `public.vendor.subscription_removed` | public | `cynthus-core-api` | `cynthus-notification`, `cynthus-partner-api`, `cynthus-audit` | User unsubscribed from a vendor's promotional notifications |
| FT-SR-007 | `internal.vendor_directory.search.performed` | internal | `cynthus-core-api` | `cynthus-partner-api` | User performed a vendor discovery search; analytics telemetry captured |

### Sample Payloads — Service and Resource Management

```json
// public.promotion.created
{
  "promotion_id": "prm_w2x3y4",
  "vendor_id": "vnd_q3r4s5",
  "workspace_id": "ws_d4e5f6",
  "name": "20% Off All Organic Produce",
  "discount_pct": 20,
  "applicable_categories": ["produce", "organic"],
  "valid_from": "2028-11-01",
  "valid_through": "2028-11-07",
  "target_account_types": ["residential", "commercial"],
  "published_at": "2028-10-28T08:00:00Z"
}

// public.vendor.subscription_created
{
  "subscription_id": "vsb_z5a6b7",
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "vendor_id": "vnd_q3r4s5",
  "vendor_name": "Kroger",
  "notification_channels": ["push", "in_app"],
  "subscribed_at": "2028-10-01T09:00:00Z"
}

// internal.vendor_directory.search.performed
{
  "search_id": "vds_c8d9e0",
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "query": "organic grocery delivery",
  "account_type": "residential",
  "geographic_area": "Chicago, IL",
  "result_sources": ["cynthus_directory", "instacart"],
  "result_count": 7,
  "performed_at": "2028-11-01T10:00:00Z"
}
```

---

## Domain: Contribution Management

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-CO-001 | `audit.partner.contribution_recorded` | audit | `cynthus-partner-api` | `cynthus-audit`, `cynthus-billing-api` | Partner contribution (capital, hardware grant, sponsorship) committed to ledger |

### Sample Payload — Contribution Management

```json
// audit.partner.contribution_recorded
{
  "contribution_id": "ctr_f1g2h3",
  "partner_id": "prt_i4j5k6",
  "workspace_id": "ws_d4e5f6",
  "type": "hardware_grant",
  "description": "10x SmartShelf sensor units — Dev Pilot Program",
  "estimated_value_usd": 2500.00,
  "recorded_at": "2028-04-01T14:00:00Z"
}
```

---

## Domain: Billing Management

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-BL-001, FT-BL-002 | `internal.system.payment_method.updated` | internal | `cynthus-billing-api` | `cynthus-audit` | User added, changed, or removed a payment method |
| FT-BL-001, FT-BL-002 | `internal.system.subscription.upgraded` | internal | `cynthus-billing-api` | `cynthus-identity`, `cynthus-audit` | User moved to a higher subscription tier; identity issues refreshed JWT |
| FT-BL-001, FT-BL-002 | `internal.system.subscription.downgraded` | internal | `cynthus-billing-api` | `cynthus-identity`, `cynthus-audit` | User moved to a lower tier; token claims reduced on next JWT refresh |
| FT-BL-001, FT-BL-002 | `internal.system.entitlement.updated` | internal | `cynthus-billing-api` | `cynthus-identity` | Booster pack purchased or cancelled (ADR-005 canonical signal); identity immediately issues refreshed JWT with updated entitlement claims |

### Sample Payloads — Billing Management

```json
// internal.system.subscription.upgraded
{
  "billing_event_id": "bil_l7m8n9",
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "previous_tier": "Residential-MI-Basic",
  "new_tier": "Residential-MI-Premium",
  "effective_date": "2027-10-01",
  "upgraded_at": "2027-10-01T00:00:00Z"
}

// internal.system.entitlement.updated
{
  "entitlement_event_id": "ent_o0p1q2",
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "action": "booster_purchased",
  "booster_id": "BP-RES-001",
  "booster_name": "Group Size Pack",
  "updated_claims": {
    "max_group_members": 10
  },
  "previous_claims": {
    "max_group_members": 5
  },
  "updated_at": "2027-10-15T11:00:00Z"
}
```

---

## Domain: Account Management

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-AM-001 | `audit.account.contact_updated` | audit | `cynthus-core-api` | `cynthus-audit` | User changed their name, email, or phone number |
| FT-AM-002 | `internal.profile.soft_preferences.updated` | internal | `cynthus-profile` | `cynthus-chat`, `cynthus-audit` | Soft preferences updated (cuisine, portion size, Energy Banker baseline, venue) |
| FT-AM-002 | `audit.profile.hard_constraint.updated` | audit | `cynthus-profile` | `cynthus-audit` | Hard constraint changed (allergen added or removed, medical condition updated); safety-critical; requires immutable audit entry |
| FT-AM-002 | `public.profile.profile.requested` | public | `cynthus-core-api` | `cynthus-profile`, `cynthus-audit` | A caller asked to create, get, update or delete their own profile; the API acknowledges the client at once and hands the request, with the caller token as a message property, to the Profile service |
| FT-AM-002 | `public.profile.profile.responded` | public | `cynthus-profile` | `cynthus-core-api`, `cynthus-audit` | The Profile service's answer with an HTTP-style status and the profile or error; the API relays it only to the caller who asked |
| FT-AM-002 | `public.profile.profile.created` | public | `cynthus-profile` | `cynthus-audit` | A profile was created; names which parts were set, not their contents |
| FT-AM-002 | `public.profile.profile.updated` | public | `cynthus-profile` | `cynthus-audit` | A profile was changed; names which parts changed, not their contents |
| FT-AM-002 | `public.profile.profile.deleted` | public | `cynthus-profile` | `cynthus-audit` | A profile was deleted; names which parts it held, not their contents |
| FT-AM-002 | `public.profile.snapshot.published` | public | `cynthus-profile` | `cynthus-analysis`, `cynthus-audit` | A user signed in and has a profile: the profile (allergies, likes, dislikes, favorites, conditions) is pushed for the Analysis engine to correlate with inventory and shopping patterns |
| FT-AM-003 | *(handled by billing signals; see FT-BL-001)* | — | — | — | Subscription preference changes route through cynthus-billing-api |
| FT-AM-004, FT-AM-005, FT-AM-006, FT-AM-007 | `audit.account.business_profile_updated` | audit | `cynthus-core-api` | `cynthus-audit` | Business or partner profile details changed |
| FT-AM-008 | `internal.account.deletion_requested` | internal | `cynthus-core-api` | `cynthus-scheduler`, `cynthus-audit` | User submitted account deletion request; 30-day grace period clock started |
| FT-AM-008 | `internal.account.deletion_confirmed` | internal | `cynthus-scheduler` | `cynthus-core-api`, `cynthus-worker`, `cynthus-audit` | Grace period elapsed without cancellation; irreversible purge queued |
| FT-AM-008 | `audit.account.data_erased` | audit | `cynthus-worker` | `cynthus-audit` | PII purge completed; audit records pseudonymized per GDPR/CCPA |
| FT-AM-009 | `internal.profile.notification_preferences.updated` | internal | `cynthus-profile` | `cynthus-notification`, `cynthus-scheduler` | User updated notification channel, per-type toggles, quiet hours, or batching preferences |
| FT-AM-010 | `internal.account.onboarding_started` | internal | `cynthus-core-api` | `cynthus-audit` | First-run wizard launched for new user |
| FT-AM-010 | `internal.account.onboarding_completed` | internal | `cynthus-core-api` | `cynthus-chat`, `cynthus-audit` | Onboarding wizard completed; Astri greeting session triggered |

**Profile request and response.** The profile request, response, fact and snapshot signals are `public.*` by decision, although the other profile signals above are `internal.*`. Allergies and medical conditions are hard constraints: the Profile service publishes `audit.profile.hard_constraint.updated` before it commits a change to them, and refuses the change if it cannot. Profile signal bodies hold health information and are never logged.

### Sample Payloads — Account Management

```json
// audit.profile.hard_constraint.updated
{
  "audit_event_id": "aev_r3s4t5",
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "constraint_type": "allergen",
  "action": "added",
  "value": "shellfish",
  "previous_constraints": ["peanuts", "tree_nuts"],
  "updated_constraints": ["peanuts", "tree_nuts", "shellfish"],
  "updated_at": "2027-04-10T09:00:00Z"
}

// internal.account.deletion_requested
{
  "deletion_request_id": "del_u6v7w8",
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "grace_period_ends_at": "2027-05-10T09:00:00Z",
  "requested_at": "2027-04-10T09:00:00Z"
}

// audit.account.data_erased
{
  "erasure_id": "ers_x9y0z1",
  "user_id_hash": "sha256:a3f9c2b1...",
  "workspace_id": "ws_d4e5f6",
  "records_purged": {
    "inventory_items": 412,
    "meal_plans": 38,
    "recipes": 94,
    "chat_sessions": 210,
    "profile_records": 1
  },
  "clinical_data_excluded": false,
  "erased_at": "2027-05-10T09:01:00Z"
}

// internal.profile.notification_preferences.updated
{
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "channels": { "push": true, "email": false, "sms": false, "in_app": true },
  "type_toggles": { "inventory_low": true, "item_expiry": true, "meal_vote": true, "biometric_alert": true },
  "quiet_hours": { "start": "22:00", "end": "07:00", "timezone": "America/Chicago" },
  "batching": "instant",
  "updated_at": "2027-04-10T10:00:00Z"
}
```

---

## Domain: Rating Management

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-RT-001 | `public.rating.created` | public | `cynthus-core-api` | `cynthus-analysis`, `cynthus-chat`, `cynthus-audit` | User submitted a rating for a recipe, meal, provider, or venue; feeds preference model |
| FT-RT-001 | `public.rating.updated` | public | `cynthus-core-api` | `cynthus-analysis`, `cynthus-audit` | User revised an existing rating |
| FT-RT-002 | `internal.profile.favorite.added` | internal | `cynthus-profile` | `cynthus-chat`, `cynthus-analysis` | User flagged an entity as a favorite; Astri prioritizes in future suggestions |
| FT-RT-002 | `internal.profile.favorite.removed` | internal | `cynthus-profile` | `cynthus-chat`, `cynthus-analysis` | Favorite flag removed from an entity |

### Sample Payloads — Rating Management

```json
// public.rating.created
{
  "rating_id": "rat_a2b3c4",
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "entity_type": "recipe",
  "entity_id": "rec_c5d6e7",
  "entity_name": "Classic Beef Tacos",
  "score": 4,
  "max_score": 5,
  "notes": "Family loved it. Could use more lime.",
  "rated_at": "2027-10-15T20:30:00Z"
}

// internal.profile.favorite.added
{
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "entity_type": "recipe",
  "entity_id": "rec_c5d6e7",
  "added_at": "2027-10-15T20:31:00Z"
}
```

---

## Domain: Tag Management

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-TG-001 | `internal.tag.created` | internal | `cynthus-core-api` | `cynthus-audit` | User-defined tag created in the workspace tag registry |
| FT-TG-001 | `internal.tag.assigned` | internal | `cynthus-core-api` | `cynthus-analysis`, `cynthus-audit` | Tag assigned to an entity (recipe, item, venue, provider) |
| FT-TG-001 | `internal.tag.removed` | internal | `cynthus-core-api` | `cynthus-audit` | Tag unassigned from an entity or deleted from the registry |

### Sample Payload — Tag Management

```json
// internal.tag.assigned
{
  "tag_id": "tag_d5e6f7",
  "tag_name": "quick-weeknight",
  "workspace_id": "ws_d4e5f6",
  "assigned_by": "usr_a1b2c3",
  "entity_type": "recipe",
  "entity_id": "rec_c5d6e7",
  "assigned_at": "2028-02-01T10:00:00Z"
}
```

---

## Domain: Access Control

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-AC-001 | `audit.access.provider_data_consent_granted` | audit | `cynthus-health-api` | `cynthus-audit`, `cynthus-identity` | User granted a provider access to their health data; scope, duration, and data types recorded |
| FT-AC-001 | `audit.access.provider_data_consent_revoked` | audit | `cynthus-health-api` | `cynthus-audit`, `cynthus-identity` | User revoked provider data access; identity service immediately invalidates affected claims |
| FT-AC-002 | `public.access.request.submitted` | public | `cynthus-core-api` | `cynthus-notification`, `cynthus-audit` | Access request submitted to the owner of a resource (inventory location, recipe library, group, engagement) |
| FT-AC-002 | `public.access.request.approved` | public | `cynthus-core-api` | `cynthus-identity`, `cynthus-notification`, `cynthus-audit` | Resource owner approved access request; permissions provisioned |
| FT-AC-002 | `public.access.request.denied` | public | `cynthus-core-api` | `cynthus-notification`, `cynthus-audit` | Resource owner denied the request |
| FT-AC-003 | *(same signal flow as FT-AC-002; provider is the requesting actor)* | — | — | — | Provider data access requests use the same `public.access.request.*` signals with actor_type set to PROVIDER |

### Sample Payloads — Access Control

```json
// audit.access.provider_data_consent_granted
{
  "consent_id": "cst_g8h9i0",
  "user_id": "usr_a1b2c3",
  "provider_id": "prv_q6r7s8",
  "workspace_id": "ws_d4e5f6",
  "data_scopes": ["meal_history", "inventory_history", "biometric_snapshots"],
  "duration_days": 90,
  "expires_at": "2029-09-01T00:00:00Z",
  "granted_at": "2029-06-03T10:00:00Z"
}

// public.access.request.submitted
{
  "request_id": "arq_j1k2l3",
  "workspace_id": "ws_d4e5f6",
  "requester_id": "usr_b5c6d7",
  "requester_type": "USER",
  "resource_type": "recipe_library",
  "resource_id": "lib_f8g9h0",
  "requested_role": "contributor",
  "reason": "I want to add family recipes to the shared library.",
  "submitted_at": "2027-10-20T09:00:00Z"
}

// public.access.request.approved
{
  "request_id": "arq_j1k2l3",
  "workspace_id": "ws_d4e5f6",
  "approved_by": "usr_a1b2c3",
  "requester_id": "usr_b5c6d7",
  "resource_type": "recipe_library",
  "resource_id": "lib_f8g9h0",
  "granted_role": "contributor",
  "approved_at": "2027-10-20T10:15:00Z"
}
```

---

## Domain: Accessibility

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-AX-001, FT-AX-002, FT-AX-003, FT-AX-005 | `internal.profile.accessibility_preference.updated` | internal | `cynthus-profile` | `cynthus-chat`, `cynthus-core-api` | Accessibility setting changed — screen reader mode, haptics, Zen Mode, high-contrast, or dark mode toggled; Astri response formatter and UI rendering update accordingly |
| FT-AX-004 | `internal.spatial.object_detected` | internal | `cynthus-video` | `cynthus-chat` | Object identified in smart glasses video frame with clock-face position metadata |
| FT-AX-004 | `internal.spatial.frame_processed` | internal | `cynthus-video` | `cynthus-chat` | Batch of video frames processed; spatial map of kitchen environment updated |
| FT-AX-006 | `internal.profile.locale.updated` | internal | `cynthus-profile` | `cynthus-core-api`, `cynthus-chat` | User changed language or locale setting |

### Sample Payloads — Accessibility

```json
// internal.profile.accessibility_preference.updated
{
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "preference": "zen_mode",
  "enabled": true,
  "updated_at": "2027-10-01T08:00:00Z"
}

// internal.spatial.object_detected
{
  "detection_id": "det_m4n5o6",
  "session_id": "lss_p7q8r9",
  "workspace_id": "ws_d4e5f6",
  "user_id": "usr_a1b2c3",
  "object": "olive_oil_bottle",
  "catalog_item_id": "cat_p6q7r8",
  "clock_position": 2,
  "distance_inches": 18,
  "confidence": 0.94,
  "detected_at": "2029-01-15T18:35:10Z"
}

// internal.profile.locale.updated
{
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "previous_locale": "en-US",
  "new_locale": "es-MX",
  "updated_at": "2030-03-01T09:00:00Z"
}
```

---

## Domain: Reporting and Compliance

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-RP-001 | *(synchronous audit log query; no async signal)* | — | — | — | User Data Access Report is a read-only query against the immutable audit ledger |
| FT-RP-002 | *(synchronous analytics query; no async signal)* | — | — | — | Provider Service Usage Report is a read-only aggregation query |
| FT-RP-003 | *(synchronous analytics query; no async signal)* | — | — | — | Partner Device Usage Report is a read-only aggregation query |
| FT-RP-004 | *(synchronous ledger query; no async signal)* | — | — | — | Partner Contribution Report is a read-only ledger query |
| FT-RP-005 | `internal.data_export.requested` | internal | `cynthus-core-api` | `cynthus-worker` | User submitted a data portability export request; worker job queued |
| FT-RP-005 | `internal.data_export.completed` | internal | `cynthus-worker` | `cynthus-notification` | Export archive packaged; secure download link sent to user |

### Sample Payloads — Reporting and Compliance

```json
// internal.data_export.requested
{
  "export_id": "exp_s9t0u1",
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "format": "json",
  "scopes": ["inventory", "meal_plans", "recipes", "profile", "chat_history"],
  "include_clinical_data": false,
  "requested_at": "2030-01-10T09:00:00Z",
  "sla_deadline_at": "2030-01-13T09:00:00Z"
}

// internal.data_export.completed
{
  "export_id": "exp_s9t0u1",
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "archive_size_mb": 14.2,
  "download_url": "https://cynthus-exports.blob.core.windows.net/exports/exp_s9t0u1.zip",
  "download_expires_at": "2030-01-17T09:00:00Z",
  "completed_at": "2030-01-10T09:45:00Z"
}
```

---

## Domain: Data Analytics and Dashboards

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-DA-001, FT-DA-002 | *(synchronous analytics query; no async signal)* | — | — | — | Group Sentiment and Voting Dashboards are read-only queries over data written by `public.rating.created` and `public.meal.vote.*` signals |
| FT-DA-003 | *(synchronous analytics query; no async signal)* | — | — | — | Enterprise Multi-Group Sentiment Dashboard is a read-only cross-tenancy aggregation |
| FT-DA-004 | `internal.analysis.harmony_score.computed` | internal | `cynthus-analysis` | `cynthus-core-api`, `cynthus-notification` | 24-hour Harmony Score computed; low score triggers Astri rebalancing recommendations |
| FT-DA-005 | *(synchronous dashboard query; no async signal)* | — | — | — | Clinical Triage Dashboard reads from `cynthus-health-db` and the audit ledger; access itself is recorded via `audit.health.provider_data_access` |
| FT-DA-006 | `internal.analytics.spend.snapshot_recorded` | internal | `cynthus-analysis` | `cynthus-core-api` | Weekly/monthly grocery spend aggregation computed; result available for dashboard queries |
| FT-DA-007 | `internal.analytics.trend.computed` | internal | `cynthus-analysis` | `cynthus-partner-api` | Anonymized culinary trend batch computation complete; output available for B2B Predictive Reporting Portal |
| FT-DA-008 | *(synchronous dashboard query consuming DA-007 output; no async signal)* | — | — | — | B2B Supplier Predictive Reporting Portal serves the trend data produced by FT-DA-007 via synchronous query |

### Sample Payloads — Data Analytics and Dashboards

```json
// internal.analysis.harmony_score.computed
{
  "computation_id": "hsc_v2w3x4",
  "group_id": "grp_v9w0x1",
  "workspace_id": "ws_d4e5f6",
  "score": 71,
  "max_score": 100,
  "dimensions": {
    "meal_preference_satisfaction": 80,
    "workload_distribution": 65,
    "resource_equity": 72,
    "wellness_adherence": 68
  },
  "recommendation_triggered": true,
  "computed_at": "2027-10-16T00:00:00Z"
}

// internal.analytics.spend.snapshot_recorded
{
  "snapshot_id": "spd_y5z6a7",
  "workspace_id": "ws_d4e5f6",
  "period": "2027-10",
  "total_spend_usd": 412.50,
  "by_category": {
    "protein": 145.00,
    "produce": 92.00,
    "dairy": 55.00,
    "pantry": 78.50,
    "beverages": 42.00
  },
  "budget_target_usd": 450.00,
  "computed_at": "2027-11-01T00:00:00Z"
}

// internal.analytics.trend.computed
{
  "computation_id": "trd_b8c9d0",
  "period": "2030-Q1",
  "top_rising_ingredients": ["tahini", "miso paste", "chili crisp"],
  "top_substitution_patterns": [{ "original": "butter", "substitute": "olive_oil", "frequency_pct": 18 }],
  "regional_shifts": [{ "region": "midwest_us", "trend": "mediterranean_adoption", "yoy_growth_pct": 23 }],
  "records_analyzed": 4200000,
  "pii_stripped": true,
  "computed_at": "2030-04-01T02:00:00Z"
}
```

---

## Domain: Platform Infrastructure

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-PL-001 | *(consumer, not publisher)* | — | — | — | Cache sync (`cynthus-core-cache`) consumes `public.inventory.mutation.recorded` and other inventory signals; emits no dedicated signal of its own |
| FT-PL-001 | `internal.cache.sync.invalidated` | internal | `cynthus-core-cache` | `cynthus-core-api` | A cache entry expired or was explicitly invalidated; next read will hydrate from `cynthus-core-db` |
| FT-PL-002 | *(real-time WebSocket infrastructure; no Service Bus signal)* | — | — | — | The WebSocket hub is a stateless ingress gateway; session events are logged in-process |
| FT-PL-003 | `internal.spatial.object_detected` | internal | `cynthus-video` | `cynthus-chat` | (Shared with FT-AX-004) — Object identified in smart glasses feed |
| FT-PL-003 | `internal.spatial.frame_processed` | internal | `cynthus-video` | `cynthus-chat` | (Shared with FT-AX-004) — Batch of video frames processed |
| FT-PL-004 | `internal.worker.job.queued` | internal | `cynthus-core-api`, `cynthus-recipe`, `cynthus-worker` | `cynthus-worker` | Long-running job enqueued in the worker cluster |
| FT-PL-004 | `internal.worker.job.completed` | internal | `cynthus-worker` | originating service | Async job finished successfully; result reference returned to caller |
| FT-PL-004 | `internal.worker.job.failed` | internal | `cynthus-worker` | originating service, `cynthus-notification` | Async job failed; originating service may retry; user notified if user-visible |

### Sample Payloads — Platform Infrastructure

```json
// internal.cache.sync.invalidated
{
  "cache_key": "inventory_snapshot:ws_d4e5f6",
  "workspace_id": "ws_d4e5f6",
  "reason": "ttl_expired",
  "invalidated_at": "2027-04-14T07:00:05Z"
}

// internal.worker.job.queued
{
  "job_id": "job_e1f2g3",
  "job_type": "receipt_ocr",
  "workspace_id": "ws_d4e5f6",
  "submitted_by_service": "cynthus-core-api",
  "input_blob_uri": "https://cynthus-storage.blob.core.windows.net/receipts/job_e1f2g3.jpg",
  "priority": "normal",
  "queued_at": "2027-04-10T10:05:00Z"
}

// internal.worker.job.completed
{
  "job_id": "job_e1f2g3",
  "job_type": "receipt_ocr",
  "workspace_id": "ws_d4e5f6",
  "output_reference": "internal.inventory.scan.completed",
  "duration_ms": 4200,
  "completed_at": "2027-04-10T10:05:42Z"
}

// internal.worker.job.failed
{
  "job_id": "job_h4i5j6",
  "job_type": "url_recipe_scrape",
  "workspace_id": "ws_d4e5f6",
  "error_code": "SCRAPE_BLOCKED",
  "error_message": "Target host returned 403; paywall or bot-detection active.",
  "retry_count": 3,
  "failed_at": "2028-06-01T11:05:00Z"
}
```

---

## Domain: Security and Identity

| Feature | Signal Namespace | Topic | Publisher | Consumers | Synopsis |
|---|---|---|---|---|---|
| FT-SI-001 | `internal.identity.svid.issued` | internal | `spire-agent` | `cynthus-audit` | New X.509 SVID issued to a service workload container |
| FT-SI-001 | `internal.identity.svid.rotated` | internal | `spire-agent` | `cynthus-audit` | Short-lived SVID auto-rotated without service restart |
| FT-SI-001 | `audit.identity.svid.revoked` | audit | `spire-server` | `cynthus-audit` | SVID revoked; potential container compromise or policy violation |
| FT-SI-002 | `audit.identity.token_exchanged` | audit | `cynthus-core-api` | `cynthus-audit` | External JWT successfully exchanged for internal context headers |
| FT-SI-002 | `audit.identity.token_exchange_failed` | audit | `cynthus-core-api` | `cynthus-audit`, `cynthus-notification` | Token exchange rejected (invalid, expired, or tampered JWT); security event |
| FT-SI-004 | `audit.identity.user.authenticated` | audit | `cynthus-identity` | `cynthus-audit`, `cynthus-profile` | A user signed in with correct credentials. Carries the user id and username; never the password |
| FT-SI-004 | `audit.identity.user.rejected` | audit | `cynthus-identity` | `cynthus-audit` | A sign-in was refused. Carries the username that was tried and no tenant (nil UUID); never the password |
| FT-SI-004 | `audit.identity.token.issued` | audit | `cynthus-identity` | `cynthus-audit` | An access token was issued. Carries the token id (`jti`), signing key id, lifetime, roles and permissions; never the token |
| FT-SI-005 | `audit.identity.access.granted` | audit | `cynthus-core-api`, `cynthus-inventory` | `cynthus-audit` | A request carried a valid token that grants the permission it needs (HTTP 2xx path) |
| FT-SI-005 | `audit.identity.access.rejected` | audit | `cynthus-core-api`, `cynthus-inventory` | `cynthus-audit` | A request had no valid token: missing, malformed, expired, forged or for another caller (HTTP 401); security event |
| FT-SI-005 | `audit.identity.access.denied` | audit | `cynthus-core-api`, `cynthus-inventory` | `cynthus-audit` | A valid token lacked the permission the request needs (HTTP 403): the role-based access violation; security event |
| FT-SI-003 | `audit.system.ledger.entry_written` | audit | `cynthus-audit` | SIEM / archive system | Audit entry committed to write-once ledger; consumed by external SIEM integrations |

**Reading the access signals.** `audit.identity.access.rejected` means the caller could not be identified (401). `audit.identity.access.denied` means the caller was identified but their role does not allow the request (403), so it is the signal that shows a role-based access violation. Signals about an unknown caller carry the nil UUID as organization, workspace and actor. The `identity` publisher is the auth container; the API and Inventory services publish the access signals for the requests they check, so a request the API forwards to Inventory is recorded by both.

### Sample Payloads — Security and Identity

```json
// internal.identity.svid.issued
{
  "svid_id": "svid_k7l8m9",
  "spiffe_id": "spiffe://cynthus.io/ns/core/sa/cynthus-recipe",
  "service": "cynthus-recipe",
  "valid_from": "2027-01-15T12:00:00Z",
  "valid_until": "2027-01-15T13:00:00Z",
  "issued_at": "2027-01-15T12:00:00Z"
}

// audit.identity.svid.revoked
{
  "svid_id": "svid_n0o1p2",
  "spiffe_id": "spiffe://cynthus.io/ns/core/sa/cynthus-worker",
  "service": "cynthus-worker",
  "revocation_reason": "container_anomaly_detected",
  "revoked_at": "2027-06-01T03:15:00Z"
}

// audit.identity.token_exchanged
{
  "exchange_id": "tex_q3r4s5",
  "user_id": "usr_a1b2c3",
  "workspace_id": "ws_d4e5f6",
  "organization_id": "org_t6u7v8",
  "token_jti": "jwt_w9x0y1",
  "scopes_granted": ["core:read", "inventory:write", "recipe:read"],
  "exchanged_at": "2027-01-15T12:03:00Z"
}

// audit.identity.token_exchange_failed
{
  "attempt_id": "tex_z2a3b4",
  "token_jti": "jwt_c5d6e7",
  "failure_reason": "token_expired",
  "source_ip": "10.0.1.45",
  "attempted_at": "2027-01-15T12:04:00Z"
}

// audit.system.ledger.entry_written
{
  "ledger_entry_id": "led_f8g9h0",
  "entry_type": "profile_hard_constraint_updated",
  "actor_id": "usr_a1b2c3",
  "resource_type": "profile",
  "resource_id": "usr_a1b2c3",
  "action": "allergen_added",
  "timestamp": "2027-04-10T09:00:00Z",
  "immutable": true
}
```

---

## Appendix A: Signal Count by Topic

| Topic | Signal Count |
|---|---|
| `cynthus-topic-public` | 62 |
| `cynthus-topic-internal` | 61 |
| `cynthus-topic-audit` | 22 |
| **Total** | **145** |

---

## Appendix B: Services as Publishers and Consumers

| Service | Primary Publisher Domains | Primary Consumer Role |
|---|---|---|
| `cynthus-core-api` | Meal planning, inventory CRUD, group, engagement, account, access control, shopping list requests | Context assembly; routes to Intelligence subnet; forwards to notification |
| `cynthus-recipe` | Recipe CRUD, import, scaling, substitution | Consumes worker job completion signals |
| `cynthus-profile` | Profile mutations (hard constraints, soft preferences, notification prefs, favorites, accessibility) | Consumed by `cynthus-chat` and `cynthus-core-api` for suggestion filtering |
| `cynthus-chat` | AI companion interaction facts, substitution suggestions, vote auto-resolution | Consumes context bundles from `cynthus-core-api`; never calls back into Core at runtime |
| `cynthus-identity` | *(no direct publisher)* | Consumes `internal.system.entitlement.updated`, `public.group.member_added`, `public.access.request.approved` to issue refreshed JWTs |
| `cynthus-billing-api` | Subscription, payment, and entitlement signals | Consumes RPM billing log signals; source of truth for booster state |
| `cynthus-scheduler` | Inventory low/expiry, meal suggestion schedule trigger, auto-purchase reminders, meal gap detection, promotion expiry | Consumes meal plan, shopping list schedule, and notification preference signals |
| `cynthus-worker` | Worker job completion, OCR, scrape, export, nutrition enrichment | Consumes job-queued signals from Service Bus worker queue |
| `cynthus-partner-api` | Service registry, promotions, device registry, vendor directory, fulfillment orders | Consumes vendor subscription and fulfillment signals |
| `cynthus-shopping` | Shopping list CRUD and all shopping list item lifecycle signals | Consumes `public.inventory.item.low` to auto-append items to procurement list |
| `cynthus-messaging` | Message sent, recipe/item share signals | Consumes meal vote, inventory low, and other signals to render interactive chat cards |
| `cynthus-notification` | *(no direct publisher)* | Consumes signals from all domains that carry notification fan-out requirements |
| `cynthus-analysis` | Harmony Score, spend snapshots, trend computation, anomaly detection, correlation results | Consumes rating, vote, telemetry, and inventory signals |
| `cynthus-health-api` | Provider data access audit events, RPM billing logs | Consumes biometric anomaly and consent signals |
| `cynthus-video` | Spatial object detection and frame processing signals | Independent consumer of camera feed; publishes to `cynthus-topic-internal` only |
| `cynthus-audit` | Ledger entry written | Exclusive consumer of `cynthus-topic-audit`; write-once; never publishes domain signals |
| `cynthus-core-cache` | Cache invalidation signals | Exclusive consumer of inventory mutation signals for cache hydration |
| `spire-agent` / `spire-server` | SVID lifecycle signals | Consumed by `cynthus-audit` only |

---

## Appendix C: Features with No Async Signal

The following features operate exclusively via synchronous gRPC queries and produce no Service Bus signals:

| Feature | Reason |
|---|---|
| FT-MP-003 — Browse Meals by Category | Read-only catalog query |
| FT-RM-003 — Search Recipes | Read-only filtered query |
| FT-AI-003 — Screen-Reader Response Linearization | In-process formatting within `cynthus-chat` |
| FT-AI-004 — Low-Latency TTS Voice Streaming | Hot-path WebSocket stream; bypasses Service Bus |
| FT-MS-002 — Interactive In-Chat Cards | Rendered by `cynthus-messaging` upon consuming other domain signals |
| FT-AC-003 — Provider Requests Access to User Data | Reuses `public.access.request.*` signal flow |
| FT-AM-003 — Manage Subscription Preferences | Handled by `cynthus-billing-api` billing signals |
| FT-RP-001 — User Data Access Report | Read-only audit ledger query |
| FT-RP-002 — Provider Service Usage Report | Read-only analytics aggregation |
| FT-RP-003 — Partner Device Usage Report | Read-only analytics aggregation |
| FT-RP-004 — Partner Contribution Report | Read-only ledger query |
| FT-DA-001 — Group Sentiment Dashboard | Read-only query over rating/vote data |
| FT-DA-002 — Group Voting History Dashboard | Read-only query over vote history |
| FT-DA-003 — Enterprise Multi-Group Sentiment Dashboard | Read-only cross-tenancy aggregation |
| FT-DA-005 — Clinical Triage Dashboard | Read-only health data query; access logged via `audit.health.provider_data_access` |
| FT-DA-008 — B2B Supplier Predictive Reporting | Read-only query consuming DA-007 trend output |
| FT-PL-002 — WebSocket Hub | Real-time streaming infrastructure; no Service Bus involvement |
| FT-SR-005 — Device and Service Promotions | Reuses `public.promotion.*` signal flow from FT-SR-003 |
