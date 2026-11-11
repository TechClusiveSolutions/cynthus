# Architectural Design Document (ADD)

Project: Cynthus Life Ecosystem

Architecture Pattern: Choreographer (Event-Driven Microservices)

Design Methodology: Component-Driven Engineering (Backend FSD Adaptation)

Target Runtime: Python 3.11+ / FastAPI / FastStream

Messaging Backbone: Azure Service Bus (AMQP)

---

## 1. Document Purpose & Scope

This Architectural Design Document (ADD) serves as the definitive engineering blueprint for implementing the Cynthus Life Ecosystem. It translates the functional boundaries, compliance requirements, enterprise tenancy rules, and non-visual user experiences defined in the Product Requirements Document (PRD) into a strict technical implementation specification.

The technical architecture balances high-throughput logistics, continuous device streams, and multi-tenant isolation with remote monitoring telemetry constraints, physical database partitioning, private network separation, and strict HIPAA audit accountability.

---

## 2. System Architecture & Topology

The Cynthus Life Ecosystem utilizes an asynchronous Choreographer Architecture. Individual microservices interact implicitly by broadcasting immutable facts (signals) to a centralized enterprise messaging spine rather than orchestrating downstream dependencies via direct commands.

### 2.1 Deployment Network Boundaries

To protect proprietary intelligence intellectual property and prevent exposure of clinical, corporate, or financial operational resources, the system partitions cloud network space into isolated Azure Virtual Networks (VNets).

```
                                  [ Public Internet ]
                                           |
       +-----------------------------------+-----------------------------------+
       | (HTTPS / WSS via cynthus.app)                                         | (HTTPS via cynthus.health)
       v                                                                       v
+-------------------------------------------------------+               +-------------------------------------------------------+
| VNET-CYNTHUS-CORE                                     |               | VNET-CYNTHUS-PORTAL                                   |
| (Public Edge Gateway Boundary - Open Source Core)     |               | (External Clinical Gateway Boundary - Closed Source)  |
|                                                       |               |                                                       |
|  +--------------------+       +--------------------+  |               |  +--------------------+       +--------------------+  |
|  | cynthus-core-web   |       | cynthus-core-api   |  |               |  | cynthus-portal-web |       | cynthus-portal-api |  |
|  +--------------------+       +--------------------+  |               |  +--------------------+       +--------------------+  |
|                        \               |              |               |                        \               |              |
+-------------------------\--------------|--------------+               +-------------------------\--------------|--------------+
                           \             |                                                         \             |
                            \            | Azure VNet Peering (Private IP Only)                     \            | AMQP (B2B Events)
                             v           v                                                           v           v
+-------------------------------------------------------------------------------------------------------+        |
| VNET-CYNTHUS-INTELLIGENCE (Private Closed-Source Brains Boundary)                                     |        |
|                                                                                                       |        |
|  +--------------------+       +--------------------+       +--------------------+                     |        |
|  |    cynthus-chat    |====>  |  cynthus-analysis  |====>  |   cynthus-vision   |                     |        |
|  |  (Astri Chat Core) | gRPC  | (Predictive Logic) | gRPC  | (Smart Glasses HUD)|                     |        |
|  +--------------------+       +--------------------+       +--------------------+                     |        |
|                                                                                                       |        |
+-------------------------------------------------------------------------------------------------------+        |
                                         ^                                                                       |
                                         |                                                                       |
                                         +----------------------- AMQP (System Event Spine) ---------------------+
                                         |                                                                       |
                                         v                                                                       v
                               +-----------------------------------------------------------------------------------+
                               |                                Azure Service Bus                                  |
                               |                                 (Choreographer)                                   |
                               +-----------------------------------------------------------------------------------+

```

* `VNET-CYNTHUS-CORE`: Publicly routed subnet hosting consumer and small-to-medium business (SMB) frontend traffic (`cynthus-core-web`) and edge processing routers (`cynthus-core-api`). It handles public ingress, routes media channels via `cynthus-messaging-engine`, and houses the open-source microservices.
* `VNET-CYNTHUS-INTELLIGENCE`: Private, dark subnet containing no public IP allocations. It isolates closed-source proprietary analytical, conversational, and computer vision engines (`cynthus-chat`, `cynthus-analysis`, and `cynthus-vision`).
* `VNET-CYNTHUS-PORTAL`: Demilitarized subnet hosting external healthcare provider and clinical partner interfaces (`cynthus-portal-web` and `cynthus-portal-api`). It enforces regulatory validation and clinical partner access controls before data exchange.
* Cross-VNet Communication: High-frequency conversational token streams bypass Azure Service Bus latency. Instead, `cynthus-core-api` handles persistent user connections and routes data streams to `cynthus-chat` via private IP routing over an established Azure VNet Peering bridge.

### 2.2 Domain Topology & Repositories

The codebase is partitioned into distinct repositories to isolate domain logic, licensing models, and deployment runtimes:

* `cynthus-identity` (*Closed-Source*): Houses the `cynthus-identity-api` microservice. It manages multi-tenant access control, cryptographic verification, token generation, and the core Identity and Access Management (IAM) state models.
* `cynthus-core` (*Open-Source*): Governed by the open-source community, this layer handles physical data domains, logistics foundations, and interfaces through highly focused services:
* `cynthus-core-api`: Direct public HTTPS/REST entry point.
* `cynthus-core-web`: Fully accessible, semantic consumer user interface renderer.
* `cynthus-inventory`: Tracks physical pantry spaces, storage zones, shelf allocations, and item weights.
* `cynthus-recipe`: Manages libraries, multi-recipe mappings, external web scraping, and receipt/photo OCR parsing loops.
* `cynthus-logistics`: Coordinates purchase manifests, automated reorders, and external supplier cart syncs.
* `cynthus-messaging-engine`: Dedicated real-time WebSocket hub routing text chats and WebRTC signaling metadata.
* `cynthus-scheduler`: Background engine processing cron tasks, item expiration windows, and time-based tasks.
* `cynthus-worker`: Handles background data formatting and parallel ingestion tasks.


* `cynthus-intel` (*Closed-Source*): Hosts secure, proprietary analytical brains and computer vision systems:
* `cynthus-analysis`: Computes household harmony indices, voting patterns, and predictive lifestyle metrics.
* `cynthus-chat`: Runtime for Astri, managing multi-agent prompt matrices and streaming conversational tokens.
* `cynthus-vision`: Processes smart glasses real-time video frames to calculate spatial coordinates and recipe errors.


* `cynthus-portal` (*Closed-Source*): Facilitates secure interaction with external healthcare stakeholders via `cynthus-portal-api` (provider telemetry bridge) and `cynthus-portal-web` (clinical remote care interface).
* `cynthus-commerce` (*Closed-Source*): [NEW] Contains `cynthus-billing-api` and `cynthus-partner-portal`. It manages monetization structures, payment processing, subscription component boosters, supplier lead tracking, and merchant advertisements.
* `cynthus-audit` (*Closed-Source*): Houses `cynthus-audit-api`, which logs immutable audit facts to guarantee HIPAA compliance.
* `cynthus-infra` (*Open-Source Dev-Only*): Composes the local developer container playground by pairing `cynthus-store` (SQL Server storage backend) with `cynthus-messaging` (local Azure Service Bus emulator container).

---

## 3. Data Isolation, Identity & Tenancy Strategy

### 3.1 Logical Multi-Tenancy Hierarchy

Multi-tenancy is enforced strictly across all data layers, storage systems, and messaging topics using a two-tier enterprise structure:

* `organization_id` (The Corporate Tenant Boundary): Maps to the global corporate or enterprise contract account (e.g., an event planning agency, commercial distributor, or healthcare provider). It owns global identity mappings and master compliance controls.
* `workspace_id` (The Functional Isolation Key): Replaces localized household boundaries. A single organization may provision dozens of independent workspaces to isolate distinct clients, departments, or specific remote tracking environments. Every event message must carry these keys to prevent cross-tenant data visibility.

### 3.2 Hybrid RBAC and ABAC Hierarchy

`cynthus-identity-api` issues cryptographically signed JSON Web Tokens (JWT) containing standard role claims alongside environmental attribute contexts (Attribute-Based Access Control) to evaluate constraints like active session consent and active workspace profile parameters:

* `Primary Caregiver` / `Workspace Administrator`: Full administrative rights, including checklist/task delegation, inventory base management, telemetry visibility, and external partner gateway authorizations.
* `Care Recipient` / `Client Contributor`: Read-write access to assigned tasks, basic chatbot capabilities, and localized telemetry data inputs.
* `Standard User` / `Team Member`: Read-write access to core logistics (pantry/supply mutations, general scheduling, planning configurations) without portal override permissions.

### 3.3 Database Partitioning & PHI Isolation

To satisfy strict medical-grade data isolation requirements, the persistence layer utilizes isolated database paradigms:

* General Logistics Data: Stored in transactional schemas handling core logistics, inventory, and task activities.
* Protected Health Information (PHI): Completely isolated within a dedicated database named `vesta_clinical`. This database layer implements field-level encryption for all biometric telemetry and patient data, satisfying the 2026 HIPAA Security Rule.

### 3.4 Cryptographic Vault Isolation Handshake

Processing sensitive workspace or clinical telemetry requires a localized key exchange mechanism independent of standard API access tokens. When `cynthus-intelligence` services process secure telemetry arrays, an ephemeral runtime handshake handles decryption using user-derived keys supplied during the individual session via `internal.system.handshake.established` patterns.

---

## 4. Messaging, Component & Signal Contracts

The messaging system consolidates fine-grained task events into an optimized Component-Driven Schema Pattern utilizing a unified top-level namespace (`cynthus.messaging`).

### 4.1 Development Layout: Shared Common Kernel Models

To ensure clean development workflows, easily scannable git diffs, and predictable import mapping, all codebases must strictly enforce a one-class-per-module rule. Primitives used across both public open-source repos and closed proprietary modules are isolated in a shared dependency wheel library called `MessagingCommon`.

```text
cynthus-messaging-common/
+-- src/
    +-- cynthus/
        +-- messaging/
            +-- shared/                        # Common Polymorphic Kernel
                +-- actor_model.py             # Class: ActorModel (IAM sub-object)
                +-- resource_model.py          # Class: ResourceModel (Polymorphic asset context)
                +-- signal_message_envelope.py # Class: SignalMessageEnvelope[T]

```

The `ActorModel` and `ResourceModel` structures completely eliminate the data-blindness bottleneck. By passing a resource's explicit type and operational context in the message, downstream consumers (such as `cynthus-billing-api` or Astri) process the event context asynchronously without executing expensive synchronous database lookups.

### 4.2 Hybrid Codebase Boundary Enforcement

To support open-source infrastructure routing without exposing closed-source intellectual property, the global common spine implements a generic type structure with a runtime default fallback.

Open-source microservices handling private signals parse them as opaque read-only buckets (`SignalMessageEnvelope[dict]`). They fully validate multi-tenant isolation routing context headers (`organization_id`, `workspace_id`) but do not inspect the proprietary data body nested inside, eliminating public intellectual property leakage.

```markdown
| Ingesting Service Type | Inbound Signal Classification | Pydantic Validation Binding Depth |
| :--- | :--- | :--- |
| Open-Source Service | Public Component (`public.device.*`, `public.group.*`) | Deep Validation (Strict Pydantic Model) |
| Open-Source Service | Private Component (`internal.lifestyle.*`, `internal.video.*`) | Opaque Validation (`SignalMessageEnvelope[dict]`) |
| Closed-Source Service | Any Component Classification | Deep Validation (Strict Pydantic Model via Internal Wheel) |

```

### 4.3 Unified Service Ingestion & Dispatch Matrix

```markdown
| Component Domain | Namespace | Core Publishers | Core Consumers |
| :--- | :--- | :--- | :--- |
| `identity` *(Private)*| `public.identity.*` | `cynthus-identity-api` | `cynthus-core-api`, `cynthus-inventory`, `cynthus-billing-api` |
| `device` *(Public)* | `public.device.*` | `cynthus-worker` | `cynthus-analysis`, `cynthus-portal-api`, `cynthus-chat` |
| `inventory` *(Public)*| `public.inventory.*` | `cynthus-inventory` | `cynthus-core-api`, `cynthus-analysis`, `cynthus-logistics` |
| `recipe` *(Public)* | `public.recipe.*` | `cynthus-recipe` | `cynthus-core-api`, `cynthus-chat` |
| `logistics` *(Public)*| `public.logistics.*` | `cynthus-logistics`, `cynthus-partner-portal`| `cynthus-partner-portal`, `cynthus-billing-api` |
| `group` *(Public)* | `public.group.*` | `cynthus-messaging-engine`, `cynthus-core-api` | `cynthus-core-api`, `cynthus-chat`, `cynthus-analysis` |
| `user` *(Public)* | `public.user.*` | `cynthus-core-api` | `cynthus-analysis`, `cynthus-chat` |
| `audit` *(Private)* | `internal.audit.*` | `cynthus-portal-api`, `cynthus-identity-api` | `cynthus-audit-api` |
| `chat` *(Private)* | `internal.chat.*` | `cynthus-chat` | `cynthus-analysis`, `cynthus-core-api` |
| `lifestyle` *(Private)*| `internal.lifestyle.*`| `cynthus-analysis` | `cynthus-chat` |
| `video` *(Private)* | `internal.video.*` | `cynthus-messaging-engine`, `cynthus-vision` | `cynthus-vision`, `cynthus-chat`, `cynthus-core-api` |
| `system` *(Private)* | `internal.system.*` | `cynthus-identity-api`, `cynthus-billing-api` | `cynthus-analysis`, `cynthus-identity-api`, `cynthus-core-api` |

```

---

## 5. High-Frequency Telemetry Ingestion Architecture (The Dual-Stream Path)

To support wearable device ingestion without overloading the centralized topic bus, the system splits telemetry processing into a Hot Path and a Warm/Choreography Path:

```
[ Wearable / Glasses Peripheral ]
              |
              +---> (Hot Path: WebSockets / WebRTC Video) ---> [ High-Throughput Buffer / Time-Series DB / cynthus-vision ]
              |                                                                        | (Aggregation Window / Frame Processing)
              |                                                                        v
              +---> (Choreography Path: AMQP) <--- [ Ingestion Worker / cynthus-messaging-engine ]
                                                                   |
                                                                   v (Converts to Lifecycles)
                                                          Azure Service Bus Spine

```

1. The Hot Path: Continuously streaming sensors (such as live heart rate tracking, high-frequency wearable biometric telemetry, or smart glasses real-time video streams) push raw data intervals over WebSockets or WebRTC directly to high-throughput time-series buffers or the `cynthus-vision` pipeline, bypassing Azure Service Bus.
2. The Warm Path: Ingestion workers summarize hot path data into structured time-slice snapshots (`public.device.telemetry.streamed`) or emit instant computer vision threat flags (`internal.video.anomaly.detected`) onto the core choreography bus.

---

## 6. Technical Implementation Blueprint (FastAPI + FastStream)

Per system standards, the following primitives declare the global schema boundaries. To expose individual modules cleanly without forcing deep consumer imports, package `__init__.py` files are utilized as public API facade layers.

### `shared/actor_model.py`

```python
# cynthus/messaging/shared/actor_model.py
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class ActorType(str, Enum):
    USER = "USER"
    GROUP = "GROUP"
    PROVIDER = "PROVIDER"
    SUPPLIER = "SUPPLIER"
    AI_AGENT = "AI_AGENT"
    SYSTEM = "SYSTEM"

class ActorModel(BaseModel):
    """The polymorphic representation of an identity interacting within the IAM fabric."""
    id: str = Field(..., description="Unique identification token.")
    type: ActorType = Field(..., description="Structural classification enum.")
    role: str = Field(..., description="Operational context mask (e.g., LEGAL_GUARDIAN).")
    acting_on_behalf_of: Optional[str] = Field(None, description="Optional root parent user context.")

```

### `shared/resource_model.py`

```python
# cynthus/messaging/shared/resource_model.py
from enum import Enum
from pydantic import BaseModel, Field

class ResourceType(str, Enum):
    INVENTORY_LOCATION = "INVENTORY_LOCATION"
    INVENTORY_SHELF = "INVENTORY_SHELF"
    RECIPE_LIBRARY = "RECIPE_LIBRARY"
    SERVICE_REGISTRY = "SERVICE_REGISTRY"
    ENGAGEMENT_SPACE = "ENGAGEMENT_SPACE"
    USER_GROUP = "USER_GROUP"

class ResourceModel(BaseModel):
    """The polymorphic definition of any tracked asset partition in the ecosystem."""
    id: str = Field(..., description="The unique underlying reference key.")
    type: ResourceType = Field(..., description="Asset class discriminator enum.")
    role: str = Field(..., description="Functional sub-context designation.")

```

### `shared/signal_message_envelope.py`

```python
# cynthus/messaging/shared/signal_message_envelope.py
from datetime import datetime, timezone
from typing import Generic, TypeVar, Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict

PayloadT = TypeVar("PayloadT", bound=Any, default=Any)

class SignalMessageEnvelope(BaseModel, Generic[PayloadT]):
    """The immutable common structural envelope published across the Service Bus."""
    model_config = ConfigDict(frozen=True, populate_by_name=True)
    
    signal_id: UUID = Field(default_factory=uuid4)
    correlation_id: UUID = Field(..., description="Trace ID tracking cross-service interactions.")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sender_service: str = Field(..., description="The microservice binary that emitted the signal.")
    schema_version: str = Field("1.0.0", description="Semantic layout version.")
    
    organization_id: str = Field(..., description="Corporate tenant boundary context.")
    workspace_id: str = Field(..., description="Functional isolation partition key.")
    payload: PayloadT

```

### FastAPI Unified Lifespan Structural Pattern

```python
# Inside downstream application runtimes (e.g., cynthus-core-api)
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

logger = logging.getLogger("cynthus.infra")

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """Manages thread-safe FastStream broker lifespan hooks over the service run."""
    logger.info("Initializing FastStream Core Broker contexts on Azure Service Bus connection.")
    yield
    logger.info("De-initializing FastStream broker connections cleanly.")

app = FastAPI(lifespan=lifespan)

```

---

## 7. Regulatory Compliance, Auditing & Verification

### 7.1 HIPAA Compliance Safeguards (`cynthus-portal`)

To maintain end-to-end alignment with regulatory constraints, the B2B portal API gateway restricts external connections to read-only paradigms. Any data retrieval routine targeting telemetry registers verification steps:

```
[External Partner]           cynthus-portal-api            cynthus-identity-api         cynthus-audit-api
         |                           |                             |                            |
         |--- Request Telemetry ---->|                             |                            |
         |                           |--- Validate Permission ---->|                            |
         |                           |<-- Context Validated -------|                            |
         |                           |                                                          |
         |                           |--- Log Immutable Access Fact --------------------------->|
         |                           |    (internal.audit.access.logged)                        |
         |<-- Stream Read-Only Data -|                                                          |

```

1. Consent Token Verification: The inbound bearer token signature is evaluated against `cynthus-identity-api` public cryptographic certificates to ensure valid user authorization, active clinician access scope, and active workspace profile parameters exist for the active session.
2. Immutable Audit Emission: Prior to transmitting the requested metrics, `cynthus-portal-api` blocks response execution until an event fact of type `internal.audit.access.logged` is successfully committed to the `cynthus-audit-api` tracking ledger.

### 7.2 AI Governance & Compliance Transparency

To satisfy 2026 state-level AI governance laws (such as TRAIGA), any automated clinical insights, lifestyle assessments, or conversational responses generated by `cynthus-intelligence` services must incorporate structural compliance parameters. The conversational logging structure must append an automated transparency metadata block (`model_configuration_hash`) certifying the exact LLM configuration model utilized, explicitly disclosing AI usage within any medical context.

### 7.3 Endpoint Routing Matrix

Ecosystem routing boundaries strictly isolate corporate, consumer, and clinical traffic profiles at DNS edge routers:

* `cynthus.app`: The public interface gateway hosting `cynthus-core-web` for standard user and consumer application workspaces.
* `auth.cynthus.app`: Global multi-tenant authentication and token issuance gateway managed by `cynthus-identity-api`.
* `cynthus.health`: The secure B2B partner gateway interface hosting the `cynthus-portal-web` clinical dashboard layout.
* `api.cynthus.health`: Secure backend endpoint processing high-performance biometric telemetry, continuous wearable summaries, and clinical conversational requests through `cynthus-portal-api`.

---

## 8. Accessibility & Interface Contract

To fulfill interface contracts, the system establishes strict formatting limits for conversational payloads generated by `cynthus-chat`.

* Response payloads emitted by Astri are restricted to logical, sequential text formats optimized for screen-reader layout trees, preventing reliance on visual design elements.
* User interfaces do not utilize geometric orientation tags or spatial navigation layouts.
* Data arrays returned from AI evaluations are processed into descriptive structural patterns that describe data linearly, removing physical visualization dependency entirely.
* Real-time spatial tracking tokens passed via `internal.video.spatial.mapped` leverage standardized clock-face orientation fields (`relative_clock_position: int` constrained from `1` to `12`) and exact metric distances to translate physical environment metrics into voice descriptions for low-vision individuals.
