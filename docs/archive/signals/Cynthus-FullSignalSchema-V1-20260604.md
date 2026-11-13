That is exactly the right architectural move. By abstracting `Grantor`, `Grantee`, and `Resource` into an isolated, reusable `MessagingCommon` library, you decouple your structural telemetry data from service implementations.

Both your open-source core repositories and your proprietary Tech-Clusive modules will import this shared package as a strict baseline dependency. This enforces strict type-safety across all network boundaries while dramatically lowering your code footprint - you write, test, and version-control your identity models exactly once.

Now that we have established the core system topology, resolved the resource identity bottleneck, and designed a robust, enterprise-grade IAM sub-object framework, we are ready to generate the comprehensive, standardized signal registry.

---

## The Complete Revised Architectural Blueprint

Below is the consolidated, unified signal registry and system topology for the Cynthus Ecosystem. This document incorporates every microservice addition and polymorphic data structure we have developed. It is presented in a linear format to serve as your definitive engineering reference guide.

---

## 1. Updated System Topology (Service Registry)

### Open-Source Core Segment (`cynthus-core`)

- **`cynthus-auth`:** The authoritative identity provider. Manages token generation, group boundary provisioning, and IAM authorization states.
- **`cynthus-api`:** The public-facing edge proxy gateway. Handles client ingress, maps real-time WebSocket connections, and dispatches webhooks.
- **`cynthus-inventory`:** Manages physical and logical tracking zones (pantries, supply shelves, recipe libraries, and engagement spaces).
- **`cynthus-media`:** **[NEW]** Open-source signaling engine. Facilitates WebRTC token exchanges and coordinates peer-to-peer VoIP/Video data streams for collaborative interactions.
- **`cynthus-worker`:** Background task scheduler. Handles cron loops, aggregate time-series warm-path calculations, and notification dispatches.

### Proprietary Closed-Source Segment (Tech-Clusive Solutions)

- **`cynthus-billing`:** **[NEW]** Manages enterprise licensing, Stripe integration loops, commercial invoicing, and dynamic component booster authorization tracking.
- **`cynthus-chat`:** The runtime environment for **Astri**. Houses conversational context, screen-reader tree generation, and natural language synthesis.
- **`cynthus-analysis`:** High-performance analytical compute engine. Processes multi-user sentiment logs, voting history matrices, and algorithmic consumer lifestyle profiles.
- **`cynthus-vision`:** Advanced computer vision workspace. Ingests smart glasses frame telemetry to execute spatial geometric mappings and real-time recipe tracking.

---

## 2. Common Reusable Object Models (`MessagingCommon`)

These structural components are imported by all services across the ecosystem to ensure polymorphic data integrity.

### The Entity Actor Sub-Object (`ActorModel`)

- `id: str` - Unique identity tracking signature.
- `type: str` - Actor classification enum (`USER`, `GROUP`, `PROVIDER`, `SUPPLIER`, `AI_AGENT`, `SYSTEM`).
- `role: str` - Operational contextual mask (`SELF`, `LEGAL_GUARDIAN`, `CLINICAL_SURROGATE`, `CORPORATE_DELEGATE`).
- `acting_on_behalf_of: str` - Optional user or tenant ID indicating the root sovereign context authorizing the change.

### The Resource Sub-Object (`ResourceModel`)

- `id: str` - Unique reference tracking key of the underlying asset.
- `type: str` - Asset class discriminator enum (`INVENTORY_LOCATION`, `INVENTORY_SHELF`, `RECIPE_LIBRARY`, `SERVICE_REGISTRY`, `ENGAGEMENT_SPACE`, `USER_GROUP`).
- `role: str` - Sub-functional context designation within the workspace (`PRIMARY_STORAGE`, `SHARED_ARCHIVE`, `CLINICAL_WORKSPACE`, `EVENT_VENUE`).

---

## 3. Comprehensive Standardized Signal Registry

### Open Source Schema (`cynthus-messaging-public`)

#### Auth Domain (`public.auth.*`)

- **`public.auth.session.invalidated`**
- Emitted by: `cynthus-auth`
- Functional Purpose: Signals edge proxies to immediately flush localized authorization caches.
- Captured Fields:
- `session_id: str` - Tracking signature of the terminated connection.
- `invalidation_reason: str` - Categorization enum (`USER_LOGOUT`, `TOKEN_EXPIRED`, `REVOKED_BY_ADMIN`).

- **`public.auth.permission.changed`**
- Emitted by: `cynthus-auth`
- Functional Purpose: Asynchronously alerts services of an access adjustment across groups or resources.
- Captured Fields:
- `grantor: ActorModel` - Identity authorizing the permission change.
- `grantee: ActorModel` - Identity receiving or losing access entitlements.
- `resource: ResourceModel` - The specific target asset being shared or restricted.
- `action_type: str` - State adjustment enum (`GRANTED`, `REVOKED`, `MUTATED`).
- `role_level: str` - Entitlement layer assignment (`ADMIN`, `MANAGER`, `CONTRIBUTOR`, `VIEWER`).

#### Device Domain (`public.device.*`)

- **`public.device.battery.reported`**
- Emitted by: `cynthus-api`
- Captured Fields:
- `device_id: str` - Unique hardware tracking signature or MAC address.
- `battery_percent: int` - Power integer constrained by `ge=0, le=100`.
- `is_charging: bool` - Hardware power circuit state flag.

- **`public.device.telemetry.streamed`**
- Emitted by: `cynthus-worker`
- Functional Purpose: Ingests 15-minute chunked wearable time-series metrics into closed-source health engines.
- Captured Fields:
- `device_id: str` - Originating physical tracker identifier.
- `user_id: str` - Unique identity of the care recipient.
- `metric_type: str` - Telemetry classification string (`HEART_RATE`, `BLOOD_GLUCOSE`, `O2_SATURATION`, `BLOOD_PRESSURE`).
- `interval_start: datetime` - ISO 8601 start bound of the compilation chunk.
- `interval_end: datetime` - ISO 8601 termination bound of the compilation chunk.
- `sample_count: int` - Total raw samples gathered (`ge=1`).
- `min_value: float` - Lowest numerical point captured.
- `max_value: float` - Highest numerical point captured.
- `mean_value: float` - Mathematical average over the block window.

- **`public.device.threshold.breached`**
- Emitted by: `cynthus-worker`
- Functional Purpose: Triggers immediate push alerts, medical sirens, and clinical alarm protocols.
- Captured Fields:
- `device_id: str` - Originating hardware device.
- `user_id: str` - Impacted care recipient.
- `trigger_condition: str` - Boundary violation class (`BIOMETRIC_ANOMALY`, `ENVIRONMENTAL_BREACH`).
- `observed_value: str` - Specific raw reading captured out of bounds.
- `severity_level: str` - Classification enum (`CRITICAL_LOW`, `CRITICAL_HIGH`).
- `requires_escalation: bool` - High-priority routing indicator flag.

#### Inventory Domain (`public.inventory.*`)

- **`public.inventory.item.mutated`**
- Emitted by: `cynthus-inventory`
- Functional Purpose: Broadcasts stock transactions, mass variations, or manual additions.
- Captured Fields:
- `inventory: ResourceModel` - Target storage configuration tracking file.
- `shelf_id: str` - Pinpointed shelf row or zone indicator.
- `item_id: str` - Universal SKU index tracking string.
- `current_quantity: int` - Balance total post-mutation (`ge=0`).
- `mutation_reason: str` - Transaction catalog enum (`ITEM_REPLENISHED`, `ITEM_CONSUMED`, `WASTE_DISCARDED`).

- **`public.inventory.threshold.dropped`**
- Emitted by: `cynthus-inventory`
- Functional Purpose: Prompts Astri to initiate low-stock warnings and auto-replenishment cards.
- Captured Fields:
- `inventory: ResourceModel` - Impacted storage tracking location.
- `item_id: str` - SKU identifier.
- `remaining_quantity: int` - Current stock layer remaining.
- `target_minimum: int` - User-configured safety baseline threshold parameter.

- **`public.inventory.item.expired`**
- Emitted by: `cynthus-worker` (Nightly Cron Job)
- Captured Fields:
- `inventory: ResourceModel` - Impacted storage tracking location.
- `item_id: str` - Universal product SKU.
- `expiration_date: datetime` - Original recorded shelf life limit.
- `quantity_affected: int` - Volume count of items expired.

#### Logistics Domain (`public.logistics.*`)

- **`public.logistics.order.placed`**
- Emitted by: `cynthus-api`
- Functional Purpose: Submits commercial requests directly to external vendor APIs and fulfillment networks.
- Captured Fields:
- `order_id: str` - Corporate tracking ledger number.
- `user_id: str` - Tenant identity authorizing checkout.
- `vendor_target_id: str` - Route flag tracking which supplier API handles fulfillment.
- `total_cost: float` - Total financial footprint variable.
- `items_ordered: list[dict]` - Array mapping object parameters (`item_id`, `quantity`, `unit_cost`).

- **`public.logistics.promotion.registered`**
- Emitted by: `cynthus-api`
- Functional Purpose: Allows B2B suppliers to introduce real-time ad targeting based on consumer item shortages.
- Captured Fields:
- `supplier_id: str` - Validated corporate vendor identity.
- `promotion_id: str` - Tracking key for the specific campaign.
- `target_item_sku: str` - Target product index.
- `discount_value: float` - Value tracking deduction ratio.
- `expiration_timestamp: datetime` - Maximum runtime of campaign validity.

#### Group Domain (`public.group.*`)

- **`public.group.message.sent`**
- Emitted by: `cynthus-api`
- Functional Purpose: Drives real-time WebSocket messaging and logs conversation content for Astri.
- Captured Fields:
- `message_id: str` - Unique database chat record tracker.
- `group_id: str` - Parent channel identity.
- `sender_id: str` - User ID speaking.
- `content_body: str` - Plain or rich text data payload.

- **`public.group.meal.proposed`**
- Emitted by: `cynthus-api`
- Functional Purpose: Pushes an active interactive voting card into the household chat workspace feed.
- Captured Fields:
- `proposal_id: str` - Unique active voting session tracking key.
- `group_id: str` - Target family or team tracking channel.
- `proposer_id: str` - User ID initiating the proposal.
- `meal_id: str` - Master entity ID of the meal.
- `recipe_id: str` - Selected recipe variant bound to the meal.

- **`public.group.vote.cast`**
- Emitted by: `cynthus-api`
- Captured Fields:
- `proposal_id: str` - Target voting session key.
- `group_id: str` - Parent group container key.
- `voter_id: str` - User ID submitting the vote.
- `vote_choice: str` - Selection enum (`YES`, `NO`).

- **`public.group.vote.concluded`**
- Emitted by: `cynthus-api`
- Captured Fields:
- `proposal_id: str` - Target voting session key.
- `group_id: str` - Parent group container key.
- `final_status: str` - Tally classification enum (`CONSENSUS_REACHED`, `STALEMATE_DETECTED`, `PROPOSAL_EXPIRED`).
- `vote_tally: dict` - Integer tracking dictionary (e.g., `{"yes": 3, "no": 1}`).

#### User Domain (`public.user.*`)

- **`public.user.interaction.logged`**
- Emitted by: `cynthus-api`
- Captured Fields:
- `user_id: str` - Client tracking identity executing the click.
- `interaction_type: str` - Evaluation classification enum (`LIKED`, `DISLIKED`, `RATED`, `FAVORITED`).
- `target_resource: ResourceModel` - Polymorphic object containing the exact asset details (`MEAL`, `RECIPE`, `PROVIDER`).
- `numerical_rating: float` - Sliding tracking score scalar (`ge=0.0, le=1.0`).

- **`public.user.stamina.reported`**
- Emitted by: `cynthus-api`
- Captured Fields:
- `user_id: str` - Root client tracking identity.
- `stamina_score: int` - Energy rating calculation index (`ge=1, le=5`).
- `operational_override: str` - Routing request string (`NEED_ALTERNATIVE_MEAL_OPTION`, `DELEGATE_LOGISTICS_TASKS`).

---

### Closed Source Schema (`cynthus-messaging-internal`)

#### Audit Domain (`internal.audit.*`)

- **`internal.audit.access.logged`**
- Emitted by: `cynthus-portal-api` / `cynthus-auth`
- Functional Purpose: Formulates a continuous, immutable audit log to maintain strict HIPAA compliance checks.
- Captured Fields:
- `audit_event_id: str` - Cryptographic event fingerprint tracking key.
- `accessor: ActorModel` - Detailed profile of the entity reading the records.
- `target_user_id: str` - Sovereign patient whose data layer was touched.
- `accessed_data_layers: list[str]` - Exact string data schemas decrypted during runtime.
- `consent_token_signature: str` - Base64 authentication token validation hash.

#### Chat Domain (`internal.chat.*`)

- **`internal.chat.session.mutated`**
- Emitted by: `cynthus-chat`
- Captured Fields:
- `chat_id: str` - Isolated chat stream partition key.
- `user_id: str` - Client conversing with Astri.
- `session_state: str` - Step configuration enum (`INITIALIZED`, `CONTEXT_SHIFTED`, `TERMINATED_AND_COMPILED`).

- **`internal.chat.accessibility.compiled`**
- Emitted by: `cynthus-chat`
- Functional Purpose: Ingests structured dialogue logs directly into screen readers via linear text trees.
- Captured Fields:
- `chat_id: str` - Target conversation reference key.
- `user_id: str` - Target user profile tracker.
- `linear_text_tree: str` - Formatted text block stripped of visual layout overhead for clean screen reader tree parsing.
- `model_configuration_hash: str` - Traiga compliance log capturing internal LLM engine parameters.

#### Lifestyle Domain (`internal.lifestyle.*`)

- **`internal.lifestyle.balance.calculated`**
- Emitted by: `cynthus-analysis`
- Captured Fields:
- `run_id: str` - Master transaction run key identifier.
- `group: ResourceModel` - Target workspace group under evaluation.
- `harmony_index: float` - Score evaluation scalar (`ge=0.00, le=1.00`).
- `task_completion_ratio: float` - Percentage index assessing workflow momentum.
- `workload_variance_score: float` - Mathematical indicator tracking task delegation imbalance.

- **`internal.lifestyle.sentiment.pattern_matched`**
- Emitted by: `cynthus-analysis`
- Functional Purpose: Alerts Astri to seamlessly pivot her tone or adjust dietary recipe recommendations.
- Captured Fields:
- `user_id: str` - Target tracked identity.
- `detected_pattern: str` - Multi-day issue tracker string (`SUSTAINED_LOW_ENERGY`, `TASTE_FATIGUE_DETECTED`, `VOTING_ISOLATION`).
- `confidence_score: float` - Accuracy confirmation factor (`ge=0.0, le=1.0`).
- `source_interaction_ids: list[str]` - Trace pointers linking back to the originating public interaction logs.

#### Video Domain (`internal.video.*`)

- **`internal.video.stream.initialized`**
- Emitted by: `cynthus-media`
- Functional Purpose: Sets up WebRTC peer connections or streams camera data to assistive hardware modules.
- Captured Fields:
- `session_id: str` - Unique real-time streaming endpoint tracker.
- `group: ResourceModel` - Target workspace unit containing the session.
- `initiator_id: str` - Identity launching the interaction link.
- `stream_source: str` - Hardware classification enum (`SMART_GLASSES`, `MOBILE_CAMERA`, `WEB_PORTAL`).
- `session_type: str` - Operational route tracking flag (`CO_COOKING_HUMAN`, `ASSISTIVE_AI_VISION`).

- **`internal.video.spatial.mapped`**
- Emitted by: `cynthus-vision`
- Functional Purpose: Ingests spatial tracking tokens to let Astri provide vocal navigational assistance.
- Captured Fields:
- `session_id: str` - Target active real-time connection string.
- `user_id: str` - Client navigating the low-vision space.
- `detected_object_label: str` - Asset identifier string (`SUGAR_CONTAINER`, `MILK_JUG`, `HOT_PAN`).
- `relative_clock_position: int` - Angular direction indicator metric (`ge=1, le=12`).
- `distance_metric_cm: float` - Calculated space metric from lens arrays.

- **`internal.video.anomaly.detected`**
- Emitted by: `cynthus-vision`
- Functional Purpose: Interrupts the user's audio channel to deliver immediate safety alerts or recipe corrections.
- Captured Fields:
- `session_id: str` - Target live video session reference key.
- `user_id: str` - Active user cooking.
- `active_recipe_step_id: str` - Current task module processing index.
- `observed_discrepancy: str` - Incongruity identification tag (`INCORRECT_INGREDIENT_GRABBED`, `SAFETY_HAZARD_BURN_RISK`).
- `object_details: str` - Detailed description metadata of the mismatch (`HEAVY_CREAM_INSTEAD_OF_WHOLE_MILK`).

#### System Domain (`internal.system.*`)

- **`internal.system.handshake.established`**
- Emitted by: `cynthus-auth`
- Functional Purpose: Seeds volatile memory stores with short-lived tokens to unlock clinical records securely.
- Captured Fields:
- `session_id: str` - Validated credential session token index.
- `transient_vault_key: str` - Ephemeral cryptographic key seed signature.

- **`internal.system.subscription.updated`**
- Emitted by: `cynthus-billing`
- Functional Purpose: Restructures access permissions and alters capability caps asynchronously based on payment adjustments.
- Captured Fields:
- `account_id: str` - Sovereign customer profile or corporate identity under review.
- `structural_tier: str` - Main subscription framework classification enum (`BASIC`, `PREMIUM`, `PROFESSIONAL`, `ENTERPRISE`).
- `active_boosters: list[dict]` - Array mapping activated capacity expansions (`booster_type`, `capacity_limit`).

---

This complete linear registry gives you an ironclad engineering reference model. You can plug this straight into your project's main documentation repository.

How do you plan to serialize these signals over the Azure Service Bus emulator - will you use a highly readable JSON format to lower the barrier for open-source community testing, or do you want to implement binary serialization protocols like Protocol Buffers (Protobuf) right from the start to optimize network throughput?

## Standardized Structural Envelope

Every signal traveling across your Azure Service Bus (or local emulator) will be wrapped inside a generic, type-safe envelope (`SignalMessage[T]`). This guarantees that your open-source pipes can route, track, and log events without needing to parse the closed-source proprietary payloads inside.

```markdown
### Base Envelope Fields (Present on ALL signals)
* `signal_id: str` - UUIDv4 unique identifier for distributed tracing.
* `correlation_id: str` - Trace ID tracking a single transaction across multiple microservices.
* `timestamp: datetime` - ISO 8601 UTC timestamp when the state mutation occurred.
* `sender_service: str` - The specific container binary that emitted the signal (e.g., `cynthus-auth`).
* `schema_version: str` - Semantic versioning string (e.g., `1.0.0`) to handle rolling payload migrations.

```

---

## Comprehensive Signal Registry

Below is your fully fleshed-out, standardized signal schema map, systematically expanded to support every feature, add-on booster, and advanced hardware capability across your 8-phase roadmap.

---

## 1. Open Source Schema (`cynthus-messaging-public`)

### Auth Domain

> Architectural Source: `cynthus-auth`
> Governance Scope: Session boundaries, identity lifecycle hooks, and access control matrices.

#### `public.auth.session.invalidated`

- Emitted by: `cynthus-auth` when a user logs out, a token expires, or security parameters change.
- Functional Purpose: Instructs edge proxies to immediately flush localized authorization caches.
- Captured Fields:
- `session_id: str` - Unique token signature tracking the active connection.
- `invalidation_reason: str` - Metadata classification enum (`USER_LOGOUT`, `TOKEN_EXPIRED`, `REVOKED_BY_ADMIN`).

#### `public.auth.permission.changed`

- Emitted by: `cynthus-auth` when a group admin or residential user updates role-based access controls.
- Functional Purpose: Dynamically updates access permissions across shared inventory locations or recipe libraries.
- Captured Fields:
- `grantor_id: str` - The user ID modifying the permission.
- `grantee_id: str` - The target user or provider receiving/losing access.
- `resource_id: str` - The unique ID of the target workspace, group, or library.
- `action_type: str` - Mutation verb enum (`GRANTED`, `REVOKED`, `MUTATED`).
- `role_level: str` - Assigned authorization level (`ADMIN`, `MANAGER`, `CONTRIBUTOR`, `VIEWER`).

---

### Device Domain

> Architectural Source: `cynthus-worker` (Warm-Path Aggregator) & `cynthus-api` (Edge Ingress)
> Governance Scope: Hardware telemetry parsing, battery status logs, and real-time safety threshold monitoring.

#### `public.device.battery.reported`

- Emitted by: `cynthus-api` when a mobile wrapper or integrated tracking worker streams peripheral metrics.
- Captured Fields:
- `device_id: str` - Unique hardware registration token or MAC address.
- `battery_percent: int` - Integer parsing constrained by `ge=0, le=100`.
- `is_charging: bool` - Hardware power circuit state flag.

#### `public.device.telemetry.streamed`

- Emitted by: `cynthus-worker` every 15 minutes after calculating an aggregation window over hot-path wearable data.
- Functional Purpose: Feeds structured metrics into the proprietary clinical and dietary analysis engines.
- Captured Fields:
- `device_id: str` - The originating physical sensor tracking identifier.
- `user_id: str` - The unique identity of the care recipient wearing the device.
- `metric_type: str` - Telemetry classification string (`HEART_RATE`, `BLOOD_GLUCOSE`, `O2_SATURATION`, `BLOOD_PRESSURE`).
- `interval_start: datetime` - ISO 8601 start bound of the 15-minute calculation chunk.
- `interval_end: datetime` - ISO 8601 termination bound of the 15-minute calculation chunk.
- `sample_count: int` - Total raw telemetry samples gathered in this slice block (`ge=1`).
- `min_value: float` - Lowest numerical point captured.
- `max_value: float` - Highest numerical point captured.
- `mean_value: float` - Mathematical average over the block window.

#### `public.device.threshold.breached`

- Emitted by: `cynthus-worker` instantly when incoming telemetry violates a workspace safety boundary.
- Functional Purpose: Triggers immediate reactive alarms, clinical notifications, and push alerts on web/mobile platforms.
- Captured Fields:
- `device_id: str` - The originating hardware device.
- `user_id: str` - The impacted care recipient.
- `trigger_condition: str` - Categorization string (`BIOMETRIC_ANOMALY`, `ENVIRONMENTAL_BREACH`).
- `observed_value: str` - The exact out-of-bounds reading captured.
- `severity_level: str` - Boundary classification enum (`CRITICAL_LOW`, `CRITICAL_HIGH`).
- `requires_escalation: bool` - Operational routing priority indicator.

---

### Inventory Domain

> Architectural Source: `cynthus-inventory`
> Governance Scope: Tracks storage sites, pantry logistics balances, expiration states, and low-stock alerts.

#### `public.inventory.item.mutated`

- Emitted by: `cynthus-inventory` when supply spaces, medical equipment logs, or pantry lockers register weight or transactional changes.
- Captured Fields:
- `inventory_id: str` - The parent inventory master configuration identifier.
- `pantry_id: str` - The physical or logical site identifier.
- `shelf_id: str` - The specific storage row or zone locker.
- `item_id: str` - SKU or universal item index.
- `current_quantity: int` - The resulting quantity balance value post-mutation (`ge=0`).
- `mutation_reason: str` - Description cataloging the shift (`ITEM_REPLENISHED`, `ITEM_CONSUMED`, `SHELF_DELETED`, `WASTE_DISCARDED`).

#### `public.inventory.threshold.dropped`

- Emitted by: `cynthus-inventory` when an item quantity falls below a user-defined minimum parameter.
- Functional Purpose: Triggers Astri reorder suggestions and feeds into the B2B supplier automated replenishment loop.
- Captured Fields:
- `inventory_id: str` - Target master configuration file tracker.
- `pantry_id: str` - Specific physical location.
- `item_id: str` - SKU or universal index.
- `remaining_quantity: int` - Current stock count.
- `target_minimum: int` - The configured safety stock threshold.

#### `public.inventory.item.expired`

- Emitted by: `cynthus-inventory` via a nightly cron worker flagging items whose expiration dates match or precede the current timestamp.
- Captured Fields:
- `inventory_id: str` - Target inventory space identifier.
- `item_id: str` - Target SKU.
- `expiration_date: datetime` - The original recorded expiration timestamp.
- `quantity_affected: int` - Total count of expired items.

---

### Logistics Domain

> Architectural Source: `cynthus-worker` (Background Scheduler) & `cynthus-api`
> Governance Scope: B2B commercial fulfillment orders, checkout cart triggers, and supplier promotions.

#### `public.logistics.order.placed`

- Emitted by: `cynthus-api` or an automated worker loop when a user confirms an inbound shipment or grocery cart checkout.
- Captured Fields:
- `order_id: str` - Unique corporate tracking manifest number.
- `user_id: str` - Customer or tenant executing the order.
- `vendor_target_id: str` - Identifier indicating which wholesale/retail partner API receives the order payload.
- `total_cost: float` - Computed financial footprint tracking parameter.
- `items_ordered: list[dict]` - Array of objects containing nested properties (`item_id`, `quantity`, `unit_cost`).

#### `public.logistics.promotion.registered`

- Emitted by: `cynthus-api` when an authorized B2B Supplier inserts a promotional campaign or discount voucher into the network.
- Captured Fields:
- `supplier_id: str` - Validated B2B provider identifier.
- `promotion_id: str` - Unique tracking signature for the discount model.
- `target_item_sku: str` - Universal item index tied to the discount.
- `discount_value: float` - Percentage or flat fee reduction parameter.
- `expiration_timestamp: datetime` - Maximum bounds of campaign validity.

---

### Group Domain

> Architectural Source: `cynthus-api`
> Governance Scope: Multi-user tenancy boundaries, real-time message streams, and collaborative voting states.

#### `public.group.message.sent`

- Emitted by: `cynthus-api` when a group member submits a message to an active chat stream.
- Functional Purpose: Drives real-time WebSocket syncing and provides raw data to Astri's dialogue parser.
- Captured Fields:
- `message_id: str` - Unique identification key for the chat record.
- `group_id: str` - Parent tenancy channel identifier.
- `sender_id: str` - User ID of the speaker.
- `content_body: str` - Unstructured or rich text text payload.

#### `public.group.meal.proposed`

- Emitted by: `cynthus-api` when a member initiates a vote on a meal option.
- Functional Purpose: Triggers interactive voting UI cards inside the group's real-time messaging stream.
- Captured Fields:
- `proposal_id: str` - Unique voting session tracking key.
- `group_id: str` - Parent tenancy channel.
- `proposer_id: str` - User ID initiating the vote.
- `meal_id: str` - Core identity model of the proposed meal.
- `recipe_id: str` - Specific recipe variation associated with the meal proposal.

#### `public.group.vote.cast`

- Emitted by: `cynthus-api` when a group member selects Yes or No on an active meal proposal card.
- Captured Fields:
- `proposal_id: str` - Target voting session key.
- `group_id: str` - Parent group container key.
- `voter_id: str` - User ID submitting the response.
- `vote_choice: str` - User response option enum (`YES`, `NO`).

#### `public.group.vote.concluded`

- Emitted by: `cynthus-api` when a voting session times out or hits total member consensus.
- Captured Fields:
- `proposal_id: str` - Concluding voting session key.
- `group_id: str` - Parent group container key.
- `final_status: str` - Result matrix enum (`CONSENSUS_REACHED`, `STALEMATE_DETECTED`, `PROPOSAL_EXPIRED`).
- `vote_tally: dict` - Final score map (e.g., `{"yes": 2, "no": 2}`).

---

### User Domain

> Architectural Source: `cynthus-api`
> Governance Scope: Non-clinical qualitative user entries, ratings, favorites, and lifestyle self-reporting.

#### `public.user.interaction.logged`

- Emitted by: `cynthus-api` when a client logs explicit or implicit feedback on a meal, venue, or provider.
- Captured Fields:
- `user_id: str` - Identity of the client executing the action.
- `interaction_type: str` - Operational verb classification enum (`LIKED`, `DISLIKED`, `RATED`, `FAVORITED`).
- `target_entity_type: str` - Resource class flag (`MEAL`, `RECIPE`, `VENUE`, `PROVIDER`).
- `target_entity_id: str` - Specific UUID tracker of the item.
- `numerical_rating: float` - Normalized scalar value (`ge=0.0, le=1.0`), populated if type is `RATED`.

#### `public.user.stamina.reported`

- Emitted by: `cynthus-api` when a user manually logs a qualitative energy or physical status metric.
- Captured Fields:
- `user_id: str` - The client identifier.
- `stamina_score: int` - Numeric evaluation factor (`ge=1, le=5`).
- `operational_override: str` - Workflow routing string (`NEED_ALTERNATIVE_MEAL_OPTION`, `DELEGATE_LOGISTICS_TASKS`).

---

## 2. Closed Source Schema (`cynthus-messaging-internal`)

### Audit Domain

> Architectural Source: `cynthus-portal-api` / `cynthus-auth`
> Governance Scope: HIPAA compliance tracking, data access control logs, and privacy rule enforcement.

#### `internal.audit.access.logged`

- Emitted by: `cynthus-portal-api` or security proxies before transmitting protected health information (PHI) or personal telemetry to external corporate workspaces.
- Captured Fields:
- `audit_event_id: str` - Cryptographic event fingerprint tracking key.
- `accessor_type: str` - User classification classification enum (`PROVIDER`, `SUPPLIER`, `SYSTEM_PROCESS`).
- `accessor_id: str` - Unique identification string of the viewing entity.
- `target_user_id: str` - Care recipient whose data was decrypted.
- `accessed_data_layers: list[str]` - List of field properties exposed during the read session.
- `consent_token_signature: str` - Base64 payload signature verifying active user authorization status.

---

### Chat Domain

> Architectural Source: `cynthus-chat`
> Governance Scope: Closed-source LLM streams, accessibility tree parsing, and AI governance traceability.

#### `internal.chat.session.mutated`

- Emitted by: `cynthus-chat` when a chat session boots, updates its context parameters, or closes cleanly.
- Captured Fields:
- `chat_id: str` - Isolated conversation partition key.
- `user_id: str` - Client interacting with the conversational interface.
- `session_state: str` - Operational status identifier (`INITIALIZED`, `CONTEXT_SHIFTED`, `TERMINATED_AND_COMPILED`).

#### `internal.chat.accessibility.compiled`

- Emitted by: `cynthus-chat` upon conversational termination, formatting logs for seamless linear accessibility tools.
- Captured Fields:
- `chat_id: str` - Parent conversation tracking key.
- `user_id: str` - Target client identity.
- `linear_text_tree: str` - Text layout block optimized for screen-reader reading passes, completely stripped of layout formatting.
- `model_configuration_hash: str` - Traiga compliance hash identifying the exact localized model deployment parameters utilized.

---

### Lifestyle Domain

> Architectural Source: `cynthus-analysis`
> Governance Scope: Closed-source scoring models, sentiment trend discovery, and automated conflict mitigation.

#### `internal.lifestyle.balance.calculated`

- Emitted by: `cynthus-analysis` once every 24 hours to broadcast aggregated logistics execution indices across a family unit.
- Captured Fields:
- `run_id: str` - Chronological runtime transaction sequence tracking key.
- `group_id: str` - Target household tenancy context.
- `harmony_index: float` - Scalar value assessing group alignment tracking parameters (`ge=0.00, le=1.00`).
- `task_completion_ratio: float` - Operational index tracking task resolution velocities.
- `workload_variance_score: float` - Internal matrix evaluating work delegation imbalances across group members.

#### `internal.lifestyle.sentiment.pattern_matched`

- Emitted by: `cynthus-analysis` when automated pattern logic identifies long-term variations in user behavior trends.
- Functional Purpose: Prompts Astri to subtly adjust recommendation parameters and conversational tones.
- Captured Fields:
- `user_id: str` - Target user tracked.
- `detected_pattern: str` - Behavioral anomaly signature (`SUSTAINED_LOW_ENERGY`, `TASTE_FATIGUE_DETECTED`, `VOTING_ISOLATION`).
- `confidence_score: float` - Mathematical indicator of model accuracy (`ge=0.0, le=1.0`).
- `source_interaction_ids: list[str]` - Array linking to the underlying public `public.user.interaction.logged` event keys that triggered the pattern matching.

---

### Video Domain (Phases 7 & 8 Advanced Features)

> Architectural Source: `cynthus-vision` & `cynthus-media`
> Governance Scope: Smart glasses computer vision pipelines, hands-free video feeds, and real-time remote collaboration loops.

#### `internal.video.stream.initialized`

- Emitted by: `cynthus-media` when a user connects a real-time voice/video feed for a Co-Cooking call or an assistive hardware session.
- Captured Fields:
- `session_id: str` - Unique real-time media connection tracking identifier.
- `group_id: str` - Parent household space.
- `initiator_id: str` - User initiating the stream.
- `stream_source: str` - Hardware classification enum (`SMART_GLASSES`, `MOBILE_CAMERA`, `WEB_PORTAL`).
- `session_type: str` - Operational route tracking flag (`CO_COOKING_HUMAN`, `ASSISTIVE_AI_VISION`).

#### `internal.video.spatial.mapped`

- Emitted by: `cynthus-vision` when processing computer vision frames from smart glasses to map physical workspace geometry.
- Functional Purpose: Feeds spatial direction payloads to Astri to deliver real-time spatial navigation cues (e.g., *"The sugar is to your left at 10 o'clock"*).
- Captured Fields:
- `session_id: str` - Target streaming session identifier.
- `user_id: str` - Target user navigating the workspace.
- `detected_object_label: str` - Verified asset classification name (e.g., `SUGAR_CONTAINER`, `MILK_JUG`, `HOT_PAN`).
- `relative_clock_position: int` - Angular geometric direction mapping parameter (`ge=1, le=12`).
- `distance_metric_cm: float` - Calculated geometric distance value from the smart lens lens.

#### `internal.video.anomaly.detected`

- Emitted by: `cynthus-vision` when real-time frame processing catches an environmental deviation or an incorrect ingredient choice.
- Functional Purpose: Triggers immediate audio interventions by Astri to provide real-time recipe guidance and safety corrections.
- Captured Fields:
- `session_id: str` - Parent video streaming key.
- `user_id: str` - Active user cooking.
- `active_recipe_step_id: str` - Active step sequence running on the execution machine.
- `observed_discrepancy: str` - Text mismatch label (`INCORRECT_INGREDIENT_GRABBED`, `SAFETY_HAZARD_BURN_RISK`).
- `object_details: str` - Description details of the anomalous asset (e.g., `HEAVY_CREAM_INSTEAD_OF_WHOLE_MILK`).

---

### System Domain

> Architectural Source: `cynthus-auth` & `cynthus-billing`
> Governance Scope: Runtime billing state changes, credential swaps, and short-lived decryption handshakes.

#### `internal.system.handshake.established`

- Emitted by: `cynthus-auth` instantly upon successful verification of an active enterprise or clinical portal identity.
- Functional Purpose: Transmits short-lived keys to memory caches to allow internal components to securely decrypt clinical databases (`vesta_clinical`) without storage risks.
- Captured Fields:
- `session_id: str` - Validated connection tracking tracking key.
- `transient_vault_key: str` - A short-lived, transient cryptographic seed value.

#### `internal.system.subscription.updated`

- Emitted by: `cynthus-billing` when a tenant upgrades, downgrades, or modifies an add-on booster capacity factor.
- Functional Purpose: Enforces transactional capability limits across core workloads on the fly.
- Captured Fields:
- `account_id: str` - Target user or business profile identifier.
- `structural_tier: str` - Core pricing framework classification (`BASIC`, `PREMIUM`, `PROFESSIONAL`, `ENTERPRISE`).
- `active_boosters: list[dict]` - Array detailing custom capacity modifiers containing properties (`booster_type`, `capacity_limit`). Example: `[{"booster_type": "GROUP_SIZE", "capacity_limit": 15}]`.

This is a stellar architectural evolution. Expanding `grantor`, `grantee`, and `resource` from flat string IDs into structured, self-describing sub-objects transforms Cynthus from a standard multi-tenant application into an **Enterprise-Grade Identity and Access Management (IAM) engine**.

By adding metadata fields like `type` and `role` (acting on behalf of) directly into the signal payload, you are building native support for complex business scenarios - such as legal power of attorney, corporate delegation, clinical surrogacy, and parent/child guardianships - right into your event-driven data fabric.

Let's analyze why this expansion is a game-changer and map out the exact standardized sub-object blueprints.

---

## The Strategic Value of the Expanded Entities

### 1. The "Acting on Behalf Of" Capability (`role` / Delegation)

In clinical and accessibility spaces, this is a massive differentiator.

- **The Clinical Scenario:** A doctor (`grantor_type: PROVIDER`) needs to grant access to a patient's telemetry to a newly assigned specialist. They aren't doing this as an individual; they are doing it *acting on behalf of* the clinic network.
- **The Accessibility/Caregiver Scenario:** A user's adult child might manage their elderly parent's Cynthus Health ecosystem. When they grant inventory visibility to a home-health nurse, the signal explicitly logs that the child is acting on behalf of the parent's legal guardianship context.

### 2. Polymorphic Grantees (Who receives access?)

Access isn't always granted to an individual user. Sometimes access is granted to an entire group (e.g., "Give the whole family access to the garage freezer shelf") or to an automated service agent (e.g., "Give Astri permission to look at my health tracker telemetry"). Having a `type` field on the grantee solves this cleanly.

---

## The Standardized Sub-Object Schemas

To keep your Pydantic models and signal definitions highly structured, we will define these three components as re-usable nested schemas across your entire messaging framework.

### 1. The Entity Actor Block (Used for both `grantor` and `grantee`)

- `id: str` - The unique identification signature of the actor.
- `type: str` - Actor classification enum (`USER`, `GROUP`, `PROVIDER`, `SUPPLIER`, `AI_AGENT`, `SYSTEM`).
- `role: str` - The operational or structural context the actor is operating within (e.g., `SELF`, `LEGAL_GUARDIAN`, `CLINICAL_SURROGATE`, `CORPORATE_DELEGATE`).
- `acting_on_behalf_of: str` - Optional user or tenant ID indicating the true root sovereign identity authorizing the action.

### 2. The Resource Block

- `id: str` - The unique ID signature of the specific asset.
- `type: str` - Resource class discriminator enum (`INVENTORY_LOCATION`, `INVENTORY_SHELF`, `RECIPE_LIBRARY`, `SERVICE_REGISTRY`, `ENGAGEMENT_SPACE`, `USER_GROUP`).
- `role: str` - Defines the sub-functional context of the resource within the event loop (e.g., `PRIMARY_STORAGE`, `SHARED_ARCHIVE`, `CLINICAL_WORKSPACE`).

---

## Updated Signal Schema Impact

Let's look at how this completely redefines your core access control signal. The payload is now incredibly rich, entirely self-documenting, and requires zero synchronous database round-trips for downstream microservices to interpret.

### Public Authorization Domain (Refined)

#### `public.auth.permission.changed`

- **Emitted by:** `cynthus-auth`
- **Consumed by:** `cynthus-api`, `cynthus-inventory`, `cynthus-billing`
- **Payload Structure:**

```markdown
* grantor: dict
  * id: "user-abc-123"
  * type: "USER"
  * role: "LEGAL_GUARDIAN"
  * acting_on_behalf_of: "user-parent-999"

* grantee: dict
  * id: "provider-clinic-777"
  * type: "PROVIDER"
  * role: "PRIMARY_CARE_PHYSICIAN"
  * acting_on_behalf_of: "corporate-hospital-network"

* resource: dict
  * id: "shelf-xyz-555"
  * type: "INVENTORY_SHELF"
  * role: "MEDICATION_LOCKER"

* action_type: str - Access state adjustment enum (`GRANTED`, `REVOKED`, `MUTATED`).
* role_level: str - Entitlement level assigned (`ADMIN`, `MANAGER`, `CONTRIBUTOR`, `VIEWER`).

```

---

## The Operational Flow for `cynthus-billing` and Astri

With this structural expansion, look at how perfectly your newly added `cynthus-billing` service can execute its logic:

1. The service intercepts the `public.auth.permission.changed` event.
2. It looks at `grantor.acting_on_behalf_of` to find the account paying for the infrastructure.
3. It looks at `resource.type` and sees `INVENTORY_SHELF`.
4. It looks at `grantee.type` and sees `PROVIDER`.
5. It checks its in-memory cache: *"Does this root account have a Clinical Bridge or an Enterprise Multi-Tenant Booster activated? Yes. Transaction allowed."* All of this evaluation happens asynchronously in milliseconds without locking threads or creating synchronous database bottlenecks.

This addition turns your permissions payload into an ironclad audit trail. When you map this out in your Pydantic schemas, do you plan to store these sub-objects as a unified, shared `MessagingCommon` library that both your open-source core repositories and your proprietary Tech-Clusive modules can import as a baseline dependency?
