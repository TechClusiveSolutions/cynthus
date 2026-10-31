# Architectural Design Document (ADD)

**Project:** Cynthus Life Ecosystem

**Architecture Pattern:** Choreographer (Event-Driven Microservices)

**Design Methodology:** Feature Slice Design (FSD)

**Target Runtime:** Python 3.11+ / FastAPI / FastStream

**Messaging Backbone:** Azure Service Bus (AMQP)

---

## 1. Document Purpose & Scope

This Architectural Design Document (ADD) serves as the definitive engineering blueprint for implementing the **Cynthus Life Ecosystem**. It translates the functional boundaries, compliance requirements, enterprise tenancy rules, and non-visual user experiences defined in the Product Requirements Document (PRD) into a strict technical implementation specification.

The technical architecture balances high-throughput logistics, continuous device streams, and multi-tenant isolation with remote monitoring telemetry constraints, private network separation, and strict HIPAA audit accountability.

---

## 2. System Architecture & Topology

The Cynthus Life Ecosystem utilizes an asynchronous Choreographer Architecture. Individual microservices interact implicitly by broadcasting immutable facts (events) to a centralized enterprise messaging spine rather than orchestrating downstream dependencies via direct commands.

### 2.1 Deployment Network Boundaries

To protect proprietary intelligence intellectual property and prevent exposure of clinical or operational resources, the system partitions cloud network space into isolated Azure Virtual Networks (VNets).

```
                                  [ Public Internet ]
                                           |
                                           v  (HTTPS / WSS via cynthus.app)
+-----------------------------------------------------------------------------------------+
| VNET-CYNTHUS-CORE (Public Edge Gateway Boundary)                                        |
|                                                                                         |
|  +--------------------+      +--------------------+      +--------------------+         |
|  |    cynthus-web     |      |    cynthus-api     |      | cynthus-inventory  |         |
|  +--------------------+      +--------------------+      +--------------------+         |
+-----------------------------------------------------------------------------------------+
                                           ^
                                           | Azure VNet Peering (Private IP Only)
                                           v
+-----------------------------------------------------------------------------------------+
| VNET-CYNTHUS-INTELLIGENCE (Private Closed-Source Boundary)                              |
|                                                                                         |
|  +--------------------+      +--------------------+                                     |
|  |    cynthus-chat    |====> |  cynthus-analysis  |                                     |
|  |  (Internal Ingress)| gRPC | (No Public Routes) |                                     |
|  +--------------------+      +--------------------+                                     |
+-----------------------------------------------------------------------------------------+

```

1. **`VNET-CYNTHUS-CORE`:** Publicly routed subnet hosting frontend traffic (`cynthus-web`) and edge processing routers (`cynthus-api`). It acts as an open reverse proxy for real-time traffic.


2. **`VNET-CYNTHUS-INTELLIGENCE`:** Private, dark subnet containing no public IP allocations. It isolates the closed-source proprietary elements (`cynthus-chat` and `cynthus-analysis`).


3. **Cross-VNet Communication:** High-frequency components, such as the live user dialogue stream, bypass Azure Service Bus latency. Instead, `cynthus-api` maintains low-latency connections to `cynthus-chat` via private IP routing over an established **Azure VNet Peering** bridge.



---

## 3. Data Isolation, Identity & Tenancy Strategy

### 3.1 Logical Multi-Tenancy Hierarchy

Multi-tenancy is enforced strictly across all data layers, storage systems, and messaging topics using a two-tier enterprise structure:

* **`organization_id` (The Corporate Tenant Boundary):** Maps to the global small-to-medium business (SMB) or enterprise contract account (e.g., an event planning agency or healthcare provider). It owns global RBAC mappings and master compliance controls.


* **`workspace_id` (The Functional Isolation Key):** Replaces localized household boundaries. A single organization may provision dozens of independent workspaces to isolate distinct clients, independent corporate functions, specific event projects, or distinct remote patient tracking environments. Every event message must carry these keys to prevent cross-tenant data visibility.



### 3.2 Role-Based Access Control (RBAC) Hierarchy

`cynthus-auth` issues cryptographically signed JSON Web Tokens (JWT) containing a roles claim array mapping user clearance within an active workspace:

* **`Primary Caregiver` / `Workspace Administrator`:** Full administrative rights, including checklist/task delegation, inventory base management, telemetry visibility, and external partner gateway authorizations.


* **`Care Recipient` / `Client Contributor`:** Read-write access to assigned tasks, basic chatbot capabilities, and localized telemetry data inputs.


* **`Standard User` / `Team Member`:** Read-write access to core logistics (pantry/supply mutations, general scheduling, planning configurations) without portal override permissions.



### 3.3 Cryptographic Vault Isolation Handshake

To satisfy **Req A.3**, processing sensitive workspace or clinical telemetry requires a localized key exchange mechanism independent of standard API access tokens. When `cynthus-intelligence` services process secure telemetry arrays, an ephemeral runtime handshake handles decryption using user-derived keys supplied during the individual session via `system.authentication.updated` patterns.

---

## 4. Messaging & Entity-Lifecycle Schema Specification

The messaging system consolidates fine-grained task events into an optimized **Entity-Lifecycle (State-Change) Schema Pattern** to prevent topic explosion on the Azure Service Bus instance.

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
    "actor_id": { "type": ["string", "null"], "default": null },
    "payload": { "type": "object" }
  }
}

```

### 4.2 Core Domain Payloads

#### 4.2.1 User Inventory Domain (`user.inventory.updated`)

Fires when supply spaces, event equipment logs, or pantry trackers register mutations. Supports real-time logistics mutations (**Req B.1**, **Req B.2**).

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

Fires instantly when an external wearable or localized edge tracker breaches a critical boundary condition, triggering reactive anomaly alerts (**Req C.1**).

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

#### 4.2.5 Audit Domain (`audit.portal.created`)

Fires as an immutable record whenever external enterprise partners inspect workspace tracking values (**Req D.1**, **Req D.2**).

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

To support wearable device ingestion without overloading the centralized topic bus, the system splits telemetry processing into a **Hot Path** and a **Warm/Choreography Path**:

```
[ Wearable Device ]
        |
        +---> (Hot Path: WebSockets / MQTT) ---> [ High-Throughput Buffer / Time-Series DB ]
        |                                                       | (Aggregation Window)
        |                                                       v
        +---> (Choreography Path: AMQP) <--- [ Ingestion Worker / Proxy Edge Layer ]
                                                            |
                                                            v (Converts to Lifecycles)
                                                   cynthus-events-topic

```

1. **The Hot Path:** Continuously streaming sensors (such as live heart rate tracking or high-frequency ambient telemetry) push raw data intervals over WebSockets or MQTT directly to a time-series cache or high-throughput analytics buffer, bypassing Azure Service Bus.


2. **The Warm Path:** An ingestion broker summarizes the hot path data into structured time-slice snapshots (`device.telemetry.updated`) or evaluates incoming values against threshold rules to emit instant mutation flags (`device.tracker.updated`) onto the core choreography bus.



---

## 6. Technical Implementation Blueprint (FastAPI + FastStream)

Per system standards, microservice loops bind asynchronous message subscriptions into FastAPI application life-cycle runtimes. The pattern below demonstrates how to construct the thread-safe global base engine wrapper.

```python
import logging
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
    actor_id: Optional[str] = None
    payload: PayloadT

    model_config = ConfigDict(
        frozen=True,
        populate_by_name=True,
        json_encoders={datetime: lambda dt: dt.astimezone(timezone.utc).isoformat()}
    )

# --- FastAPI Integration Application Blueprint ---
class SystemLifecyclePayload(BaseModel):
    system_id: str
    current_state: str
    reason: str

app = FastAPI()

@app.on_event("startup")
async def initialize_message_loop():
    """Ties asynchronous message polling into FastAPI engine lifespan hooks."""
    logger.info("Initializing FastStream Core Broker contexts.")
    # In practice, establish your Azure Service Bus broker connection strings here.
    logger.info("Cynthus workspace messaging loops bound successfully.")

```

---

## 7. Regulatory Compliance, Auditing & Verification

### 7.1 HIPAA Compliance Safeguards (`cynthus-portal`)

To maintain end-to-end alignment with **Req D.1** and **Req D.2**, the B2B portal API gateway restricts external connections to strict read-only paradigms. Any data retrieval routine targeting telemetry registers verification steps:

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

1. **Consent Token Verification:** The inbound bearer token signature is evaluated against `cynthus-auth` public cryptographic certificates to ensure valid user authorization exists for the active session.


2. **Immutable Audit Emission:** Prior to transmitting the requested metrics, `cynthus-portal-api` blocks response execution until an event fact of type `audit.portal.created` is successfully committed to the log repository.



---

## 8. Accessibility & Interface Contract

To fulfill **Req C.2**, the system establishes strict rules for conversational payloads generated by `cynthus-chat`.

* Response payloads emitted by Astri are restricted to logical, sequential text formats optimized for screen-reader layout trees.


* User interfaces do not utilize geometric orientation tags or spatial navigation layouts.


* Data arrays returned from AI evaluations are processed into descriptive structural patterns that describe data linearly, removing physical visualization dependency entirely.
