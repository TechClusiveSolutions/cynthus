Here is the complete transformation of your events list into the **Entity-Lifecycle (State-Change) Schema Pattern**.

Per your instructions, all original features, payload fields, and business logic have been fully preserved, and the new additions (such as AI, clinical, and audit components) are integrated. Everything now shares a uniform **Message Envelope** structure, clean lowercase-with-dots naming conventions, strict ISO 8601 UTC temporal structures, and cross-service correlation tracking.

---

# Cynthus Unified Lifecycle Events Schema

All events broadcast across the `cynthus-events-topic` share an identical top-level envelope. The `payload` object shifts dynamically based on the target `event_type` and the `lifecycle_action`.

## Global Envelope Template

```json
{
  "event_id": "string (UUIDv4)",
  "event_type": "string (e.g., 'provider.service.created')",
  "lifecycle_action": "string (created | updated | deleted | snapshot)",
  "correlation_id": "string (UUIDv4 Tracking GUID)",
  "timestamp": "string (ISO 8601 UTC: YYYY-MM-DDTHH:MM:SSZ)",
  "household_id": "string (Tenant Isolation Boundary Key)",
  "actor_id": "string (User, Provider, or System Agent ID)",
  "payload": {}
}

```

---

## 1. Partner Domain

### `partner.promotion`

#### partner.promotion.created

Emitted when a partner initializes a promotional offer.

- **Payload:**

```json
{
  "promotion_id": "Promo123",
  "partner_id": "PartnerA"
}

```

#### partner.promotion.deleted

Emitted when a partner terminates an existing promotion.

- **Payload:**

```json
{
  "promotion_id": "Promo123"
}

```

---

## 2. Provider Domain

### `provider.service`

#### provider.service.created

Emitted when a provider adds a new operational capability to their catalog.

- **Payload:**

```json
{
  "provider_id": "Provider1",
  "service_id": "ServiceA"
}

```

#### provider.service.deleted

Emitted when a provider flags a service as permanently unavailable.

- **Payload:**

```json
{
  "service_id": "ServiceA"
}

```

### `provider.service_list`

#### provider.service_list.created

Emitted when a master service list container is created.

- **Payload:**

```json
{
  "provider_id": "Provider1",
  "service_list_id": "ServiceList1"
}

```

#### provider.service_list.updated

Emitted when a service offering is added to or removed from a service list.

- **Payload:**

```json
{
  "service_list_id": "ServiceList1",
  "services": [
    { "offering_id": "Offering1" }
  ],
  "meta": {
    "mutation_reason": "service_added" 
  }
}

```

> *Note: Replacing your historical `ServiceAdded` and `ServiceRemoved` actions, this unified state snapshot tells downstream consumers exactly what offerings live in the list after the atomic transaction.*

#### provider.service_list.deleted

Emitted when a service list configuration is unlinked from the provider profile.

- **Payload:**

```json
{
  "service_list_id": "ServiceList1"
}

```

### `provider.service_location`

#### provider.service_location.created

Emitted when a provider sets up an active operational center or clinic.

- **Payload:**

```json
{
  "provider_id": "Provider1",
  "location_id": "LocNorth"
}

```

---

## 3. System Domain

### `system.authentication`

#### system.authentication.created

Emitted when a user successfully passes credential checks and logs in.

- **Payload:**

```json
{
  "user_id": "User1",
  "session_id": "Sess998"
}

```

#### system.authentication.updated

Emitted when a user successfully processes a secondary cryptographic decryption handshake to access closed-source clinical data domains.

- **Payload:**

```json
{
  "user_id": "User1",
  "handshake_status": "COMPLETED",
  "handshake_timestamp": "2026-06-01T13:20:54Z"
}

```

#### system.authentication.deleted

Emitted when an active profile token explicitly expires or is revoked.

- **Payload:**

```json
{
  "user_id": "User1",
  "session_id": "Sess998",
  "reason": "expired"
}

```

### `system.inventory`

#### system.inventory.updated

Emitted when internal system tasks flag upcoming shelf expirations or generate automated alert payloads.

- **Payload:**

```json
{
  "inventory_id": "Inventory1",
  "shelf_id": "Shelf1",
  "item_id": "item1",
  "alert_type": "ItemExpirationNotificationCreated",
  "expires_on": "2026-06-01T00:00:00Z"
}

```

### `system.runtime`

#### system.runtime.updated

Emitted when core edge processing layers cross internal lifecycle initialization steps.

- **Payload:**

```json
{
  "system_id": "System1",
  "current_state": "STARTUP_COMPLETED",
  "previous_state": "STARTUP_INITIATED",
  "reason": "maintenance_window_closed"
}

```

> *Note: This simplifies `system.shutdown.initiated`, `system.startup.initiated`, and `system.startup.completed` into a standard machine-state progression tracking layout.*

---

## 4. User Domain

### `user.group`

#### user.group.created

Emitted when a secure household tenant container is generated.

- **Payload:**

```json
{
  "group_id": "Group1",
  "is_family": true,
  "is_primary": true,
  "created_on": "2026-06-01T08:00:00Z"
}

```

#### user.group.updated

Emitted when adding or removing members from a household boundary without altering underlying tenant data rules.

- **Payload:**

```json
{
  "group_id": "Group1",
  "members": [
    { "member_id": "User1", "role": "Primary Caregiver" },
    { "member_id": "User2", "role": "Care Recipient" }
  ],
  "meta": {
    "mutation_reason": "member_added",
    "target_member_id": "User2"
  }
}

```

#### user.group.deleted

Emitted when a user terminates a household group context.

- **Payload:**

```json
{
  "group_id": "Group1"
}

```

### `user.inventory`

#### user.inventory.created

Emitted when a user initializes a physical tracking tracking workspace.

- **Payload:**

```json
{
  "inventory_id": "Inventory1",
  "created_on": "2026-06-01T08:00:00Z"
}

```

#### user.inventory.updated

Emitted when items are used, replenished, or otherwise manipulated within an active tracking context.

- **Payload:**

```json
{
  "inventory_id": "Inventory1",
  "shelf_id": "Shelf1",
  "item_id": "Item1",
  "current_quantity": 4,
  "expires_on": "2026-12-15T00:00:00Z",
  "meta": {
    "mutation_reason": "item_replenished" 
  }
}

```

> Note: Consolidates `ItemReplenished`, `ItemUsed`, `ShelfAdded`, and `ItemAdded` into state updates, simplifying the tasks processed by `cynthus-worker`.
>
>

#### user.inventory.deleted

Emitted when an entire inventory configuration is dropped.

- **Payload:**

```json
{
  "inventory_id": "Inventory1"
}

```

### `user.library`

#### user.library.created

Emitted when a profile generates a collection registry space.

- **Payload:**

```json
{
  "library_id": "Library1",
  "created_on": "2026-06-01T08:00:00Z"
}

```

#### user.library.updated

Emitted when content indexes or attached recipes are added or removed.

- **Payload:**

```json
{
  "library_id": "Library1",
  "recipes": [
    { "recipe_id": "Recipe1" }
  ],
  "meta": {
    "mutation_reason": "recipe_added"
  }
}

```

#### user.library.deleted

Emitted when a library container asset is scrubbed.

- **Payload:**

```json
{
  "library_id": "Library1"
}

```

### `user.meal`

#### user.meal.created

Emitted when a user configures a target recipe execution target.

- **Payload:**

```json
{
  "meal_id": "Meal1",
  "created_on": "2026-06-01T08:00:00Z"
}

```

#### user.meal.updated

Emitted when a user modifies tags, updates preferences, or toggles selection states.

- **Payload:**

```json
{
  "meal_id": "Meal1",
  "is_favorite": true,
  "tags": ["Tag1"],
  "meta": {
    "mutation_reason": "favorite_added"
  }
}

```

> *Note: Replaces four granular events (`FavoriteAdded`, `FavoriteRemoved`, `TagAdded`, `TagRemoved`) with a unified meal metadata configuration layer.*

#### user.meal.deleted

Emitted when a user drops a planned meal option.

- **Payload:**

```json
{
  "meal_id": "Meal1"
}

```

### `user.recipe`

#### user.recipe.created

Emitted when a recipe data array is loaded into the user system.

- **Payload:**

```json
{
  "recipe_id": "Recipe1",
  "name": "Almond Flour Pancakes"
}

```

#### user.recipe.updated

Emitted when ingredients, allergen declarations, or instructional guides are altered.

- **Payload:**

```json
{
  "recipe_id": "Recipe1",
  "allergens": ["nuts"]
}

```

#### user.recipe.deleted

Emitted when a user removes a custom recipe blueprint from their records.

- **Payload:**

```json
{
  "recipe_id": "Recipe1"
}

```

### `user.schedule`

#### user.schedule.created

Emitted when a household tracking calendar framework is established.

- **Payload:**

```json
{
  "schedule_id": "Sched556"
}

```

#### user.schedule.updated

Emitted when scheduled windows accept alternative meal variants, re-arrange cooking slots, or resolve calendar contentions.

- **Payload:**

```json
{
  "schedule_id": "Sched556",
  "scheduled_meals": [
    { "meal_id": "Meal1", "target_date": "2026-06-02" }
  ],
  "meta": {
    "mutation_reason": "meal_added"
  }
}

```

---

## 5. Clinical Domain

### `clinical.signal`

#### clinical.signal.created

Emitted when a raw data point is ingested via an active external webhook or localized Bluetooth proxy node.

- **Payload:**

```json
{
  "signal_id": "Sig9988",
  "metric_type": "BloodPressure",
  "raw_value": "135/85"
}

```

---

## 6. Interactive Domain

### `interactive.chat`

#### interactive.chat.updated

Emitted when Astri registers a dynamic configuration mutation, such as when user targets accept a meal selection change or trigger localized resolution protocols.

- **Payload:**

```json
{
  "interaction_id": "Int7732",
  "current_state": "SUGGESTION_ACCEPTED",
  "context_domain": "meal.suggestion",
  "entity_id": "Recipe1"
}

```

---

## 7. Audit Domain

### `audit.portal`

#### audit.portal.created

Emitted as a permanent, read-only event footprint confirming whenever B2B partners access clinical data views via secure access checkpoints.

- **Payload:**

```json
{
  "audit_log_id": "Aud7711",
  "clinician_id": "DrSmith",
  "target_user_id": "User2",
  "accessed_fields": ["BloodGlucose", "BloodPressure"],
  "consent_token_signature": "sig_v1_88eeffaa332211bb"
}

```

---

## 8. Analytics Domain

### `analytics.household`

#### analytics.household.updated

Emitted when automated intelligence passes complete calculations back down to the worker stream, such as calculating biometric anomalies or the household's current harmony index.

- **Payload:**

```json
{
  "metric_calculated": "harmony_score",
  "score_value": 82,
  "anomalies_found": false,
  "factors": {
    "task_completion_rate": 0.91,
    "workload_variance": 0.12
  }
}

```

### Summary of Improvements

- **Topic Count Safety:** Reduced your planned baseline topics from **38 separate event names down to 17 standard lifecycle paths**, avoiding potential maintenance challenges on Azure Service Bus.

- **Astri AI Processing:** The conversational and predictive systems (`cynthus-chat` / `cynthus-analysis`) can now process the complete state of an entity directly from the event payload, reducing the need to request full records back from the databases via API.

Rule 2: Would you like to write a set of Pydantic model configurations that match this unified lifecycle state layout next?
