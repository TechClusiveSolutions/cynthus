# Persistence layer abstraction

Status: approved plan, 2026-11-14. Tracking issue: cynthus#71. Slices: cynthus-shared#157 (S1), cynthus#72 (S2),
cynthus-core#230 (S3), cynthus-core#231 (S4).

## Intent

Mirror the event-to-signal design on the storage side. Business logic knows only domain objects (events and
resources). A separate persistence layer translates them to and from PostgreSQL rows (long-term storage) and Redis
entries (short-term storage). The two sides are tested independently.

Criteria set by the owner:

- No Python code has raw SQL statements, except in very specific situations.
- Dictionaries that are cached are not crafted by business logic.
- There is a very distinct line between business logic and persistence code. Each side can be tested independently of the
  other, for short-term and long-term persistence.

The use case that motivates it: a user asks to update another user's recipe. A recipe update request event is generated,
the recipe owner is notified and makes a decision. The request, the decision and the response are all persisted.
PostgreSQL holds the records and Redis holds the in-between data. Tables, serializers and cache entries are built by
dedicated code, not by hand-written insert statements or dictionaries in business code. The recipe flow is a later
feature (see Out of scope); the inventory location is the first proof.

## What exists today

- Every service container has a hand-written ORM package `models/` with its own `Base`, naming convention, schema and
  `RecordMixin` (id, organization_id, workspace_id, created_at, updated_at, deleted_at). The containers are inventory,
  profile, recipe and shopping (cynthus-core) and auth (cynthus-trust). `base.py` and `record_mixin.py` are copied into
  each container. Alembic migrations are per container.
- Business rules and persistence share a class. `LocationService` and the shelf, item and owner services take an
  `AsyncSession` and build `select`, `add`, `flush`, `execute` and `refresh` calls inline next to the rules. Creating a
  location also creates its default shelf in the same transaction.
- The domain classes live in cynthus-shared (`cynthus.core.event`, `cynthus.core.resource`). The ORM classes in the
  containers are separate classes for the same things with different shapes. Nothing translates between them.
- There is almost no raw SQL. `text()` appears only in partial-index predicates and in migrations. The real problem is
  inline ORM queries in business code.
- Redis is used through the shared `RedisClient`. Callers build their own keys and values: API replies, recipe picture
  uploads, the notification hub and the OAuth state store. The values are simple strings, not structured event or
  resource data.
- ADR-011 makes every delete a soft delete and enforces one default per workspace with a partial unique index. ADR-013
  keeps event requests, decisions and conditions append-only in Auth, for access requests only. ADR-014 gives each
  segment its own database and cache. ADR-010 defines tenants.

## Decisions

- Library plus per-segment. cynthus-shared holds the abstractions: serializer bases, the registry, the cache key and
  entry, and the boundary check. Each segment keeps its own ORM tables and concrete serializers, so schemas stay
  isolated as ADR-014 requires.
- Both directions. Every serializer has `to_record` and `from_record` (the cache serializer has the equivalent), with a
  round-trip test, so business logic never touches ORM rows or raw cache dictionaries.
- The first proof is the inventory location: `LocationService` create, get, list, update and delete.
- Enforcement is an import-boundary test per segment plus ruff rule S608, with a short named exception list (index
  predicates and migrations). No new dependency.
- Business code depends on a repository interface (a port) defined next to it. The serializers are tools of the
  persistence side; the repository is the line. Handlers build the repository from the session and pass it in, so
  business methods no longer take an `AsyncSession`.
- `archived` becomes part of the domain `StorageLocation`. `created_at` and `updated_at` stay persistence-only.
- The first cache consumer is the API reply cache, because structured resource caching has no consumer today.
- ADR-015 records the rule.
- The milestone is "Cynthus 1.0 - Platform Foundation Complete", the priority is P2 and the size is XL, split into slices
  no bigger than M.

## Design

### Library in cynthus-shared

The new package `cynthus.persistence` has one class per module:

- `record.RecordSerializer[T]` (abstract): `domain: ClassVar[type[T]]`, `to_record(obj) -> dict[str, Any]` and
  `from_record(record) -> T`. A serializer is pure: no session, no clock, no I/O.
- `record.RecordSerializerRegistry`: `register`, `serializer_for` (by object or class name), unique domain names, an empty
  registry is honoured. `record.UnknownRecordError` is a `LookupError`.
- `cache.CacheKey.build(namespace, tenant_id, workspace_id, *parts)`: the one place that shapes cache keys, with
  validated parts, a length limit, and tenant and workspace always present.
- `cache.CacheEntry` (a frozen dataclass with key, value and expiry) and `cache.CacheSerializer[T]` (abstract) with
  `to_entry` and `from_value`.
- `boundary.ImportBoundary(package_roots, forbidden_prefixes, allowed_modules)`: scans modules with `ast`, and
  `violations()` lists the offenders. Each segment uses it in one test.
- The domain class `StorageLocation` gains `archived_at` and the `archived` property.

### Segment: cynthus-core inventory

- `inventory/repositories/LocationRepository` (abstract) offers create, get, list_live, update, soft_delete, count_live
  and what the default-location rules need. It takes and returns domain objects. `ShelfRepository` is the same for
  shelves, and shelf creation on location create stays atomic in one unit of work.
- `inventory/persistence/` holds `LocationRecordSerializer`, `ShelfRecordSerializer`, `SqlLocationRepository` and
  `SqlShelfRepository`. Only this code uses the session and `inventory.models`.
- `LocationService` keeps the rules and calls the repositories only. The handler is the composition root.
- Import boundary: `inventory.operations`, `inventory.service` and the handlers, except the composition module, may not
  import `sqlalchemy`, `inventory.models`, `inventory.persistence` or `cynthus.core.redis`.

## Slices

Each slice is its own issue and no slice is bigger than M.

1. S1, cynthus-shared#157, size M: the `cynthus.persistence` library, `StorageLocation.archived`, the boundary helper,
   `docs/persistence.md`, and release v0.19.0.
2. S2, cynthus#72, size S: ruff S608 and the boundary-test pattern in `templates/repo`, ADR-015, and a pointer in the
   engineering standards.
3. S3, cynthus-core#230, size M: inventory serializers and repositories, `LocationService` converted, the boundary
   test, and tests at every level. Depends on S1.
4. S4, cynthus-core#231, size S: the API reply cache through `CacheSerializer`. Depends on S1 and not on S3.

The order is S1, then S2 and S3 in parallel, then S4.

## Acceptance criteria

- AC1, lint and CI: ruff S608 is enabled in cynthus-shared and cynthus-core, and `text()` appears only in the listed
  exception files (model index predicates and migrations).
- AC2, unit: the import-boundary test fails when a business module imports `sqlalchemy`, `inventory.models`,
  `inventory.persistence` or the Redis client, and passes on dev. There is one per segment.
- AC3, unit: `LocationService` tests run with a fake repository and never import `sqlalchemy` (the test asserts that).
  `SqlLocationRepository` tests run on in-memory SQLite without business code.
- AC4, unit: `from_record(to_record(x)) == x` for location and shelf, including soft-deleted and archived states, and the
  record carries tenant and workspace ids.
- AC5, boundary and unit: no module outside the persistence side builds a cache key or value, and reply keys come from
  `CacheKey`.
- AC6, feature and system: the existing location tests pass without changing their expectations. After a deploy, which
  needs the owner's yes, the live end-to-end suite on JMac keeps 44 passed, 0 failed and 5 skipped.
- AC7, feature integration: each slice has a test from a real domain object to a persisted record or cache entry and
  back.
- AC8, docs: this design, ADR-015, `docs/persistence.md`, the CHANGELOGs and README links, with the markdown checks
  passing.
- AC9, accessibility: there is no user-facing change, so this does not apply.

## Risks

- Creating a location also creates a shelf and uses counts and refreshes in one transaction. The repository interface
  must keep that atomic, or the rewrite changes behaviour. If it cannot, the coder stops and reports.
- The shared release in S1 gates the core slices, so S1 stays small.
- The domain and ORM classes differ today (`archived`, audit columns), and the decisions above say where each lives.
- Serializers stay synchronous and pure. Only the repository awaits.
- Deploying a refactor with no new feature needs the owner's explicit yes and a rollback plan, which is the previous
  image.

## Out of scope

Other containers (profile, recipe, shopping and auth, one plan each), sharing `Base` and `RecordMixin` through the
library, a collaboration request type (an ADR-013 extension), the recipe-update flow, any database schema or API change,
and the cynthus-core-cache consumer of inventory signals.
