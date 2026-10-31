# Architectural Design Document (ADD)

Project: Cynthus Life Ecosystem

Architecture Pattern: Choreographer (Event-Driven Microservices)

Design Methodology: Feature Slice Design (FSD)

Target Runtime: Python 3.11+ / FastAPI / FastStream

Messaging Backbone: Azure Service Bus (AMQP)

## 1. Document Purpose & Scope

This Architectural Design Document (ADD) serves as the definitive engineering blueprint for implementing the Cynthus Life Ecosystem. It translates the functional boundaries, compliance requirements, enterprise tenancy rules, and non-visual user experiences defined in the Product Requirements Document (PRD) into a strict technical implementation specification.

The technical architecture balances high-throughput logistics, continuous device streams, and multi-tenant isolation with remote monitoring telemetry constraints, physical database partitioning, private network separation, and strict HIPAA audit accountability.

---

## 2. System Architecture & Topology

The Cynthus Life Ecosystem utilizes an asynchronous Choreographer Architecture. Individual microservices interact implicitly by broadcasting immutable facts (events) to a centralized enterprise messaging spine rather than orchestrating downstream dependencies via direct commands.

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
|                                        |              |               |                                        |              |
+----------------------------------------|--------------+               +----------------------------------------|--------------+
                                         |                                                                       |
                                         | Azure VNet Peering (Private IP Only)                                  | AMQP (B2B Events)
                                         v                                                                       |
+-------------------------------------------------------------------------------------------------------+        |
| VNET-CYNTHUS-INTELLIGENCE (Private Closed-Source Boundary)                                            |        |
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
                               |                               Azure Service Bus                                   |
                               |                                (Choreographer)                                    |
                               +-----------------------------------------------------------------------------------+

```

* `VNET-CYNTHUS-CORE`: Publicly routed subnet hosting consumer and small-to-medium business (SMB) frontend traffic (`cynthus-web`) and edge processing routers (`cynthus-api`). It acts as an open reverse proxy for real-time interaction.


* `VNET-CYNTHUS-INTELLIGENCE`: Private, dark subnet containing no public IP allocations. It isolates the closed-source proprietary elements (`cynthus-chat` and `cynthus-analysis`).


* `VNET-CYNTHUS-PORTAL`: Demilitarized subnet hosting external healthcare provider, enterprise stakeholder, and clinical partner interfaces (`cynthus-portal-web` and `cynthus-portal-api`). It enforces regulatory validation and partner access controls before routing data.


* Cross-VNet Communication: High-frequency components, such as the live user dialogue stream, bypass Azure Service Bus latency. Instead, `cynthus-api` maintains low-latency connections to `cynthus-chat` via private IP routing over an established Azure VNet Peering bridge.



### 2.2 Domain Topology & Repositories

The codebase is partitioned into five distinct, decoupled repositories to isolate domain logic, licensing models, and runtime deployment contexts:

* `cynthus-auth` (The Identity Hub) — *Open-Source*: Handles identity management, token issuance, multi-tenant RBAC + ABAC logic, and HIPAA audit routing boundaries.


* `cynthus-core` (The Logistics & Engine Layer) — *Open-Source*: Handles physical data domains and user interfaces through four specialized services: `cynthus-api` (public edge gateway), `cynthus-web` (accessible user interface frontend), `cynthus-inventory` (asset mutation and transactional state manager), and `cynthus-worker` (asynchronous background processor and `cynthus-scheduler` loop controller).


* `cynthus-intelligence` (The AI Engine Domain) — *Closed-Source*: Hosts secure, proprietary analytical processors and the Astri AI chat runtime via `cynthus-analysis` (autonomous predictive trend data analytics) and `cynthus-chat` (conversational chatbot handler optimized for live token streaming).


* `cynthus-portal` (The External Partner Gateway) — *Open/Closed Hybrid*: Facilitates secure interaction with external B2B stakeholders via `cynthus-portal-api` (backend endpoint enforcing regulatory rules) and `cynthus-portal-web` (clinical dashboard rendering secure data visualizations).


* `cynthus-infrastructure` (The Local Sandbox Layer) — *Open-Source Dev-Only*: Composes the local developer ecosystem by pairing `cynthus-store` (emulated block/table storage) with `cynthus-messaging` (local Azure Service Bus container emulator).



---

## 3. Data Isolation, Identity & Tenancy Strategy

### 3.1 Logical Multi-Tenancy Hierarchy

Multi-tenancy is enforced strictly across all data layers, storage systems, and messaging topics using a two-tier enterprise structure:

* `organization_id` (The Corporate Tenant Boundary): Maps to the global corporate or enterprise contract account (e.g., an event planning agency, commercial distributor, or healthcare provider). It owns global identity mappings and master compliance controls.


* `workspace_id` (The Functional Isolation Key): Replaces localized household boundaries. A single organization may provision dozens of independent workspaces to isolate distinct clients, corporate departments, specific event projects, or distinct remote patient tracking environments. Every event message must carry these keys to prevent cross-tenant data visibility.



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

To satisfy Req A.3, processing sensitive workspace or clinical telemetry requires a localized key exchange mechanism independent of standard API access tokens. When `cynthus-intelligence` services process secure telemetry arrays, an ephemeral runtime handshake handles decryption using user-derived keys supplied during the individual session via `system.authentication.updated` patterns.

---

## 4. Messaging & Entity-Lifecycle Schema Specification

The messaging system consolidates fine-grained task events into an optimized Entity-Lifecycle (State-Change) Schema Pattern to prevent topic explosion on the Azure Service Bus instance.

### 4.1 Global Message Envelope (The Common Spine)

Every asynchronous transmission published to `cynthus-events-topic` conforms to an immutable base schema layout, implementing the `CrossServiceCorrelationGuid` diagnostic strategy.

```json
{
  "$schema": "https://schemas.cynthus.health/v1/envelope.json",
  "type": "object",
  "required": [
    "event_id",
    "event_type",
    "lifecycle_action",
    "correlation_id",
    "timestamp",
    "organization_id",
    "workspace_id",
    "actor_id",
    "payload"
  ],
  "properties": {
    "event_id": { "type": "string", "format": "uuid" },
    "event_type": { "type": "string" },
    "lifecycle_action": { "type": "string", "enum": ["created", "updated", "deleted", "snapshot"] },
    "correlation_id": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "organization_id": { "type": "string" },
    "workspace_id": { "type": "string" },
    "actor_id": { "type": "string" },
    "payload": { "type": "object" }
  }
}

```

### 4.2 Core Domain Payloads

#### 4.2.1 User Inventory Domain (`user.inventory.updated`)

Fires when supply spaces, event equipment logs, or pantry trackers register mutations. Supports real-time logistics mutations (Req B.1, Req B.2).

```json
{
  "inventory_id": "string",
  "shelf_id": "string",
  "item_id": "string",
  "current_quantity": "integer",
  "expires_on": { "type": ["string"], "format": "date-time" },
  "meta": {
    "mutation_reason": "item_replenished | item_used | shelf_added"
  }
}

```

#### 4.2.2 Clinical & Device Domain (`clinical.signal.created`)

Fires when discrete telemetry points are manually generated or received via third-party webhooks.

```json
{
  "signal_id": "string",
  "metric_type": "BloodPressure | BloodGlucose | StepCounter",
  "raw_value": "string"
}

```

#### 4.2.3 Continuous Telemetry Domain (`device.telemetry.updated`)

Fires when an edge integration worker aggregates continuous wearable device streams (e.g., smartwatches, biometric trackers) over a time-slice block. Reduces message overhead on the choreography backbone.

```json
{
  "device_id": "string",
  "user_id": "string",
  "metric_stream": "string (e.g., HeartRate)",
  "interval_start": "string (ISO 8601 Format)",
  "interval_end": "string (ISO 8601 Format)",
  "metrics": {
    "sample_count": "integer",
    "mean_value": "number",
    "max_value": "number",
    "min_value": "number"
  },
  "meta": {
    "device_battery_percent": "integer",
    "sync_source": "string"
  }
}

```

#### 4.2.4 Device Trigger Domain (`device.tracker.updated`)

Fires instantly when an external wearable or localized edge tracker breaches a critical boundary condition, triggering reactive anomaly alerts (Req C.1).

```json
{
  "device_id": "string",
  "user_id": "string",
  "trigger_condition": "BiometricAnomalyDetected | EnvironmentalBreach",
  "telemetry_slice": {
    "metric_type": "string",
    "observed_value": "string",
    "threshold_severity": "CRITICAL_LOW | CRITICAL_HIGH"
  },
  "meta": {
    "requires_immediate_escalation": "boolean",
    "escalation_target_role": "string"
  }
}

```

#### 4.2.5 Lifestyle Analytics Domain (`lifestyle.harmony.calculated`)

Fires once every 24 hours when `cynthus-analysis` computes the current operational and social metrics of a workspace perimeter (Req B.5, Req C.3).

```json
{
  "calculation_id": "string",
  "harmony_score": "number (0.00 to 1.00)",
  "contributing_factors": {
    "task_completion_rate": "number",
    "resource_balance_index": "number",
    "workload_variance": "number"
  }
}

```

#### 4.2.6 Procurement & Order Domain (`logistics.order.wholesale`)

Fires when automated replenishment logic or scaled recipe boundaries generate automated external vendor fulfillments (Req B.2, Req B.7).

```json
{
  "order_id": "string",
  "vendor_target_api": "string",
  "items": [
    { "item_id": "string", "quantity": "integer", "unit_cost": "number" }
  ],
  "total_estimated_cost": "number"
}

```

#### 4.2.7 Remote Patient Monitoring Billing Domain (`clinical.billing.compliance`)

Fires to summarize operational data transmission metrics required to satisfy 2026 Remote Patient Monitoring (RPM) billing codes.

```json
{
  "session_id": "string",
  "patient_user_id": "string",
  "eligible_cpt_codes": {
    "99454_data_transmission": { "eligible": "boolean", "days_tracked_in_period": "integer" },
    "99445_physiologic_logging": { "eligible": "boolean" },
    "99470_interactive_time": { "eligible": "boolean", "accumulated_minutes": "integer" }
  }
}

```

#### 4.2.8 Audit Domain (`audit.portal.created`)

Fires as an immutable record whenever external enterprise partners or clinicians inspect workspace tracking values via the partner portal (Req D.1, Req D.2).

```json
{
  "audit_log_id": "string",
  "clinician_id": "string",
  "target_user_id": "string",
  "accessed_fields": { "type": "array", "items": { "type": "string" } },
  "consent_token_signature": "string"
}

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

Per system standards, microservice loops bind asynchronous message subscriptions into FastAPI application runtimes using modern native context-manager lifespans to declare thread-safe, global module-level broker contexts.

```python
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from enum import Enum
from typing import Generic, TypeVar, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict
from fastapi import FastAPI

logger = logging.getLogger("cynthus.infra")
PayloadT = TypeVar("PayloadT", bound=BaseModel)

class LifecycleAction(str, Enum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    SNAPSHOT = "snapshot"

class CynthusBaseEnvelope(BaseModel, Generic[PayloadT]):
    """Global immutable event wrapper enforcing CrossServiceCorrelationGuid."""
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    lifecycle_action: LifecycleAction
    correlation_id: UUID
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    organization_id: str
    workspace_id: str
    actor_id: str
    payload: PayloadT

    model_config = ConfigDict(
        frozen=True,
        populate_by_name=True,
        json_encoders={datetime: lambda dt: dt.astimezone(timezone.utc).isoformat()}
    )

# --- FastAPI Unified Lifespan Structural Pattern ---
@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """Manages thread-safe FastStream broker lifespan hooks over the service run."""
    logger.info("Initializing FastStream Core Broker contexts on Azure Service Bus connection.")
    # Initialize global messaging loops and server-side subscription filters here.
    yield
    logger.info("De-initializing FastStream broker connections cleanly.")

app = FastAPI(lifespan=lifespan)

```

---

## 7. Regulatory Compliance, Auditing & Verification

### 7.1 HIPAA Compliance Safeguards (`cynthus-portal`)

To maintain end-to-end alignment with Req D.1 and Req D.2, the B2B portal API gateway restricts external connections to strict read-only paradigms. Any data retrieval routine targeting telemetry registers verification steps:

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

To satisfy 2026 state-level AI governance laws (such as TRAIGA), any automated clinical insights, lifestyle assessments, or conversational responses generated by `cynthus-intelligence` services must incorporate structural compliance parameters. The `cynthus-chat` payload must append an automated transparency metadata block certifying the exact LLM configuration model utilized, explicitly disclosing AI usage within any medical context.

### 7.3 Endpoint Routing Matrix

Ecosystem routing boundaries strictly isolate corporate, consumer, and clinical traffic profiles at DNS edge routers:

* `cynthus.app`: The public interface gateway hosting `cynthus-web` for standard user and consumer application workspaces.


* `auth.cynthus.app`: Global multi-tenant authentication and token issuance gateway managed by `cynthus-auth`.


* `cynthus.health`: The secure B2B partner gateway interface hosting the `cynthus-portal-web` clinical dashboard layout.


* `api.cynthus.health`: Secure backend endpoint processing high-performance biometric telemetry, continuous wearable summaries, and clinical conversational requests through `cynthus-portal-api`.



---

## 8. Accessibility & Interface Contract

To fulfill Req C.2, the system establishes strict formatting limits for conversational payloads generated by `cynthus-chat`.

* Response payloads emitted by Astri are restricted to logical, sequential text formats optimized for screen-reader layout trees, preventing reliance on visual design elements.
* User interfaces do not utilize geometric orientation tags or spatial navigation layouts.
* Data arrays returned from AI evaluations are processed into descriptive structural patterns that describe data linearly, removing physical visualization dependency entirely.
