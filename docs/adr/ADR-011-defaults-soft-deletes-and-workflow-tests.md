# ADR-011: Defaults, soft deletes and the workflow integration tests

**Status:** Proposed (2026-11-12)
**Relates to:** ADR-009 (the Service object and layout), ADR-010 (tenants and billing), ADR-007 (signal broker).

## Context

The owner asked for integration tests that follow a person from registration to unregistering: a tenant and a user are
created, a workspace is created, a recipe is written, a list is made from it, locations and shelves are created and
changed, items are moved, a location is deleted, and the user unregisters. Writing them showed that several steps
do not exist yet, and that three rules were not written down: what a default is, what deleting means, and how
these tests run without the real services.

What the code does today (2026-11-12): registration creates a user whose record carries `organization_id` and
`workspace_id`, there is no tenant entity and nothing creates a workspace; inventory has no default flags, no move
operation and no shelf created with a location; most deletes are SQL deletes (locations have `archived_at`, shopping
lists have `deleted_at`); there is no list-from-recipe and no unregister.

## Decision

### Defaults: one per workspace for each kind of thing

A default is the choice the system makes when the person does not choose. For each kind of resource, a workspace has
**at most one default**, and a resource that contains others has at most one default among its own:

- Location: One default per workspace.
- Shelf: One default per location.
- Engagement place: One default per workspace (the place an engagement uses when none is given).

- When a workspace has exactly one location, that location is the default; when a location has exactly one shelf, that
  shelf is the default. The first one created becomes the default; making another default clears the previous one in
  the same change.
- The database enforces it: a partial unique index on `is_default` among live rows (rows with no `deleted_at`).
- A location is created with one shelf, so adding items to a location always has a target: the location's default shelf.
- Deleting the default makes the system promote the remaining one when exactly one is left; otherwise there is no
  default until the person picks one, and an operation that needs one is refused with a message saying so.

### Shelf fill order

A shelf has a default **fill order**, the order in which positions are filled. It names the starting corner and
whether a row or a column is filled first:

- back left
  - Rows first (`horizontal`): `back_left_horizontal`
  - Columns first (`vertical`): `back_left_vertical`
- back right
  - Rows first (`horizontal`): `back_right_horizontal`
  - Columns first (`vertical`): `back_right_vertical`
- front left
  - Rows first (`horizontal`): `front_left_horizontal`
  - Columns first (`vertical`): `front_left_vertical`
- front right
  - Rows first (`horizontal`): `front_right_horizontal`
  - Columns first (`vertical`): `front_right_vertical`

The default is `back_left_horizontal`. The value is stored on the shelf as text.

### Soft deletes

- **Every delete is a soft delete.** A row gets `deleted_at` and stays; reads ignore rows that have it. The only
  exception is an explicit data-removal request, which removes the rows for real.
- Deleting a thing deletes what it contains in the same change, with the same `deleted_at` value, so restoring it brings the
  same rows back and nothing else. A non-empty location is deleted with its shelves and items; the API asks for
  confirmation first.
- Every table that holds a person's data gets `deleted_at`. This is a migration in each of inventory, profile, recipe and
  shopping, and every query filters on it.
- Unregistering soft-deletes the user and the tenants they alone own (what happens to a tenant with other members is
  not decided here), and revokes their tokens.

### How the workflow tests run

- **Records** are created in schemas named `test_<service>` (for example `test_inventory`), in a real Postgres, by the
  services' own migrations. The schema name is the service's name with a prefix taken from the environment
  (`DB_SCHEMA_PREFIX`, empty in production); the tests set it and drop the schemas afterwards.
- **A test database connector** gives the tests a session on those schemas without the service's own start-up.
- **The API is mocked at its new schema.** Endpoints that do not exist yet (create a workspace, create a list from a recipe,
  move items, unregister) are described by request and response schemas and served by a mock, so the tests
  fix the contract before the logic is written. The real endpoint logic is written later, test first.
- **The broker is mocked** with the in-memory signal bus the shared library already has (`InMemorySignalBus`); the
  RabbitMQ round trip stays covered by the shared integration tests against a real broker.
- **Fixtures** for the core model classes live with the classes (`cynthus.core.test.fixture`), as the messaging
  fixtures do.
- A second test follows the same workflow through the API and checks the signals emitted and the values in the cache.

## Not decided here

- The Engagement and its Place have no tables or classes yet; the default-place rule applies when they are built.
- How a list made from a recipe uses locations.
- What happens to a tenant with other members when its owner unregisters.

## Consequences

- Four services get a migration (`deleted_at`, and the default and fill-order columns in inventory) and their models
  change; the endpoints' own logic is not changed by this ADR.
- The workflow tests are written first and fail on the steps that are not built, each failing for a named reason.

## Work plan

1. Fixtures and model changes in cynthus-shared (defaults, fill order, `deleted_at`).
2. Migrations and models in inventory (defaults, fill order, `deleted_at`), then profile, recipe and shopping (`deleted_at`).
3. The schema prefix and the test database connector.
4. The API schema mocks and the workflow tests (database test, then API test).
5. The endpoint logic, one step at a time, turning each failing step green.

## Review triggers

- A kind of resource needs more than one default per scope.
- A table cannot take `deleted_at` (for example because a unique key must hold across deleted rows).
