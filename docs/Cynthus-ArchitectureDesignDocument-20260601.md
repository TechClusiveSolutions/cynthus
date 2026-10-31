# Architectural Design Document (ADD)

Project: Cynthus Life Ecosystem

Architecture Pattern: Choreographer (Event-Driven Microservices)

Design Methodology: Feature Slice Design (FSD)

Target Runtime: Python 3.11+ / FastAPI / FastStream

Messaging Backbone: Azure Service Bus (AMQP)

## 1. Document Purpose & Scope

This Architectural Design Document (ADD) serves as the definitive engineering blueprint for implementing the Cynthus Life Ecosystem. It translates the functional boundaries, compliance requirements, and non-visual user experiences defined in the Product Requirements Document (PRD) into a strict technical implementation specification.

The technical architecture balances high-throughput household logistics and multi-tenant isolation with remote patient monitoring (RPM) telemetry constraints, private network separation, and strict HIPAA audit accountability.

## 2. System Architecture & Topology

The Cynthus Life Ecosystem utilizes an asynchronous Choreographer Architecture. Individual microservices interact implicitly by broadcasting immutable facts (events) to a centralized enterprise messaging spine rather than orchestrating downstream dependencies via direct commands.

### 2.1 Deployment Network Boundaries

To protect proprietary intelligence intellectual property and prevent exposure of clinical resources, the system partitions cloud network space into isolated Azure Virtual Networks (VNets).

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

1. `VNET-CYNTHUS-CORE`: Publicly routed subnet hosting frontend traffic (`cynthus-web`) and edge processing routers (`cynthus-api`). It acts as an open reverse proxy for real-time traffic.
2. `VNET-CYNTHUS-INTELLIGENCE`: Private, dark subnet containing no public IP allocations. It isolates the closed-source proprietary elements (`cynthus-chat` and `cynthus-analysis`).
3. Cross-VNet Communication: High-frequency components, such as the live user dialogue stream, bypass Azure Service Bus latency. Instead, `cynthus-api` maintains low-latency connections to `cynthus-chat` via private IP routing over an established Azure VNet Peering bridge.

## 3. Data Isolation, Identity & Tenancy Strategy

### 3.1 Logical Multi-Tenancy Boundary

Multi-tenancy is enforced strictly at the Household Tenant Level (`household_id`) across all data layers, storage systems, and messaging topics.

* Every published event message must contain a root-level `household_id` to establish isolation boundaries.
* Database access points use Row-Level Security (RLS) tracking the verified tenant claim, preventing cross-tenant data leaks.

### 3.2 Role-Based Access Control (RBAC) Hierarchy

`cynthus-auth` issues cryptographically signed JSON Web Tokens (JWT) containing a `roles` claim array mapping user clearance within a specific household:

* `Primary Caregiver`: Full system rights, including checklist delegation, inventory configuration, clinical telemetry visibility, and external portal provider authorization.
* `Care Recipient`: Read-write access to assigned tasks, basic chat capabilities, and localized clinical telemetry inputs.
* `Standard User`: Read-write logistics access (pantry mutations, general scheduling, meal choices) without clinical portal override permissions.

### 3.3 Cryptographic Vault Isolation Handshake

To satisfy Req A.3, processing sensitive clinical signals requires a localized key exchange mechanism independent of standard API access tokens.

When `cynthus-intelligence` services require raw health arrays, the service does not decrypt the field using database credentials. Instead, an ephemeral application handshake handles decryption using user-derived keys supplied directly during the individual session via `system.authentication.updated` patterns.

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
    "household_id",
    "payload"
  ],
  "properties": {
    "event_id": { "type": "string", "format": "uuid" },
    "event_type": { "type": "string" },
    "lifecycle_action": { "type": "string", "enum": ["created", "updated", "deleted", "snapshot"] },
    "correlation_id": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "household_id": { "type": "string" },
    "actor_id": { "type": ["string", "null"], "default": null },
    "payload": { "type": "object" }
  }
}

```

### 4.2 Core Domain Payloads

#### 4.2.1 Provider Domain (`provider.service_list.updated`)

Fires when service offerings are altered within a provider master list container.

```json
{
  "service_list_id": "string",
  "services": [
    { "offering_id": "string" }
  ],
  "meta": {
    "mutation_reason": "string"
  }
}

```

#### 4.2.2 User Inventory Domain (`user.inventory.updated`)

Fires when inventory tracking contexts process replenishment, usage, or shelf updates. Supports real-time logistics mutations (Req B.1, Req B.2).

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

#### 4.2.3 Clinical Domain (`clinical.signal.created`)

Fires instantly when raw remote monitoring devices streams biometric records into the system edge (Req C.1).

```json
{
  "signal_id": "string",
  "metric_type": "BloodPressure | BloodGlucose | StepCounter",
  "raw_value": "string"
}

```

#### 4.2.4 Audit Domain (`audit.portal.created`)

Fires as an immutable entry whenever B2B partners access clinical data vectors (Req D.1, Req D.2).

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

## 5. Technical Implementation Blueprint (FastAPI + FastStream)

Per system standards, microservice loops bind asynchronous message subscriptions into FastAPI application life-cycle runtimes. The pattern below demonstrates how to construct the thread-safe global base engine wrapper.

```python
import logging
from datetime import datetime, timezone
from enum import Enum
from typing import Generic, TypeVar, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict
from fastapi import FastAPI
from faststream.broker import KafkaBroker # Swappable with Azure Service Bus ASBpy Broker

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
    household_id: str
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
    logger.info("Cynthus system-level messaging loops bound successfully.")

```

---

## 6. Regulatory Compliance, Auditing & Verification

### 6.1 HIPAA Compliance Safeguards (`cynthus-portal`)

To maintain end-to-end alignment with Req D.1 and Req D.2, the B2B API gateway restricts external clinical requests to strict read-only paradigms.

Every request targeting clinical telemetry triggers a validation sequence before data block reconstruction:

```
[External Clinician]         cynthus-portal-api            cynthus-auth            Secure Audit Log
         |                           |                           |                        |
         |--- Request Telemetry ---->|                           |                        |
         |                           |--- Validate Token Signature ---->|                 |
         |                           |<-- Consent Validated -----|                        |
         |                           |                                                    |
         |                           |--- Write Immutable Event Fact -------------------->|
         |                           |    (audit.portal.created)                          |
         |<-- Stream Read-Only Data -|                                                    |

```

1. Consent Token Verification: The inbound bearer token signature is evaluated against `cynthus-auth` public cryptographic certificates to ensure valid user authorization exists for the active session.
2. Immutable Audit Emission: Prior to transmitting the requested health metrics, `cynthus-portal-api` blocks the response execution thread until an event fact of type `audit.portal.created` is successfully committed to the log repository.

---

## 7. Accessibility & Interface Contract

To fulfill Req C.2, the system establishes strict rules for conversational payloads generated by `cynthus-chat`.

* Response payloads emitted by Astri are restricted to logical, sequential text formats optimized for screen-reader layout trees.
* User interfaces do not utilize geometric orientation tags or spatial navigation layouts.
* Data arrays returned from AI evaluations are processed into descriptive structural patterns that describe structural data linearly, removing physical visualization dependency entirely.