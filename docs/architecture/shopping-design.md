# Shopping service: list, order and placement design

Status: **agreed 2026-11-08; phase 1 (lists and items) is built, phases 2 and 3 are not.** Related: cynthus-core#12 (feature), #147 (models), cynthus-shared#75 and #77 (signals), the signal catalog "Domain: Shopping List" (FT-SL-001 to 011), and the group, tenant and workspace design (still open).

## 1. Concepts

- **Shopping list**: a standing notebook of what a person or business wants. Always editable. Holds *requested* items.
- **List order**: one submission of (part of) the wanted items to one provider. This is where the status lifecycle lives (the user's draft statuses new / in-progress / completed / cancelled belong here, not on the list).
- **Procurement batch**: the placer's request to buy items from one or more lists. A planner turns a batch into one or more list orders. The system decides single versus several orders from shipping cost and delivery timelines.
- **Provider**: one concept for store, marketplace and direct vendor (roles, not separate tables). A marketplace (Instacart, DoorDash) fulfils through stores (Kroger), so an order has a *channel provider* and each line a *fulfilled-by provider*. Provider data (locations, cutoff and amendment rules, fees) belongs to the Partner side and is shared; Shopping keeps ids plus a name snapshot.
- **Requested versus sourced**: a list item keeps the request; an order line keeps a snapshot of the request and what was actually supplied, so later reviews can find purchasing mistakes (asked for Vital Farms, got Eggland's Best) and a list can be repeated "as requested" or "as received".

## 2. Tables

Conventions: schema `shopping`; every table has `id` (uuid), `organization_id`, `workspace_id`, `created_at`, `updated_at`; names per cynthus-core engineering standards; `processed_requests` for idempotent writes.

**Phase 1 (lists)**

- `shopping_lists`: `name`, `owner_id` (requester), `requester_notes`, `archived_at`, `deleted_at`, `is_procurement_target` (at most one per workspace), `event_at`, `event_timezone`, `lead_time` (interval), `deliver_to_location_id` (reference to the shared address concept).
- `shopping_list_items`: `list_id`, `name` (free text), `catalog_item_id` and `inventory_item_id` (nullable references; the latter stops a repeated low-stock signal adding a duplicate), `requested_quantity` numeric(12,3), `requested_unit` (code), `notes`, `source` (manual, low_stock, generated, meal_gap), `preferred_provider_id`, `not_before` / `not_after` (resolved timestamps), `not_before_offset` / `not_after_offset` (relative to the list's `event_at`), `position`, `removed_at`.
- `processed_requests`.

**Phase 2 (orders, single destination)**

- `list_orders`: `provider_id` (channel), `status` (draft, proposed, awaiting_approval, submitted, accepted, preparing, in_transit, delivered, partially_fulfilled, cancelled, failed), `provider_order_ref`, `submitted_at`, `amend_until`, `locked_at`, `delivery_window_start/end`, fees (delivery, service, tip), totals.
- `list_order_lines`: request snapshot (name, brand, quantity, unit), sourced product, `sourced_quantity` and `sourced_unit` (may differ, e.g. 2 lb versus 32 oz), `substitution_reason`, `substitution_approved_by`, `fulfilled_by_provider_id`, price, `sourced_at`, `sourced_by`.
- `order_line_sources`: which list items (and how much of each) a line came from; carries the **source** list's own `organization_id` / `workspace_id`.

**Phase 3 (batches, planner, cross-tenant)**

- `procurement_batches` (placer's tenant), `batch_items`, planner `plan_alternatives`, and `shopping_preferences` (see section 5).

## 3. Editing and locking

The list is always editable. Items in a submitted order are frozen by that provider's rule. Each order stores `amend_until` (deadline from the provider's policy) and `locked_at` (provider reported accepted or preparing); whichever comes first wins. Later changes become an amendment request to the provider or stay on the list for the next order.

## 4. Time windows

A commercial list sets `event_at` and a `lead_time`, giving a default "no later than". An item can override with `not_before` and `not_after`, absolute or as an offset from the event (catering example: lunch Friday, supplies no later than Wednesday, cake no earlier than Thursday). A personal list has no window: as soon as possible. Offsets recompute if the event moves, until the order locks. Windows are **hard constraints on grouping**: items whose windows do not overlap cannot share a delivery (supplies and cake become two orders whatever the shipping costs). Cost is optimized inside that.

## 5. Placement, providers and policy

- Astri queries all supported providers (within reason) and suggests alternatives.
- The client's **deny list** of providers is always honored.
- If no provider can meet the order's constraints, the system **asks the client how to proceed**.
- Each client sets an **order placement guideline**: `order_with_approval` (default; always ask first), `best_effort_auto_order` (place the closest plan and flag it), and others to be named (for example auto-order only when every constraint is met, with a spending limit).
- Settings live in `shopping_preferences` (per workspace, optional per-user override): placement mode, deny list, optional spend limit. Open: how the "ask when nothing fits" rule interacts with best-effort mode.

## 6. Tenancy and cost

A planner can place one order from lists in different workspaces and tenants. The batch, orders and lines belong to the planner's tenant and workspace. `order_line_sources` carries the source tenant and workspace so each client sees only their own contribution and their share of costs; the planner sees everything. Reading a client's list needs a grant (group design still open), so items are recorded at batch creation and not re-read. The planner's tenant pays (payment permission, held by no management role by default); fees are stored on the order and allocated to source lists by share of line totals; charging clients back belongs to Billing. Combining orders needs compatible destinations as well as windows.

## 7. Where things live

Lists, batches, orders and sourcing records: Shopping. Provider catalog, rules and quotes: Partner side. Plan selection and alternatives: probably Logistics (PRD names `cynthus-logistics` for purchase manifests and supplier cart sync) with Astri producing suggestions. To decide when the planner is built.

## 8. Effects on the signal catalog

New signals are needed for the order lifecycle (submitted, accepted, amended, delivered, substitution, cancelled), batch creation and plan proposal. Existing `item.checked_off` stays for in-store shopping by the requester. Existing auto-purchase rows (FT-SL-010) overlap with orders and should be reconciled when order signals are defined. Catalog change belongs in cynthus#26's follow-up.

## 9. Open questions

1. Hard deadline not met versus best-effort mode (section 5).
2. Who owns providers and units as shared reference data.
3. End-of-day versus time-of-day deadlines; business versus calendar days for lead time.
4. Fee allocation basis (value versus count).
5. How a client's list is shared to a planner (depends on the paused group and permission design).
6. Names and number of placement guidelines.
