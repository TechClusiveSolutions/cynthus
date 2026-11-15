# Axe audit script (live, signed-in accessibility audit)

Type: infrastructure (developer tool plus skill). Repository: cynthus-tools. Tracking issue: cynthus#81. Approved by the owner 2026-11-15.

## Intent (binding)

Owner, 2026-11-15: "turn the current CI job into a full CLI-based script that can login as a user. It can be run like the audit skill we built." The script replaces the idea of stubbing API responses: it audits the real pages of a deployed stack as a real signed-in user. The CI job `a11y` (cynthus-core PR 243 and 245, markup only, scripts blocked) stays as the fast gate.

Problem and approach are separate. Problem: the CI check cannot see what scripts add (lists with data, messages, errors, the opened navigation), so accessibility of those states is unchecked, and the owner is the only tester of them. Owner's first thought on approach: a CLI that logs in, run on demand like python-repo-audit.

## Survey: what exists

Verified 2026-11-15 on cynthus-core dev (after PR 245), cynthus-testing dev (5894de0) and cynthus-tools main.

- F1. CI check (cynthus-core `containers/web/a11y/check.mjs`): builds the 22 pages with `containers/web/build/build.mjs`, serves them like nginx (pages by name, files from `static/`), blocks the page's own scripts, runs axe-core 4.10.2 through Playwright 1.49.1 with tags wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa, best-practice. `allowed.json` holds exceptions with reasons; a stale one fails. All 22 pages pass.
- F2. Pages are shells; scripts fill them. Pages: account, forgot-password, inventory, items (list, detail, form, delete), shelves (same four), locations (same four), login, profile, register, register-check-email, reset-password, unavailable, verify. Per-record pages take an id from the address (`/inventory/items/{id}`, `/new`, `/{id}/edit`, `/{id}/delete`), see `static/js/records.js` (route table). Shelf and item forms take a parent in the query (`?location=`, `?shelf=`).
- F3. Navigation is disclosure navigation built by `static/js/nav.js` from `site/nav.json`; only Inventory, Profile and Account are available, the rest are marked unavailable.
- F4. Sign-in is `POST /session/login` through the Web service (cookies set by the Session service, token never in the answer); a browser request with an `Origin` header must name the site or be in `ALLOWED_ORIGINS` (`docs/cynthus-session.md`). A real browser driving the real login page satisfies both. Wrong passwords lock the account and the client address (hard lock ends only with a password reset).
- F5. Writes are acknowledged, then confirmed over the notification socket; the page then announces the result ("Location added."). A script must wait for the announcement, not for the request.
- F6. cynthus-testing already runs against JMac as a seeded user (`E2E_SEED_USER`, `E2E_SEED_PASSWORD`, default user `test.user@example.com`) and uses `E2E_WEB_URL`. It is Python with no browser and runs in a container on the stack network. Not verified: what data the seeded user has on JMac now.
- F7. cynthus-tools is a private repository with no CI and no branch protection (commit to main). It holds `audit/python_repo_audit.py` with tests, `skills/python-repo-audit`, `skills/feature-run`, `skills/plan-feature` (copies; `~/.claude/skills` is the source of truth), `metrics/`, `ci/`.
- F8. The audit skill's shape: a deterministic script writes JSON and markdown reports to the metrics folder, the session triages findings, files one issue in the repository, logs with `wlog.py` and `usage.py`, and does not fix anything.
- F9. Engineering standards (cynthus, `docs/engineering-standards.md`): user-facing functionality meets WCAG 2.2 AA and is checked automatically in CI where a page is rendered (line 42). This script adds a live check; it does not replace the CI one.
- F10. ADR-011 (soft deletes): deleting a record through the web marks it deleted, it does not remove the row. Cleanup by this script therefore leaves deleted rows. Not verified in the running stack.
- F11. Not existing, needed: a documented test user with a known password for the audit (the seeded user exists, its password is not in any repository, correctly), a way to read the stack URL (JMac address and Web port, `WEB_PORT`, not verified from outside the stack network), and the pinned axe-core file for Python (see D1 and A3).

## Decisions (owner)

- D1 (2026-11-15). Placement: cynthus-tools, Python (Playwright for Python plus axe-core). CI job stays in cynthus-core.
- D2 (2026-11-15, revised same day). Test data: the audit runs on a throwaway test stack on the `cynthus` VM (192.168.56.60), started fresh for the run and removed afterwards, then the original stack is put back. The script creates its own data through the real pages and audits every state. It does not delete data: the stack is discarded. (Replaces create-and-clean-up on a shared stack; a cleanup script on the real database was rejected: soft deletes, per-segment databases, risk.)
- D3 (2026-11-15). Credentials: environment variables only (the audit user's password is generated per run, see A2; the VM login is your normal ssh key).
- D4 (2026-11-15). First version covers every page, signed in, with data. Not chosen, therefore out of scope: opened navigation menus as their own states, error and validation states, signed-out and registration flows.

## Assumptions (confirm or change)

- A1. Name: script `cynthus-tools/a11y/axe_audit.py`, skill `axe-audit`, run id `axe-audit-<yyyymmdd>`.
- A2 (revised). The audit user is registered through the real register page on the throwaway stack, the verification link is read from that stack's mail sink, and the password is generated per run and kept in memory. No stored password, no secrets folder. Variables: `AXE_URL` (base address of the Web service, for example `http://JMac.attlocal.net:<port>`), `AXE_USER`, `AXE_PASSWORD`. Never printed, never written to the reports, never in an argument. The skill reads the password from `D:\Private\Jad\scratchpad\cynthus\secrets` (an existing folder) into the process environment; I do not read the secrets folder without your yes at run time.
- A3. Axe source: Python `playwright` plus a pinned `axe.min.js` of axe-core 4.10.2 (the version CI uses), loaded from the `axe-core` npm package tarball hash-pinned in a `requirements-a11y.txt` plus a small fetch step, or the `axe-playwright-python` package if it bundles 4.10.x. Slice 1 verifies which and records the version in every report. Same tags as CI.
- A4 (revised). No record cleanup: the test stack is removed (see S0). Records carry a run marker (`axe-audit-<timestamp>`) only so a report names them. The stack script's `down` runs on every exit path, so an interrupted run still removes the test stack and restores the original.
- A5. Safety: one sign-in attempt only (a fresh stack has no lockout history, but the rule stays); on any failure the script stops (no retries), so it cannot lock the test account. A wrong or missing variable fails before any browser opens.
- A6. The script only touches the host named in `AXE_URL`, and refuses to run when the host is not in an allow-list in its config (the VM address 192.168.56.60 by default and `localhost`). JMac and any production host are not on the list.
- A7. Report: JSON (every violation with page state, rule, impact, nodes, help URL) and markdown, in `<metrics>/audits/axe-<date>.*`, plus a screenshot per failing state in `<metrics>/audits/axe-<date>/`. Exit code 1 when any violation exists, 2 when the run itself failed (sign-in, timeout), 0 otherwise.
- A8. Board values: Size per slice below, tracking issue XL as the skill default (Feature label), Priority P2, milestone "Cynthus 1.0 - Platform Foundation Complete", Status Planned, due date today plus 3 days. Your template had no size or priority for this one.
- A9. Slice issues are filed in cynthus-tools (Applies to: Platform, Subtype: Infrastructure), tracking issue in cynthus, design document in cynthus `docs/features/axe-audit-script.md`.
- A10 (revised). A live run stops the VM's current stack, so it needs your explicit yes each time I start it, like a deploy. Never `docker compose down -v` on the original stack: its volumes are kept, so putting it back restores its data. The test stack uses its own compose project name and its own volume names (override file), so a mistake in `down` cannot touch the original's data.
- A11. Stack lifecycle (your sequence, 2026-11-15): record what runs (`docker ps`, compose project, image tags), `docker compose down` on the original (no `-v`), bring the test stack up with override files (fresh volumes), wait for the Web health check, run the audit, `docker compose down -v` on the test project only, `docker compose up -d` on the original, wait for its health. The script reports what was running before and after; a difference is reported, not hidden.
- A12. The VM's stack is not fully working today: `cynthus-infra-messaging` crash-loops (exit 139) and `cynthus-scheduler` is unhealthy (seen 2026-11-15 over ssh). Writes are confirmed over the notification socket (F5), so without a working messaging emulator the data states may not appear. S0 starts with a spike that says what works; states that cannot be reached are reported as did-not-run.

## Design

Python package `cynthus-tools/a11y/` (no import of any service code):

- `config.py`: `AuditConfig` (frozen dataclass: `base_url`, `user`, `password`, `out_dir`, `run_id`, `headless`) and `load_config(env)`; raises `ConfigError` (missing or malformed variable, host not allowed). `password` is excluded from `repr`.
- `browser.py`: `open_session(config)` context manager (Chromium, one context, viewport 1280 by 900) and `sign_in(page, config)` which drives the real `/login` page and waits for `/inventory`; raises `SignInError` on any other outcome and never retries.
- `axe.py`: `AxeRunner` with `scan(page, state_name) -> list[Violation]`, same tags as CI, axe-core source loaded from the pinned file; `Violation` and `Node` dataclasses.
- `states.py`: `State` (name, url, setup) and `walk_states(scenario)`; `scenario.py` holds the ordered scenario: static pages (inventory, items, shelves and locations lists empty, profile, account), then create location, shelf, item through their forms (waiting for the announcement), then list populated, detail, edit form, delete confirmation page for each kind and the messages shown after add, save and delete, then cleanup.
- `cleanup.py`: `Cleaner` tracks created records by the run marker; `sweep(page)` removes leftovers of earlier runs. Raises `CleanupError` (reported, makes the exit code 2).
- `report.py`: `write_reports(result, out_dir)` writing JSON and markdown; `Result` (states checked, violations, notes, did-not-run list). A state that could not be reached is listed as "did not run", never as passed.
- `axe_audit.py`: the CLI (`python a11y/axe_audit.py [--out DIR] [--headed] [--only STATE ...]`) and exit codes of A7.
- Tests (pytest, in `a11y/`): unit tests with a fake page object for config, report, scenario ordering and cleanup; one feature integration test that serves a tiny local site (login form, a page with a known violation, a page without) and runs the real browser against it. No test touches JMac.

Rules between parts: `scenario.py` knows page addresses and form labels (from the Web page templates), `axe.py` knows nothing of Cynthus, `report.py` knows nothing of the browser.

## Slices

Order: S0 and S1 in parallel; then S2; then S3; S4 any time. All in cynthus-tools unless stated.

- S0 (M): `jmac/axe_stack.sh up|down|status` (tests with a fake `docker` and `ssh`): the lifecycle of A11, override files (container, volume and project names), a trap that restores the original, and a spike run that records what works on the VM (messaging crash, scheduler) and what the audit needs from the stack. Depends on nothing.

- S1 (M): config, browser sign-in, axe runner, report, CLI, tests on the local test site. Delivers an audit of the signed-in pages that need no data (account, profile, inventory, empty lists). Depends on nothing.
- S2 (M): scenario with data (register the audit user through the page and the mail sink, create, audit, no delete), announcement waits, tests with fake pages and the local site. Depends on S1 (and on S0 for the register step).
- S3 (S): skill `axe-audit` (SKILL.md like python-repo-audit: steps, triage, one issue in cynthus-core, logging, gotchas), README and CHANGELOG, install to `~/.claude/skills`, first live run on the VM with your yes, saved report. Depends on S0 and S2.
- S4 (XS, cynthus repository): design document `docs/features/axe-audit-script.md`, a sentence in engineering standards section on automated checks pointing at both checks, CHANGELOG. Depends on nothing; it is the design document pull request.

## Acceptance criteria (testable)

- AC1 (unit). Without `AXE_URL`, `AXE_USER` or `AXE_PASSWORD`, or with a host outside the allow-list, `load_config` raises `ConfigError` and no browser is started. The password never appears in `repr`, the reports or the log output (test greps all three).
- AC2 (feature integration). Against the local test site, sign-in succeeds with the right password and the run stops with `SignInError` and exactly one login attempt with a wrong one.
- AC3 (feature integration). On a local page with a known violation the report lists that rule, the node and a screenshot, and the exit code is 1; on a clean page it is 0.
- AC4 (unit). A state that could not be reached is in "did not run" and the exit code is 2 when sign-in or a step failed, never 0.
- AC5 (unit and feature integration). `axe_stack.sh down` runs on every exit path (success, failure, interrupt), removes only the test project (never `-v` on the original) and brings the original back; a test with a fake docker checks the command order and that no `-v` is used on the original project.
- AC6 (unit). The scenario visits, for each of items, shelves and locations, the list (empty and populated), the new form, the record, the edit form and the delete page, and the account, profile and inventory pages; a test fails when one is removed.
- AC7 (CI-equivalent, tools tests). `python -m pytest a11y` passes in a fresh virtual environment; ruff passes with the repository's settings.
- AC8 (system, manual, S3). One live run on the VM produces the JSON and markdown reports; afterwards the VM runs exactly the containers, images and volumes it ran before (compared by the script) and no test container or volume remains. The result and any violations go into one issue in cynthus-core.
- AC9 (documentation). README, CHANGELOG and the skill describe the variables, the safety rules (A5, A6) and what the script does not check; the design document links the CI check.
- AC10 (accessibility). Not applicable to the tool's own output beyond: the markdown report has one level-one heading, ordered headings and no pipe tables (screen reader rules), checked by a test.

## Risks and unknowns

- R1. Writes are acknowledged then confirmed over the socket (F5): the wait for the announcement may be flaky. If a state does not appear within the timeout, record "did not run" and continue; the coder stops and reports if more than one state is flaky.
- R2. A fresh stack needs working Auth, registration and a mail sink (auth, auth-db and the mail sink are healthy on the VM today). If registration or verification fails, the coder stops and reports.
- R7. Memory and ports: the VM has about 12 GB (8 GB free with part of the stack up). The test stack runs after the original is down, as you planned; side by side is not planned.
- R3. Putting the original stack back could fail (containers were already unhealthy). S0 records health before; the restore step compares and reports, and does not claim the original is healthy when it was not.
- R4. Axe in a page with the content security policy: CI proved injection works with scripts blocked; with scripts on it is not verified. If injection is refused, S1 uses `page.add_script_tag` through a route-fulfilled local file or CDP `Runtime.evaluate`; stop and report if neither works.
- R5. Python on the PC is 3.14 and Playwright for Python wheels may lag; S1 verifies and may pin 3.12.
- R6. Axe finds about a third of accessibility problems. The report says so. The skill must not claim the pages are accessible; the owner's screen reader tests stay.

## Out of scope

- Opened navigation menus as separate states, error and validation states, the signed-out and registration flows (D4); follow-up issue after the first live run.
- Running it in CI against a deployed stack (needs a test tenant and a secret in CI); follow-up.
- Fixing the violations it finds: they become issues in cynthus-core and go through feature-run.
- Audits of the other front ends and of chat or Astri pages (not built).

## Issue plan

- Tracking issue cynthus#81: "Axe audit script (live, signed-in accessibility audit)", Feature, XL, P2, Planned, milestone Cynthus 1.0 - Platform Foundation Complete.
- cynthus-tools#1 (S0), #2 (S1), #3 (S2), #4 (S3): S0 (M), S1 (M), S2 (M), S3 (S), each Infrastructure, Applies to Platform.
- cynthus#82 (S4): S4 (XS), Infrastructure, Applies to Docs.
- Design document: this file, pull request "Part of #81".
