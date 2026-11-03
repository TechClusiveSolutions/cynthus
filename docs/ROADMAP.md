# Cynthus roadmap

**Version:** 1.0 (2026-11-03)  
**Sources:** PRD 4.2 section 9 (phases, targets, services, features), `cynthus-web` NEXT-STEPS, `tools/TESTING.md` open items, `architecture/web-app-conversion-plan.md`.  
**Rule:** this file summarises the plan. Scope and dates are owned by the PRD; change them there first.

Every phase keeps two commitments from Phase 1: `organization_id` and `workspace_id` on all schemas and APIs (active from Phase 3), and entitlement claims in the JWT (updated by booster packs from Phase 3).

## Where we are (2026-11-03)

- **Prototype:** `cynthus-web` (Node) implements the Phase 1-3 "Basic" feature set plus a few Phase 4 items. It stays as a reference until the Python services reach parity.
- **Python services:** scaffolded across `cynthus-core`, `cynthus-trust`, `cynthus-intelligence`, `cynthus-health`, `cynthus-messaging-core` and `cynthus-messaging`. 2058 Python tests and 64 Node tests pass at 99.0 % statement coverage; import and syntax defects were repaired (`tools/FIX-LOG.md`).
- **Not started:** user-facing behaviour in the Python services. `cynthus-intelligence` (analysis) still depends on `faststream.azure` (ADR-006).

## Phases

| Phase | Target | Astri | Theme |
|---|---|---|---|
| 1 | January 2027 | v1.0 single-session assistant | Core MVP |
| 2 | Q2 2027 | v1.5 profile-persistent, inventory-aware | Inventory intelligence and user profile |
| 3 | Q4 2027 | v2.0 group-aware | Group workspaces, messaging, billing |
| 4 | H1 2028 | v2.5 event planning, early predictive logic | Engagements, analytics, recipe import |
| 5 | H2 2028 | v3.0 commerce-aware | B2B commercial launch |
| 6 | H1 2029 | v3.5 real-time cooking guide | Live companion and partner platform |
| 7 | H2 2029, pending regulatory approval | v4.0 clinical intelligence | Clinical integration |
| 8 | 2030 | v4.5 enterprise intelligence | Enterprise scale and compliance |

### Phase 1 - Core MVP (January 2027)

- **Services:** `cynthus-identity`, `cynthus-core-api`, `cynthus-core-web`, `cynthus-inventory`, `cynthus-recipe`, `cynthus-profile`, `cynthus-chat`, the three domain databases (`cynthus-core-db`, `cynthus-trust-db`, `cynthus-intel-db`), `cynthus-signal-bus`, `cynthus-signal-db`, `cynthus-shared`.
- **Features:** FT-MP-001 to 005, FT-AI-001, FT-AC-002, FT-AM-001.
- **Deferred:** groups, messaging, billing, clinical, commerce, analytics.

### Phase 2 - Inventory intelligence and user profile (Q2 2027)

- **Services:** `cynthus-worker`, `cynthus-scheduler`.
- **Features:** FT-IM-001 to 003, 005, 007; FT-RM-001 to 003; FT-AM-002; FT-RT-002; FT-MP-002.

### Phase 3 - Group workspaces, messaging and billing (Q4 2027)

- **Services:** `cynthus-messaging-engine`, `cynthus-billing-api`, `cynthus-analysis` (Harmony Score baseline).
- **Features:** FT-MP-006 to 009; FT-GM-001 to 003; FT-IM-002, 004, 006, 008; FT-MS-001 to 003; FT-BL-001; FT-AM-003; FT-AX-001, 002.

### Phase 4 - Engagements, analytics and recipe import (H1 2028)

- **Services:** `cynthus-logistics`, `cynthus-partner-api` (read-only stubs).
- **Features:** FT-MP-010; FT-RM-004; FT-EM-001 to 003; FT-CO-001; FT-RT-001; FT-TG-001; FT-DA-001, 002.

### Phase 5 - B2B commercial launch (H2 2028)

- **Services:** `cynthus-partner-api` (full), `cynthus-comm-web`.
- **Features:** FT-IM-009; FT-SR-001 to 003; FT-BL-002; FT-AM-004; FT-RP-002.

### Phase 6 - Live companion and partner platform (H1 2029)

- **Services:** `cynthus-video`.
- **Features:** FT-LC-001; FT-SR-004, 005; FT-AM-005 to 007; FT-RP-003, 004.

### Phase 7 - Clinical integration (H2 2029, pending regulatory approval)

- **Go-live depends on:** SaMD regulatory strategy review, BAA execution with provider partners, HIPAA penetration testing, FDA SaMD classification for wearable-assisted RPM.
- **Services:** `cynthus-health-api`, `cynthus-health-web`, `cynthus-device` (telemetry aggregator), `cynthus-audit` (PHI access logging), `cynthus-health-db`.
- **Features:** FT-CL-001, 002; FT-RM-005; FT-AC-001, 003.

### Phase 8 - Enterprise scale and compliance (2030)

- **Features:** FT-RP-001, FT-DA-003.

## Engineering work between now and Phase 1

Not in the PRD; drawn from the project's own notes. Unprioritised.

1. **Port the prototype into the Python services** following `architecture/web-app-conversion-plan.md`: ownership by service, `cynthus-core-web` serving the existing accessible front end, FastStream behind `SignalPublisher`/`SignalSubscriber` (ADR-006).
2. **Resolve the test open items** in `tools/TESTING.md`: the `faststream.azure` dependency, router/module name shadowing, the scheduler's import-time file read, half-moved payload folders, two outdated tests, folder naming.
3. **Close the documentation gaps** listed in `README.md`: missing feature definitions, services the catalog uses that ADD 6.0 does not name, one name for two messaging services.
4. **Prototype hardening** (only while it remains the reference): a manual NVDA/JAWS pass, chat over WebSockets or SSE instead of 4-second polling, deployment with HTTPS, a persistent volume and a real session secret.
5. **Rotate the Groq and OpenRouter keys.**

## Not scheduled

Phase 4+ items in the prototype's NEXT-STEPS (billing tiers and boosters, supplier ordering, wearables, care-team sharing) follow the phases above. A React/Next.js renderer for `cynthus-core-web` is planned (PRD, Phase 1 service list) but the conversion plan ships the existing front end first.
