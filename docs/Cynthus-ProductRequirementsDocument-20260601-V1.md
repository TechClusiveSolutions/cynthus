# Product Requirements Document (PRD)

## Project: Cynthus Life Ecosystem

### 1. Executive Summary & Vision

**Cynthus Life** is an inclusive, distributed microservice ecosystem designed to serve as an intelligent domestic companion. Built on a foundation of "Life-Logistics," the system seamlessly coordinates four core pillars of a modern household: household asset and pantry management, remote patient monitoring (RPM) and clinical integration, secure family coordination, and AI-driven interactive companionship.

The system is designed with a strict **accessibility-first mindset**, ensuring that screen-reader efficiency, semantic clarity, and high-contrast layouts are treated as core architectural parameters rather than compliance updates.

The human interface of the system is **Astri**, a logic-first, empathetic AI chat persona that translates the complex telemetry of the household into clear, actionable human dialogue.

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
* **Scope:** Manages identity management, authentication, fine-grained role-based access control (RBAC), and cross-household tenancy boundaries.
* **Primary Boundary:** Issues cryptographically secure tokens mapping individual profiles to a shared household unit.


2. **`cynthus-core` (The Logistics & Engine Layer) — *Open-Source***
* **Scope:** Handles the system's physical data domains and user interfaces through four specialized services:
* `cynthus-api`: The public edge gateway handling direct interaction, session authentication, and secure routing with users' devices.
* `cynthus-web`: The user interface frontend rendering accessible web layouts.
* `cynthus-inventory`: Handles physical inventory management and transactional mutations.
* `cynthus-worker`: Executes resource-intensive asynchronous background tasks, and manages `cynthus-scheduler` routines for periodic system loops.




3. **`cynthus-intelligence` (The AI Engine Domain) — *Closed-Source***
* **Scope:** Hosts secure, proprietary analytical processors and the **Astri AI** chat runtime across two specialized services:
* `cynthus-analysis`: An autonomous AI agent handling heavy predictive data analysis, telemetry modeling, and trend calculations.
* `cynthus-chat`: A conversational chatbot handler optimized for live user interaction.




4. **`cynthus-portal` (The External Partner Gateway) — *Open/Closed Hybrid***
* **Scope:** Facilitates secure interaction with external healthcare providers and clinical partners through two dedicated layers:
* `cynthus-portal-api`: A backend endpoint enforcing clinical validation and partner access rules.
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

To illustrate the integration of components, consider the following domestic lifecycle sequence:

```
[User Device]      cynthus-api      cynthus-chat      Service Bus     cynthus-worker   cynthus-inventory
     |                  |                 |                |                 |                 |
     |--- Send Msg ---->|                 |                |                 |                 |
     |    (WebSocket)   |--- Proxy Msg -->|                |                 |                 |
     |                  |    (Intra-VNet) |                |                 |                 |
     |                  |                 |-- Publish ---->|                 |                 |
     |                  |<-- Stream Tx ---|   Event        |                 |                 |
     |<-- Render Text --|    (Tokens)     |   (accepted)   |                 |                 |
     |   (Real-time)    |                 |                |--- Dispatch --->|                 |
     |                  |                 |                |    Event        |--- Mutate Stock>|

```

1. **User Request:** A user communicates a meal selection adjustment via `cynthus-web` to `cynthus-api` over a secure WebSocket channel.
2. **AI Processing:** `cynthus-api` proxies the text stream inside the private VNet peering layer to `cynthus-chat`. `cynthus-chat` streams conversational tokens back to the user's screen in real time.
3. **Event Dispatch:** Simultaneously, `cynthus-chat` publishes an integration event to `cynthus-events-topic` with a property of `event_type = 'suggestion.accepted'`.
4. **Choreographed Reaction:** The Service Bus evaluates subscription rules. The `cynthus-core` subscription detects the event and dispatches the payload to **`cynthus-worker`**.
5. **Logistics Resolution:** `cynthus-worker` picks up the message, writes the updated meal parameters to the PostgreSQL instance, and broadcasts a downstream command to `cynthus-inventory` to decrement physical asset counts.

---

### 5. Unified Object Domain Model

To standardize data flow across the Service Bus event layout and the `cynthus-intelligence` translation layer, the system categorizes all domestic and clinical telemetry into three abstract domains:

#### 1. Signals (Data Inputs)

A **Signal** represents a raw, discrete data point ingested by the ecosystem from an external boundary.

* *Pantry Signal:* An RFID scan, manual entry, or barcode swipe indicating a change in food stock.
* *Clinical Signal:* A biometric payload ingested via webhook or Bluetooth API (e.g., blood glucose readings, blood pressure telemetry, step counters).
* *Environmental Signal:* Home sensor telemetry (e.g., ambient temp, entry alerts).

#### 2. Activities (Real-World Events)

An **Activity** is a real-world, localized event or operational task occurring within the domestic perimeter.

* *Domestic Activity:* Cooking a scheduled meal, running an inventory update, or processing a delivery window.
* *Task Activity:* An item on the family chore checklist assigned to a specific profile with an absolute expiration deadline.
* *Clinical Activity:* A recorded medication administration event or a planned therapy window.

#### 3. Engagements (Planned Interactions)

An **Engagement** represents a high-level, multi-profile interaction model managed by the orchestration layer.

* *The Harmony Score:* A quantitative metric evaluating household equilibrium by balancing workload distribution, individual wellness thresholds, and scheduled downtime.
* *Conflict Resolution Strategy:* The automated negotiation protocol triggered by Astri when scheduled events overlap (e.g., conflicting calendar windows, dietary mismatches during meal planning).
* *Provider Portal Telemetry:* A secure, read-only data view summarizing specific clinical Signals for export to a healthcare professional via `cynthus-portal-api`.

---

### 6. Functional Requirements Matrix

#### Module A: Cynthus-Auth (Identity & Tenancy)

* **Req A.1 - Household Boundaries:** The system must isolate data at the "Household Tenant" level. No cross-tenant data leaks are permitted on the shared Azure Service Bus topic.
* **Req A.2 - Granular RBAC:** Profiles within a household must support distinct role allocations (e.g., `Primary Caregiver`, `Care Recipient`, `Standard User`).
* **Req A.3 - Cryptographic Vault Isolation:** Access to clinical Signals inside `cynthus-intelligence` repositories requires a separate decryption handshake using user-derived keys, distinct from standard application tokens.

#### Module B: Cynthus-Core (Life-Logistics)

* **Req B.1 - Inventory Mutation Tracking:** The `cynthus-inventory` service must process pantry Signals with an absolute processing latency of less than 200ms to ensure real-time inventory tracking.
* **Req B.2 - The Smart List Engine:** When a pantry Signal flags an item as depleted, `cynthus-worker` must automatically append the asset to the household shopping registry, filtered by preferred merchant categories.
* **Req B.3 - Recipe Constraint Matching:** The engine must parse ingredients against a multi-profile allergen/dietary restriction array before rendering preparation suggestions.

#### Module C: Cynthus-Intelligence (The Astri AI Engine)

* **Req C.1 - Telemetry Anomaly Detection:** `cynthus-analysis` must continuously monitor incoming clinical Signals. If a biometric value breaches a predefined clinical threshold, the system must escalate the event to a priority alert notification published on the Service Bus.
* **Req C.2 - Non-Visual Dialogue Strategy:** All interface payloads returned by the `cynthus-chat` service must be structured to ensure seamless parsing by assistive technologies, avoiding layout elements that rely on spatial placement.
* **Req C.3 - Core Harmony Computation:** `cynthus-analysis` must evaluate historical Activity completion patterns and task balances once every 24 hours to generate the daily domestic Harmony index.

#### Module D: Cynthus-Portal (B2B Clinical Gateway)

* **Req D.1 - Read-Only HIPAA Auditing:** `cynthus-portal-api` must restrict external clinician connections to read-only views of authorized health signals. Every data access action must write an immutable entry to an independent secure audit log.
* **Req D.2 - Patient Consent Verification:** `cynthus-portal-api` must inspect token signatures issued by `cynthus-auth` before exposing any historical telemetry stream, ensuring active patient consent is validated per session.

---

### 7. Digital Footprint & Endpoint Strategy

To separate user contexts cleanly and prepare for enterprise expansion, the domain routing architecture is configured as follows:

* **`cynthus.app`**: The primary front-facing web space hosting `cynthus-web` for the consumer ecosystem.
* **`auth.cynthus.app`**: The global authentication gateway managed by `cynthus-auth`.
* **`cynthus.health`**: The secure B2B gateway hosting `cynthus-portal-web`, enabling external clinical partners to securely log in.
* **`api.cynthus.health`**: The private API endpoint processing high-performance biometric telemetry and conversational runtime requests through `cynthus-portal-api`.

---

### 8. Developer Workflow & Technical Standards

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

Every asynchronous message handled by the choreographer must append an explicit correlation identifier within the application metadata properties to map data flow transparently through `cynthus-auth`, `cynthus-core`, `cynthus-portal`, and `cynthus-intelligence`.
