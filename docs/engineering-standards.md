# Engineering Standards

These standards apply to every Cynthus repository. They follow the conventions of the AREA project
(`area-project/docs/architecture/engineering-standards.md`), adapted to Cynthus' service layout.

## 1. Module structure

- **One class per module.** A module defines exactly one class (plus private helpers it needs). The module is named
  for the class in `snake_case`: `ConstraintMatcher` lives in `constraint_matcher.py`.
- Packages re-export their public classes from `__init__.py`; `__init__.py` holds no logic.
- No module-level mutable state. Resources (database sessions, HTTP clients, brokers) are created in the application
  lifespan, stored on `app.state`, and handed to code through FastAPI dependencies or constructor arguments.
- Every function and method has type annotations for parameters and the return value.

```python
# good: one class, injected collaborators
class InventorySnapshotBuilder:
    def __init__(self, repository: InventoryRepository) -> None:
        self._repository = repository

    def build(self, workspace_id: str) -> InventorySnapshot: ...
```

## 2. Tests

- **One test module per source module**, named `test_<module>.py`, in the same relative position under `test/`.
  `src/inventory/service/inventory_snapshot_builder.py` is tested by
  `test/service/test_inventory_snapshot_builder.py`.
- Unit tests use fakes for collaborators (repositories, HTTP clients, the broker). They never need Docker, the
  network or a real database; SQLite in memory stands in for PostgreSQL.
- Every behaviour change ships with a test that fails without it. Bug fixes begin with a failing test.
- `python -m pytest --cov=src --cov-fail-under=75` must pass. Coverage is a floor, not a goal.
- Expected failures (`xfail`) are allowed only for a documented, tracked defect, and name the issue number.

## 3. Linting

- **Python:** `ruff check .` (configuration in `pyproject.toml`). CI runs it as the `lint` job.
- **Documentation:** `markdownlint-cli2` over the Markdown files the repository owns (`docs.yml`).
- Fix findings; do not blanket-disable rules. A targeted `# noqa: <rule>` needs a reason in the same comment.

## 4. HTTP endpoints

- REST resources are plural nouns; actions that are not CRUD are sub-resources (`POST /meals/{id}/consume`).
- Errors use a single envelope: `{"error": "<human readable message>"}` with the right status code.
- Services trust the signed access token only. A route declares the permission it needs through a dependency.
- Every row and every signal carries `organization_id` and `workspace_id`.

## 5. Logging

- Module loggers are created through `logging.getLogger(__name__)`; request-scoped details are passed as arguments.
- Every cross-service operation logs the `correlation_id`.
- Never log secrets, tokens, passwords or health values.

## 6. Messaging

- Signals are published and consumed through the FastStream broker defined in ADR-006 (Azure Service Bus).
- Application code depends on the `SignalPublisher` interface, never on the broker class directly.
- Hard-constraint changes emit `internal.audit.constraint.mutated` before the change is committed.

## 7. Workflow and branching

1. **A GitHub issue exists before work with a deliverable starts.** Exploratory work may be filed afterwards.
2. Set the issue's properties when work starts: Issue Type, Milestone, Priority, Subtype, Applies to, Estimated
   Completion, labels, and a link to the relevant design document. Add it to the *Cynthus Engineering Tracker*
   project (<https://github.com/orgs/TechClusiveSolutions/projects/6>) and move its Status to `In Progress`.
3. **Create the branch with `gh issue develop <number> --base dev`** and use the name GitHub generates.
4. **Feature branches merge into `dev`; `dev` merges into `main`.** There are no direct commits to either.
5. Open a pull request into `dev`. Its description follows `.github/pull_request_template.md` and contains
   `Closes #<issue>`.
6. CI must pass (`lint` and `test`). Request GitHub Copilot as a reviewer, read its feedback, and address or explicitly
   dismiss each point. Re-request the review after pushing fixes.
7. Merge with a squash commit once the checks are green and the feedback is resolved. Delete the branch.
8. Trivial fixes still get an issue; it may be one line.

### Issue types

| Type | The deliverable is |
|---|---|
| Planning | a design document |
| Research | a knowledge document |
| Testing | a test result |
| Application Feature / Bug | code or configuration inside the running application |
| Infrastructure Feature / Bug | CI, repository settings, provisioning: anything outside the application |

A change that spans application and infrastructure is split into two issues.

### Status values

`Backlog`, `Planned`, `In Progress`, `Testing`, `Complete`, `Cancelled`.

### Milestones

Milestones are objective-based and shared by all repositories:
Platform Foundation, Identity & Profile, Inventory & Recipe, Planning & Logistics, Astri, Health & Web.

## 8. Releases

`dev` is the integration branch. A release is a pull request from `dev` into `main`, followed by a version tag.
