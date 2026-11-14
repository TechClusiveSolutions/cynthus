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
- **Tests come in three levels.** A *unit test* checks one function or object: can the event be created, does it have
  the right properties, do its methods return the right values. A *feature integration test* checks a whole feature, or
  a series of features, inside one repository with the outside mocked: when an inventory item created event is
  generated, a `public.inventory.item.created` message reaches the mocked broker. A *system integration test* checks
  that a subsystem works across services and lives in `cynthus-testing`: when a user creates an item through the API
  service, the Inventory service builds the event from the signal on the broker.
- **Coverage targets.** The floor above stays until a repository adopts the targets: 90 percent of lines and 80
  percent of branches, measured with `--cov-branch`. Each repository adopts them in its own issue. New modules are
  expected to be at 100 percent line and branch.
- **User-facing functionality meets WCAG 2.2 level AA** and is checked automatically in CI where a page is rendered, and
  by hand with a screen reader before release. Automated checks find only part of the problems.
- Expected failures (`xfail`) are allowed only for a documented, tracked defect, and name the issue number.

## 3. Linting

- **Python:** `ruff check .` (configuration in `pyproject.toml`). CI runs it as the `lint` job; `test` runs the unit tests with the coverage gate.
- **Documentation:** `markdownlint-cli2` over the Markdown files the repository owns (the `docs-lint` job in `ci.yml`).
- **Documentation for screen readers:** `.github/scripts/check_markdown.py` (also in the `docs-lint` job) fails on non-ASCII characters (write `-` for a dash, `->` for an arrow, no emoji), pipe tables (write a list: one item per row, the columns as nested items), a code block without a language (use `text`), CR line endings, trailing spaces, a missing final newline, a README not named `README.md`, a root README whose headings are not the standard ones (next bullet), and a relative link whose file or heading does not exist. The product owner reads the documentation with a screen reader, so these are not style preferences.
- **README structure:** every repository's root `README.md` is a quick start, and `check_markdown.py` fails when its headings differ. One level 1 heading (the name of the repository), then exactly these level 2 headings in this order: `Description`, `Prerequisites`, `Installation`, `Minimal configuration`, `Gotchas`, `More documentation`. Minimal configuration lists only what must be set to start, not every setting. A section with nothing to say says so in one line. Anything longer lives in the `docs` folder and `More documentation` links to it. `templates/repo/README.md` is the model.
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

- Signals are published and consumed through the `SignalPublisher` and `SignalSubscriber` interfaces. The broker behind them is chosen by `SIGNAL_BROKER` (ADR-006 and ADR-007): Azure Service Bus by default, or RabbitMQ.
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
6. CI must pass (`lint`, `test` and `docs-lint`). Review is by an independent reviewer who sees only the spec and the
   diff (section 9). GitHub Copilot reviews are not requested at present.
7. The owner gives an explicit yes, then the pull request is merged with a merge commit once the checks are green. A
   pull request into `dev` does not close its issue (`Closes` acts only on the default branch), so close the issue by
   hand after the pull request shows as merged. Delete the branch.
8. Trivial fixes still get an issue; it may be one line.

### Issue types

- Planning: a design document
- Research: a knowledge document
- Testing: a test result
- Application Feature / Bug: code or configuration inside the running application
- Infrastructure Feature / Bug: CI, repository settings, provisioning: anything outside the application

A change that spans application and infrastructure is split into two issues.

### Status values

`Backlog`, `Planned`, `In Progress`, `Testing`, `Complete`, `Cancelled`.

### Milestones

Milestones are objective-based and shared by all repositories:
Platform Foundation, Identity & Profile, Inventory & Recipe, Planning & Logistics, Astri, Health & Web.

## 8. Releases

`dev` is the integration branch. A release is a pull request from `dev` into `main`, followed by a version tag.

## 9. Feature development with roles

A feature is finished only when it has: an entry in a design document, an issue, unit tests and a feature integration
test, developer documentation, and (where a user sees it) user documentation and a WCAG check. A pull request exists
for every feature that reaches production. The user documentation requirement is a soft rule: not every line of code
is described there.

### 9.1 Roles

- **Designer** writes the spec: inputs, outputs, use cases, numbered acceptance criteria, and which test level covers
  each criterion. Before writing it, the designer reads the existing classes it will build on.
- **Coder** implements the production code and its documentation from the spec.
- **Tester** writes the tests from the spec alone and does not read the coder's new files.
- **Reviewer** reads only the spec and the diff, never the coder's or the tester's reasoning, and reports findings
  ranked by severity with a failure scenario for each.
- **Coordinator** is the main session. It talks to the owner, opens the issue, branch and pull request, keeps them up to
  date, runs the full checks, fixes small findings and routes the rest back to the right role.
- **Recorder** is a script, not an agent (section 9.5).

### 9.2 Steps

1. Design: the owner states the task, the coordinator proposes, and the owner approves or asks for options.
2. Open the issue and the branch (section 7).
3. Implement and test. For work of size M or larger the coder and tester run in parallel from the spec. For XS and S
   work one agent writes both and a fresh reviewer still reviews.
4. Run lint, the full test suite and the coverage report locally.
5. Independent review. Fix blockers and should-fix findings, then ask the same reviewer for a short delta check when
   production code changed after the first review.
6. Commit, push, and open the pull request into `dev`.
7. The coordinator reports and waits. The owner's explicit yes is required before every merge and every deploy; a
   notification or an agent's report is never approval.

### 9.3 Briefs and context

- Each agent gets a short written brief: the spec, the files it may read and write, and what it must not touch. It never
  gets another agent's transcript.
- Resume an agent for follow-up work instead of starting a new one; it already holds the context.
- Agents do not commit, push or open pull requests. The coordinator does.

### 9.4 Specs

- Check the existing classes before writing a spec. A spec that ignores what already exists is the most expensive
  mistake: the first design of the event-to-signal work was reworked after review for this reason.
- Number the acceptance criteria. Name the exception type each failure raises; tests that accept several exception types
  let a wrong implementation pass.
- Say what is out of scope and where it goes (a follow-up issue).

### 9.5 Recording

- A run log and a main-session usage report are kept outside every repository, so recording never needs a pull request.
  The log records each phase with a timestamp, the tokens and seconds each subagent reports, and every defect with who
  caught it: tests, coverage, CI, review or self-review.
- A run that is done entirely in the main session is logged the same way. It is the baseline for comparing the
  workflow, and the comparison is made per phase and per artifact, not on totals alone, because sizes differ.
