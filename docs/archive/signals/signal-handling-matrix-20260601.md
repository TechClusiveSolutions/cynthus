## 1. Service List

### cynthus-analysis

Package: Cynthus-Intelligence
Status: closed-source
Signals Published: Lifestyle
signals Consumed: Clinical, Device, Inventory, System

### cynthus-core-api

Package: Cynthus-Core
Status: open-source
Signals Published: Clinical
signals Consumed: Auth, Chat, Device, Lifestyle

### cynthus-identity

Package: Cynthus-Trust
Status: closed-source
Signals Published: Auth, System
signals Consumed: Audit

### cynthus-chat

Package: Cynthus-Intelligence
Status: closed-source
Signals Published: Chat
signals Consumed: System

### cynthus-inventory

Package: Cynthus-Core
Status: open-source
Signals Published: Inventory
signals Consumed: Logistics

### cynthus-health-api

Package: Cynthus-Health
Status: closed-source
Signals Published: Audit
signals Consumed: Auth, Chat, Clinical, Logistics

### cynthus-health-web

Package: Cynthus-Health
Status: closed-source
Signals Published:
signals Consumed:

### cynthus-scheduler

Package: Cynthus-Core
Status: open-source
Signals Published:
signals Consumed:

### cynthus-core-web

Package: Cynthus-Core
Status: open-source
Signals Published:
signals Consumed:

### cynthus-worker

Package: Cynthus-Core
Status: open-source
Signals Published: Clinical, Device, Logistics
signals Consumed: Audit, Auth, Inventory, Lifestyle

## 2. Mapped Publisher & Consumer Matrix

### Audit

Tracks B2B portal compliance intercepts and data inspections for HIPAA audit requirements.

Publishers:

- `cynthus-health-api` (Emitted before streaming requested biometric registries to external partners)

Consumers:

- `cynthus-identity` (Validates compliance boundaries, coordinates security auditing records)
- `cynthus-worker` (Saves immutable event facts to the compliance log tracking repository)

### Auth

Manages identity states, role/attribute changes, and cryptographic token handshakes.

Publishers:

- `cynthus-identity` (Emits token status changes or session parameter updates)

Consumers:

- `cynthus-core-api` (Clears cached session validation contexts)
- `cynthus-health-api` (Synchronizes active partner session parameter checks)
- `cynthus-worker` (Records security log histories)

### Chat

Coordinates asynchronous conversational tracking, usage transparency metadata, and state auditing.

Publishers:

- `cynthus-chat` (Emits conversational metadata blocks, text layout linear summaries, and AI governance transparency logs)

Consumers:

- `cynthus-worker` (Saves linear screen-reader text histories to persistent operational data layers)
- `cynthus-health-api` (For enterprise auditing/oversight reviews of AI clinical interactions)

### Clinical

Handles individual discrete telemetry points, manual entries, and Remote Patient Monitoring (RPM) billing code compliance summaries.

Publishers:

- `cynthus-core-api` (Transforms manual user inputs or third-party webhooks into facts)
- `cynthus-worker` (Calculates and emits monthly billing summaries like `clinical.billing.compliance`)

Consumers:

- `cynthus-analysis` (Ingests discrete entries to calculate behavioral trend patterns)
- `cynthus-health-api` (Exposes clinical entries to read-only dashboards post-consent checking)

### Device

Manages aggregated warm-path time-slice telemetry blocks and instant real-time anomaly tracker boundary breaches.

Publishers:

- `cynthus-worker` (The continuous ingestion worker aggregating raw hot-path database windows)

Consumers:

- `cynthus-analysis` (Processes continuous metric blocks into predictive assessments)
- `cynthus-core-api` (Listens for critical anomaly flags to bubble immediate push notifications to consumer interfaces)

### Inventory

Tracks mutations to space equipment logs, pantry supplies, and logistics asset states.

Publishers:

- `cynthus-inventory` (The microservice handling physical mutations and transactional records)

Consumers:

- `cynthus-worker` (Processes automated background evaluation parameters)
- `cynthus-analysis` (Monitors resource consumption balances for lifestyle calculations)

### Lifestyle

Distributes computed 24-hour workspace harmony matrix scores, tracking tasks, variances, and operational indices.

Publishers:

- `cynthus-analysis` (The proprietary predictive calculation engine)

Consumers:

- `cynthus-worker` (Prepares automated scheduling variations or logs performance assessments)
- `cynthus-core-api` (Delivers calculated insights to consumer `cynthus-web` instances)

### Logistics

Handles scaled recipe configurations and automated external B2B vendor inventory fulfillment routing.

Publishers:

- `cynthus-worker` (The asynchronous background scheduler processing active automated replenishment parameters)

Consumers:

- `cynthus-inventory` (Increments pending incoming order tracking logs)
- `cynthus-health-api` (If required to coordinate delivery manifests or routing checks with partner supply portals)

### System

Handles cross-cutting infrastructure state changes that force runtime behavior mutations across services, specifically the distribution of session parameters and ephemeral authorization keys.

Publishers:

- `cynthus-identity` (Dispatches user-derived session parameters upon successful verification)

Consumers:

- `cynthus-analysis` (Listens for these temporary keys to execute the ephemeral runtime handshake and decrypt protected telemetry values in memory)
- `cynthus-chat` (Listens for these temporary keys to execute the ephemeral runtime handshake and decrypt protected telemetry values in memory)
