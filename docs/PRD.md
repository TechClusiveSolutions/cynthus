# Master Product Requirements Document: Cynthus Life Ecosystem

**Product Name:** Cynthus (also referred to as Cynthus Life or Cynthus Life Ecosystem)
**Parent Organization:** Tech-Clusive Solutions, LLC
**Document Version:** 4.2 (June 2026)
**Status:** Architectural Design Phase - Pricing, Roadmap, and Booster Pack Model Finalized
**Guiding Principle:** Universal Design and Accessibility-First Architecture. Screen-reader efficiency, semantic clarity, and high-contrast layouts are treated as core architectural parameters rather than compliance updates.

---

## 1. Executive Summary & Vision

Cynthus is an inclusive, multimodal lifestyle companion and distributed microservice ecosystem designed for individuals, families, and businesses. Built on a foundation of "Life-Logistics," the platform seamlessly bridges daily kitchen management and asset tracking with professional healthcare monitoring and remote clinical integration. By utilizing a decoupled, choreographed microservice architecture, Cynthus coordinates four core pillars:

- Asset, pantry, supply, and food logistics management.
- Remote monitoring, healthcare wearable telemetry, and clinical integration.
- Secure data coordination across user, corporate tenant, and clinical workspaces.
- AI-driven interactive companionship and analytical lifestyle logic.

The primary human interface of the platform is **Astri**, a logic-first, empathetic AI chat persona that translates complex system telemetry and environmental data into clear, actionable human dialogue.

---

## 2. Strategic Objectives and Value Propositions

Cynthus establishes a unique "Platform Network Effect" by interconnecting three distinct user groups.

### 2.1 User Value (Individuals, Families, and Roommates)

- **Accessible Autonomy:** Provides fully accessible autonomy for blind, deaf, and neurodivergent users through multimodal interface contracts.
- **Decision Fatigue Reduction:** Minimizes daily planning friction through AI-powered meal planning and the "Energy Banker" system built on Spoon Theory logic.
- **Safety Assurance:** Enforces strict hard-constraint allergy and medical safety logic across all recommendations. No suggestion may bypass a user's registered hard constraints.

### 2.2 Provider Value (Doctors, Dietitians, and Clinical Staff)

- **Automated Remote Monitoring:** Automates Remote Patient Monitoring (RPM) data collection and tracks patient adherence.
- **Clinical Decision Support:** Delivers actionable clinical insights through pantry inventory analysis, symptom correlation, and biometric telemetry.
- **Billing Optimization:** Facilitates billable medical services via compliant CPT codes.

### 2.3 Partner Value (Hardware Manufacturers and Retailers)

- **Wearable Device Utility:** Enhances consumer wearable utility (e.g., Garmin, smart rings) by integrating fitness tracking data into lifestyle and wellness workflows.
- **Replenishment Revenue:** Drives targeted fulfillment revenue for grocers and wholesalers through automated API integrations.

---

## 3. User Personas and Stories

Each persona demonstrates a unique touchpoint within the unified Cynthus architecture.

### 3.1 The Parent (Admin Workspace)

As a blind parent, I need to perform a "Budget Audit" using Cynthus's voice interface to ensure our weekly grocery spend is on track while managing my children's nutritional needs.

### 3.2 The Medical User (Care Recipient)

As a user with Type 2 Diabetes, I need Cynthus to monitor my continuous glucose monitor (CGM) and cross-reference my pantry to suggest low-glycemic snacks when my levels are trending high.

### 3.3 The Small Business Owner (Caterer/Commercial Workspace)

As an event planner, I need Cynthus to scale a recipe for 50 people with varying allergies and automatically generate a wholesale order for my partner grocer.

### 3.4 MVP Primary User Story (Phase 1)

As a user, I open the Cynthus app and am immediately presented with a chat window. Astri greets me and asks about my day.

**Path A - Cook at home:** Astri asks a few questions about my preferences. She retrieves my current inventory and selects a recipe that matches my preferences and satisfies all of my registered dietary and medical hard constraints. She presents a meal suggestion I can accept or reject. If I reject it, she offers an alternative.

**Path B - Go out or order in:** Astri generates a realistic meal idea based on my current preferences and hard constraints without consulting inventory.

**Path C - Manual mode:** I dismiss the chat and enter planning mode. I browse my inventory by food category. The app presents a meal suggestion that matches my current preferences and satisfies my hard constraints without requiring me to interact with Astri.

---

## 4. Functional Requirements Matrix

Features are segmented into four priority levels (P1-P4) aligned to phased delivery milestones. Priority 1 and Priority 2 features comprise the Free Tier. Priority 3 and Priority 4 features map to paid and partner tiers.

### 4.1 Module A: Cynthus Trust (Identity & Compliance)

- **Req A.1 - Workspace Boundary Stub (P1):** Every user account must be assigned a `workspace_id` at registration. In Phase 1 this is a 1:1 mapping (one user, one workspace). The `workspace_id` must be present in all database schemas, API contracts, JWT token claims, and message envelopes from day one to support multi-user workspace expansion in Phase 2 without schema migration.

- **Req A.2 - Organizational Tenant Boundary (P1):** The system must isolate data at the multi-tenant organization level (`organization_id`) and further separate operations into distinct workspaces (`workspace_id`). No cross-tenant data leaks are permitted on the shared message bus.

- **Req A.3 - Granular Role-Based Access Control (P1):** Profiles within a workspace must support distinct role allocations based on both RBAC and Attribute-Based Access Control (ABAC), accommodating designations such as Primary Caregiver, Care Recipient, Standard User, or commercial administrative managers. Phase 1 implements single-user accounts only; role expansion targets Phase 2.

- **Req A.4 - Cryptographic Vault Isolation (P4):** Access to sensitive clinical or private security signals inside `cynthus-intelligence` repositories requires a separate decryption handshake using user-derived cryptographic keys, distinct from standard application tokens.

### 4.2 Module B: Cynthus Core (Life-Logistics)

- **Req B.1 - Basic Inventory & Mutation Tracking (P1):** The system must support standard logging and predictive state tracking of pantry, fridge, and freezer items. The inventory engine must process physical asset mutations with an absolute processing latency of less than 200ms.

- **Req B.2 - User Profile & Hard-Constraint Registry (P1):** The `cynthus-profile` service must maintain a strict separation between soft preferences and hard constraints for each user profile. Soft preferences (favorite cuisines, portion sizes, UI preferences, Energy Banker energy defaults) are freely mutable. Hard constraints (allergens, diagnosed dietary conditions, medication-driven restrictions) are safety-critical and must generate a timestamped audit event on every modification. The allergy hard-filter must be evaluated and applied by `cynthus-profile` before any meal suggestion is rendered, regardless of the suggestion pathway.

- **Req B.3 - Recipe Management & Constraint Filtering (P1):** The system must maintain a recipe library. `cynthus-recipe` must expose a constraint-filtered recipe query API that accepts a set of hard constraints from `cynthus-profile` and returns only safe candidates. No recipe result set may bypass this filter.

- **Req B.4 - Context Assembly (P1):** `cynthus-core-api` must act as the context aggregator for all AI-powered suggestion flows. Before any user message or intent is forwarded to `cynthus-chat`, the API layer must retrieve the current inventory snapshot from `cynthus-inventory`, the filtered recipe candidates from `cynthus-recipe`, and the user's full constraint and preference profile from `cynthus-profile`, then package them into a single structured context payload. The Intelligence subnet receives assembled context only - it never calls back into Core services directly.

- **Req B.5 - Smart List Engine & Shared Grocery Sync (P2):** The platform must maintain shared, real-time lists for households, roommates, and commercial operations. When an asset signal flags an essential item as depleted, background workers must automatically append it to the workspace procurement registry, filtered by preferred merchant categories.

- **Req B.6 - Cynthus-AI "Daily Spark" (P1):** Provide contextual, real-time meal suggestions based on the user's current time of day, available inventory, and pre-assembled profile context.

- **Req B.7 - Harmony Score (P2):** Utilize AI-mediated conflict resolution to balance group meal voting, workload distribution, resource usage, operational completion patterns, and individual safety and wellness thresholds across a workspace. Targets Phase 2 multi-user workspaces.

- **Req B.8 - Energy Banker (P2):** Implement a recipe filtering mechanism based on current versus future energy levels, leveraging Spoon Theory logic to adapt to user fatigue. Energy defaults are stored as a soft preference in `cynthus-profile`.

- **Req B.9 - Advanced Costing & Wholesale Logistics (P3):** Provide real-time price-per-portion analysis, recipe scaling logic, volume logistics, and automatic wholesale order generation for small business owners and caterers.

### 4.3 Module C: Cynthus Intelligence (Astri AI Engine)

- **Req C.1 - Conversational Lifestyle Companion (P1):** `cynthus-chat` must support a real-time streaming conversational interface (Astri) capable of processing pre-assembled context payloads from `cynthus-core-api` to generate meal suggestions, lifestyle guidance, and general companionship dialogue. The Intelligence subnet must maintain no direct outbound dependencies to Core services at runtime.

- **Req C.2 - Non-Visual Dialogue Strategy & Sensory Profiles (P1):** Provide real-time interface adaptations for screen readers (Blind), haptics and strobes (Deaf), and Zen Mode (Dyslexic). All interface payloads returned by the chat service must be structured to ensure seamless parsing by assistive technologies, avoiding layout elements that rely on spatial placement or geometric orientation.

- **Req C.3 - Multimodal Wearable Integration & Anomaly Detection (P2):** Support basic health statistic synchronization with wearable watches and smart rings. The analytical processor must continuously monitor incoming telemetry streams (blood glucose, heart rate, blood pressure, steps). High-frequency raw tracking lines must bypass the service bus via a dedicated ingestion buffer. If a calculated aggregate slice or biometric threshold breaches a predefined margin, the system must instantly emit a priority alert lifecycle event.

- **Req C.4 - Core Harmony Computation (P2):** The intelligence engine must evaluate historical activity completion patterns, resource balances, and task loads once every 24 hours to generate the updated workspace Harmony index.

- **Req C.5 - Advanced Wearable HUD (P3):** Support smart glasses integrations to render step-by-step preparation, kitchen guidance, and logistics assistance via `cynthus-video`.

### 4.4 Module D: Cynthus Health (B2B Clinical Gateway)

- **Req D.1 - Read-Only HIPAA Auditing (P3):** Restrict external clinical stakeholders and enterprise partners to read-only views of authorized signals. Every data access action must write an immutable entry to an independent secure audit log to meet HIPAA regulations.

- **Req D.2 - Patient & Tenant Consent Verification (P3):** The portal gateway must inspect token signatures issued by authentication services before exposing historical telemetry streams, ensuring active consent and access scopes are validated per session.

- **Req D.3 - RPM Billing Compliance (P3):** Automate the logging of physiologic data transmissions to support CPT code tracking. Clinician interaction time must be logged to support practice billing. All RPM workflows must pass regulatory review before deployment.

---

## 5. Medical and Clinical Specifications

### 5.1 Remote Patient Monitoring (RPM) Logic

- **CPT Tracking:** Automate the logging of physiologic data transmissions, ensuring accurate tracking of active data transmission periods. Clinician interaction time within the portal framework must be logged to support practice billing.
- **Clinical Triage Dashboards:** Provide specialized, triage-based dashboard views that automatically flag patients exhibiting high-risk nutritional trends, biometric anomalies, or critical telemetry threshold breaches.

### 5.2 Symptom-Inventory Correlation

The closed-source analytical engine must run correlation algorithms linking internal workspace inventory usage (such as consumption of high-sodium items) with user-reported symptoms or wearable anomalies (such as elevated heart rate spikes or reported evening pain).

### 5.3 Regulatory Note on Wearable Devices

Consumer wearable devices (e.g., Garmin watches, smart rings) are not FDA-cleared medical devices. The use of consumer wearable data to support RPM billing and clinical workflows requires a documented regulatory strategy aligned with FDA Software as a Medical Device (SaMD) guidance. This regulatory strategy must be established and reviewed prior to Health module go-live.

---

## 6. Technical & Architecture Specifications

The system is built upon an Event-Driven Choreography pattern. Individual microservices interact implicitly by broadcasting immutable facts (signals) to a centralized enterprise messaging spine rather than orchestrating downstream dependencies via direct commands.

### 6.1 Unified Object Domain Model

All operational tracking and telemetry are categorized into three abstract domains:

- **Signals (System Messages):** A message generated in response to any event initiated by an actor, either directly or indirectly. Signals are the foundational communication primitive of the messaging spine. Examples: a wearable device transmitting a biometric reading, a user authenticating to the system, an inventory item dropping below threshold, a background worker completing an OCR job.

- **Activities (Real-World Actions):** An event representing an action that a user, partner, service provider, or supplier performs in the real world. Activities describe things that happen, not things that are planned. Examples: a user changing a dietary preference value, a supplier fulfilling a purchase order, a clinician accepting a live companion video call, a caregiver logging a medication administration.

- **Engagements (Planned Real-World Events):** A planned event that a user, supplier, service provider, or partner may attend in the real world. Engagements describe things that are scheduled to happen. Examples: a company lunch, a meal with friends, a scheduled visit at the doctor's office, a catering delivery window, a planned therapy session.

### 6.2 Microservice Decomposition

The ecosystem is partitioned into seven domain segments isolating business logic, licensing models, and runtime deployment contexts.

#### Cynthus Trust - Closed-Source

Manages identity, authentication, authorization, and compliance auditing. Closed-source to protect security architecture and regulatory audit integrity.

- `cynthus-identity`: Multi-tenant identity management, JWT issuance, RBAC/ABAC access control. Maps user profiles to organizations and workspaces.
- `cynthus-audit`: Immutable append-only audit ledger. Records every data access and hard-constraint mutation event.
- `cynthus-trust-cache`: High-speed caching layer for trust domain (token validation, session data).
- `cynthus-trust-db`: Clustered persistent storage for the trust domain with schema-isolated partitions per service.

#### Cynthus Core - Open-Source

Governed by open-source community contribution. Handles physical data domains, logistics foundations, user profiles, and the primary consumer interface.

- `cynthus-core-api`: Primary public HTTPS/REST and WebSocket edge. Handles user sessions, context assembly, and request routing. Acts as the context aggregator before forwarding to Intelligence.
- `cynthus-inventory`: Predictive state management for pantry, fridge, and freezer items. Processes physical asset mutations.
- `cynthus-recipe`: Recipe library management, external recipe ingestion, OCR parsing, and constraint-filtered recipe query API.
- `cynthus-logistics`: Purchase manifests, automated reorders, delivery tracking, and external supplier integrations.
- `cynthus-profile`: User preference and hard-constraint registry. Owns the allergy hard-filter. Distinguishes soft preferences (mutable) from hard constraints (audit-logged on mutation).
- `cynthus-scheduler`: Background cron engine for periodic tasks, item expiration windows, and time-based system loops.
- `cynthus-worker`: Asynchronous background task processor for data ingestion, OCR jobs, receipt scanning, and non-time-sensitive formatting tasks.
- `cynthus-core-web`: Fully accessible, semantic consumer UI renderer (React/Next.js, SSR).
- `cynthus-core-cache`: High-speed caching layer for core domain services.
- `cynthus-core-db`: Clustered persistent storage for the core domain with schema-isolated partitions per service.

#### Cynthus Intelligence - Closed-Source

Private, dark subnet. Contains no public IP allocations. All inbound traffic arrives via pre-assembled context payloads through VNet peering from Core. Makes no outbound runtime calls to Core services.

- `cynthus-chat`: Runtime for the Astri AI persona. Processes pre-assembled context payloads and generates streaming conversational responses.
- `cynthus-analysis`: Autonomous AI agent executing predictive lifestyle analysis, biometric trend modeling, Harmony index calculations, and sentiment analysis.
- `cynthus-video`: Smart glasses HUD pipeline. Processes real-time video frames, calculates spatial coordinates, and generates clock-face orientation guidance for low-vision users.
- `cynthus-intel-cache`: High-speed caching layer for intelligence domain services.
- `cynthus-intel-db`: Clustered persistent storage for the intelligence domain with schema-isolated partitions per service.

#### Cynthus Health - Closed-Source

Demilitarized subnet hosting external healthcare provider and clinical partner interfaces. Enforces regulatory validation and consent verification before all data exchange.

- `cynthus-health-api`: Primary edge for clinical integrations. Enforces HIPAA consent token verification and read-only data access patterns.
- `cynthus-device`: Device telemetry aggregator (provisional: expected in the `cynthus-health` repository; HUD data may need a different home). Ingests wearable and biometric data streams. Routes hot-path data (raw telemetry) to time-series buffers and warm-path summaries to the Service Bus.
- `cynthus-health-web`: Clinical dashboard UI renderer for authorized B2B healthcare partners.
- `cynthus-health-cache`: High-speed caching layer for health domain services.
- `cynthus-health-db`: Dedicated PHI-isolated persistent storage implementing field-level encryption for all biometric and patient data.

#### Cynthus Commerce - Closed-Source

Manages monetization structures, payment processing, subscription management, supplier relationships, and partner integrations.

- `cynthus-billing-api`: Subscription lifecycle management, payment processing, and account tier enforcement.
- `cynthus-partner-api`: Partner and supplier integrations, wholesale API connections, slotting and bounty tracking.
- `cynthus-comm-web`: UI renderer for partner, supplier, and provider commercial interactions.
- `cynthus-comm-cache`: High-speed caching layer for commerce domain services.
- `cynthus-comm-db`: Clustered persistent storage for the commerce domain with schema-isolated partitions per service.

#### Cynthus Emulators - Open-Source (Developer Environment Only)

Local developer container environment. Not deployed to production. Enables community contributors to run the full Core stack locally without cloud dependencies.

- `cynthus-signal-bus`: Azure Service Bus emulator container for local message routing.
- `cynthus-signal-db`: MS SQL storage backend for the Service Bus emulator.

#### Cynthus Shared - Open-Source

Shared Pydantic model library distributed as a Python wheel. Contains common signal schema primitives used across both open-source and closed-source repositories. The public wheel exposes envelope headers only; closed-source services install the private internal wheel for deep payload validation (see ADR-004).

### 6.3 Context Assembly Pattern

The context assembly pattern is the critical boundary between open-source Core and closed-source Intelligence. `cynthus-core-api` is solely responsible for aggregating all data required by Astri before any AI processing occurs.

```text
User Request
     |
     v
cynthus-core-api
     |
     +-- GET /profile/constraints  --> cynthus-profile   (hard constraints + soft prefs)
     |
     +-- GET /inventory/snapshot   --> cynthus-inventory  (current pantry state)
     |
     +-- GET /recipe/candidates    --> cynthus-recipe     (filtered by hard constraints)
     |
     v
Assembled Context Payload
     |
     v
cynthus-chat (Intelligence VNet - dark subnet)
     |
     v
Streaming Response --> cynthus-core-api --> User
```

`cynthus-chat` receives the assembled payload and generates a response. It never calls back into Core at runtime. This keeps the Intelligence subnet dark, protects closed-source IP, and ensures community contributors can develop and test Core context assembly logic independently.

### 6.4 Messaging Spine & Asynchronous Choreography

- **Enterprise Messaging Spine:** Azure Service Bus (AMQP), with Redis utilized for high-speed cache and local message routing.
- **Three-Topic Architecture:** The Service Bus is partitioned into three distinct topics aligned to visibility and compliance boundaries. This enforces access control at the topic level rather than relying solely on subscription filters, and allows each topic to carry its own retention, access policy, and monitoring configuration independently.

- `cynthus-topic-public`
  - Namespace Prefix: `public.*`
  - Publishers: All open-source Core services
  - Purpose: All signals visible to open-source consumers. Carries inventory, recipe, user, group, logistics, and device namespace events.
- `cynthus-topic-internal`
  - Namespace Prefix: `internal.*`
  - Publishers: Closed-source services only
  - Purpose: Private signals not exposed to open-source repositories. Carries lifestyle, chat, video, and system namespace events. Open-source services may consume envelope headers only (opaque payload).
- `cynthus-topic-audit`
  - Namespace Prefix: `internal.audit.*`
  - Publishers: `cynthus-portal-api`, `cynthus-identity`, `cynthus-profile`
  - Purpose: Append-only compliance and safety audit events. Separate topic ensures audit records cannot be co-mingled with operational traffic and supports independent retention and integrity policies.

- **Four Lifecycle Actions:** To prevent event explosion, all domains emit events using exactly four atomic state mutation types attached to message metadata: `created`, `updated`, `deleted`, and `snapshot`. Downstream processors evaluate the state snapshot to compute deltas, minimizing subscription overhead.
- **Correlation Tracking:** Every message carries a `correlation_id` (UUIDv4) enabling cross-service trace mapping through the full ecosystem.

### 6.5 High-Frequency Telemetry: Dual-Stream Path

To support wearable device ingestion without overloading the centralized topic bus, telemetry processing splits into a Hot Path and a Warm Path.

```text
[ Wearable Device ]
        |
        +-- Hot Path (WebSockets) --> Time-Series Buffer --> cynthus-messaging aggregation
        |
        +-- Warm Path (AMQP) <-- Ingestion Worker (summarized snapshots)
                                          |
                                          v
                                  Azure Service Bus Spine
```

Raw continuous sensor data (live heart rate, CGM readings) arrives over WebSockets directly into the time-series buffer, bypassing the Service Bus. `cynthus-device` summarizes hot path data into structured time-slice snapshots and emits them onto the choreography bus as warm-path events.

### 6.6 Network Boundaries & Deployment Topology

Network isolation is enforced between domain segments in cloud deployment (Microsoft Azure):

- **`vnet-cynthus-core`:** Publicly routed subnet. Hosts `cynthus-core-api` and `cynthus-core-web`. Accepts external connections over HTTPS and WebSocket protocols.
- **`vnet-cynthus-intelligence`:** Private, dark subnet. No public IP allocations. No public endpoints. Hosts `cynthus-chat`, `cynthus-analysis`, and `cynthus-video`. Reachable only via Azure VNet Peering from Core.
- **`vnet-cynthus-health`:** DMZ subnet. Hosts `cynthus-health-api` and `cynthus-health-web`. Enforces regulatory validation and consent token verification before any data exchange.
- **Cross-VNet Communication:** High-frequency conversational token streams bypass Service Bus latency. `cynthus-core-api` routes user WebSocket sessions to `cynthus-chat` via private IP over the VNet Peering bridge. Internal AI-to-AI queries between `cynthus-chat` and `cynthus-analysis` run via synchronous gRPC within the private Intelligence namespace.

### 6.7 Global Message Envelope Structure

Every event published to any Service Bus topic must adopt the following standardized envelope schema. The `topic` field identifies which of the three topics the signal was routed to, enabling consumers to assert correct routing at runtime.

```json
{
  "signal_id": "string (UUIDv4 - global message instance)",
  "correlation_id": "string (UUIDv4 - cross-service trace identifier)",
  "timestamp": "string (ISO 8601 UTC Z-notation)",
  "sender_service": "string (originating microservice identifier)",
  "schema_version": "string (semantic version, e.g., '1.0.0')",
  "topic": "string (cynthus-topic-public | cynthus-topic-internal | cynthus-topic-audit)",
  "organization_id": "string (corporate tenant boundary key)",
  "workspace_id": "string (functional isolation partition key - present from Phase 1)",
  "payload": {
    "type": "object (domain-specific entity state structure)"
  }
}
```

---

## 7. Privacy, Compliance, and Security

### 7.1 Data Security

- **Encryption Standards:** AES-256 for data at rest. TLS 1.3 for data in transit.
- **PHI Isolation:** Protected Health Information is isolated within a dedicated, schema-isolated database layer (`cynthus-health-db`) implementing field-level encryption for all biometric and patient data.
- **Immutable Auditing:** Strict append-only logs record every instance of PHI data access and every hard-constraint profile mutation, maintained by `cynthus-audit`.

### 7.2 Hard-Constraint Mutation Auditing

Every write operation against a user's hard-constraint profile (allergen additions, removals, or modifications) must emit a timestamped, immutable audit event regardless of the requesting user's role. This is not a HIPAA requirement at the MVP stage but a foundational safety record. The event must capture the before-state, the after-state, the actor, and the timestamp.

### 7.3 Consent and AI Governance

- **Consent Bridge:** A secure authorization handshake allowing users to explicitly invite healthcare professionals or corporate stakeholders into specific, bounded telemetry data streams.
- **AI Transparency:** Automated disclosures accompany any AI-generated output or clinical analysis within a medical context, satisfying applicable state-level AI governance frameworks. All conversational logs must append a `model_configuration_hash` metadata block certifying the exact LLM configuration utilized.

---

## 8. Business and Domain Strategy

### 8.1 Domain Portfolio Routing

- `cynthus.app`: Primary consumer and commercial gateway hosting `cynthus-core-web`.
- `auth.cynthus.app`: Global multi-tenant authentication gateway managed by `cynthus-identity`. The `auth.` subdomain is intentionally preserved over `id.` for external developer clarity - OAuth and OIDC conventions make this endpoint immediately recognizable to third-party integrators and clinical partners without documentation.
- `cynthus.tech`: Open-source developer documentation, API architecture logs, and community contribution hub.
- `cynthus.health`: Secure B2B partner gateway hosting `cynthus-health-web` for clinical and enterprise stakeholders.
- `api.cynthus.health`: High-performance private API endpoint for biometric telemetry and clinical workflows via `cynthus-health-api`.

### 8.2 Subscription Tier Structure

Tiers follow the naming convention `{AccountType}-{Class}-{Level}`. Class codes: `MP` (Meal Planning), `IM` (Inventory Management), `MI` (Meal Planning + Inventory), `CM` (Clinical Monitoring), `DA` (Data Analytics). Basic tier is free forever across all account types. The complete pricing matrix, base tier resource limits, and booster pack add-ons are defined in the Cynthus Feature Registry (companion document).

#### Consumer - Meal Planning Only (MP)

- Residential-MP-Basic
  - Monthly: $0
  - Annual: $0
- Residential-MP-Premium
  - Monthly: $10
  - Annual: $100
- Residential-MP-Professional
  - Monthly: $20
  - Annual: $200
- Residential-MP-Enterprise
  - Monthly: $30
  - Annual: $300
- Commercial-MP-Basic
  - Monthly: $0
  - Annual: $0
- Commercial-MP-Premium
  - Monthly: $10
  - Annual: $100
- Commercial-MP-Professional
  - Monthly: $20
  - Annual: $200
- Commercial-MP-Enterprise
  - Monthly: $30
  - Annual: $300

#### Consumer - Inventory Management Only (IM)

- Residential-IM-Basic
  - Monthly: $0
  - Annual: $0
- Residential-IM-Premium
  - Monthly: $10
  - Annual: $100
- Residential-IM-Professional
  - Monthly: $20
  - Annual: $200
- Residential-IM-Enterprise
  - Monthly: $30
  - Annual: $300
- Commercial-IM-Basic
  - Monthly: $0
  - Annual: $0
- Commercial-IM-Premium
  - Monthly: $10
  - Annual: $100
- Commercial-IM-Professional
  - Monthly: $20
  - Annual: $200
- Commercial-IM-Enterprise
  - Monthly: $30
  - Annual: $300
- Supplier-IM-Basic
  - Monthly: $0
  - Annual: $0
- Supplier-IM-Premium
  - Monthly: $10
  - Annual: $100
- Supplier-IM-Professional
  - Monthly: $20
  - Annual: $200
- Supplier-IM-Enterprise
  - Monthly: $30
  - Annual: $300

#### Consumer - Meal Planning + Inventory (MI)

- Residential-MI-Basic
  - Monthly: $0
  - Annual: $0
- Residential-MI-Premium
  - Monthly: $15
  - Annual: $150
- Residential-MI-Professional
  - Monthly: $30
  - Annual: $300
- Residential-MI-Enterprise
  - Monthly: $50
  - Annual: $500
- Commercial-MI-Basic
  - Monthly: $0
  - Annual: $0
- Commercial-MI-Premium
  - Monthly: $15
  - Annual: $150
- Commercial-MI-Professional
  - Monthly: $30
  - Annual: $300
- Commercial-MI-Enterprise
  - Monthly: $50
  - Annual: $500

#### Provider - Clinical Monitoring (CM)

- Provider-CM-Basic
  - Monthly: $0
  - Annual: $0
  - Included Patients: 3 (view-only)
- Provider-CM-Premium
  - Monthly: $149
  - Annual: $1,490
  - Included Patients: 25
- Provider-CM-Professional
  - Monthly: $299
  - Annual: $2,990
  - Included Patients: 50

Per-patient booster: $8/patient/month above Premium threshold; $6/patient/month above Professional threshold.

#### Provider & Supplier - Data Analytics (DA)

- Provider-DA-Basic
  - Monthly: $0
  - Annual: $0
- Provider-DA-Premium
  - Monthly: $49
  - Annual: $490
- Provider-DA-Professional
  - Monthly: $99
  - Annual: $990
- Supplier-DA-Basic
  - Monthly: $0
  - Annual: $0
- Supplier-DA-Premium
  - Monthly: $29
  - Annual: $290
- Supplier-DA-Professional
  - Monthly: $79
  - Annual: $790

#### Partner

- Partner-Community
  - Monthly: $0
  - Annual: $0
  - Description: Open-source access, developer documentation, community forums.
- Partner-Integration
  - Monthly: $199
  - Annual: $1,990
  - Description: Device registry, promotion listings, standard API access, basic reporting.
- Partner-Strategic
  - Monthly: Custom
  - Annual: Custom
  - Description: Co-development, co-marketing, custom revenue-sharing, dedicated partner success.

#### Booster Packs (Add-Ons)

Booster packs expand a single resource dimension without a full tier upgrade. Representative examples:

- Residential
  - Booster: Group Size Pack (+5 members)
  - Unit Price: $0.99/month
- Residential
  - Booster: Library Pack (+1 library)
  - Unit Price: $0.99/month
- Residential
  - Booster: Location Pack (+1 location)
  - Unit Price: $1.99/month
- Commercial
  - Booster: Group Size Pack (+10 members)
  - Unit Price: $4.99/month
- Commercial
  - Booster: Location Pack (+1 location)
  - Unit Price: $4.99/month
- Provider
  - Booster: Patient Capacity (Premium)
  - Unit Price: $8.00/patient/month
- Provider
  - Booster: Patient Capacity (Professional)
  - Unit Price: $6.00/patient/month
- Supplier
  - Booster: Promotion Slots (+3 slots)
  - Unit Price: $9.99/month
- Partner
  - Booster: Device Registry Pack (+10 listings)
  - Unit Price: $49.00/month

Full booster catalog is defined in the Feature Registry (Section 6).

### 8.3 Revenue Drivers

- Partner bounties from hardware manufacturers for consumer wearable activations within the health ecosystem.
- Transaction fees from wholesale supply orders processed via partner merchant APIs.
- Slotting fees charged to partner grocers and wholesalers for preferential placement in the automated replenishment engine.
- Revenue-sharing models with medical practices utilizing automated RPM tracking.

---

## 9. Phased Rollout Plan

Each phase has a defined Astri capability version. Astri grows incrementally - each phase makes her smarter and more contextually aware without requiring full rewrites of prior capability.

**Schema forward-compatibility commitment (all phases):** All database schemas and API contracts include `organization_id` and `workspace_id` fields from initial Phase 1 deployment. These fields are auto-populated with defaults for single-user accounts in Phase 1 and become functionally active in Phase 3 when multi-user group workspaces are introduced.

**Entitlement forward-compatibility commitment (all phases):** JWT token claims include entitlement fields (`max_group_members`, `max_locations`, etc.) from Phase 1 deployment. Booster packs activated in Phase 3 (with `cynthus-billing-api`) will update these claims without requiring token structure changes.

---

### Phase 1 - Core MVP (Target: January 2027)

**Astri v1.0 - Single-Session Conversational Assistant.** Greets the user, gathers current preferences, and generates meal suggestions from the pre-assembled context payload (inventory snapshot + filtered recipe candidates + hard constraints). No cross-session memory. No group awareness. Streaming response via WebSocket.

**Services activated:**

- `cynthus-identity` - single-user auth, JWT with `workspace_id` and entitlement stubs
- `cynthus-core-api` - context assembly, WebSocket routing to Intelligence
- `cynthus-core-web` - consumer UI (React/Next.js SSR)
- `cynthus-inventory` - pantry CRUD, mutation tracking (<200ms latency requirement)
- `cynthus-recipe` - recipe library, constraint-filtered query API
- `cynthus-profile` - soft preferences + hard constraints, allergy hard-filter, mutation audit events
- `cynthus-chat` - Astri conversational engine (streaming)
- `cynthus-core-db`, `cynthus-trust-db`, `cynthus-intel-db` - schema-isolated persistence
- `cynthus-signal-bus`, `cynthus-signal-db` - local development emulators
- `cynthus-shared` - common `SignalMessageEnvelope` primitives

**Features delivered:** FT-MP-001-005, FT-AI-001, FT-AC-002, FT-AM-001

**Deferred:** All group, messaging, billing, clinical, commerce, and analytics features.

---

### Phase 2 - Inventory Intelligence & User Profile (Target: Q2 2027)

**Astri v1.5 - Profile-Persistent and Inventory-Aware.** Astri carries the full preference and constraint profile between sessions. She knows what is expiring in the user's inventory and factors it into meal suggestions proactively without being asked. Scheduled meal suggestion subscriptions activated.

**Services activated:**

- `cynthus-worker` - background data ingestion, OCR jobs, receipt scanning
- `cynthus-scheduler` - item expiry alerting, scheduled suggestion delivery

**Features delivered:** FT-IM-001-003, FT-IM-005, FT-IM-007, FT-RM-001-003, FT-AM-002, FT-RT-002, FT-MP-002

---

### Phase 3 - Group Workspaces, Messaging & Billing (Target: Q4 2027)

**Astri v2.0 - Group-Aware.** Astri understands group composition and all member preference and constraint profiles simultaneously. She generates meal suggestions that satisfy every member's hard constraints at once, can facilitate the voting flow conversationally, and maintains group context within a session.

**Services activated:**

- `cynthus-messaging-engine` - real-time WebSocket hub for group chat and interactive cards
- `cynthus-billing-api` - subscription management, booster pack entitlements, tier enforcement
- `cynthus-analysis` - initial activation for Harmony Score baseline computation

**Features delivered:** FT-MP-006-009, FT-GM-001-003, FT-IM-002, FT-IM-004, FT-IM-006, FT-IM-008, FT-MS-001-003, FT-BL-001, FT-AM-003, FT-AX-001-002

---

### Phase 4 - Engagements, Analytics & Recipe Import (Target: H1 2028)

**Astri v2.5 - Event-Planning Assistant with Early Predictive Logic.** Astri can plan engagements by cross-referencing attendee constraint matrices, detect meal fatigue patterns from voting history, and act as an impartial tie-breaker using inventory expiry data and historical preferences.

**Services activated:**

- `cynthus-logistics` - purchase manifests, smart list reorders, supplier cart sync
- `cynthus-partner-api` (read-only integration stubs) - groundwork for Phase 5 B2B

**Features delivered:** FT-MP-010, FT-RM-004, FT-EM-001-003, FT-CO-001, FT-RT-001, FT-TG-001, FT-DA-001-002

---

### Phase 5 - B2B Commercial Launch (Target: H2 2028)

**Astri v3.0 - Commerce-Aware.** Astri can initiate inventory reorders from registered suppliers, interact with supplier catalogs, understand commercial recipe scale (50+ portions), and assist with catering logistics and B2B planning workflows.

**Services activated:**

- `cynthus-partner-api` (full) - wholesale supplier integrations, slotting, bounty tracking
- `cynthus-comm-web` - partner and supplier commercial portal

**Features delivered:** FT-IM-009, FT-SR-001-003, FT-BL-002, FT-AM-004, FT-RP-002

---

### Phase 6 - Live Companion & Partner Platform (Target: H1 2029)

**Astri v3.5 - Real-Time Cooking Guide.** Astri provides step-by-step recipe guidance during active cooking sessions, responds to live queries mid-preparation, and coordinates with live human companions or providers sharing the same session. Hardware partner device integrations (smart scales, connected fridges) become active.

**Services activated:**

- `cynthus-video` - smart glasses HUD, real-time video frame processing, clock-face orientation guidance

**Features delivered:** FT-LC-001, FT-SR-004-005, FT-AM-005-007, FT-RP-003-004

---

### Phase 7 - Clinical Integration (Target: H2 2029 - Pending Regulatory Approval)

**Astri v4.0 - Clinical Intelligence.** Astri interprets biometric telemetry (CGM trends, heart rate patterns), correlates dietary patterns with health outcomes, generates clinician-grade dietary modification suggestions, and communicates findings in plain accessible language for both users and providers. All outputs carry AI transparency disclosures per applicable governance frameworks.

**Go-live contingent on:** Completed SaMD regulatory strategy review, BAA execution with provider partners, HIPAA penetration testing, and FDA SaMD classification determination for wearable-assisted RPM workflows.

**Services activated:**

- `cynthus-health-api` - clinical partner ingress, consent token verification
- `cynthus-health-web` - clinical dashboard for authorized providers
- `cynthus-device` - wearable device telemetry aggregator (hot/warm dual-stream path)
- `cynthus-audit` - immutable PHI access logging
- `cynthus-health-db` - PHI-isolated, field-level encrypted storage

**Features delivered:** FT-CL-001-002, FT-RM-005, FT-AC-001, FT-AC-003

---

### Phase 8 - Enterprise Scale & Compliance (Target: 2030)

**Astri v4.5 - Enterprise Intelligence.** Astri analyzes sentiment and preference patterns across full organizational tenancies, identifies systemic trends (e.g., meal fatigue across a corporate catering operation), generates proactive enterprise-level recommendations, and produces compliance-ready audit summaries on demand.

**Features delivered:** FT-RP-001, FT-DA-003

---

## 10. Developer Workflow and Technical Standards

### 10.1 Build Engine and Framework

- **Backend:** FastAPI (Python 3.11+) for all microservices. FastStream for Service Bus consumer and publisher bindings, initialized via FastAPI lifespan hooks.
- **Frontend:** React/Next.js with Server-Side Rendering (SSR) for `cynthus-core-web`, `cynthus-health-web`, and `cynthus-comm-web`.
- **Containerization:** All services containerized via Docker. Local developer environments composed via Docker Compose using `cynthus-signal-bus` and `cynthus-signal-db` emulators.
- **Message Bindings:** FastStream broker contexts must tie directly into FastAPI native startup lifespans. All subscription and publisher declarations are defined as global, thread-safe module-level variables.

### 10.2 One-Class-Per-Module Rule

All codebases must strictly enforce a one-class-per-module convention. This ensures clean git diffs, predictable import mapping, and scannable repository structure for community contributors.

### 10.3 Logging Verbosity Profile

- **Level:** Trace (verbose during development, configurable in production).
- **Structure:** Semantic structured logging.
- **Correlation Strategy:** Every asynchronous message handled by any service must append an explicit `correlation_id` within its top-level metadata envelope to enable cross-service trace mapping.

### 10.4 Hybrid Messaging Schema Strategy (ADR-004)

The messaging contract is distributed as two distinct Python wheel packages under a unified namespace:

- `cynthus-messaging-public` (Open-Source): Contains the `SignalMessageEnvelope[T]` generic envelope and shared primitive models. Open-source services parse private signal payloads as opaque `dict` buckets, validating only envelope headers (`organization_id`, `workspace_id`, `correlation_id`) to preserve multi-tenant security isolation without exposing closed-source payload schemas.
- `cynthus-messaging-internal` (Closed-Source / Private Azure Artifact): Extends the public package with deep, strongly-typed Pydantic model validation for all private signal namespaces. Available only to closed-source services authenticating against the private Azure Artifacts feed.

- Open-Source
  - Signal Classification: Public (`public.device.*`, `public.inventory.*`)
  - Validation Depth: Deep (strict Pydantic model)
- Open-Source
  - Signal Classification: Private (`internal.lifestyle.*`, `internal.video.*`)
  - Validation Depth: Opaque (`SignalMessageEnvelope[dict]`)
- Closed-Source
  - Signal Classification: Any
  - Validation Depth: Deep (strict Pydantic via internal wheel)

### 10.5 Community Contribution Boundary

Community contributions are accepted for all Cynthus Core and Cynthus Shared services. Schema contracts (message envelopes and API response models) will be published and frozen before the repository is opened for external contributions. Contributors may not merge changes that alter the `SignalMessageEnvelope` top-level structure, the `workspace_id` or `organization_id` field contracts, or the `cynthus-profile` hard-constraint API without maintainer approval.
