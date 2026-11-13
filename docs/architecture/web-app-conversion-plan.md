# Plan: converting the prototype web app into the Python services

The first prototype (`cynthus-web`, Node.js) proved the feature set. This plan moves every feature into the
service that the Architectural Design Document (ADD v6) says owns it. The prototype stays in place as a reference
until the Python services reach parity; its browser front end is reused (decision 3 below).

## Decisions

1. **Meals, suggestions and group votes** live in `cynthus-core-api`. The language-model parts (suggestion generation,
   vote tie-breaking, health insight) are delegated to `cynthus-analysis`.
2. **Personal health logging** lives in Core, inside `cynthus-profile`. `cynthus-health-api` stays the read-only
   clinical edge for external providers, with the PHI isolation described in the ADD.
3. **UI:** the Python `cynthus-core-web` service serves the existing accessible JavaScript front end now. A React/Next.js
   renderer, as the ADD describes, is a later, separate piece of work.
4. **Messaging:** `faststream-azure-servicebus` behind `SignalPublisher`/`SignalSubscriber` interfaces (ADR-006).

## Feature ownership

- Register, login, logout, password change, account deletion
  - Owning service: `cynthus-identity` (`cynthus-trust/auth`)
  - Notes: JWT with role and entitlement claims; a personal workspace is created at registration
- Profile, diet, allergies, dislikes, likes, units, medical notes
  - Owning service: `cynthus-profile`
  - Notes: Hard constraints (allergies, diet) are audited before every write
- Groups, members, roles, invite codes
  - Owning service: `cynthus-profile`
  - Notes: Workspace membership
- Group chat
  - Owning service: `cynthus-core-api`
  - Notes: Polling now; the WebSocket hub (`cynthus-messaging-engine`) comes later
- Personal health metrics and summaries
  - Owning service: `cynthus-profile`
  - Notes: Not PHI; no clinical sharing
- Locations, inventory, adjustments, log, alerts
  - Owning service: `cynthus-inventory`
  - Notes: `GET /inventory/snapshot` for context assembly
- Libraries, recipes, ratings, favorites, import
  - Owning service: `cynthus-recipe`
  - Notes: `GET /recipe/candidates` applies the allergy hard-filter
- Shopping list, restock
  - Owning service: `cynthus-logistics`
  - Notes: none
- Meals, consume, suggestions, group votes
  - Owning service: `cynthus-core-api`
  - Notes: none
- Astri chat
  - Owning service: `cynthus-chat`
  - Notes: Receives an assembled context payload; makes no outbound calls
- Suggestion generation, vote tie-break, health insight
  - Owning service: `cynthus-analysis`
  - Notes: Also payload-driven
- Dashboard, search, export, request routing
  - Owning service: `cynthus-core-api`
  - Notes: Context assembly layer
- Static front end
  - Owning service: `cynthus-core-web`
  - Notes: none
- Scheduled suggestions, expiry alerts
  - Owning service: `cynthus-scheduler`
  - Notes: Publishes signals; consumed by `cynthus-core-api`

## Cross-cutting rules

- One class per module, one unit test module per source module (engineering standards, sections 1 and 2).
- Each service owns its tables, in its own PostgreSQL schema inside the domain database. Tests use SQLite.
- `organization_id` and `workspace_id` are present on every row and every signal from the start.
- Services accept the identity service's signed JWT (RS256 in deployments, HS256 for local runs and tests).
- The hard-constraint guarantee is structural: `cynthus-recipe` filters candidates against the profile service's
  constraints, so unsafe recipes never reach `cynthus-chat` or `cynthus-analysis`. Both AI services additionally verify
  their output against the constraints that arrive in the payload.

## Delivery order (milestones)

1. Platform Foundation: tooling, CI, linting, messaging interfaces and adapter.
2. Identity & Profile.
3. Inventory & Recipe.
4. Planning & Logistics.
5. Astri (context assembly, chat, analysis).
6. Health & Web.

Each feature set is a GitHub issue in the owning repository, tracked on the *Cynthus Engineering Tracker* project.
