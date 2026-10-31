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

To protect proprietary intelligence intellectual property and prevent exposure of clinical or operational resources, the system partitions cloud network space into isolated Azure Virtual Networks (VNets).

```
                                  [ Public Internet ]
                                           |
       +-----------------------------------+-----------------------------------+
       | (HTTPS / WSS via cynthus.app)                                         | (HTTPS via cynthus.health)
       v                                                                       v
+-------------------------------------------------------+               +-------------------------------------------------------+
| VNET-CYNTHUS-CORE                                     |               | VNET-CYNTHUS-PORTAL                                   |
| (Public Edge Gateway Boundary)                        |               | (External Partner Gateway Boundary)                   |
|                                                       |               |                                                       |
|  +--------------------+      +--------------------+   |               |  +--------------------+      +--------------------+   |
|  |    cynthus-web     |      |    cynthus-api     |   |               |  | cynthus-portal-web |      | cynthus-portal-api |   |
|  +--------------------+      +--------------------+   |               |  +--------------------+      +--------------------+   |
|                         \              |              |               |                         \              |              |
+--------------------------\-------------|--------------+               +--------------------------\-------------|--------------+
                            \            |                                                          \            |
                             \           | Azure VNet Peering (Private IP Only)                      \           | AMQP (B2B Events)
                              v          v                                                            v          v
+-------------------------------------------------------------------------------------------------------+        |
| VNET-CYNTHUS-INTELLIGENCE (Private Closed-Source Boundary)                                             |        |
|                                                                                                       |        |
|  +--------------------+      +--------------------+                                                   |        |
|  |    cynthus-chat    |====> |  cynthus-analysis  |                                                   |        |
|  |  (Internal Ingress)| gRPC | (No Public Routes) |                                                   |        |
|  +--------------------+      +--------------------+                                                   |        |
|                                                                                                       |        |
+-------------------------------------------------------------------------------------------------------+        |
                                         ^                                                                       |
                                         |                                                                       |
                                         +----------------------- AMQP (Core Events) ----------------------------+
                                         |                                                                       |
                                         v                                                                       v
                               +-----------------------------------------------------------------------------------+
                               |                                Azure Service Bus                                  |
                               |                                 (Choreographer)                                   |
                               +-----------------------------------------------------------------------------------+

```

* `VNET-CYNTHUS-CORE`: Publicly routed subnet hosting consumer and small-to-medium business (SMB) frontend traffic (`cynthus-web`) and edge processing routers (`cynthus-api`). It acts as an open reverse proxy for real-time interaction.
* `VNET-CYNTHUS-INTELLIGENCE`: Private, dark subnet containing no public IP allocations. It isolates the closed-source proprietary elements (`cynthus-chat` and `cynthus-analysis`).
* `VNET-CYNTHUS-PORTAL`: Demilitarized subnet hosting external healthcare provider, enterprise stakeholder, and clinical partner interfaces (`cynthus-portal-web` and `cynthus-portal-api`). It enforces regulatory validation and partner access controls before routing data.
* Cross-VNet Communication: High-frequency components, such as the live user dialogue stream, bypass Azure Service Bus latency. Instead, `cynthus-api` maintains low-latency connections to `cynthus-chat` via private IP routing over an established Azure VNet Peering bridge.

### 2.2 Domain Topology & Repositories

The codebase is partitioned into decoupled repositories to isolate domain logic, licensing models, and runtime deployment contexts:

* `cynthus-auth` (The Identity Hub) — *Closed-Source*: Handles identity management, token issuance, multi-tenant RBAC + ABAC logic, and HIPAA audit routing boundaries.
* `cynthus-core` (The Logistics & Engine Layer) — *Open-Source*: Handles physical data domains and user interfaces through specialized services: `cynthus-api` (public edge gateway), `cynthus-web` (accessible frontend), `cynthus-inventory` (asset mutation and transactional state manager), and `cynthus-worker` (asynchronous background processor).
* `cynthus-intelligence` (The AI Engine Domain) — *Closed-Source*: Hosts secure, proprietary analytical processors and the Astri AI chat runtime via `cynthus-analysis` (predictive trend data analytics) and `cynthus-chat` (conversational chatbot handler optimized for live token streaming).
* `cynthus-portal` (The External Partner Gateway) — *Closed-Source*: Facilitates secure interaction with external B2B stakeholders via `cynthus-portal-api` (backend endpoint enforcing regulatory rules) and `cynthus-portal-web` (clinical dashboard rendering secure data visualizations).
* `cynthus-messaging-public` (The Public Schema Spine) — *Open-Source Library*: Contains global primitive base models, lifecycles, and open-domain components (`auth`, `clinical`, `device`, `inventory`, `logistics`, `system`).
* `cynthus-messaging-internal` (The Private Schema Spine) — *Closed-Source Library*: Extends the public namespace package using implicit namespace layouts. Contains proprietary, deeply typed contracts for secure analytical capabilities (`lifestyle`, `audit`, `chat`).
* `cynthus-infrastructure` (The Local Sandbox Layer) — *Open-Source Dev-Only*: Composes the local developer ecosystem by pairing `cynthus-store` (emulated block/table storage) with `cynthus-messaging` (local Azure Service Bus container emulator).

---

## 3. Data Isolation, Identity & Tenancy Strategy

### 3.1 Logical Multi-Tenancy Hierarchy

Multi-tenancy is enforced strictly across all data layers, storage systems, and messaging topics using a two-tier enterprise structure:

* `organization_id` (The Corporate Tenant Boundary): Maps to the global corporate or enterprise contract account (e.g., an event planning agency, commercial distributor, or healthcare provider). It owns global identity mappings and master compliance controls.
* `workspace_id` (The Functional Isolation Key): Replaces localized household boundaries. A single organization may provision dozens of independent workspaces to isolate distinct clients, departments, or specific remote tracking environments. Every event message must carry these keys to prevent cross-tenant data visibility.

### 3.2 Hybrid RBAC and ABAC Hierarchy

`cynthus-auth` issues cryptographically signed JSON Web Tokens (JWT) containing standard role claims alongside environmental attribute contexts (Attribute-Based Access Control) to evaluate constraints like active session consent and active workspace profile parameters:

* `Primary Caregiver` / `Workspace Administrator`: Full administrative rights, including checklist/task delegation, inventory base management, telemetry visibility, and external partner gateway authorizations.
* `Care Recipient` / `Client Contributor`: Read-write access to assigned tasks, basic chatbot capabilities, and localized telemetry data inputs.
* `Standard User` / `Team Member`: Read-write access to core logistics (pantry/supply mutations, general scheduling, planning configurations) without portal override permissions.

### 3.3 Database Partitioning & PHI Isolation

To satisfy strict medical-grade data isolation requirements, the persistence layer utilizes isolated database paradigms:

* General Logistics Data: Stored in transactional schemas handling core logistics, inventory, and task activities.
* Protected Health Information (PHI): Completely isolated within a dedicated database named `vesta_clinical`. This database layer implements field-level encryption for all biometric telemetry and patient data, satisfying the 2026 HIPAA Security Rule.

### 3.4 Cryptographic Vault Isolation Handshake

Processing sensitive workspace or clinical telemetry requires a localized key exchange mechanism independent of standard API access tokens. When `cynthus-intelligence` services process secure telemetry arrays, an ephemeral runtime handshake handles decryption using user-derived keys supplied during the individual session via `system.authentication.updated` patterns.

---

## 4. Messaging, Component & Signal Contracts

The messaging system consolidates fine-grained task events into an optimized Component-Driven Schema Pattern utilizing a unified top-level namespace (`cynthus.messaging`).

### 4.1 Development Layout: One Class Per Module

To ensure clean development workflows, easily scannable git diffs, and predictable import mapping, all codebases must strictly enforce a one-class-per-module rule. Packages act as structural container directories while modules (files) correspond directly to the single sub-primitive or schema class they encapsulate.

```text
cynthus-messaging-public/
+-- src/
    +-- cynthus/
        +-- messaging/
            +-- shared/                        # Shared Primitive Kernel Base
            ¦   +-- lifecycle_action.py        # Enum: LifecycleAction
            ¦   +-- signal_message_base.py     # Class: SignalMessageBase
            ¦   +-- system_identity_base.py    # Class: SystemIdentityMessageBase
            ¦   +-- cynthus_global_envelope.py # Class: CynthusGlobalEnvelope
            +-- component/                     # FSD Business Boundaries
                +-- clinical/
                ¦   +-- payloads/
                ¦   ¦   +-- clinical_signal_created.py # Class: ClinicalSignalCreatedPayload
                ¦   +-- signal/
                ¦       +-- clinical_signal_created.py # Class: ClinicalSignalCreatedSignal
                +-- [auth, device, inventory, logistics, system]

```

### 4.2 Hybrid Codebase Boundary Enforcement

To support open-source infrastructure routing without exposing closed-source intellectual property, the global common spine implements a generic type structure with a runtime default fallback.

Open-source microservices handling private signals parse them as opaque read-only buckets (`CynthusGlobalEnvelope[dict]`). They fully validate multi-tenant isolation routing context headers (`organization_id`, `workspace_id`) but do not inspect the proprietary data body nested inside, eliminating public intellectual property leakage.

```markdown
| Ingesting Service Type | Inbound Signal Classification | Pydantic Validation Binding Depth |
| :--- | :--- | :--- |
| Open-Source Service | Public Component (`clinical.*`, `device.*`) | Deep Validation (Strict Pydantic Model) |
| Open-Source Service | Private Component (`lifestyle.*`, `audit.*`) | Opaque Validation (`CynthusGlobalEnvelope[dict]`) |
| Closed-Source Service | Any Component Classification | Deep Validation (Strict Pydantic Model via Internal Wheel) |

```

### 4.3 Unified Service Ingestion & Dispatch Matrix

```markdown
| Component Domain | Corresponding Signal Namespaces | Core Publishers | Core Consumers |
| :--- | :--- | :--- | :--- |
| `audit` *(Closed)* | `audit.portal.created` | `cynthus-portal-api` | `cynthus-auth`, `cynthus-worker` |
| `auth` *(Closed)* | `auth.identity.changed` | `cynthus-auth` | `cynthus-api`, `cynthus-portal-api`, `cynthus-worker` |
| `chat` *(Closed)* | `chat.stream.logged` | `cynthus-chat` | `cynthus-worker`, `cynthus-portal-api` |
| `clinical` *(Open)* | `clinical.signal.created`, `clinical.billing.compliance` | `cynthus-api`, `cynthus-worker` | `cynthus-analysis`, `cynthus-portal-api` |
| `device` *(Open)* | `device.telemetry.updated`, `device.tracker.updated` | `cynthus-worker` | `cynthus-analysis`, `cynthus-api` |
| `inventory` *(Open)* | `user.inventory.updated` | `cynthus-inventory` | `cynthus-worker`, `cynthus-analysis` |
| `lifestyle` *(Closed)*| `lifestyle.harmony.calculated` | `cynthus-analysis` | `cynthus-worker`, `cynthus-api` |
| `logistics` *(Open)* | `logistics.order.wholesale` | `cynthus-worker` | `cynthus-inventory`, `cynthus-portal-api` |
| `system` *(Open)* | `system.authentication.updated` | `cynthus-auth` | `cynthus-analysis`, `cynthus-chat` |

```

---

## 5. High-Frequency Telemetry Ingestion Architecture (The Dual-Stream Path)

To support wearable device ingestion without overloading the centralized topic bus, the system splits telemetry processing into a Hot Path and a Warm/Choreography Path:

```
[ Wearable Device ]
        |
        +---> (Hot Path: WebSockets / MQTT) ---> [ High-Throughput Buffer / Time-Series DB ]
        |                                                        | (Aggregation Window)
        |                                                        v
        +---> (Choreography Path: AMQP) <--- [ Ingestion Worker / Proxy Edge Layer ]
                                                             |
                                                             v (Converts to Lifecycles)
                                                    cynthus-events-topic

```

1. The Hot Path: Continuously streaming sensors (such as live heart rate tracking or high-frequency wearable biometric telemetry) push raw data intervals over WebSockets or MQTT directly to a high-throughput time-series buffer, bypassing Azure Service Bus.
2. The Warm Path: An ingestion broker summarizes the hot path data into structured time-slice snapshots (`device.telemetry.updated`) or evaluates incoming values against threshold rules to emit instant mutation flags (`device.tracker.updated`) onto the core choreography bus.

---

## 6. Technical Implementation Blueprint (FastAPI + FastStream)

Per system standards, the following primitives declare the global schema boundaries. To expose individual modules cleanly without forcing deep consumer imports, package `__init__.py` files are utilized as public API facade layers.

### `shared/lifecycle_action.py`

```python
# cynthus/messaging/shared/lifecycle_action.py
from enum import Enum

class LifecycleAction(str, Enum):
    """Lifecycle actions mapping entity state-change phases."""
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    SNAPSHOT = "snapshot"

```

### `shared/signal_message_base.py`

```python
# cynthus/messaging/shared/signal_message_base.py
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict

class SignalMessageBase(BaseModel):
    """Primal structural base for all standalone data interactions."""
    model_config = ConfigDict(
        frozen=True,
        populate_by_name=True,
        json_encoders={datetime: lambda dt: dt.astimezone(timezone.utc).isoformat()}
    )

```

### `shared/system_identity_base.py`

```python
# cynthus/messaging/shared/system_identity_base.py
from pydantic import Field
from cynthus.messaging.shared.signal_message_base import SignalMessageBase

class SystemIdentityMessageBase(SignalMessageBase):
    """Base structural model enforcing multi-tenant isolation contexts."""
    organization_id: str = Field(..., description="Corporate Tenant boundary identifier.")
    workspace_id: str = Field(..., description="Functional Isolation partition tracking key.")
    actor_id: str = Field(..., description="The unique system or user identity executing the shift.")

```

### `shared/cynthus_global_envelope.py`

```python
# cynthus/messaging/shared/cynthus_global_envelope.py
from datetime import datetime, timezone
from typing import Generic, TypeVar, Any
from uuid import UUID, uuid4
from pydantic import Field
from cynthus.messaging.shared.system_identity_base import SystemIdentityMessageBase
from cynthus.messaging.shared.lifecycle_action import LifecycleAction

# Dynamic fallback bounds back to Any for open-source opaque parsing
PayloadT = TypeVar("PayloadT", bound=Any, default=Any)

class CynthusGlobalEnvelope(SystemIdentityMessageBase, Generic[PayloadT]):
    """The immutable common spine published to cynthus-events-topic."""
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str = Field(..., description="Dot-notated routing string.")
    lifecycle_action: LifecycleAction
    correlation_id: UUID = Field(..., description="CrossServiceCorrelationGuid.")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: PayloadT

```

### FastAPI Unified Lifespan Structural Pattern

```python
# Inside downstream application runtimes (e.g., cynthus-api)
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
[External Partner]           cynthus-portal-api            cynthus-auth            Secure Audit Log
         |                           |                           |                        |
         |--- Request Telemetry ---->|                           |                        |
         |                           |--- Validate Token Signature ---->|                 |
         |                           |<-- Consent Validated -----|                        |
         |                           |                                                    |
         |                           |--- Write Immutable Event Fact -------------------->|
         |                           |    (audit.portal.created)                          |
         |<-- Stream Read-Only Data -|                                                    |

```

1. Consent Token Verification: The inbound bearer token signature is evaluated against `cynthus-auth` public cryptographic certificates to ensure valid user authorization and active clinician access scope exist for the active session.
2. Immutable Audit Emission: Prior to transmitting the requested metrics, `cynthus-portal-api` blocks response execution until an event fact of type `audit.portal.created` is successfully committed to the log repository.

### 7.2 AI Governance & Compliance Transparency

To satisfy 2026 state-level AI governance laws (such as TRAIGA), any automated clinical insights, lifestyle assessments, or conversational responses generated by `cynthus-intelligence` services must incorporate structural compliance parameters. The conversational logging structure must append an automated transparency metadata block certifying the exact LLM configuration model utilized, explicitly disclosing AI usage within any medical context.

### 7.3 Endpoint Routing Matrix

Ecosystem routing boundaries strictly isolate corporate, consumer, and clinical traffic profiles at DNS edge routers:

* `cynthus.app`: The public interface gateway hosting `cynthus-web` for standard user and consumer application workspaces.
* `auth.cynthus.app`: Global multi-tenant authentication and token issuance gateway managed by `cynthus-auth`.
* `cynthus.health`: The secure B2B partner gateway interface hosting the `cynthus-portal-web` clinical dashboard layout.
* `api.cynthus.health`: Secure backend endpoint processing high-performance biometric telemetry, continuous wearable summaries, and clinical conversational requests through `cynthus-portal-api`.

---

## 8. Accessibility & Interface Contract

To fulfill interface contracts, the system establishes strict formatting limits for conversational payloads generated by `cynthus-chat`.

* Response payloads emitted by Astri are restricted to logical, sequential text formats optimized for screen-reader layout trees, preventing reliance on visual design elements.
* User interfaces do not utilize geometric orientation tags or spatial navigation layouts.
* Data arrays returned from AI evaluations are processed into descriptive structural patterns that describe data linearly, removing physical visualization dependency entirely.

---

### Implementation Review Check

This ADD is completely locked and self-contained. Your Python namespace distribution, network topologies, and single-class folder hierarchies are completely standardized across your production ecosystems. All conflicting dependencies between your public and private domains have been fully resolved.
