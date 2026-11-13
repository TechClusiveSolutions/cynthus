# Archive

Superseded drafts, kept for history. Nothing here is current; use the masters listed in `../README.md`.

- `prd/`
  - Contents: PRD drafts 2026-03-03, 2026-06-01 V1-V3
  - Superseded by: `../PRD.md` (4.2)
- `add/`
  - Contents: ADD drafts 2026-06-01 to V5
  - Superseded by: `../ARCHITECTURE.md` (6.0)
- `signals/`
  - Contents: Signal lists, schemas, events lists, the 2026-06-01 handling matrix
  - Superseded by: `../signals/signal-catalog.md`, `../signals/signal-list-by-service.md`
- `features/`
  - Contents: Feature list 2026-06-04
  - Superseded by: `../features/feature-registry.md`
- `overviews/`
  - Contents: Early overviews and app notes, the 2026-06-04 system topology blueprint
  - Superseded by: `../ARCHITECTURE.md`
- `notes/`
  - Contents: Implementation and directory-structure notes
  - Superseded by: none
- `vesta/`
  - Contents: Predecessor project (Vesta, called Selda inside the files): object list, API contract
  - Superseded by: - (the object list may inform the data model)

## Topology blueprint (2026-06-04): names that changed in ADD 6.0

The blueprint predates ADD 6.0 and is not folded into it. Its structural models (envelope, actor, resource) are covered by ADD sections 5 and 7. Its service names differ:

- `cynthus-vision`: `cynthus-video`
- `cynthus-intel` repository: Cynthus Intelligence
- `cynthus-identity-api`, `cynthus-identity-db`: `cynthus-identity`, `cynthus-trust-db`
- `cynthus-portal-api`, `cynthus-portal-web`: `cynthus-health-api`, `cynthus-health-web`
- `cynthus-partner-portal`, `cynthus-commerce-db`: `cynthus-partner-api`, `cynthus-comm-web`, `cynthus-comm-db`
- `cynthus-audit-api`, `cynthus-audit-db`: `cynthus-audit`, `cynthus-trust-db`
- `cynthus-infra` (`cynthus-messaging`, `cynthus-store`): Cynthus Emulators (`cynthus-signal-bus`, `cynthus-signal-db`)
- `public.*` / `internal.*` signal registry: `signals/signal-catalog.md`
