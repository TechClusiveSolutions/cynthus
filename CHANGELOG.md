# Changelog

All notable changes to cynthus-documentation are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the versions follow
[Semantic Versioning](https://semver.org/). The Cynthus ecosystem release that bundles
each version is listed in the `cynthus` documentation repository.

Every pull request adds a line under `Unreleased`; a release renames that section to the
version and date.

## [Unreleased]

- ADR-014 (issue 61): each segment keeps its own database and cache so it can run alone during an attack or an outage; ADR-012 (`cynthus-storage`) is Superseded; `docs/infrastructure.md` states the isolation.
- Infrastructure versions and first-time setup (issue 59): `docs/infrastructure.md` records the PostgreSQL, Redis, RabbitMQ, mail sink and Service Bus emulator versions, each segment's database and cache, and the order to start a stack; linked from `docs/README.md`.
- Standard README structure (issue 57): `check_markdown.py` (and its copy in `templates/repo`) fails a root `README.md` whose headings are not Description, Prerequisites, Installation, Minimal configuration, Gotchas and More documentation, after one level 1 heading. New `templates/repo/README.md` model; the standards describe the rule; this repository's README follows it.
- Documentation for screen readers (issue 55): Markdown is ASCII only, has no tables (lists instead), names the language of every code block, and `README.md` has the standard name. `.github/scripts/check_markdown.py` now enforces this, and checks that relative links resolve, in the `docs-lint` job; markdownlint covers every Markdown file. The diagrams and tables in the signal, feature and ADR documents became lists; the archive was converted from Windows-1252 to ASCII (the damaged characters are repaired); an empty archived file (`Cynthus-ArchitectureDesignDocument-20260602-V4.md`) was removed; the engineering standards describe the rules.
- Added ADR-012 (a `cynthus-storage` repository: one Postgres server with a database and role per consumer, a private network per consumer, Auth's Redis kept separate) and ADR-013 (access requests: append-only decisions, conditions as their own records with expiry of 5 days for access requests and 7 for collaboration requests, and the rule that nobody grants a privilege they lack). Issues 48 and 49.
- Added ADR-011, the rules for defaults (one per kind per workspace, one default shelf per location, shelf fill orders), soft deletes everywhere except data-removal requests, and how the registration-to-first-use workflow tests run (test_* schemas, mocked API schema, in-memory broker). Issue 46.
- Added ADR-010, the tenant model: the tenant is the boundary (personal or organizational), a parent tenant with the same owner bridges an owner's tenants and holds no workspaces, an owner never gets owner rights through another user's token, billing accounts are separate and attached per tenant, and `tenant_id` replaces `organization_id` additively. Issue 44.
- Corrected ADR-008: the Domain container reduces broker connections on RabbitMQ only; the Azure Service Bus SDK opens a connection per sender and per receiver, so on the emulator the full stack (about 17 connections) exceeds the cap of 10 and only a subset (9 connections on Aries) fits. Issue 42.
- Added ADR-009, the design for one Service object (identity in `cynthus.core`, runtime in `cynthus.service`) and one layout for every service package, building on shared issue 93; left the tenant and organization vocabulary for a separate decision. Amended ADR-008 (handler time limit 60 s, shared subscriber, link to ADR-009). Issue 40.
- Added ADR-008, the design for running inventory, profile, shopping and logistics as one hosting container chosen by `SERVICES`, with Recipe, Auth, the gateways and the Celery services kept separate; includes the measurements, the settled questions and the work plan. Issue 38 (core issue 184).
- The draft 1.0 release manifest now pins cynthus-shared v0.11.1 (selectable signal broker) and records that the dev stack has run on RabbitMQ. Issue 36.
- Added ADR-007, the decision to make the signal broker selectable by environment (`SIGNAL_BROKER`: Azure Service Bus by default, or RabbitMQ). It records the RabbitMQ topology (topic exchange, quorum queue per subscription, dead-letter queues, delivery limit, publisher confirms), the behaviour both brokers must share, and what RabbitMQ lacks. ADR-006 is marked partly superseded and engineering standards section 6 now describes the selectable broker.
- Added the ecosystem release manifest: `releases/README.md` explains the versioning scheme (ecosystem manifest, per-app SemVer, a separate signal schema version) and `releases/1.0.md` is the draft 1.0 set pinning every repo's current tag.

## [0.1.0] - 2026-11-10

- Align documents with the messaging-library model; add cynthus-device (#13)
- Render behavioural namespace tests (#6)
- Catalog the Shopping signals and document the Shopping design (#27) (#29)
- Catalog the chat message requested and generated signals (#24)
- Catalog the inventory owner added and removed facts (#21)
- Add the profile signals to the signal catalog (#19)
- Add the identity audit signals to the signal catalog (#17)
- Add inventory shelf signals to the signal catalog (#15)
- Consolidate master design documents (#10)
- Reorganize design documents into master PRD, architecture and roadmap (#8)
- Establish the Cynthus engineering workflow (#1) (#2)
- Add architecture notes and the cross-repository test tooling
- Initial commit
