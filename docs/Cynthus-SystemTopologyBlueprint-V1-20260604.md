## Refined System Topology Blueprint

### 1. Cynthus Core (Life & Logistics Foundation)

* **Repository:** `cynthus-core` (Segment: Open-Source Public)
* **Services:**
* `cynthus-core-api`: Direct public HTTPS/REST entry point for mobile/web apps.
* `cynthus-inventory`: Handles pantry locations, physical item allocations, and weight/transaction states.
* `cynthus-recipe`: **[NEW]** Manages recipe libraries, external URL ingestion, and OCR parsing loops.
* `cynthus-logistics`: **[NEW]** Manages purchase manifests, cart synchronization, and B2B vendor routing.
* `cynthus-messaging-engine`: **[NEW]** High-concurrency WebSockets hub for group chat routing and WebRTC signaling.
* `cynthus-scheduler`: Handles system cron tasks, item expiration evaluation loops, and baseline timed tasks.
* `cynthus-worker`: Manages background parallel data transformations, ingestion buffers, and async tasks.
* `cynthus-core-db` & `cynthus-core-cache`: Dedicated persistence and Redis storage arrays.



### 2. Cynthus Infrastructure (The Messaging Pipe)

* **Repository:** `cynthus-infra` (Segment: Open-Source Public)
* **Services:**
* `cynthus-messaging`: Azure Service Bus emulator workspace.
* `cynthus-store`: SQL Server backing the local messaging state emulator.



### 3. Cynthus Intelligence (The Analytical Brains)

* **Repository:** `cynthus-intel` (Segment: Proprietary Closed-Source)
* **Services:**
* `cynthus-analysis`: Core predictive processing engine. Computes sentiment matrices and voting patterns.
* `cynthus-chat`: Runtime for **Astri**. Manages streaming conversational LLM context and intent parsing.
* `cynthus-vision`: **[NEW]** Real-time computer vision proxy. Ingests smart glasses frame streams for spatial navigation mapping.
* `cynthus-intel-db` & `cynthus-intel-cache`: Secure, private memory and persistence structures.



### 4. Cynthus Identity (Sovereign Trust & IAM)

* **Repository:** `cynthus-identity` (Segment: Proprietary Closed-Source)
* **Services:**
* `cynthus-identity-api`: Authoritative multi-tenant access control and encryption clearinghouse.
* `cynthus-identity-db` & `cynthus-identity-cache`: Protected data layer isolation.



### 5. Cynthus Portal (Clinical Remote Care)

* **Repository:** `cynthus-portal` (Segment: Proprietary Closed-Source)
* **Services:**
* `cynthus-portal-api`: Primary entry point and data stream proxy for clinical healthcare providers.
* `cynthus-portal-web`: Specialized user interface renderer tailored for clinical workflows.
* `cynthus-portal-db` & `cynthus-portal-cache`: HIPAA-compliant, auditable persistence layers.



### 6. Cynthus Commerce (B2B Billing & Vendor Exchanges)

* **Repository:** `cynthus-commerce` (Segment: Proprietary Closed-Source)
* **Services:**
* `cynthus-billing-api`: **[NEW]** Manages monetization tiers, Stripe pipelines, and modular entitlement checks.
* `cynthus-partner-portal`: **[NEW]** Ingress API and web interface for device vendors and asset suppliers to manage promotions.
* `cynthus-commerce-db`: **[NEW]** Ledger tracking B2B transactions, affiliate referral balances, and corporate accounts.



### 7. Cynthus Auditing (Compliance Ledger)

* **Repository:** `cynthus-audit` (Segment: Proprietary Closed-Source)
* **Services:**
* `cynthus-audit-api`: Cryptographic security tracing tool that enforces immutable logging controls.
* `cynthus-audit-db`: WORM (Write Once, Read Many) secure audit database engine.



---

## Reusable Structural Models (`MessagingCommon`)

These standard data contracts are globally available to guarantee consistency across all domains.

### Common Envelope Structure

```python
class SignalMessage[T]:
    signal_id: str          # UUIDv4 message identifier
    correlation_id: str     # Trace ID tracking async workflows across services
    timestamp: datetime     # ISO 8601 UTC execution stamp
    sender_service: str     # Executable service binary name that emitted the signal
    schema_version: str     # Semantic data layout flag (e.g., "1.0.0")
    payload: T              # Specific domain data model block

```

### Common Identity Sub-Objects

```python
class ActorModel:
    id: str                 # ID string of the actor entity
    type: str               # Actor enum: USER, GROUP, PROVIDER, SUPPLIER, AI_AGENT, SYSTEM
    role: str               # Contextual string: SELF, LEGAL_GUARDIAN, CLINICAL_SURROGATE, CORPORATE_DELEGATE
    acting_on_behalf_of: str # Optional root parent user/tenant ID context

class ResourceModel:
    id: str                 # Reference ID string of the underlying resource asset
    type: str               # Resource enum: INVENTORY_LOCATION, INVENTORY_SHELF, RECIPE_LIBRARY, 
                            # SERVICE_REGISTRY, ENGAGEMENT_SPACE, USER_GROUP
    role: str               # Utility label: PRIMARY_STORAGE, SHARED_ARCHIVE, CLINICAL_WORKSPACE, EVENT_VENUE

```

---

## Definitive Implementation Signal Registry

This reference guide maps the exact interaction flow across the entire platform.

---

### Identity & Access Management Domain (`public.identity.*`)

#### `public.identity.permission.changed`

* **Initiating Event:** A user, provider, or group administrator creates a resource, shares access to a specific asset, or revokes active user roles.
* **Publisher:** `cynthus-identity-api` (Repo: `cynthus-identity`)
* **Segment:** Proprietary Closed-Source (Emitted out to the Public Bus Engine)
* **Consumers:** `cynthus-core-api`, `cynthus-inventory`, `cynthus-recipe`, `cynthus-billing-api`
* **Payload Model:**
* `grantor: ActorModel`
* `grantee: ActorModel`
* `resource: ResourceModel`
* `action_type: str` — Options: `GRANTED`, `REVOKED`, `MUTATED`
* `role_level: str` — Options: `ADMIN`, `MANAGER`, `CONTRIBUTOR`, `VIEWER`



#### `public.identity.session.invalidated`

* **Initiating Event:** A client logs out, an identity session window times out, or active authorization parameters change.
* **Publisher:** `cynthus-identity-api` (Repo: `cynthus-identity`)
* **Segment:** Proprietary Closed-Source
* **Consumers:** `cynthus-core-api`, `cynthus-portal-api`, `cynthus-partner-portal`
* **Payload Model:**
* `session_id: str` — Tracking key string.
* `user_id: str` — Targeted actor ID signature.
* `invalidation_reason: str` — Options: `USER_LOGOUT`, `TOKEN_EXPIRED`, `REVOKED_BY_ADMIN`



---

### Telemetry & Peripheral Tracking Domain (`public.device.*`)

#### `public.device.telemetry.streamed`

* **Initiating Event:** A health integration background task completes processing an aggregation window over the raw time-series metrics.
* **Publisher:** `cynthus-worker` (Repo: `cynthus-core`)
* **Segment:** Open-Source Public
* **Consumers:** `cynthus-analysis`, `cynthus-portal-api`
* **Payload Model:**
* `device_id: str` — Unique hardware tracking signature or MAC string.
* `user_id: str` — Profile ID of the care recipient.
* `metric_type: str` — Options: `HEART_RATE`, `BLOOD_GLUCOSE`, `O2_SATURATION`, `BLOOD_PRESSURE`
* `interval_start: datetime` — ISO 8601 start bound.
* `interval_end: datetime` — ISO 8601 end bound.
* `sample_count: int` — Volume count of metrics analyzed (`ge=1`).
* `min_value: float` — Minimum calculated metric.
* `max_value: float` — Maximum calculated metric.
* `mean_value: float` — Average calculated metric.



#### `public.device.threshold.breached`

* **Initiating Event:** High-frequency time-series processing flags an out-of-bounds biometric reading or environmental danger parameter.
* **Publisher:** `cynthus-worker` (Repo: `cynthus-core`)
* **Segment:** Open-Source Public
* **Consumers:** `cynthus-core-api`, `cynthus-portal-api`, `cynthus-chat`
* **Payload Model:**
* `device_id: str` — Originating tracking device.
* `user_id: str` — Target profile identity impacted.
* `trigger_condition: str` — Options: `BIOMETRIC_ANOMALY`, `ENVIRONMENTAL_BREACH`
* `observed_value: str` — Data point that triggered the alert.
* `severity_level: str` — Options: `CRITICAL_LOW`, `CRITICAL_HIGH`
* `requires_escalation: bool` — Routing priority indicator.



#### `public.device.battery.reported`

* **Initiating Event:** A connected wearable peripheral pushes diagnostic data layers into the platform interface wrapper.
* **Publisher:** `cynthus-core-api` (Repo: `cynthus-core`)
* **Segment:** Open-Source Public
* **Consumers:** `cynthus-worker`
* **Payload Model:**
* `device_id: str` — Core identity of target unit.
* `battery_percent: int` — Integer parsing (`ge=0, le=100`).
* `is_charging: bool` — Circuit connection state flag.



---

### Asset & Pantry Logistics Domain (`public.inventory.*`)

#### `public.inventory.item.mutated`

* **Initiating Event:** A user uses an ingredient, dumps stale waste, scans an invoice receipt, or checks off a barcode item.
* **Publisher:** `cynthus-inventory` (Repo: `cynthus-core`)
* **Segment:** Open-Source Public
* **Consumers:** `cynthus-core-api`, `cynthus-analysis`
* **Payload Model:**
* `inventory: ResourceModel` — Target location and storage context.
* `shelf_id: str` — Identifier tracking the row or container zone.
* `item_id: str` — Universal SKU or target index tracking sequence.
* `current_quantity: int` — Resulting metric total post-mutation (`ge=0`).
* `mutation_reason: str` — Options: `ITEM_REPLENISHED`, `ITEM_CONSUMED`, `WASTE_DISCARDED`



#### `public.inventory.threshold.dropped`

* **Initiating Event:** An inventory calculation step registers that a core item has fallen below a user's defined minimum safety threshold.
* **Publisher:** `cynthus-inventory` (Repo: `cynthus-core`)
* **Segment:** Open-Source Public
* **Consumers:** `cynthus-logistics`, `cynthus-chat`
* **Payload Model:**
* `inventory: ResourceModel` — Asset parent identifier.
* `item_id: str` — Core product SKU.
* `remaining_quantity: int` — Current stock level.
* `target_minimum: int` — Configured floor baseline limit.



#### `public.inventory.item.expired`

* **Initiating Event:** A background task parses storage arrays and flags an active item that has passed its shelf-life expiration date.
* **Publisher:** `cynthus-scheduler` (Repo: `cynthus-core`)
* **Segment:** Open-Source Public
* **Consumers:** `cynthus-inventory`, `cynthus-chat`
* **Payload Model:**
* `inventory: ResourceModel` — Target storage location identifier.
* `item_id: str` — Target product SKU index.
* `expiration_date: datetime` — Recorded shelf limit time.
* `quantity_affected: int` — Total item volume impacted.



---

### Culinary Data & Parsing Domain (`public.recipe.*`)

#### `public.recipe.ingestion.processed`

* **Initiating Event:** The recipe scanner engine completes an external web-scrape or processes a physical recipe photo through an OCR data transformation loop.
* **Publisher:** `cynthus-recipe` (Repo: `cynthus-core`)
* **Segment:** Open-Source Public
* **Consumers:** `cynthus-core-api`, `cynthus-chat`
* **Payload Model:**
* `library_id: str` — Target Recipe Library resource context.
* `recipe_id: str` — Generated recipe transaction tracker.
* `source_type: str` — Options: `OCR_SCAN`, `URL_PARSE`, `MANUAL_INPUT`
* `parsed_title: str` — Extracted text heading.
* `structured_ingredients: list[dict]` — List containing items (`item_name`, `quantity`, `unit`).
* `raw_text_payload: str` — Clean unstructured transcription engine output block.



---

### Supply Chain & Commerce Domain (`public.logistics.*`)

#### `public.logistics.order.placed`

* **Initiating Event:** A user confirms a cart purchase request or an automated low-stock background routine triggers a pre-authorized B2B checkout.
* **Publisher:** `cynthus-logistics` (Repo: `cynthus-core`)
* **Segment:** Open-Source Public
* **Consumers:** `cynthus-partner-portal`, `cynthus-billing-api`, `cynthus-inventory`
* **Payload Model:**
* `order_id: str` — Corporate invoice tracking string.
* `buyer: ActorModel` — Profile making the purchase.
* `vendor_target_id: str` — Destination identifier indicating which merchant API maps to the request.
* `total_cost: float` — Total cost tracking index.
* `items_ordered: list[dict]` — Elements parsing objects (`item_id`, `quantity`, `unit_cost`).



#### `public.logistics.promotion.registered`

* **Initiating Event:** A corporate merchant updates their promotion cache or targets a discount profile code toward specific item shortages.
* **Publisher:** `cynthus-partner-portal` (Repo: `cynthus-commerce`)
* **Segment:** Proprietary Closed-Source
* **Consumers:** `cynthus-logistics`, `cynthus-chat`
* **Payload Model:**
* `supplier_id: str` — Verified commercial provider.
* `promotion_id: str` — Track signature identifier.
* `target_item_sku: str` — Impacted catalog code.
* `discount_value: float` — Percentage drop value parameters.
* `expiration_timestamp: datetime` — Active campaign duration window.



---

### Collective Collaboration & Sync Domain (`public.group.*`)

#### `public.group.message.sent`

* **Initiating Event:** A group participant pushes a chat line or shares an in-app asset card inside an active workspace conversation thread.
* **Publisher:** `cynthus-messaging-engine` (Repo: `cynthus-core`)
* **Segment:** Open-Source Public
* **Consumers:** `cynthus-core-api`, `cynthus-chat`
* **Payload Model:**
* `message_id: str` — Unique database record key identifier.
* `group_id: str` — Target tenant communication workspace context.
* `sender_id: str` — ID string of the speaker.
* `content_body: str` — Structural message content or link card object string.



#### `public.group.meal.proposed`

* **Initiating Event:** A household member triggers a dining selection card to initiate a democratic dinner vote.
* **Publisher:** `cynthus-core-api` (Repo: `cynthus-core`)
* **Segment:** Open-Source Public
* **Consumers:** `cynthus-messaging-engine`, `cynthus-chat`
* **Payload Model:**
* `proposal_id: str` — Voting run tracking session signature.
* `group: ResourceModel` — Target group context.
* `proposer_id: str` — Profile ID launching the vote.
* `meal_id: str` — Target meal identifier.
* `recipe_id: str` — Structural index mapping the chosen recipe variation.



#### `public.group.vote.cast`

* **Initiating Event:** An individual group participant selects Yes or No on an active in-line voting card.
* **Publisher:** `cynthus-core-api` (Repo: `cynthus-core`)
* **Segment:** Open-Source Public
* **Consumers:** `cynthus-messaging-engine`, `cynthus-analysis`
* **Payload Model:**
* `proposal_id: str` — Target voting tracking key.
* `group_id: str` — Parent workspace tracking boundary.
* `voter_id: str` — Profile executing the transaction.
* `vote_choice: str` — Options: `YES`, `NO`



#### `public.group.vote.concluded`

* **Initiating Event:** A meal vote meets absolute consensus thresholds or its timer duration window expires.
* **Publisher:** `cynthus-messaging-engine` (Repo: `cynthus-core`)
* **Segment:** Open-Source Public
* **Consumers:** `cynthus-core-api`, `cynthus-chat`, `cynthus-inventory`
* **Payload Model:**
* `proposal_id: str` — Resolved session signature tracking index.
* `group: ResourceModel` — Target group boundary context.
* `final_status: str` — Options: `CONSENSUS_REACHED`, `STALEMATE_DETECTED`, `PROPOSAL_EXPIRED`
* `vote_tally: dict` — Execution balance summary (e.g., `{"yes": 3, "no": 1}`).



---

### User Insights & Feedback Domain (`public.user.*`)

#### `public.user.interaction.logged`

* **Initiating Event:** A client clicks a favorite indicator, logs a meal rating, or updates a preference filter.
* **Publisher:** `cynthus-core-api` (Repo: `cynthus-core`)
* **Segment:** Open-Source Public
* **Consumers:** `cynthus-analysis`
* **Payload Model:**
* `user_id: str` — Profile execution tracking identifier.
* `interaction_type: str` — Options: `LIKED`, `DISLIKED`, `RATED`, `FAVORITED`
* `target_resource: ResourceModel` — Target item context evaluated.
* `numerical_rating: float` — Sliding validation metric, populated if type is `RATED` (`ge=0.0, le=1.0`).



#### `public.user.stamina.reported`

* **Initiating Event:** A user pushes a qualitative statement or logs their physical energy level into the client UI.
* **Publisher:** `cynthus-core-api` (Repo: `cynthus-core`)
* **Segment:** Open-Source Public
* **Consumers:** `cynthus-analysis`, `cynthus-chat`
* **Payload Model:**
* `user_id: str` — Profile tracking identifier.
* `stamina_score: int` — Value score scaling tracking bounds (`ge=1, le=5`).
* `operational_override: str` — Options: `NEED_ALTERNATIVE_MEAL_OPTION`, `DELEGATE_LOGISTICS_TASKS`



---

### Privacy Enforcements & Auditing Domain (`internal.audit.*`)

#### `internal.audit.access.logged`

* **Initiating Event:** An internal service layer prepares to decrypt or stream protected health metrics or personal log details to external contexts.
* **Publisher:** `cynthus-portal-api` / `cynthus-identity-api`
* **Segment:** Proprietary Closed-Source (Internal Bus Only)
* **Consumers:** `cynthus-audit-api`
* **Payload Model:**
* `audit_event_id: str` — Cryptographic immutable unique sequence tracking hash.
* `accessor: ActorModel` — Identity accessing the database parameters.
* `target_user_id: str` — Patient or resident whose data layer was touched.
* `accessed_data_layers: list[str]` — Exact string list of data parameters decrypted.
* `consent_token_signature: str` — Base64 access control verification token validation hash.



---

### Accessibility & LLM Management Domain (`internal.chat.*`)

#### `internal.chat.session.mutated`

* **Initiating Event:** An active conversation lifecycle window initializes, switches context targets, or closes cleanly.
* **Publisher:** `cynthus-chat` (Repo: `cynthus-intel`)
* **Segment:** Proprietary Closed-Source
* **Consumers:** `cynthus-analysis`
* **Payload Model:**
* `chat_id: str` — Conversation block stream partition tracking key.
* `user_id: str` — Active user conversation tracking identifier.
* `session_state: str` — Options: `INITIALIZED`, `CONTEXT_SHIFTED`, `TERMINATED_AND_COMPILED`



#### `internal.chat.accessibility.compiled`

* **Initiating Event:** A live dialogue window closes, prompting the platform to structure the output for clean screen reader execution.
* **Publisher:** `cynthus-chat` (Repo: `cynthus-intel`)
* **Segment:** Proprietary Closed-Source
* **Consumers:** `cynthus-core-api` (Pushed out to clear WebSocket arrays)
* **Payload Model:**
* `chat_id: str` — Target session signature reference tracker.
* `user_id: str` — Target profile identity.
* `linear_text_tree: str` — Structured string payload completely stripped of layout visual indicators for clean linear screen-reader tree parsing.
* `model_configuration_hash: str` — System compliance hash capturing active LLM architecture parameters.



---

### Machine Intelligence Scoring Domain (`internal.lifestyle.*`)

#### `internal.lifestyle.balance.calculated`

* **Initiating Event:** The predictive compute processor completes analyzing a 24-hour window of family logistics metrics.
* **Publisher:** `cynthus-analysis` (Repo: `cynthus-intel`)
* **Segment:** Proprietary Closed-Source
* **Consumers:** `cynthus-chat`
* **Payload Model:**
* `run_id: str` — Dynamic runtime tracking instance.
* `group: ResourceModel` — Target group workspace under analysis.
* `harmony_index: float` — Mathematical tracker scaling boundary changes (`ge=0.00, le=1.00`).
* `task_completion_ratio: float` — Evaluation index processing execution speeds.
* `workload_variance_score: float` — Imbalance check measuring distribution gaps across actors.



#### `internal.lifestyle.sentiment.pattern_matched`

* **Initiating Event:** The pattern recognition engine identifies long-term variations in user behavior logs.
* **Publisher:** `cynthus-analysis` (Repo: `cynthus-intel`)
* **Segment:** Proprietary Closed-Source
* **Consumers:** `cynthus-chat`
* **Payload Model:**
* `user_id: str` — Target user under monitoring.
* `detected_pattern: str` — Options: `SUSTAINED_LOW_ENERGY`, `TASTE_FATIGUE_DETECTED`, `VOTING_ISOLATION`
* `confidence_score: float` — Accuracy measurement scaling tracking values (`ge=0.0, le=1.0`).
* `source_interaction_ids: list[str]` — Array linking back to public interaction events that triggered the match.



---

### Spatial Vision & Real-Time Media Domain (`internal.video.*`)

#### `internal.video.stream.initialized`

* **Initiating Event:** A user connects a live camera feed or initiates a peer-to-peer Co-Cooking video call.
* **Publisher:** `cynthus-messaging-engine` (Repo: `cynthus-core`)
* **Segment:** Open-Source Public (Internal Bus Tracking)
* **Consumers:** `cynthus-vision`, `cynthus-core-api`
* **Payload Model:**
* `session_id: str` — Dynamic media streaming transaction tracker.
* `group: ResourceModel` — Active parent workspace unit.
* `initiator_id: str` — Profile launching the connection.
* `stream_source: str` — Options: `SMART_GLASSES`, `MOBILE_CAMERA`, `WEB_PORTAL`
* `session_type: str` — Options: `CO_COOKING_HUMAN`, `ASSISTIVE_AI_VISION`



#### `internal.video.spatial.mapped`

* **Initiating Event:** The computer vision engine processes a frame from smart glasses and maps an asset's position relative to the user.
* **Publisher:** `cynthus-vision` (Repo: `cynthus-intel`)
* **Segment:** Proprietary Closed-Source
* **Consumers:** `cynthus-chat`
* **Payload Model:**
* `session_id: str` — Target active connection identifier.
* `user_id: str` — Client navigating the low-vision space.
* `detected_object_label: str` — Product classification string (`SUGAR_CONTAINER`, `MILK_JUG`, `HOT_PAN`).
* `relative_clock_position: int` — Angular tracking parameter mapping coordinates (`ge=1, le=12`).
* `distance_metric_cm: float` — Spatial depth calculation from lens arrays.



#### `internal.video.anomaly.detected`

* **Initiating Event:** Real-time visual tracking detects a cooking hazard or a product selection mismatch during recipe assembly.
* **Publisher:** `cynthus-vision` (Repo: `cynthus-intel`)
* **Segment:** Proprietary Closed-Source
* **Consumers:** `cynthus-chat`
* **Payload Model:**
* `session_id: str` — Active video connection reference tracking key.
* `user_id: str` — Active user cooking.
* `active_recipe_step_id: str` — Active task module configuration step under review.
* `observed_discrepancy: str` — Options: `INCORRECT_INGREDIENT_GRABBED`, `SAFETY_HAZARD_BURN_RISK`
* `object_details: str` — Description details string (e.g., `HEAVY_CREAM_INSTEAD_OF_WHOLE_MILK`).



---

### Core Commercial & Financial States Domain (`internal.system.*`)

#### `internal.system.handshake.established`

* **Initiating Event:** A secure clinical portal registration succeeds, prompting volatile token dissemination to allow decryption access.
* **Publisher:** `cynthus-identity-api` (Repo: `cynthus-identity`)
* **Segment:** Proprietary Closed-Source
* **Consumers:** `cynthus-analysis`, `cynthus-portal-api`
* **Payload Model:**
* `session_id: str` — Validated session signature tracking identifier.
* `transient_vault_key: str` — Short-lived cryptographic seed token string.



#### `internal.system.subscription.updated`

* **Initiating Event:** A billing event logs a transaction update, a tier shift, or activates a component booster upgrade.
* **Publisher:** `cynthus-billing-api` (Repo: `cynthus-commerce`)
* **Segment:** Proprietary Closed-Source
* **Consumers:** `cynthus-identity-api`, `cynthus-core-api`
* **Payload Model:**
* `account_id: str` — Sovereign account identification key string.
* `structural_tier: str` — Options: `BASIC`, `PREMIUM`, `PROFESSIONAL`, `ENTERPRISE`
* `active_boosters: list[dict]` — Array mapping objects detailing custom capacity limits (`booster_type`, `capacity_limit`).

