# Product Requirements Document (PRD)

## Project: Cynthus Life Ecosystem

### 1. Executive Summary & Vision

**Cynthus Life** is an inclusive, distributed microservice ecosystem designed to serve as an intelligent companion for modern logistics and health monitoring. Built on a foundation of "Life-Logistics," the system seamlessly coordinates four core pillars: asset and pantry/supply management, remote monitoring and clinical integration, secure coordination across user spaces, and AI-driven interactive companionship.

The system is designed with a strict **accessibility-first mindset**, ensuring that screen-reader efficiency, semantic clarity, and high-contrast layouts are treated as core architectural parameters rather than compliance updates.

The human interface of the system is **Astri**, a logic-first, empathetic AI chat persona that translates the complex telemetry of the environment into clear, actionable human dialogue.

---

### 2. Architectural Overview (The Cynthus Framework)

The system leverages a **Choreographer Architecture** utilizing **Feature Slice Design (FSD)** principles to maximize decoupling, fault tolerance, and atomic service boundaries.

The entire system's asynchronous choreography is unified by an enterprise messaging spine managed via **Azure Service Bus**. Microservices do not directly command each other; instead, they emit immutable facts (events) to a centralized topic. Downstream services monitor dedicated subscriptions, applying localized filtering to process relevant data slices independently.

```
                                 +--------------------+
                                 |    Cynthus-Auth    |
                                 +---------+----------+
                                           | (JWT / Claims)
                                           v
+--------------------+            +------------------+            +----------------------+
|    Cynthus-Core    |<== AMQP ==>|  Azure Service   |<== AMQP ==>| Cynthus-Intelligence |
| (cynthus-api/web/  |            |       Bus        |            | (cynthus-chat/       |
|  inventory/worker) |            | (Choreographer)  |            |  analysis)           |
+--------------------+            +--------+---------+            +----------------------+
                                           |
                                           | AMQP (B2B Events)
                                           v
                                  +------------------+
                                  |  Cynthus-Portal  |
                                  | (portal-api/web) |
                                  +------------------+


```

#### Domain Topology & Repositories

The codebase is partitioned into five distinct, decoupled repositories to isolate domain logic, licensing models, and runtime contexts:

1. **`cynthus-auth` (The Identity Hub) — *Open-Source***
* **Scope:** Manages identity management, authentication, fine-grained role-based access control (RBAC), and cross-organizational tenancy boundaries.
* **Primary Boundary:** Issues cryptographically secure tokens mapping individual user profiles to a shared corporate organization or specific workspace.


2. **`cynthus-core` (The Logistics & Engine Layer) — *Open-Source***
* **Scope:** Handles physical data domains and user interfaces through four specialized services:
* `cynthus-api`: The public edge gateway handling direct interaction, session authentication, and secure routing with client devices.
* `cynthus-web`: The user interface frontend rendering accessible layouts.
* `cynthus-inventory`: Handles physical asset mutations and transactional inventory state management.
* `cynthus-worker`: Executes resource-intensive asynchronous background tasks and manages `cynthus-scheduler` routines for periodic system loops.




3. **`cynthus-intelligence` (The AI Engine Domain) — *Closed-Source***
* **Scope:** Hosts secure, proprietary analytical processors and the **Astri AI** chat runtime across two specialized services:
* `cynthus-analysis`: An autonomous AI agent handling heavy predictive data analysis, telemetry modeling, and trend calculations.
* `cynthus-chat`: A conversational chatbot handler optimized for live user interaction.




4. **`cynthus-portal` (The External Partner Gateway) — *Open/Closed Hybrid***
* **Scope:** Facilitates secure interaction with external healthcare providers, enterprise stakeholders, and clinical partners through two dedicated layers:
* `cynthus-portal-api`: A backend endpoint enforcing regulatory validation and partner access rules.
* `cynthus-portal-web`: An administrative and clinical dashboard interface rendering secure data visualization for authorized B2B stakeholders.




5. **`cynthus-infrastructure` (The Local Sandbox Layer) — *Open-Source Dev-Only***
* **Scope:** Composes the local developer ecosystem by pairing `cynthus-store` (emulated block/table storage) with `cynthus-messaging` (the local Azure Service Bus container emulator).



---

### 3. Network Boundaries & Deployment Topology

To protect proprietary intellectual property and maximize edge security, the ecosystem enforces absolute network isolation between open-source components and closed-source intelligence engines when deployed to cloud infrastructure (such as Microsoft Azure).

```
[ Public Internet ]
       |
       v  (HTTPS / WSS)
+-------------------------------------------------------+
| VNET-CYNTHUS-CORE                                     |
|  - cynthus-web                                        |
|  - cynthus-api  (Exposed Public Edge Gateway)         |
+-------------------------------------------------------+
       |
       |  Azure VNet Peering (Private IP Only)
       v  
+-------------------------------------------------------+
| VNET-CYNTHUS-INTELLIGENCE                             |
|  - cynthus-chat      (Internal Ingress Only)          |
|  - cynthus-analysis  (No Public Endpoint)             |
+-------------------------------------------------------+

```

#### 1. Public-Facing Core Network

The `vnet-cynthus-core` virtual network layer hosts user-facing edge nodes (`cynthus-api` and `cynthus-web`). It accepts external browser and device connections over secure HTTPS and WebSocket protocols.

#### 2. Isolated Intelligence Network

The `vnet-cynthus-intelligence` virtual network layer holds no public IP allocations and remains entirely dark to the public internet.

#### 3. Intra-Namespace Peering & Real-Time Communication

High-bandwidth, low-latency interactions bypass the asynchronous Service Bus to maintain strict thread responsiveness:

* **The Live Chat Loop:** The user's device communicates with `cynthus-api` via WebSockets. `cynthus-api` acts as an asynchronous reverse proxy, communicating across a secure **Azure VNet Peering** bridge directly to the internal endpoint of `cynthus-chat`.
* **The Trend Query Loop:** When `cynthus-chat` requires complex historical reports, it issues a synchronous internal HTTP/gRPC request to its neighbor, `cynthus-analysis`, entirely within the private namespace.

---

### 4. Asynchronous Signal & Messaging Workflow

While real-time conversation and data fetching happen over direct, private network paths, all systemic mutations, side effects, and decoupled domain cross-talk run through the **Azure Service Bus** using a unified event topic topology.

#### The Topic and Subscription Architecture

The ecosystem uses a single aggregate topic named `cynthus-events-topic`. Microservices attach a custom application metadata property (`event_type`) to every published message. Subscriptions act as virtual queues, utilizing server-side SQL filters to route specific message slices to individual services.

```
                                     +----------------------+
                                     | cynthus-events-topic |
                                     +----------+-----------+
                                                |
         +----------------------+---------------+---------------+----------------------+
         |                      |                               |                      |
         v                      v                               v                      v
[ cynthus-api-sub ]   [ cynthus-auth-sub ]          [ cynthus-inventory-sub ] [ cynthus-analysis-sub ]
         |                      |                               |                      |
  Filters for:           Filters for:                    Filters for:           Filters for:
  - meal.suggestion      - user.auth.request             - inventory.lookup.req - user.auth.response
                                                         - inventory.refreshed  - inventory.lookup.res

```

#### Step-by-Step Choreography Workflow Example

To illustrate the integration of components, consider the following lifecycle sequence:

```
[User Device]      cynthus-api      cynthus-chat      Service Bus     cynthus-worker   cynthus-inventory
     |                  |                 |                |                 |                 |
     |--- Send Msg ---->|                 |                |                 |                 |
     |    (WebSocket)   |--- Proxy Msg -->|                |                 |                 |
     |                  |    (Intra-VNet) |                |                 |                 |
     |                  |                 |-- Publish ---->|                 |                 |
     |                  |<-- Stream Tx ---|   Event        |                 |                 |
     |<-- Render Text --|    (Tokens)     |   (updated)    |                 |                 |
     |   (Real-time)    |                 |                |--- Dispatch --->|                 |
     |                  |                 |                |    Event        |--- Mutate Stock>|

```

1. **User Request:** A user communicates an operational adjustment via `cynthus-web` to `cynthus-api` over a secure WebSocket channel.
2. **AI Processing:** `cynthus-api` proxies the text stream inside the private VNet peering layer to `cynthus-chat`. `cynthus-chat` streams conversational tokens back to the user's screen in real time.
3. **Event Dispatch:** Simultaneously, `cynthus-chat` publishes an integration event to `cynthus-events-topic` utilizing the standard schema payload pattern (e.g., `lifecycle_action = 'updated'`).
4. **Choreographed Reaction:** The Service Bus evaluates subscription rules. The `cynthus-core` subscription detects the event and dispatches the payload to **`cynthus-worker`**.
5. **Logistics Resolution:** `cynthus-worker` picks up the message, writes the updated domain parameters to the persistence instance, and broadcasts a downstream command to `cynthus-inventory` to decrement or adjust physical asset counts.

---

### 5. Unified Object Domain Model

To standardize data flow across the Service Bus event layout and the `cynthus-intelligence` translation layer, the system categorizes all operational and tracking telemetry into three abstract domains:

#### 1. Signals (Data Inputs)

A **Signal** represents a raw, discrete data point ingested by the ecosystem from an external boundary.

* *Supply Signal:* An RFID scan, manual entry, or barcode swipe indicating a change in food or equipment stock.
* *Clinical/Wearable Signal:* A biometric payload ingested via webhook, direct API connectivity, or continuous wearable telemetry streams (e.g., blood glucose readings, heart rates, blood pressure telemetry, step counters).
* *Environmental Signal:* Ambient sensor telemetry (e.g., room temperature, shipping asset locations, entry alerts).

#### 2. Activities (Real-World Events)

An **Activity** is a real-world, localized event or operational task occurring within a workspace perimeter.

* *Logistics Activity:* Processing a catering delivery window, running an inventory update, or coordinating a scheduled resource.
* *Task Activity:* An item on a shared operational checklist assigned to a specific profile with an absolute expiration deadline.
* *Clinical Activity:* A recorded medication administration event or a planned therapy window.

#### 3. Engagements (Planned Interactions)

An **Engagement** represents a high-level, multi-profile interaction model managed by the orchestration layer.

* *The Harmony Score:* A quantitative metric evaluating workspace equilibrium by balancing workload distribution, resource usage, operational completion patterns, and individual safety/wellness thresholds.
* *Conflict Resolution Strategy:* The automated negotiation protocol triggered by Astri when scheduled events overlap (e.g., conflicting calendar windows, dietary or ingredient mismatches during meal planning, asset availability conflicts).
* *Provider/B2B Portal Telemetry:* A secure, read-only data view summarizing specific workspace or health Signals for export to a professional stakeholder via `cynthus-portal-api`.

---

### 6. Architectural Optimization & Schema Design

To ensure high-throughput processing, scale smoothly for enterprise SMB use-cases, and mitigate event explosion on the messaging spine, Cynthus enforces an **Entity-Lifecycle (State-Change) Schema Pattern** paired with a global Message Envelope.

#### 6.1 Global Message Envelope Structure

Rather than flat or loosely structured payloads, every event message on the `cynthus-events-topic` must adopt a standardized top-level envelope containing cross-service tracing metadata and tenant routing vectors.

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

#### 6.2 The Entity-Lifecycle Optimization Layer

Instead of generating distinct event topics for every discrete human action (e.g., adding a tag, removing a tag, adding an item, removing an item), domains condense their topologies into four atomic state mutations: `created`, `updated`, `deleted`, and `snapshot`.

Downstream processors (such as `cynthus-analysis` or background workers) evaluate the current state snapshot inside the payload to compute deltas or drive internal updates, significantly reducing subscription overhead on the infrastructure bus.

---

### 7. Functional Requirements Matrix

#### Module A: Cynthus-Auth (Identity & Tenancy)

* **Req A.1 - Organizational & Workspace Boundaries:** The system must isolate data at the "Organization" level (`organization_id`) for multi-tenant protection, and further separate operations into distinct "Workspaces" (`workspace_id`). No cross-tenant data leaks are permitted on the shared bus.
* **Req A.2 - Granular RBAC:** Profiles within a workspace must support distinct role allocations (e.g., `Primary Caregiver`, `Care Recipient`, `Standard User`, or commercial equivalents like administrative managers).
* **Req A.3 - Cryptographic Vault Isolation:** Access to sensitive clinical or private security Signals inside `cynthus-intelligence` repositories requires a separate decryption handshake using user-derived cryptographic keys, distinct from standard application tokens.

#### Module B: Cynthus-Core (Life-Logistics)

* **Req B.1 - Inventory Mutation Tracking:** The `cynthus-inventory` service must process asset Signals with an absolute processing latency of less than 200ms to ensure real-time logistics tracking.
* **Req B.2 - The Smart List Engine:** When an inventory signal flags an essential tracked asset as depleted, `cynthus-worker` must automatically append the asset to the workspace procurement registry, filtered by preferred merchant or vendor categories.
* **Req B.3 - Resource Constraint Matching:** The engine must parse ingredients and resource profiles against a multi-profile constraint array (such as user allergens, client dietary restrictions, or vehicle capacity constraints) before rendering preparation suggestions.

#### Module C: Cynthus-Intelligence (The Astri AI Engine)

* **Req C.1 - High-Frequency Telemetry & Anomaly Detection:** `cynthus-analysis` must continuously monitor incoming streams. For continuous data tracking like wearables, high-frequency raw lines bypass the service bus via a dedicated ingestion buffer path. If a calculated aggregate slice or direct biometric threshold breaches a predefined margin, the system must instantly emit a priority alert lifecycle event on the Service Bus.
* **Req C.2 - Non-Visual Dialogue Strategy:** All interface payloads returned by the `cynthus-chat` service must be structured to ensure seamless parsing by assistive technologies, avoiding layout elements that rely on spatial placement or geometric orientation.
* **Req C.3 - Core Harmony Computation:** `cynthus-analysis` must evaluate historical Activity completion patterns, resource balances, and task loads once every 24 hours to generate the workspace Harmony index.

#### Module D: Cynthus-Portal (B2B Clinical & Enterprise Gateway)

* **Req D.1 - Read-Only HIPAA Auditing:** `cynthus-portal-api` must restrict external stakeholder and clinician connections to read-only views of authorized signals. Every single data access action must write an immutable entry to an independent secure audit log (`audit.portal.created`).
* **Req D.2 - Patient & Tenant Consent Verification:** `cynthus-portal-api` must inspect token signatures issued by `cynthus-auth` before exposing any historical telemetry stream, ensuring active consent and access scopes are validated per session.

---

### 8. Digital Footprint & Endpoint Strategy

To separate user contexts cleanly and prepare for enterprise expansion, the domain routing architecture is configured as follows:

* **`cynthus.app`**: The primary front-facing web space hosting `cynthus-web` for consumer and SMB application workspaces.
* **`auth.cynthus.app`**: The global authentication gateway managed by `cynthus-auth`.
* **`cynthus.health`**: The secure B2B gateway hosting `cynthus-portal-web`, enabling external clinical and operational enterprise partners to securely log in.
* **`api.cynthus.health`**: The private API endpoint processing high-performance biometric telemetry, continuous wearable summaries, and conversational runtime requests through `cynthus-portal-api`.

---

### 9. Developer Workflow & Technical Standards

* **Build Engine & Framework Preference:** All backend infrastructure compiles via the command-line interface execution pathways utilizing the FastAPI framework running Python 3.11+. Local environment components spin up via structured Docker Compose layers.
* **Message Loop Initialization:** FastStream components handling service-to-service communication must tie into FastAPI's native startup lifespans using combined routing contexts (`event.lifespan`). Individual message layouts and subscriptions must be defined as global, thread-safe module-level variables.
* **Logging Verbosity Profile:** To maintain clear architectural insight across asynchronous distributed message processing loops, the system implements a strict diagnostic logging policy:

```json
{
  "TraceLevel": "Verbose",
  "Structure": "SemanticStructuredLogging",
  "CorrelationStrategy": "CrossServiceCorrelationGuid"
}

```

Every asynchronous message handled by the choreographer must append an explicit correlation identifier (`correlation_id`) within its top-level metadata properties to map data flow transparently through `cynthus-auth`, `cynthus-core`, `cynthus-portal`, and `cynthus-intelligence`.
