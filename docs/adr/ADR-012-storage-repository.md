# ADR-012: A cynthus-storage repository for the databases and caches

**Status:** Proposed (2026-11-12)
**Relates to:** ADR-008 (fewer, larger containers), ADR-010 (tenants), the hosting cost analysis of 2026-11-10.

## Context

Each application group runs its own database and cache: core, auth and intelligence each have a Postgres and a Redis,
defined in the compose file of the repository that uses them. Measured on JMac on 2026-11-11:

| Container | Memory |
|---|---|
| core-db, auth-db, intel-db | about 37, 60 and 25 MB |
| core-cache, auth-cache, intel-cache | about 6, 6 and 32 MB |

The owner proposed moving all six to a repository called `cynthus-storage`, running one database server and one cache
server with separate schemas, and giving Auth, Core and Intelligence each a private network to storage so that Core
can never reach the Auth or Intelligence networks. The known cost is that any storage outage affects every consumer,
including Auth; in production replicas reduce but do not remove that.

Two facts shape the answer:

- **The saving is small.** Merging all six saves about 100 MB. The reasons to do this are ownership, backup,
  replication and network isolation, not memory.
- **The caches are not interchangeable.** Auth keeps security state in Redis: sign-in lockout counters, refresh
  tokens, verification and reset records. Redis has one `maxmemory` and one eviction policy per server, and `FLUSHALL`
  is global. If another consumer fills a shared cache, keys that enforce a lockout can be evicted.

## Decision

A new repository, **cynthus-storage**, owns the stateful servers. Services keep their own schemas and migrations; the
storage repository owns the servers, their networks, their roles and their backups.

### Postgres: one server, a database and a role per consumer

- One Postgres server. Inside it, **one database per consumer** (`core`, `auth`, `intelligence`), not one database with
  several schemas. A schema is a namespace, not a boundary; a database with `REVOKE CONNECT ... FROM PUBLIC` and a login
  role of its own is.
- Each consumer connects as its own role, which can connect only to its database. Inside the core database the
  services keep their schemas (`inventory`, `profile`, `recipe`, `shopping`) and their migrations as they are.
- `pg_hba.conf` lets each role in only from its own network.
- Superuser access is for the storage repository's own tooling (migrations are run as the consumer's role).

### Networks

The storage compose file defines one network per consumer: `storage_core`, `storage_auth`, `storage_intelligence`.
The Postgres container joins all three; a consumer's compose file joins only its own, as an external network. These
are separate networks, not override files: an override file is for varying an environment, not for drawing the
topology. A consumer never joins another consumer's storage network, and Core never joins the Auth or Intelligence
ones. The cost is that the one Postgres listener is reachable from all three, so the role, the database and
`pg_hba.conf` are what isolate the data, not the network alone.

### Redis: Auth's stays separate

- **Auth: its own Redis** (`storage-cache-auth`), with `noeviction`, so a full cache refuses writes rather than
  dropping a lockout.
- **Core and Intelligence: one shared Redis** (`storage-cache`), with an ACL user per consumer limited to its key
  prefix and its channels, and a bounded `maxmemory` with an eviction policy suited to caches.
- This is two Redis servers instead of three, not one. The owner proposed one; this is the point where this ADR
  differs, and the reason is the eviction of security state above.

### What stays the same

Services find storage by `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USERNAME`, `DB_PASSWORD` and the `CACHE_*` settings. The
only change for a service is the values (the host names the storage server on its network) and the compose network it
joins.

## Options considered

1. **Leave the six containers where they are.** Nothing breaks, nothing improves: three compose files each own a
   database and a cache, and there is no single place to back up, replicate or fence.
2. **One Postgres, one Redis, schemas only (the first proposal).** The fewest containers. Schemas do not isolate
   credentials, and one Redis shares eviction and flushing across Auth and the rest. Rejected for Redis; for Postgres
   it becomes option 3 with databases instead of schemas.
3. **One Postgres with a database and role per consumer; Redis for Auth and one for the rest (this ADR).** Keeps the
   isolation that matters and gives one place for the databases.

## Consequences

- One Postgres is a single point of failure for Auth, Core and Intelligence on a host without replicas. On a
  production host the storage repository carries the replica and the backup plan. On the dev hosts a storage
  restart restarts the sign-in path too.
- Every consumer's compose file changes: it drops its database and cache services, joins its storage network and
  points `DB_HOST` and `CACHE_HOST` at storage.
- Data moves from three database volumes to one: a one-time `pg_dump` and restore per consumer, done in a window.
- The hosting cost analysis changes by about 100 MB of memory and by the number of containers to run.

## Work plan

1. Create the repository: compose file, Postgres image with the init script (databases, roles, `pg_hba.conf`), the
   Redis servers with their ACLs, networks, README, changelog.
2. Add a script that dumps and restores each consumer's database, and a check that each role cannot connect to
   another consumer's database (a test, run in the dev environment).
3. Move Core first (it has the most schemas), then Intelligence, then Auth. After each, run the end-to-end flows and
   the broker-down check.
4. Update the compose files, `.env` examples, the standards and the hosting cost analysis.
5. Add replicas and backups for production (own design).

## Not decided here

- The production replication topology and the backup schedule.
- Whether the shared Redis needs a second server once Intelligence's cache load is known.
- Whether Auth's Postgres should stay on its own server in production for blast-radius reasons (this ADR allows
  either: the roles and databases are the same).

## Review triggers

- A consumer's workload slows another's (measured query or cache latency): split that consumer out.
- Intelligence's cache use grows past what a shared server holds: give it its own Redis.
