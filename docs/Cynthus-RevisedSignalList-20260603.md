## 1. Open Source Schema (`cynthus-messaging-public`)

### Auth Component

> Architectural Source: `cynthus-auth`
> Governance Scope: Handles session verification boundary lifecycle hooks.

#### `auth.session.invalidated`

* Emitted by: `cynthus-auth` when a user manually logs out, a session times out, or security parameters change.
* Functional Purpose: Instructs `cynthus-api` to immediately flush localized token validation caches.
* Captured Fields:
* `session_id: str` — The unique token tracking signature tracking the active session.
* `invalidation_reason: str` — Explicit metadata categorization (e.g., `user_logout`, `token_expired`, `revoked_by_admin`).

### Device Component

> Architectural Source: `cynthus-worker` (Warm-Path Aggregator) & `cynthus-api` (Edge Ingress)
> Governance Scope: High-frequency wearable telemetry summaries and hardware diagnostics.

#### `device.battery.status`

* Emitted by: `cynthus-api` when an edge tracking integration worker or mobile wrapper streams power metrics.
* Captured Fields:
* `device_id: str` — Hardware MAC address or unique registration token.
* `battery_percent: int` — Direct integer parsing constrained by `ge=0, le=100`.
* `is_charging: bool` — Hardware power circuit state flag.

#### `device.biometric.trend`

* Emitted by: `cynthus-worker` every 15 minutes after calculating an aggregation window over the raw hot-path time-series data block.
* Captured Fields:
* `device_id: str` — The originating physical sensor tracking identifier.
* `user_id: str` — The unique identity of the care recipient wearing the device.
* `metric_stream_type: str` — The streaming telemetry class (e.g., `HeartRate`, `BloodGlucose`, `O2Saturation`).
* `interval_start: datetime` — ISO 8601 start bound of the 15-minute chunk.
* `interval_end: datetime` — ISO 8601 termination bound of the 15-minute chunk.
* `sample_count: int` — Total raw telemetry samples gathered in this slice block (`ge=1`).
* `min_value: float` — Lowest numerical point captured.
* `max_value: float` — Highest numerical point captured.
* `mean_value: float` — Mathematical average over the block window.

#### `device.tracker.breached`

* Emitted by: `cynthus-worker` instantly when incoming telemetry violates a workspace safety threshold boundary.
* Functional Purpose: Triggers instant reactive alarms and push notifications on `cynthus-web`.
* Captured Fields:
* `device_id: str` — The originating hardware device.
* `user_id: str` — The impacted care recipient.
* `trigger_condition: str` — Categorization string (e.g., `BiometricAnomalyDetected`, `EnvironmentalBreach`).
* `observed_value: str` — The specific out-of-bounds reading captured.
* `threshold_severity: str` — Boundary classification enum (`CRITICAL_LOW`, `CRITICAL_HIGH`).
* `requires_immediate_escalation: bool` — Operational routing priority indicator.

### Inventory Component

> Architectural Source: `cynthus-inventory`
> Governance Scope: Tracks resource supply chains, logistics assets, and mutations.

#### `inventory.item.stock`

* Emitted by: `cynthus-inventory` when supply spaces, medical equipment logs, or pantry lockers register weight or transactional changes.
* Captured Fields:
* `inventory_id: str` — The parent inventory master configuration file tracker.
* `pantry_id: str` — The physical or logical site identifier.
* `shelf_id: str` — The specific storage row or zone locker.
* `item_id: str` — Corporate SKU or universal item index.
* `current_quantity: int` — The resulting quantity balance value post-mutation (`ge=0`).
* `mutation_reason: str` — Description cataloging the shift (e.g., `item_replenished`, `item_used`, `shelf_added`).

### Logistics Component

> Architectural Source: `cynthus-worker` (Background Scheduler Loop)
> Governance Scope: B2B commercial fulfillment orders and recipe scale conversions.

#### `logistics.order.wholesale`

* Emitted by: `cynthus-worker` when an automated replenishment engine determines an asset has fallen below minimum stocking parameters.
* Captured Fields:
* `order_id: str` — Unique corporate tracking manifest number.
* `vendor_target_api: str` — Unified identifier indicating which external wholesale partner API receives the order.
* `total_estimated_cost: float` — Computed price footprint tracking parameter.
* `items: list[dict]` — An array of items containing nested sub-properties (`item_id`, `quantity`, `unit_cost`).

### User Component

> Architectural Source: `cynthus-api` (Public Edge Proxy)
> Governance Scope: Non-clinical qualitative logs, behavioral logs, and local workspace entries.

#### `user.sentiment.record`

* Emitted by: `cynthus-api` when a team member logs subjective feedback regarding daily logistics components.
* Captured Fields:
* `user_id: str` — The standard user, caregiver, or recipient identity executing the feedback.
* `action_taken: str` — Direct descriptive tracking verb (e.g., `liked_meal`, `disliked_recipe`, `tagged_provider`).
* `target_entity_id: str` — The identifier tracking what was acted upon.
* `rating_score: float` — Normalized sliding scalar tracking value (`ge=0.0, le=1.0`).

#### `user.energy.record`

* Emitted by: `cynthus-api` when a client contributor self-reports qualitative physiological stamina markers.
* Captured Fields:
* `user_id: str` — The client identifier.
* `energy_level_metric: int` — Numeric capacity evaluation factor (`ge=1, le=5`).
* `energy_level_consequence: str` — Explicit workflow operational override string (e.g., `need_alternative_meal_option`, `delegate_logistics_tasks`).

## 2. Closed Source Schema (`cynthus-messaging-internal`)

### Audit Component

> Architectural Source: `cynthus-portal-api` / `cynthus-auth`
> Governance Scope: HIPAA Title II security controls, operational access tracing, and clinical compliance records.

#### `audit.action.record`

* Emitted by: `cynthus-portal-api` or `cynthus-auth` before transmitting protected health information (PHI) to external B2B partners.
* Captured Fields:
* `audit_log_id: str` — Immutable cryptographic event tracking key.
* `clinician_id: str` — The corporate health partner executing the inspection.
* `target_user_id: str` — The care recipient whose biological telemetry registries were evaluated.
* `accessed_fields: list[str]` — Exact database property layers decrypted and streamed during the query session.
* `consent_token_signature: str` — Base64 payload signature verifying active customer workspace authorization status.

### Chat Component

> Architectural Source: `cynthus-chat`
> Governance Scope: Closed-source dialogue streams, screen-reader linear parsing logs, and AI transparency metadata.

#### `chat.session.state`

* Emitted by: `cynthus-chat` when a conversational chatbot stream initializes, shifts context, or terminates cleanly.
* Captured Fields:
* `chat_id: str` — Unique isolated conversation partition key.
* `user_id: str` — The client executing dialogue questions.
* `session_status: str` — System phase state identifier (`active`, `paused`, `completed_and_compiled`).

#### `chat.session.content`

* Emitted by: `cynthus-chat` upon conversational termination. It compiles dialogues into linear descriptive trees optimized for accessibility compliance checks.
* Captured Fields:
* `chat_id: str` — The session identification tracking signature.
* `user_id: str` — The active client identity.
* `linear_text_summary: str` — Sequential text layout block stripped of complex spatial formatting for clean screen-reader tree parsing.
* `ai_governance_model_hash: str` — Explicit trace fingerprint logging the exact localized LLM configuration utilized (satisfies TRAIGA compliance requirements).

### Lifestyle Component

> Architectural Source: `cynthus-analysis`
> Governance Scope: Closed-source analytical scores, calculations, and automated trend determinations.

#### `lifestyle.harmony.calculation`

* Emitted by: `cynthus-analysis` once every 24 hours to broadcast calculated operational balances across workspace borders.
* Captured Fields:
* `calculation_id: str` — Unique mathematical run transaction record.
* `harmony_score: float` — Normalized calculation value tracking parameter (`ge=0.00, le=1.00`).
* `task_completion_rate: float` — Mathematical ratio tracking standard logistics execution parameters.
* `resource_balance_index: float` — Inventory provisioning matrix weight value.
* `workload_variance: float` — Operational index tracking delegation disparities across workspace members.

#### `lifestyle.sentiment.analysis`

* Emitted by: `cynthus-analysis` when predictive pattern logic flags long-term changes in a workspace user's emotional responses.
* Captured Fields:
* `user_id: str` — The target user tracked.
* `sentiment_pattern_type: str` — Descriptive anomaly tracking label (e.g., `sustained_low_energy`, `meal_engagement_drop`).
* `confidence_score: float` — Algorithmic certainty evaluation parameter (`ge=0.0, le=1.0`).
* `historical_sample_ids: list[str]` — References to the underlying public `user.sentiment.record` signal identifiers that triggered the pattern match.

### System Component

> Architectural Source: `cynthus-auth`
> Governance Scope: High-priority runtime overrides and ephemeral security parameters.

#### `system.authentication.updated`

* Emitted by: `cynthus-auth` immediately upon successful verification of an active enterprise portal session.
* Captured Fields:
* `session_id: str` — The validated operational tracking session key.
* `ephemeral_vault_key: str` — A short-lived, transient user-derived cryptographic key parameter.


* Functional Target: Consumed strictly by private `cynthus-intelligence` components to execute the in-memory handshake required to decrypt clinical records (`vesta_clinical`) without writing plain text keys to persistent disk arrays.

---

### Architectural Design Alignment Note

This complete signal mapping integrates perfectly into your new object hierarchy:

```python
# Validation Execution Example (Under the hood)
# Pydantic cleanly constructs the single-class module like this:

from cynthus.messaging.common.signal_message import SignalMessage
from cynthus.messaging.public.component.device.payloads.battery_status import DeviceBatteryStatusPayload

# Open-source engine handles concrete deep type-safety effortlessly:
type DeviceBatteryStatusSignal = SignalMessage[DeviceBatteryStatusPayload]

```
