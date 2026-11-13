# Architectural Design Document (ADD)

**Project:** Cynthus Life Ecosystem
**Document Version:** 6.0 (June 2026)
**Status:** Active - reflects all architectural decisions through June 2026 design sessions
**Architecture Pattern:** Choreographer (Event-Driven Microservices)
**Design Methodology:** Component-Driven Engineering (Backend FSD Adaptation)
**Target Runtime:** Python 3.11+ / FastAPI / FastStream
**Messaging Backbone:** Azure Service Bus (AMQP)
**Companion Documents:** Cynthus PRD v4.2, Cynthus Feature Registry v1.1

---

## 1. Document Purpose & Scope

This Architectural Design Document (ADD) is the definitive engineering blueprint for the Cynthus Life Ecosystem. It translates functional boundaries, compliance requirements, multi-tenant isolation rules, and non-visual user experience contracts defined in the PRD into strict technical implementation specifications.

This version supersedes ADD V5 and incorporates the following significant changes:

- **Seven-domain service layout** replacing the prior five-repository structure.
- **`cynthus-profile` service** added to Core as the owner of soft preferences and hard constraints.
- **Context Assembly Pattern** formalized as a first-class architectural concern (Section 4).
- **Three-topic Service Bus architecture** replacing the single-topic design.
- **Workspace ID stub strategy** - `workspace_id` present in all schemas from Phase 1 even for single-user accounts.
- **Entitlement system for booster packs** - ADR-005 governing how purchased add-ons propagate to token claims.
- **All `SMH-*` naming artifacts removed** - fully migrated to `cynthus-*` naming convention throughout.

---

## 2. System Architecture & Topology

The Cynthus Life Ecosystem uses an asynchronous Choreographer Architecture. Microservices interact implicitly by broadcasting immutable facts (signals) to a centralized enterprise messaging spine rather than orchestrating downstream dependencies via direct commands.

### 2.1 Deployment Network Boundaries

To protect proprietary intellectual property and prevent exposure of clinical, corporate, or financial operational resources, the system partitions cloud network space into isolated Azure Virtual Networks (VNets).

```text
                              [ Public Internet ]
                                      |
          +--------------------------+------------------------+
          | (HTTPS/WSS via cynthus.app)     (HTTPS via cynthus.health)
          v                                                   v
+-------------------------------+             +--------------------------------+
| VNET-CYNTHUS-CORE             |             | VNET-CYNTHUS-HEALTH            |
| (Public Edge - Open Source)   |             | (Clinical DMZ - Closed Source) |
|                               |             |                                |
| cynthus-core-web              |             | cynthus-health-web             |
| cynthus-core-api              |             | cynthus-health-api             |
|                               |             | cynthus-messaging              |
+-------+---------------+-------+             +-------+------------------------+
        |               |                             |
        | VNet Peering  | AMQP (Service Bus)          | AMQP (Service Bus)
        | (Private IP)  |                             |
        v               v                             v
+-----------------------------------------------+-----------------------------+
| VNET-CYNTHUS-INTELLIGENCE          |                             |
| (Dark Subnet - No Public IPs - Closed Source)  |  Azure Service Bus          |
|                                               |  (3-Topic Choreographer)    |
| cynthus-chat   cynthus-analysis   cynthus-video|                             |
+-----------------------------------------------+-----------------------------+
```

- **`vnet-cynthus-core`:** Publicly routed subnet. Hosts `cynthus-core-api` and `cynthus-core-web`. Accepts external connections over HTTPS and WebSocket protocols. All community-contributed open-source services run here.
- **`vnet-cynthus-intelligence`:** Private dark subnet. No public IP allocations. No public endpoints. Hosts `cynthus-chat`, `cynthus-analysis`, and `cynthus-video`. Reachable only via Azure VNet Peering from Core. The Intelligence subnet makes no outbound runtime calls to Core services - it receives only pre-assembled context payloads.
- **`vnet-cynthus-health`:** DMZ subnet. Hosts `cynthus-health-api`, `cynthus-health-web`, and `cynthus-device`. Enforces HIPAA consent token verification and immutable audit emission before any data exchange with external clinical partners.

Cross-VNet conversational streaming: `cynthus-core-api` routes user WebSocket sessions to `cynthus-chat` via private IP over the VNet Peering bridge, bypassing Service Bus latency. Internal AI-to-AI queries between `cynthus-chat` and `cynthus-analysis` run via synchronous gRPC within the private Intelligence namespace.

---

### 2.2 Domain Topology & Repositories

The codebase is partitioned into seven domain segments isolating business logic, licensing models, and runtime deployment contexts.

#### Cynthus Trust - Closed-Source

Manages identity, authentication, authorization, and compliance auditing. Closed-source to protect security architecture and regulatory audit integrity.

- `cynthus-identity`: Multi-tenant identity management, JWT issuance with RBAC/ABAC claims and entitlement fields, workspace assignment.
- `cynthus-audit`: Immutable append-only audit ledger. Records PHI data access and hard-constraint profile mutation events.
- `cynthus-trust-cache`: High-speed caching for token validation and session state.
- `cynthus-trust-db`: Clustered persistent storage for the Trust domain with schema-isolated partitions per service.

#### Cynthus Core - Open-Source

Governed by open-source community contribution. Handles physical data domains, logistics, user profiles, and the primary consumer interface. Community contributors may modify all services within this domain subject to the contribution boundary rules in PRD Section 10.5.

- `cynthus-core-api`: Primary public HTTPS/REST and WebSocket edge. Handles user sessions, context assembly, and request routing to Intelligence.
- `cynthus-inventory`: Predictive state management for pantry, fridge, and freezer items. Processes physical asset mutations (<200ms latency).
- `cynthus-recipe`: Recipe library management, external recipe ingestion, OCR parsing, and constraint-filtered recipe query API.
- `cynthus-logistics`: Purchase manifests, automated reorders, delivery tracking, and external supplier integrations.
- `cynthus-profile`: User preference and hard-constraint registry. Owns the allergy hard-filter. Distinguishes soft preferences (freely mutable) from hard constraints (audit-logged on every mutation).
- `cynthus-scheduler`: Background cron engine for periodic tasks, item expiry alerts, and scheduled suggestion delivery.
- `cynthus-worker`: Asynchronous background task processor for data ingestion, OCR jobs, receipt scanning, and non-time-sensitive formatting.
- `cynthus-messaging-engine`: Real-time WebSocket hub routing intra-group text messages, interactive cards, and WebRTC signaling metadata.
- `cynthus-core-web`: Fully accessible, semantic consumer UI renderer (React/Next.js, SSR).
- `cynthus-core-cache`: High-speed caching layer for Core domain services.
- `cynthus-core-db`: Clustered persistent storage with schema-isolated partitions per Core service.

#### Cynthus Intelligence - Closed-Source

Private dark subnet. Contains no public IP allocations. All inbound data arrives as pre-assembled context payloads via VNet Peering from Core. Makes no outbound runtime calls to Core services.

- `cynthus-chat`: Runtime for the Astri AI persona. Processes pre-assembled context payloads and generates streaming conversational responses.
- `cynthus-analysis`: Autonomous AI agent executing predictive lifestyle analysis, biometric trend modeling, Harmony index computation, and sentiment analysis.
- `cynthus-video`: Smart glasses HUD pipeline. Processes real-time video frames, calculates spatial coordinates, and generates clock-face orientation guidance for low-vision users.
- `cynthus-intel-cache`: High-speed caching layer for Intelligence domain services.
- `cynthus-intel-db`: Clustered persistent storage with schema-isolated partitions per Intelligence service.

#### Cynthus Health - Closed-Source

DMZ subnet hosting external healthcare provider and clinical partner interfaces. Enforces regulatory validation and consent verification before all data exchange.

- `cynthus-health-api`: Primary edge for clinical integrations. Enforces HIPAA consent token verification and read-only data access.
- `cynthus-device`: Device telemetry aggregator (provisional: expected in the `cynthus-health` repository; HUD and video data are not health-specific, so its home may change). Ingests wearable and biometric data streams. Routes hot-path raw data to time-series buffers and summarizes warm-path events for the Service Bus.
- `cynthus-health-web`: Clinical dashboard UI renderer for authorized B2B healthcare partners.
- `cynthus-health-cache`: High-speed caching layer for Health domain services.
- `cynthus-health-db`: PHI-isolated persistent storage implementing field-level encryption for all biometric and patient data (`vesta_clinical` schema).

#### Cynthus Commerce - Closed-Source

Manages monetization, payment processing, subscription management, booster pack entitlements, supplier relationships, and partner integrations.

- `cynthus-billing-api`: Subscription lifecycle management, payment processing, booster pack activation, entitlement state management, and tier enforcement. Emits `internal.system.entitlement.updated` signals on every purchase or cancellation.
- `cynthus-partner-api`: Partner and supplier integrations, wholesale API connections, slotting and bounty tracking.
- `cynthus-comm-web`: UI renderer for partner, supplier, and provider commercial interactions (React/Next.js, SSR).
- `cynthus-comm-cache`: High-speed caching layer for Commerce domain services.
- `cynthus-comm-db`: Clustered persistent storage with schema-isolated partitions per Commerce service.

#### Cynthus Emulators - Open-Source (Developer Environment Only)

Local developer container environment. Not deployed to production. Enables community contributors to run the full Core stack locally without cloud dependencies.

- `cynthus-signal-bus`: Azure Service Bus emulator container for local message routing across all three topics.
- `cynthus-signal-db`: MS SQL storage backend for the Service Bus emulator.

#### Cynthus Shared - Open-Source

Shared Pydantic model library distributed as two Python wheel packages. See Section 5 (ADR-004) for the open/closed-source boundary strategy.

---

## 3. Data Isolation, Identity & Tenancy Strategy

### 3.1 Logical Multi-Tenancy Hierarchy

Multi-tenancy is enforced strictly across all data layers, storage systems, and messaging topics using a two-tier enterprise structure.

- **`organization_id` (Corporate Tenant Boundary):** Maps to the global corporate or enterprise contract account. Owns global identity mappings and master compliance controls.
- **`workspace_id` (Functional Isolation Key):** Replaces localized household boundaries. A single organization may provision multiple independent workspaces. Every event message and every database row must carry both keys to prevent cross-tenant data visibility.

**Phase 1 workspace stub:** In Phase 1 (single-user accounts), every user is automatically assigned a personal `workspace_id` at registration with a 1:1 user-to-workspace mapping. This field is present in all schemas and JWT claims but is not exposed in the Phase 1 UI. Phase 3 introduces shared group workspaces as a purely additive capability - no schema migration required.

### 3.2 Hybrid RBAC and ABAC Hierarchy

`cynthus-identity` issues cryptographically signed JWTs containing standard role claims alongside environmental attribute contexts (ABAC) to evaluate constraints like active session consent, active workspace profile parameters, and current entitlement limits.

**Standard roles:**

- `Primary Caregiver` / `Workspace Administrator`: Full administrative rights including inventory management, telemetry visibility, and external partner authorizations.
- `Care Recipient` / `Client Contributor`: Read-write access to assigned tasks and localized telemetry inputs.
- `Standard User` / `Team Member`: Read-write access to core logistics without portal override permissions.

### 3.3 Database Partitioning & PHI Isolation

- **General logistics data:** Stored in transactional schemas within `cynthus-core-db`, handling inventory, recipe, profile, and task state.
- **Protected Health Information (PHI):** Completely isolated within the `vesta_clinical` schema inside `cynthus-health-db`. This database implements field-level encryption for all biometric telemetry and patient data, satisfying HIPAA Security Rule requirements.

### 3.4 Entitlement System (ADR-005)

Booster packs purchased via `cynthus-billing-api` create additive entitlements above base tier limits. The entitlement propagation chain is:

```text
User purchases booster pack
        |
        v
cynthus-billing-api
  - Updates entitlement state in cynthus-comm-db
  - Emits: internal.system.entitlement.updated (cynthus-topic-internal)
        |
        v
cynthus-identity (consumes signal)
  - Issues refreshed JWT with updated entitlement claims
    e.g., "max_group_members": 15  (Basic 5 + two Group Size Packs)
         "max_locations": 4        (Basic 3 + one Location Pack)
        |
        v
Downstream services enforce limits via token claims only
  - No runtime calls to cynthus-billing-api during request processing
  - Limits are evaluated from the token, not from the database
```

This design ensures downstream services remain stateless with respect to billing and never introduce billing-layer latency into request paths.

### 3.5 Cryptographic Vault Isolation

Processing sensitive workspace or clinical telemetry requires a localized key exchange independent of standard API access tokens. When `cynthus-` services process secure telemetry arrays, an ephemeral runtime handshake handles decryption using user-derived keys supplied during the individual session via `internal.system.handshake.established` patterns.

---

## 4. Context Assembly Pattern

The context assembly pattern is the critical boundary between open-source Core and closed-source Intelligence. It ensures the Intelligence subnet remains dark and dependency-free while still giving Astri everything she needs to generate accurate, safe, and personalized responses.

### 4.1 Responsibilities

`cynthus-core-api` is solely responsible for assembling all context required by Astri before any AI processing occurs. The assembly is triggered by a user message or a detected meal-planning intent.

```text
User Request (WebSocket)
        |
        v
cynthus-core-api - Context Assembly Layer
        |
        +-- GET /profile/constraints  --> cynthus-profile
        |       Returns: hard constraints + soft preferences
        |
        +-- GET /inventory/snapshot   --> cynthus-inventory
        |       Returns: current pantry state (items, quantities, expiry dates)
        |
        +-- GET /recipe/candidates    --> cynthus-recipe
        |       Input:  hard constraints from profile
        |       Returns: constraint-filtered recipe candidates only
        |
        v
Assembled Context Payload
  {
    "user_preferences": { ... },
    "hard_constraints": [ ... ],
    "inventory_snapshot": [ ... ],
    "recipe_candidates": [ ... ],
    "conversation_history": [ ... ]  (Phase 2+: cross-session memory)
  }
        |
        v
cynthus-chat ( VNet - dark subnet, via VNet Peering)
        |
        v
Streaming token response --> cynthus-core-api --> User (WebSocket)
```

### 4.2 Hard Constraint Guarantee

The constraint-filtered recipe query (`GET /recipe/candidates`) applies the allergy hard-filter inside `cynthus-recipe` using the constraint set retrieved from `cynthus-profile`. No recipe result set is ever passed to `cynthus-chat` that has not already been validated against the user's hard constraints. Astri cannot suggest an unsafe recipe because unsafe candidates are never present in the context payload she receives.

### 4.3 Intelligence Isolation Guarantee

`cynthus-chat` has no HTTP clients, service discovery configurations, or network routes pointing to any Core service at runtime. The only inbound path to the Intelligence VNet is:

- Assembled context payloads via VNet Peering from `cynthus-core-api` (conversational).
- Aggregated warm-path telemetry events from the Service Bus (analytical, handled by `cynthus-analysis`).

This eliminates bidirectional runtime dependencies between Core and Intelligence, protecting closed-source IP and enabling community contributors to develop and test Core context assembly logic independently.

---

## 5. Messaging, Component & Signal Contracts

### 5.0 The messaging library

"Messaging" names a library, not a service. `cynthus-messaging-core` (public) and `cynthus-messaging` (private) are repositories of that library: the signal schemas and the translation helpers. Every non-infrastructure service imports it for common schema definitions and helper functions. There is no orchestrator or relay service: services communicate only by broadcasting signals on the Azure Service Bus topics they are bound to.

### 5.1 Three-Topic Service Bus Architecture

The Service Bus is partitioned into three distinct topics aligned to visibility boundaries and compliance requirements. Access policies are enforced at the topic level, not just at the subscription filter level.

- `cynthus-topic-public`
  - Namespace Prefix: `public.*`
  - Access: All services (open-source and closed-source)
  - Purpose: All signals visible to open-source consumers. Carries `identity`, `device`, `inventory`, `recipe`, `logistics`, `group`, and `user` namespace events.
- `cynthus-topic-internal`
  - Namespace Prefix: `internal.*`
  - Access: Closed-source services only
  - Purpose: Private signals not exposed to open-source repositories. Carries `lifestyle`, `chat`, `video`, and `system` namespace events. Open-source pass-through services may consume envelope headers only (opaque payload).
- `cynthus-topic-audit`
  - Namespace Prefix: `internal.audit.*`
  - Access: `cynthus-portal-api`, `cynthus-identity`, `cynthus-profile`, `cynthus-audit`
  - Purpose: Append-only compliance and safety audit events. Separate topic ensures audit records cannot be co-mingled with operational traffic and supports independent retention and integrity policies.

### 5.2 Unified Service Ingestion & Dispatch Matrix

- `identity`
  - Namespace: `public.identity.*`
  - Core Publishers: `cynthus-identity`
  - Core Consumers: `cynthus-core-api`, `cynthus-billing-api`
- `device`
  - Namespace: `public.device.*`
  - Core Publishers: `cynthus-worker`
  - Core Consumers: `cynthus-analysis`, `cynthus-health-api`, `cynthus-chat`
- `inventory`
  - Namespace: `public.inventory.*`
  - Core Publishers: `cynthus-inventory`
  - Core Consumers: `cynthus-core-api`, `cynthus-analysis`, `cynthus-logistics`
- `recipe`
  - Namespace: `public.recipe.*`
  - Core Publishers: `cynthus-recipe`
  - Core Consumers: `cynthus-core-api`, `cynthus-chat`
- `logistics`
  - Namespace: `public.logistics.*`
  - Core Publishers: `cynthus-logistics`, `cynthus-partner-api`
  - Core Consumers: `cynthus-partner-api`, `cynthus-billing-api`
- `group`
  - Namespace: `public.group.*`
  - Core Publishers: `cynthus-messaging-engine`, `cynthus-core-api`
  - Core Consumers: `cynthus-core-api`, `cynthus-chat`, `cynthus-analysis`
- `user`
  - Namespace: `public.user.*`
  - Core Publishers: `cynthus-core-api`
  - Core Consumers: `cynthus-analysis`, `cynthus-chat`
- `audit`
  - Namespace: `internal.audit.*`
  - Core Publishers: `cynthus-health-api`, `cynthus-identity`, `cynthus-profile`
  - Core Consumers: `cynthus-audit`
- `chat`
  - Namespace: `internal.chat.*`
  - Core Publishers: `cynthus-chat`
  - Core Consumers: `cynthus-analysis`, `cynthus-core-api`
- `lifestyle`
  - Namespace: `internal.lifestyle.*`
  - Core Publishers: `cynthus-analysis`
  - Core Consumers: `cynthus-chat`
- `video`
  - Namespace: `internal.video.*`
  - Core Publishers: `cynthus-messaging-engine`, `cynthus-video`
  - Core Consumers: `cynthus-video`, `cynthus-chat`, `cynthus-core-api`
- `system`
  - Namespace: `internal.system.*`
  - Core Publishers: `cynthus-identity`, `cynthus-billing-api`
  - Core Consumers: `cynthus-analysis`, `cynthus-identity`, `cynthus-core-api`

### 5.3 Four Lifecycle Actions

To prevent event explosion, all domains emit events using exactly four atomic state mutation types:

- `created`: A new entity instance has been created.
- `updated`: An existing entity instance has been mutated.
- `deleted`: An entity instance has been removed or deactivated.
- `snapshot`: A full current-state snapshot of an entity, used for cache warming and catch-up.

Downstream processors evaluate the state snapshot inside the payload to compute deltas, minimizing subscription overhead.

### 5.4 Development Layout: Shared Common Kernel (ADR-004)

To support open-source infrastructure routing without exposing closed-source intellectual property, the messaging contract is distributed as two distinct Python wheel packages under a unified namespace.

**`cynthus-messaging-public`** (Open-Source):
Contains `SignalMessageEnvelope[T]`, `ActorModel`, and `ResourceModel`. Open-source services parse private signal payloads as opaque `dict` buckets, validating only envelope headers to preserve multi-tenant security isolation.

**`cynthus-messaging-internal`** (Closed-Source / Private Azure Artifact):
Extends the public package with deep, strongly-typed Pydantic model validation for all private signal namespaces. Available only to closed-source services authenticating against the private Azure Artifacts feed.

- Open-Source
  - Signal Classification: Public (`public.device.*`, `public.inventory.*`)
  - Validation Depth: Deep (strict Pydantic model)
- Open-Source
  - Signal Classification: Private (`internal.lifestyle.*`, `internal.video.*`)
  - Validation Depth: Opaque (`SignalMessageEnvelope[dict]`)
- Closed-Source
  - Signal Classification: Any
  - Validation Depth: Deep (strict Pydantic via internal wheel)

### 5.5 Global Signal Envelope Structure

Every signal published to any Service Bus topic must adopt the following standardized envelope schema:

```python
# cynthus/messaging/shared/signal_message_envelope.py
from datetime import datetime, timezone
from typing import Generic, TypeVar, Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict

PayloadT = TypeVar("PayloadT", bound=Any, default=Any)

class SignalMessageEnvelope(BaseModel, Generic[PayloadT]):
    """Immutable common structural envelope published across the Service Bus."""
    model_config = ConfigDict(frozen=True, populate_by_name=True)

    signal_id: UUID = Field(default_factory=uuid4)
    correlation_id: UUID = Field(..., description="Trace ID tracking cross-service interactions.")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sender_service: str = Field(..., description="The microservice that emitted the signal.")
    schema_version: str = Field("1.0.0", description="Semantic layout version.")
    topic: str = Field(..., description="cynthus-topic-public | cynthus-topic-internal | cynthus-topic-audit")

    organization_id: str = Field(..., description="Corporate tenant boundary context.")
    workspace_id: str = Field(..., description="Functional isolation partition key - always present from Phase 1.")
    payload: PayloadT
```

---

## 6. High-Frequency Telemetry Ingestion (Dual-Stream Path)

To support wearable device ingestion without overloading the centralized topic bus, telemetry processing splits into a Hot Path and a Warm Path.

```text
[ Wearable Device / Smart Glasses ]
            |
            +---> Hot Path (WebSockets / WebRTC)
            |         |
            |         v
            |   High-Throughput Buffer / Time-Series DB
            |         | (Aggregation Window / Frame Processing)
            |         v
            |   cynthus-messaging (Health VNet)
            |         | (Summarizes into structured time-slice snapshots)
            |         v
            +---> Warm Path (AMQP) --> cynthus-topic-public
                                              |
                                              v
                                    Azure Service Bus Spine
                                              |
                                              v
                                    cynthus-analysis ( VNet)
```

1. **Hot Path:** Continuously streaming sensors (live heart rate, CGM readings, smart glasses video frames) push raw data intervals over WebSockets or WebRTC directly to high-throughput time-series buffers or the `cynthus-video` pipeline, bypassing the Service Bus entirely.
2. **Warm Path:** `cynthus-device` summarizes hot path data into structured time-slice snapshots (`public.device.telemetry.streamed`) or emits anomaly flags (`internal.video.anomaly.detected`) onto the choreography bus for downstream analytical processing.

---

## 7. Technical Implementation Blueprint

### 7.1 Shared Primitive Models

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
    """Polymorphic representation of an identity interacting within the IAM fabric."""
    id: str = Field(..., description="Unique identification token.")
    type: ActorType = Field(..., description="Structural classification enum.")
    role: str = Field(..., description="Operational context mask (e.g., LEGAL_GUARDIAN).")
    acting_on_behalf_of: Optional[str] = Field(None, description="Optional root parent user context.")
```

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
    """Polymorphic definition of any tracked asset partition in the ecosystem."""
    id: str = Field(..., description="Unique underlying reference key.")
    type: ResourceType = Field(..., description="Asset class discriminator enum.")
    role: str = Field(..., description="Functional sub-context designation.")
```

### 7.2 FastAPI Unified Lifespan Pattern

FastStream broker contexts must tie directly into FastAPI native startup lifespans. All subscription and publisher declarations are defined as global, thread-safe module-level variables.

```python
# Inside downstream application runtimes (e.g., cynthus-core-api)
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

logger = logging.getLogger("cynthus.infra")

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """Manages thread-safe FastStream broker lifespan hooks over the service run."""
    logger.info("Initializing FastStream broker contexts on Azure Service Bus connection.")
    yield
    logger.info("De-initializing FastStream broker connections cleanly.")

app = FastAPI(lifespan=lifespan)
```

### 7.3 One-Class-Per-Module Rule

All codebases strictly enforce a one-class-per-module convention. This ensures clean git diffs, predictable import mapping, and scannable repository structure for community contributors.

### 7.4 Logging Verbosity Profile

- **Level:** Trace (verbose during development, INFO minimum in production).
- **Structure:** Semantic structured logging.
- **Correlation Strategy:** Every asynchronous message must append a `correlation_id` (UUIDv4) within its top-level metadata envelope to enable cross-service trace mapping through the full ecosystem.

---

## 8. Regulatory Compliance, Auditing & Verification

### 8.1 HIPAA Compliance Flow (`cynthus-health`)

```text
[External Clinical Partner]   cynthus-health-api    cynthus-identity     cynthus-audit
         |                           |                     |                    |
         |--- Request Telemetry ---->|                     |                    |
         |                           |--- Validate Token ->|                    |
         |                           |<-- Context OK ------|                    |
         |                           |--- Log Immutable Access Fact ----------->|
         |                           |    (internal.audit.access.logged)        |
         |<-- Stream Read-Only Data -|                                          |
```

1. **Consent Token Verification:** The inbound bearer token signature is validated against `cynthus-identity` public cryptographic certificates to confirm valid authorization, active clinician scope, and active workspace consent parameters.
2. **Immutable Audit Emission:** `cynthus-health-api` blocks response execution until an `internal.audit.access.logged` event is successfully committed to `cynthus-audit`. No PHI data is returned before the audit record is confirmed.

### 8.2 Hard-Constraint Mutation Audit Flow

Every write to a user's hard-constraint profile in `cynthus-profile` emits an `internal.audit.constraint.mutated` event on `cynthus-topic-audit` before the mutation is committed. This event captures the before-state, after-state, actor ID, and timestamp. This is a safety record, not a HIPAA requirement, but it applies from Phase 1.

### 8.3 AI Governance & Transparency

To satisfy applicable state-level AI governance frameworks (e.g., TRAIGA), any automated clinical insights or lifestyle assessments generated by Intelligence services must append a `model_configuration_hash` metadata block certifying the exact LLM configuration version utilized. This disclosure is mandatory within any medical context and is enforced at the `cynthus-chat` response serialization layer.

---

## 9. Accessibility & Interface Contract

All Astri response payloads are subject to the following formatting constraints enforced at the `cynthus-chat` serialization layer:

- Response payloads are restricted to logical, sequential text formats optimized for screen-reader layout trees.
- No reliance on geometric orientation, spatial placement, or visual-only layout elements.
- Data arrays returned from AI evaluations are expressed in descriptive structural patterns that describe data linearly.
- Real-time spatial tracking tokens (from `cynthus-video`) use standardized clock-face orientation fields (`relative_clock_position: int`, constrained 1-12) and exact metric distances to translate physical environment data into voice-navigable descriptions for low-vision users.

---

## 10. Architectural Decision Record Index

- ADR-004
  - Title: Hybrid Open/Closed-Source Messaging Schema Strategy
  - Status: Approved
- ADR-005
  - Title: Booster Pack Entitlement Propagation via Token Claims
  - Status: Approved

### ADR-004: Hybrid Open/Closed-Source Messaging Schema Strategy

**Context:** Open-source pass-through services must route private signals without exposing closed-source intellectual property or payload schemas.

**Decision:** Twin-strategy combining layered schema distribution and dynamic envelope ingestion. The public wheel exposes envelope headers and shared primitives only. Open-source services parse private payloads as opaque `dict` buckets. Closed-source services install the private internal wheel for full deep validation.

**Consequences:**

- Positive: Complete protection of closed-source intellectual property.
- Positive: Decoupled release management cycles for Core vs.  layers.
- Positive: Full type safety inside the dark Intelligence subnet.
- Risk: Open-source pass-through services lose compile-time IDE auto-completion for private signal inner fields.

---

### ADR-005: Booster Pack Entitlement Propagation via Token Claims

**Context:** Booster pack purchases must be reflected in downstream service enforcement without introducing billing-layer latency into request paths.

**Decision:** `cynthus-billing-api` is the single source of truth for active booster state. On every purchase or cancellation, it emits `internal.system.entitlement.updated` on `cynthus-topic-internal`. `cynthus-identity` consumes this signal and issues a refreshed JWT with updated entitlement claims (e.g., `"max_group_members": 15`). Downstream services enforce all resource limits using token claims exclusively - they never call `cynthus-billing-api` at runtime.

**Consequences:**

- Positive: Zero billing-layer latency in request paths.
- Positive: Stateless enforcement in all downstream services.
- Positive: Entitlement state is auditable via token inspection.
- Risk: Brief window between booster purchase and token refresh during which old limits may be enforced. Mitigation: `cynthus-identity` targets <5 second signal processing time; UX confirms activation before the user's next interaction.
