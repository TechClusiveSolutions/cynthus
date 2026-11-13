## Master Product Requirements Document: Cynthus Life Ecosystem

Product Name: Cynthus (also referred to as Cynthus Life or Cynthus Life Ecosystem)
Parent Organization: Tech-Clusive Solutions, LLC
Document Version: 4.0 (March 2026)
Status: High-Fidelity Design Phase
Guiding Principle: Universal Design and Accessibility-First Architecture. Screen-reader efficiency, semantic clarity, and high-contrast layouts are treated as core architectural parameters rather than compliance updates.

---

## 1. Executive Summary & Vision

Cynthus is an inclusive, multimodal lifestyle companion and distributed microservice ecosystem designed for individuals, families, and businesses. Built on a foundation of "Life-Logistics," the platform seamlessly bridges daily kitchen management and asset tracking with professional healthcare monitoring and remote clinical integration. By utilizing a decoupled, choreographed microservice architecture, Cynthus coordinates four core pillars:

- Asset, pantry, supply, and food logistics management.

- Remote monitoring, healthcare wearable telemetry, and clinical integration.

- Secure data coordination across user, corporate tenant, and clinical workspaces.

- AI-driven interactive companionship and analytical lifestyle logic.

The primary human interface of the platform is Astri, a logic-first, empathetic AI chat persona that translates complex system telemetry and environmental data into clear, actionable human dialogue.

---

## 2. Strategic Objectives and Value Propositions

Cynthus establishes a unique "Platform Network Effect" by interconnecting three distinct user groups.

### 2.1 User Value (Individuals, Families, and Roommates)

- Accessible Autonomy: Provides 100% accessible autonomy for blind, deaf, and neurodivergent users.

- Decision Fatigue Reduction: Minimizes daily planning friction through AI-powered meal planning and the "Energy Banker" system.

- Safety Assurance: Enforces strict "Hard-Constraint" allergy and medical safety logic across all recommendations.

### 2.2 Provider Value (Doctors, Dietitians, and Clinical Staff)

- Automated Remote Monitoring: Automates Remote Patient Monitoring (RPM) data collection and tracks patient adherence.

- Clinical Decision Support: Delivers actionable clinical insights through pantry inventory analysis, symptom correlation, and biometric telemetry.

- Billing Optimization: Facilitates billable medical services via compliant 2026 CPT codes.

### 2.3 Partner Value (Hardware Manufacturers and Retailers)

- Wearable Device Utility: Enhances consumer wearable utility (e.g., Garmin, smart rings) by converting consumer fitness trackers into medical-grade tracking tools.

- Replenishment Revenue: Drives targeted fulfillment revenue for grocers and wholesalers through automated API integrations.

---

## 3. User Personas and Stories

Each persona demonstrates a unique touchpoint within the unified Cynthus architecture.

### 3.1 The Parent (Admin Workspace)

- Story: As a blind parent, I need to perform a "Budget Audit" using Cynthus's voice interface to ensure our $200 weekly grocery spend is on track while managing my children's nutritional needs.

### 3.2 The Medical User (Care Recipient)

- Story: As a user with Type 2 Diabetes, I need Cynthus to monitor my continuous glucose monitor (CGM) and cross-reference my pantry to suggest low-glycemic snacks when my levels are trending high.

### 3.3 The Small Business Owner (Caterer/Commercial Workspace)

- Story: As an event planner, I need Cynthus to scale a recipe for 50 people with varying allergies and automatically generate a wholesale order for my partner grocer.

---

## 4. Functional Requirements Matrix

Features are segmented into four priority levels (P1-P4). Priority 1 and Priority 2 features comprise the Free Tier, while Priority 3 and Priority 4 features map to Paid and Partner Tiers.

### 4.1 Module A: Cynthus-Auth (Identity & Tenancy)

- Req A.1 - Organizational & Workspace Boundaries (P1): The system must isolate data at the multi-tenant "Organization" level (`organization_id`) and further separate operations into distinct "Workspaces" (`workspace_id`) to replace standard household constraints. No cross-tenant data leaks are permitted on the shared message bus.

- Req A.2 - Granular Role-Based Access Control (P1): Profiles within a workspace must support distinct role allocations based on both RBAC and Attribute-Based Access Control (ABAC), accommodating designations such as Primary Caregiver, Care Recipient, Standard User, or commercial administrative managers.

- Req A.3 - Cryptographic Vault Isolation (P4): Access to sensitive clinical or private security Signals inside `cynthus-intelligence` repositories requires a separate decryption handshake using user-derived cryptographic keys, distinct from standard application tokens.

### 4.2 Module B: Cynthus-Core (Life-Logistics)

- Req B.1 - Basic Inventory & Mutation Tracking (P1): The system must support standard logging and predictive state tracking of pantry, fridge, and freezer items. The inventory engine must process physical asset mutations with an absolute processing latency of less than 200ms.

- Req B.2 - The Smart List Engine & Shared Grocery Sync (P2): The platform must maintain shared, real-time lists for households, roommates, and commercial operations. When an asset signal flags an essential item as depleted, background workers must automatically append it to the workspace procurement registry, filtered by preferred merchant categories.

- Req B.3 - Resource Constraint Matching & Allergy Hard-Filter (P1): The system must apply an absolute hard filter excluding unsafe or allergic ingredients from all meal and preparation suggestions. The engine must parse ingredients and resource profiles against a multi-profile constraint array (such as user allergens, client dietary restrictions, or commercial vehicle capacity constraints) before rendering suggestions.

- Req B.4 - Cynthus-AI "Daily Spark" (P1): Provide contextual, real-time meal suggestions based entirely on the user's current time of day and available ingredients.

- Req B.5 - Harmony Score (P2): Utilize AI-mediated conflict resolution to balance group meal voting, workload distribution, resource usage, operational completion patterns, and individual safety/wellness thresholds across a workspace.

- Req B.6 - Energy Banker (P2): Implement a recipe filtering mechanism based on current versus future energy levels, leveraging Spoon Theory logic to adapt to user fatigue.

- Req B.7 - Advanced Costing & Wholesale Logistics (P3): Provide real-time price-per-portion analysis, recipe scaling logic, volume logistics, and automatic wholesale order generation for small business owners and caterers.

### 4.3 Module C: Cynthus-Intelligence (Astri AI Engine)

- Req C.1 - Multimodal Wearable Integration & Anomaly Detection (P2): Support basic health statistic synchronization with wearable watches and smart rings. The analytical processor must continuously monitor incoming telemetry streams (blood glucose, heart rates, blood pressure, steps). High-frequency raw tracking lines must bypass the service bus via a dedicated ingestion buffer; if a calculated aggregate slice or biometric threshold breaches a predefined margin, the system must instantly emit a priority alert lifecycle event.

- Req C.2 - Non-Visual Dialogue Strategy & Sensory Profiles (P1): Provide real-time interface adaptations for screen readers (Blind), haptics and strobes (Deaf), and Zen Mode (Dyslexic). All interface payloads returned by the chat service must be structured to ensure seamless parsing by assistive technologies, avoiding layout elements that rely on spatial placement or geometric orientation.

- Req C.3 - Core Harmony Computation (P2): The intelligence engine must evaluate historical activity completion patterns, resource balances, and task loads once every 24 hours to generate the updated workspace Harmony index.

- Req C.4 - Advanced Wearable HUD (P3): Support smart glasses integrations to render step-by-step preparation, kitchen guidance, and logistics assistance.

### 4.4 Module D: Cynthus-Portal (B2B Clinical Gateway)

- Req D.1 - Read-Only HIPAA Auditing (P3): Restrict external clinical stakeholders and enterprise partners to read-only views of authorized signals. Every data access action must write an immutable entry to an independent secure audit log to meet strict HIPAA regulations.

- Req D.2 - Patient & Tenant Consent Verification (P3): The portal gateway must inspect token signatures issued by authentication services before exposing historical telemetry streams, ensuring active consent and access scopes are validated per session.

---

## 5. Medical and Clinical Specifications

### 5.1 Remote Patient Monitoring (RPM) Logic

- CPT 99454 & 99445 Tracking: Automate the logging of physiologic data transmissions, ensuring accurate tracking of active data transmission periods (requiring 2 to 15 days of data within a 30-day period).

- CPT 99470 Interaction Logging: Track and record the interactive communication time spent between clinical staff and patients within the portal framework to support practice billing.

- Clinical Triage Dashboards: Provide specialized, triage-based dashboard views that automatically flag patients exhibiting high-risk nutritional trends, biometric anomalies, or critical telemetry threshold breaches.

### 5.2 Symptom-Inventory Correlation

- The closed-source analytical engine must run correlation algorithms linking internal workspace inventory usage (such as the consumption of items with high-sodium content) with user-reported symptoms or wearable anomalies (such as reported evening pain or elevated heart rate spikes).

---

## 6. Technical & Architecture Specifications

The system is built upon an Event-Driven Choreography pattern utilizing Feature Slice Design (FSD) principles to maximize decoupling, fault tolerance, and atomic service boundaries.

### 6.1 Unified Object Domain Model

To standardize data flow across the ecosystem, all operational tracking and telemetry are categorized into three abstract domains:

- Signals (Data Inputs): Discrete data points ingested from external boundaries, including Supply Signals (RFID scans, manual inventory entry, barcode swipes), Clinical/Wearable Signals (continuous blood glucose, heart rates, blood pressure, step counters), and Environmental Signals (ambient temperature, shipping asset locations, entry alerts).

- Activities (Real-World Events): Localized events or tasks occurring within a workspace, including Logistics Activities (catering delivery windows, inventory updates), Task Activities (shared operational checklist items with absolute deadlines), and Clinical Activities (recorded medication administration or planned therapy windows).

- Engagements (Planned Interactions): High-level, multi-profile interaction models including the Harmony Score computation, Conflict Resolution Strategies (automated negotiation protocols for calendar overlaps, dietary mismatches, or asset constraints), and Provider Portal Telemetry (secure, read-only data exports).

### 6.2 Microservice Decomposition

The ecosystem is partitioned into five distinct repositories to isolate domain logic, licensing models, and runtime deployment contexts:

#### 1. `cynthus-auth` (The Identity Hub) - Open-Source Repository

- Service: SMH-Auth.

- Function: Manages multi-tenant identity management, token issuance, authentication, and fine-grained RBAC/ABAC access control. Maps individual user profiles to a shared corporate organization or workspace. Implements strict HIPAA audit logging.

#### 2. `cynthus-core` (The Logistics & Engine Layer) - Open-Source Repository

- Service: SMH-Web.

- Function: React/Next.js frontend user interface optimized for Server-Side Rendering (SSR) and strict universal accessibility layouts.

- Service: SMH-API.

- Function: The public edge gateway handling direct interaction, session authentication, WebSocket channels, and secure routing with client devices.

- Service: SMH-Inventory.

- Function: Predictive state manager handling physical asset mutations, logistics tracking, and transactional inventory state management.

- Service: SMH-Worker & SMH-Scheduler.

- Function: High-availability background processors executing resource-intensive asynchronous tasks (OCR, receipt scanning, data sync) and periodic scheduler routines for system loops.

#### 3. `cynthus-intelligence` (The AI Engine Domain) - Closed-Source Repository

- Service: Cynthus-AI (comprising `cynthus-analysis` and `cynthus-chat`).

- Function (`cynthus-analysis`): Autonomous AI agent executing heavy predictive data analysis, lifestyle logic, telemetry modeling, and daily Harmony index calculations.

- Function (`cynthus-chat`): Live conversational chatbot handler responsible for the Astri AI interface and real-time streaming token generation.

#### 4. `cynthus-portal` (The External Partner Gateway) - Open/Closed Hybrid Repository

- Service: SMH-Portal (comprising `portal-api` and `portal-web`).

- Function (`cynthus-portal-api`): Closed-source backend endpoint enforcing regulatory validation, partner access rules, per-session consent verification, and read-only clinical data queries.

- Function (`cynthus-portal-web`): Closed-source clinical gateway and administrative dashboard rendering secure data visualizations for authorized B2B stakeholders.

#### 5. `cynthus-infrastructure` - Open-Source Developer-Only Repository

- Components: Pairs `cynthus-store` (emulated block/table storage) with `cynthus-messaging` (the local container emulator for the messaging spine) to compose the local sandbox developer ecosystem.

### 6.3 Messaging Spine & Asynchronous Choreography

- Enterprise Messaging Spine: Managed natively via Azure Service Bus (with Redis utilized for high-speed cache and local message routing).

- Decoupled Interaction: Microservices do not issue direct commands to one another; they emit immutable facts (events) to a single centralized topic named `cynthus-events-topic`. Downstream services monitor dedicated subscriptions and apply localized SQL server-side filtering to ingest relevant data slices independently.

- Entity-Lifecycle Optimization Layer: To prevent event explosion, domains condense their topologies into four atomic state mutations attached to the message metadata: `created`, `updated`, `deleted`, and `snapshot`. Downstream processors evaluate the state snapshot inside the payload to compute deltas, minimizing subscription overhead.

### 6.4 Network Boundaries & Deployment Topology

Absolute network isolation is enforced between open-source components and closed-source intelligence engines when deployed to cloud infrastructure (such as Microsoft Azure):

- Public-Facing Core Network (`vnet-cynthus-core`): Hosts public edge nodes (`cynthus-api` and `cynthus-web`). It accepts external connections over secure HTTPS and WebSocket protocols.

- Isolated Intelligence Network (`vnet-cynthus-intelligence`): Holds no public IP allocations, contains no public endpoints, and remains dark to the internet. Hosts `cynthus-chat` (internal ingress only) and `cynthus-analysis`.

- Intra-Namespace Peering & Real-Time Communication: High-bandwidth, low-latency live chat loops bypass the Service Bus to maintain responsiveness. The user device connects to `cynthus-api` via WebSockets, and `cynthus-api` acts as an asynchronous reverse proxy communicating across a secure Azure VNet Peering bridge directly to the internal endpoint of `cynthus-chat`. Trend queries between `cynthus-chat` and `cynthus-analysis` run via synchronous internal HTTP/gRPC requests within the private namespace.

---

## 7. Privacy, Compliance, and Security

### 7.1 Data Security

- Encryption Standards: Full implementation of AES-256 for data at rest and TLS 1.3 for data in transit.

- PHI Isolation: To meet stringent healthcare guidelines, Protected Health Information (PHI) is isolated within a dedicated, schema-isolated database layer named `vesta_clinical` utilizing field-level encryption.

- Immutable Auditing: Strict, append-only logs (`audit.portal.created`) record every single instance of data access, meeting the compliance baselines of the 2026 HIPAA Security Rule.

### 7.2 Consent and AI Governance

- Consent Bridge: A secure authorization handshake allowing consumer users to explicitly "invite" healthcare professionals or corporate stakeholders into specific, bounded telemetry data streams.

- AI Transparency: Automated disclosures accompanying any AI-generated output or clinical analysis within a medical context, satisfying 2026 state-level AI governance frameworks (e.g., TRAIGA).

---

## 8. Business and Domain Strategy

### 8.1 Domain Portfolio Routing

The network routing topology isolates distinct business and technical contexts cleanly:

- `Cynthus.app`: The primary consumer and commercial gateway hosting the `cynthus-web` interface for standard workspaces.

- `auth.cynthus.app`: The global, multi-tenant authentication gateway managed exclusively by `cynthus-auth`.

- `Cynthusmealhub.com`: Defensive commercial domain registration reserved for market protection.

- `Cynthus.tech`: Specialized technical showcase hosting open-source code documentation, developer consultancies, and API architecture logs.

- `cynthus.health`: The secure B2B partner gateway hosting `cynthus-portal-web`, allowing external clinical and enterprise stakeholders to securely log in.

- `api.cynthus.health`: The high-performance private API endpoint processing biometric telemetry, continuous wearable summaries, and clinical conversational runtime requests through `cynthus-portal-api`.

### 8.2 Fee Schedule and Tier Tiers

- Basic Tier (Individual/Family Workspace): Free tier. Grants full access to all Priority 1 (P1) and Priority 2 (P2) features.

- Plus Tier (Power User Workspace): $4.99 per month. Includes advanced wearable HUD features, extended history tracking, and deeper AI insights.

- Enterprise Tier (SMB/Commercial Workspace/Caterer): $49.99 per month. Includes wholesale partner API integrations, volume logistics tracking, advanced costing matrices, and multi-profile workspace management.

- Provider Tier (Clinical Partner Gateway): $99.00 per month per practice/provider. Grants access to the closed-source SMH-Portal, clinical dashboards, and automated RPM billing compliance systems.

### 8.3 Revenue Drivers

- Partner "Bounties" collected from hardware manufacturers for consumer wearable device activations within the health ecosystem.

- Transaction fees calculated from wholesale supply orders processed via partner merchant APIs.

- Slotting fees charged to partner grocers and wholesalers for preferential placement within the automated replenishment engine.

- Revenue-sharing models established with medical practices utilizing automated RPM tracking software.

---

## 9. Developer Workflow and Technical Standards

### 9.1 Build Engine and Framework Preference

- Backend Compilation: All backend infrastructure compiles via command-line interface execution pathways utilizing the FastAPI framework running Python 3.11+.

- Containerization: Local environment components, store emulators (`cynthus-store`), and messaging containers (`cynthus-messaging`) spin up via structured Docker Compose layers.

- Message Loop Initialization: FastStream components handling service-to-service communication must tie directly into FastAPI's native startup lifespans using combined routing contexts (`event.lifespan`). Individual message layouts and subscriptions must be defined as global, thread-safe module-level variables.

### 9.2 Logging Verbosity Profile

To maintain explicit architectural insight across asynchronous distributed message processing loops, the system implements a strict diagnostic semantic logging policy:

- Trace Level: Verbose.

- Structure: Semantic Structured Logging.

- Correlation Strategy: Cross-Service Correlation GUID.

Every asynchronous message handled by the choreographer must append an explicit correlation identifier (`correlation_id`) within its top-level metadata envelope properties to map data flow transparently through `cynthus-auth`, `cynthus-core`, `cynthus-portal`, and `cynthus-intelligence`.

### 9.3 Global Message Envelope Structure

Every event message published on the `cynthus-events-topic` must adopt the following standardized top-level JSON envelope schema:

```json
{
  "event_id": "string (UUIDv4 Global Message Instance)",
  "event_type": "string (dot-notated topic identifier path, e.g., 'user.inventory.updated')",
  "lifecycle_action": "string (created | updated | deleted | snapshot)",
  "correlation_id": "string (UUIDv4 Cross-Service Tracking GUID)",
  "timestamp": "string (ISO 8601 UTC Z-notation Format)",
  "organization_id": "string (Global corporate tenant boundary key)",
  "workspace_id": "string (Contextual isolation boundary key replacing household constraints)",
  "actor_id": "string (Profile ID of user or system agent executing the mutation)",
  "payload": {
    "type": "object (Domain-specific entity state structure)"
  }
}

```
