# ADR-014: Each segment keeps its own database and cache

**Status:** Accepted (2026-11-13)
**Supersedes:** ADR-012 (a `cynthus-storage` repository).
**Relates to:** ADR-008 (fewer, larger containers), ADR-010 (tenants).

## Context

ADR-012 proposed moving the databases and caches of Auth, Core and Intelligence into one repository and one Postgres
server. The saving was about 100 MB of memory. The owner rejected the consolidation on 2026-11-13 for a reason the
ADR did not weigh: the segments were designed with their own databases and caches so that each is a security boundary
and can isolate itself during an attack or an outage. Billing and accounting, Trust, Core and Intelligence should each
be able to run their own API services and keep working, at limited capacity, when another segment is down or under
attack.

## Decision

- Each segment owns its database and its cache, defined in its own compose file, on its own internal network. No
  segment shares a database server, a cache server, a credential or a volume with another.
- A segment reaches another only through its public interfaces: the Auth token keys (JWKS) and signals on the broker.
  Neither is a data store, and a segment that cannot reach them degrades instead of stopping (see Consequences).
- Isolation is kept deliberately. A proposal to share a database or cache server needs a new ADR that shows how a
  segment still runs alone.
- What is shared is the recipe, not the server: one template for the database and cache containers (versions, health
  checks, backup hooks), so that four copies do not drift.

## Options considered

1. **One Postgres and one Redis for all segments (ADR-012).** Fewer containers and one place to back up. One outage,
   bad upgrade, runaway query or compromised superuser credential reaches every segment, and a segment can no longer run
   alone. Rejected.
2. **Separate servers per segment, with a shared template (this ADR).** Keeps the boundary and fixes the drift.
3. **Separate servers, no shared template (today).** Keeps the boundary; the four copies already differ (Redis is
   unpinned, backups are not defined). Rejected as the end state.

## Consequences

- The cost stays: about 100 MB more memory than a shared server, and a database and a cache to run per segment.
- Every segment needs its own backup and restore, and a restore that has been practised.
- A failure-isolation check is needed to prove the property: stop one segment's database and confirm that the others
  still answer. Until it exists, the claim is a design intent, not a tested fact.
- Cross-segment dependencies must not hide a data store. A segment that needs Auth keys keeps the last fetched keys and
  says so when they are stale.

## Work plan

1. A shared template for the database and cache containers, with pinned versions and a backup hook.
2. Backup and restore scripts per segment, and a documented restore drill.
3. A failure-isolation check in `cynthus-testing`.
4. `docs/infrastructure.md` states the isolation and why.

## Review triggers

- A production hosting plan that cannot run a server per segment: write a new ADR that keeps the isolation (separate
  servers or managed instances per segment).
