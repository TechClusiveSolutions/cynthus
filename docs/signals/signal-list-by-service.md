Service Name: cynthus-core-api
Repository: cynthus-core
Description:
Responsible For:
Signals Published:
Signals Consumed:

# Signal List By Service

## Commerce

### Billing API

### `cynthus-partner-api`: partner integrations
### `cynthus-comm-cache`: caching for commerce services
### `cynthus-comm-db`: persistant storage for commerce services
### cynthus-comm-web`: UI renderer for partner, supplier, and provider interactions

### Billing API

### Cache

### DB

## Core

### api
### cache
### db
### inventory
### logistics
### profile
### recipe
### scheduler
### shopping
### web
### worker

## Emulators
## Health
## Intelligence
## Trust


## Cynthus Trust
* `cynthus-audit`: auditing and compliance
* `cynthus-identity`: identity management and authentication
* `cynthus-trust-cache`: caching for trust services
* `cynthus-trust-db`: persistant storage for trust services (clustered and distinct schemas for each domain)
## Cynthus Core
* `cynthus-core-api`: primary edge for user interactions
* `cynthus-core-cache`: caching for core services
* `cynthus-core-db`: persistant storage for core services (clustered with distinct schemas for each domain)
* `cynthus-inventory`: inventory management
* `cynthus-recipe`: recipe ingestion and storage
* `cynthus-logistics`: inventory logistics (movement between locations, ordering, delivery, etc)
* `cynthus-core-web`: UI renderer for user interactions
* `cynthus-scheduler`: periodic time-based task management
* `cynthus-worker`: ingress and non-time-based task management
## Cynthus Intelligence
* `cynthus-analysis`: sentiment analysis, biometric trend analysis, energy level and dietary trend analysis, etc
* `cynthus-chat`: Astri persona (conversational life assistant/companion)
* `cynthus-intel-cache`: caching for intelligence services
* `cynthus-intel-db`: persistant storage for intelligence services (clustered and distinct schemas for each domain)
* `cynthus-video`: heads up display and real-time video streaming for live and AI companion mode
## Cynthus Health
* `cynthus-health-api`: primary edge for clinical integrations
* `cynthus-health-cache`: caching for health services
* `cynthus-health-db`: persistant storage for health services
* `cynthus-health-web`: UI renderer for clinical interactions
* `cynthus-messaging`: device telemetry, etc
## Cynthus Emulators
* `cynthus-signal-bus`: Azure Service Bus emulator
* `cynthus-signal-db`: MS SQL storage for the Service Bus emulator
## Cynthus Shared
* shared Pydantic model classes for common signal schemas
