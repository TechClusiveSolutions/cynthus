"""The Cynthus 1.0 backlog: every feature set, its owning repository, milestone and acceptance criteria.

Run ``python tools/backlog.py --create`` to file the issues (skips titles that already exist in the repository).
Run without arguments to list them.
"""

import argparse
import json
import sys

from tracker import ORG, Tracker, gh

FOUNDATION = 'Cynthus 1.0 — Platform Foundation Complete'
IDENTITY = 'Cynthus 1.0 — Identity & Profile Complete'
INVENTORY = 'Cynthus 1.0 — Inventory & Recipe Complete'
PLANNING = 'Cynthus 1.0 — Planning & Logistics Complete'
ASTRI = 'Cynthus 1.0 — Astri Complete'
WEB = 'Cynthus 1.0 — Health & Web Complete'

PLAN = 'docs/architecture/web-app-conversion-plan.md'
ADD = 'Cynthus-ArchitecturalDesignDocument.md'
ADR = 'docs/adr/ADR-006-faststream-azure-servicebus-adapter.md'

APP = 'Application Feature'
INFRA = 'Infrastructure Feature'
BUG = 'Application Bug'

# (repo, title, milestone, issue type, priority, subtype, applies to, summary, acceptance criteria, docs)
ISSUES = [
    # ---- Platform foundation ------------------------------------------------------------------------------------
    *[(repo, 'Adopt the Cynthus CI, lint and pull-request workflow', FOUNDATION, INFRA, 'P1 - High', 'Infrastructure', applies,
       'Add the shared repository template: `ci.yml` (ruff + pytest with a coverage gate), `docs.yml` (markdownlint), the pull request '
       'template, `pyproject.toml` lint configuration and `CLAUDE.md`. Fix existing lint findings, create/refresh `dev`, and protect '
       '`dev` and `main` (required checks `lint` and `test`).',
       ['`ruff check .` passes', 'Unit tests pass with the coverage gate in CI', '`dev` and `main` are protected', 'Template applied with `tools/bootstrap_repo.py`'],
       'docs/engineering-standards.md')
      for repo, applies in [('cynthus-core', 'Cynthus Core'), ('cynthus-trust', 'Cynthus Trust'), ('cynthus-health', 'Cynthus Health'),
                            ('cynthus-intelligence', 'Cynthus Intelligence'), ('cynthus-messaging-core', 'Cynthus Platform'),
                            ('cynthus-messaging-components', 'Cynthus Platform'), ('cynthus-mocks', 'Cynthus Platform'),
                            ('cynthus-emulators', 'Cynthus Platform')]],
    ('cynthus-messaging-core', 'Signal publisher and subscriber interfaces', FOUNDATION, APP, 'P1 - High', 'Application', 'Cynthus Platform',
     'Define `SignalPublisher` and `SignalSubscriber` (one class per module) so application code never depends on a broker class, plus an '
     'in-memory implementation for unit tests. Includes the three topic definitions from the ADD (public, internal, audit).',
     ['Interfaces and in-memory fake with unit tests', 'Topic classes for `cynthus-topic-public`, `-internal`, `-audit`', 'Envelope carries `organization_id` and `workspace_id`'],
     ADD + ' section 5'),
    ('cynthus-messaging-core', 'Azure Service Bus adapter (faststream-azure-servicebus)', FOUNDATION, APP, 'P1 - High', 'Application', 'Cynthus Platform',
     'Implement the interfaces on top of `faststream-azure-servicebus` (ADR-006) and replace every import of the non-existent `faststream.azure`. '
     'Subscriptions become plain value classes; the broker is wired in the application lifespan only.',
     ['No remaining `faststream.azure` imports', 'Adapter tested with `TestServiceBusBroker`', 'Publisher/subscriber tests pass against the fake and the test broker'],
     ADR),
    ('cynthus-messaging-core', 'Shared kernel: token verifier, error envelope and hard-constraint matcher', FOUNDATION, APP, 'P1 - High', 'Application', 'Cynthus Platform',
     'Cross-service primitives that are not signal models live in `cynthus.shared`: `TokenVerifier` (JWT claims), `ErrorEnvelope`, and '
     '`HardConstraintMatcher` (allergy/diet rules ported from the prototype). One class per module.',
     ['Matcher reproduces the prototype rules with tests', 'Verifier accepts HS256 (local) and RS256 (deployed) keys', 'Documented in the ADD notes'],
     PLAN),
    ('cynthus-emulators', 'Service Bus emulator configuration for the three topics', FOUNDATION, INFRA, 'P2 - Medium', 'Infrastructure', 'Cynthus Platform',
     'Describe `cynthus-topic-public`, `-internal` and `-audit` with one subscription per consuming service in the emulator config '
     '(the emulator cannot create entities at runtime and allows 50 entities).',
     ['Config lists all topics and subscriptions', 'Compose file starts the emulator and its SQL backend'], ADD + ' section 5.1'),
    ('cynthus', 'Lint the legacy design documents', FOUNDATION, INFRA, 'P3 - Low', 'Administration', 'Cynthus Docs',
     'About 550 markdownlint findings remain in the historical design documents under `docs/`. Fix them and widen the globs in `docs.yml`.',
     ['`markdownlint` passes on `docs/**/*.md`', '`docs.yml` globs cover the whole folder'], 'docs/'),
    # ---- Identity and profile -----------------------------------------------------------------------------------
    ('cynthus-trust', 'Identity: registration with a personal organization and workspace', IDENTITY, APP, 'P0 - Urgent', 'Application', 'Cynthus Trust',
     'Port registration. Creating an account also creates an `organization_id` and a personal `workspace_id` (ADD 3.1) and emits '
     '`public.identity.user.created`. Validation, duplicate-email and throttling rules come from the prototype.',
     ['`POST /auth/register` returns the user and sets the session cookie', 'Organization and workspace created in one transaction', 'Rate limiting', 'Scrypt hashes remain compatible with the prototype'],
     PLAN),
    ('cynthus-trust', 'Identity: login, logout and JWT issuance', IDENTITY, APP, 'P0 - Urgent', 'Application', 'Cynthus Trust',
     'Issue a signed JWT with role and entitlement claims in an HttpOnly cookie; publish verification keys; logout clears the cookie.',
     ['`POST /auth/login` and `/auth/logout`', 'Claims: sub, organization_id, workspace_id, roles, entitlements', 'Expiry and tamper tests'], ADD + ' section 3.2'),
    ('cynthus-trust', 'Identity: password change, account export and account deletion', IDENTITY, APP, 'P1 - High', 'Application', 'Cynthus Trust',
     'Password change, and account deletion that emits `public.identity.user.deleted` so services remove the user\'s data. Export is assembled by `cynthus-core-api`.',
     ['Password rules and current-password check', 'Deletion requires typing DELETE', 'Signal emitted on delete'], PLAN),
    ('cynthus-core', 'Profile: preferences and hard constraints API', IDENTITY, APP, 'P0 - Urgent', 'Application', 'Cynthus Core',
     'Port profile storage (diet, allergies, dislikes, likes, units, medical notes, suggestion schedule) and expose `GET /profile/constraints` '
     'for context assembly. Soft preferences are freely mutable; hard constraints are not.',
     ['`GET/PUT /profile`', '`GET /profile/constraints` returns hard constraints and soft preferences', 'Medical notes never leave the owner\'s requests'], ADD + ' section 4'),
    ('cynthus-core', 'Profile: audit every hard-constraint mutation', IDENTITY, APP, 'P1 - High', 'Application', 'Cynthus Core',
     'Emit `internal.audit.constraint.mutated` (before and after state, actor, time) on `cynthus-topic-audit` before a hard-constraint write commits.',
     ['Signal published before commit', 'A failed publish aborts the write', 'Soft-preference writes emit nothing'], ADD + ' section 8.2'),
    ('cynthus-core', 'Profile: groups, members, roles and invite codes', IDENTITY, APP, 'P1 - High', 'Application', 'Cynthus Core',
     'Port groups: create, join by code, role changes, removal, leave, delete. Roles: owner, manager, member, viewer. Provides role lookups to other services.',
     ['All prototype group rules ported', 'Owner cannot be removed or demoted', '`GET /groups/{id}/members` for other services'], PLAN),
    ('cynthus-core', 'Profile: personal health metrics and summaries', IDENTITY, APP, 'P2 - Medium', 'Application', 'Cynthus Core',
     'Port metric logging (kinds, units, validation), listing, deletion and the 30-day summary. Personal data only; not PHI and not shared with clinical partners.',
     ['Kinds and validation as in the prototype', 'Summary endpoint', 'Delete own metrics only'], PLAN),
    # ---- Inventory and recipe -----------------------------------------------------------------------------------
    ('cynthus-core', 'Inventory: locations and items', INVENTORY, APP, 'P0 - Urgent', 'Application', 'Cynthus Core',
     'Port locations (pantry, refrigerator, ...) and items with quantity, unit, expiry and low-stock threshold; shared locations through group roles.',
     ['CRUD with workspace scoping', 'Group-shared locations honour roles', 'New accounts get starter locations from the `user.created` signal'], PLAN),
    ('cynthus-core', 'Inventory: adjustments, log, alerts and snapshot', INVENTORY, APP, 'P1 - High', 'Application', 'Cynthus Core',
     'Quantity adjustments with an audit log, low/expiring/expired alerts, and `GET /inventory/snapshot` for context assembly. Publishes `public.inventory.item.*` signals.',
     ['Adjust and log', 'Alerts for 3 days by default', 'Snapshot lists items, quantities and expiry dates', 'Signals published'], ADD + ' section 4.1'),
    ('cynthus-core', 'Recipe: libraries and recipes', INVENTORY, APP, 'P0 - Urgent', 'Application', 'Cynthus Core',
     'Port libraries and recipes (ingredients, steps, difficulty, cost, servings), search/filter, availability against inventory, group sharing, starter recipes for new accounts.',
     ['CRUD with permission checks', 'Search and filters', 'Starter recipes seeded on `user.created`'], PLAN),
    ('cynthus-core', 'Recipe: ratings and favorites', INVENTORY, APP, 'P2 - Medium', 'Application', 'Cynthus Core',
     'Port per-user ratings (1-5) and favorite flags for recipes and meals.', ['Rate and favorite endpoints', 'Favorites listing'], PLAN),
    ('cynthus-core', 'Recipe: import from a web page', INVENTORY, APP, 'P2 - Medium', 'Application', 'Cynthus Core',
     'Port the schema.org JSON-LD importer with its SSRF protections: private and loopback addresses blocked, no redirects followed, size and time limits.',
     ['Private, loopback and link-local ranges refused before any request', 'Redirects refused', 'HowToStep / HowToSection / strings parsed'], PLAN),
    ('cynthus-core', 'Recipe: constraint-filtered candidates (`GET /recipe/candidates`)', INVENTORY, APP, 'P0 - Urgent', 'Application', 'Cynthus Core',
     'Fetch the user\'s hard constraints from the profile service and return only recipes that pass the allergy and diet filter, so unsafe recipes never reach Astri.',
     ['Filter applied inside the recipe service', 'Every workspace member\'s constraints applied for group requests', 'Property-style tests for allergens and diets'], ADD + ' section 4.2'),
    # ---- Planning and logistics ---------------------------------------------------------------------------------
    ('cynthus-core', 'Logistics: shopping list and restock', PLANNING, APP, 'P1 - High', 'Application', 'Cynthus Core',
     'Port the shopping list: add, edit, tick off, add-from-low-stock (reads inventory alerts), and restock into inventory.',
     ['CRUD', 'From-low builds items from alerts', 'Restock adds to inventory and logs it'], PLAN),
    ('cynthus-core', 'Core API: meal planning and consuming a meal', PLANNING, APP, 'P1 - High', 'Application', 'Cynthus Core',
     'Meals (planned date, category, recipes, notes, status), consuming a meal deducts matching inventory, composite meals reference several recipes.',
     ['CRUD', 'Consume deducts inventory and logs', 'Allergen warnings returned for the member\'s profile'], PLAN),
    ('cynthus-core', 'Core API: suggestion workflow (request, accept, deny)', PLANNING, APP, 'P0 - Urgent', 'Application', 'Cynthus Core',
     'Assemble context, call `cynthus-analysis`, store the pending suggestion, accept it into a meal or deny it so the next suggestion avoids it. '
     'Publishes `public.meal.suggestion.*` signals.',
     ['Request / accept / deny', 'Denied names excluded next time', 'Signals published'], PLAN),
    ('cynthus-core', 'Core API: group meal votes with Astri tie-break', PLANNING, APP, 'P1 - High', 'Application', 'Cynthus Core',
     'Propose a meal in a group, cast yes/no, view consensus, close. A split vote is resolved by `cynthus-analysis`, favouring meals that use expiring items.',
     ['Vote lifecycle', 'Allergy warning for members', 'Tie-break rationale stored', 'Signals published'], PLAN),
    ('cynthus-core', 'Core API: group chat', PLANNING, APP, 'P2 - Medium', 'Application', 'Cynthus Core',
     'Port group messages with polling. The WebSocket hub (`cynthus-messaging-engine`) is a later, separate piece.', ['Post and list messages with role checks', 'System messages for votes and suggestions'], PLAN),
    # ---- Astri --------------------------------------------------------------------------------------------------
    ('cynthus-core', 'Core API: context assembly layer', ASTRI, APP, 'P0 - Urgent', 'Application', 'Cynthus Core',
     'Build the payload Astri receives: constraints from profile, inventory snapshot, constraint-filtered recipe candidates, conversation history. '
     'This is the only path into the dark subnet.',
     ['Calls profile, inventory, recipe', 'Payload schema documented and tested', 'Failures degrade to a clear error'], ADD + ' section 4'),
    ('cynthus-intelligence', 'Chat: Astri persona service', ASTRI, APP, 'P0 - Urgent', 'Application', 'Cynthus Intelligence',
     'Payload-driven chat with no outbound calls to Core. Screen-reader-safe formatting, conversation history in the intelligence database, '
     'defensive re-check of replies against the hard constraints that arrive in the payload.',
     ['`POST /chat` accepts an assembled payload', 'History stored', 'Allergen caution when a reply violates constraints', 'No HTTP client to Core'], ADD + ' sections 4 and 9'),
    ('cynthus-intelligence', 'Analysis: suggestions, vote tie-break and health insight', ASTRI, APP, 'P0 - Urgent', 'Application', 'Cynthus Intelligence',
     'Port suggestion generation (LLM with rule-based fallback), the Astri tie-break and the health insight. Stateless: everything arrives in the payload.',
     ['Provider chain Groq then OpenRouter then rules', 'Constraint check on every result', 'Tie-break prefers expiring items'], PLAN),
    # ---- Health and web -----------------------------------------------------------------------------------------
    ('cynthus-core', 'Core API: dashboard, search and data export', WEB, APP, 'P1 - High', 'Application', 'Cynthus Core',
     'Aggregate endpoints: home dashboard, cross-domain search, account data export.', ['Dashboard', 'Search over recipes, meals, inventory, health, groups', 'Export'], PLAN),
    ('cynthus-core', 'Web: serve the accessible front end and proxy the API', WEB, APP, 'P1 - High', 'Application', 'Cynthus Core',
     'Serve the existing JavaScript front end from `cynthus-core-web` and forward `/api` to `cynthus-core-api`, with the prototype\'s security headers.',
     ['Static files with CSP headers', '`/api` proxied with cookies', 'Service worker and manifest'], PLAN),
    ('cynthus-core', 'Scheduler: scheduled suggestions and expiry alerts', WEB, APP, 'P2 - Medium', 'Application', 'Cynthus Core',
     'Publish signals for scheduled meal suggestions (login, daily, weekly, monthly) and for expiring items.', ['Task schedule configuration', 'Signals consumed by `cynthus-core-api`'], ADD),
    ('cynthus-health', 'Health API: clinical edge aligned with the ADD', WEB, APP, 'P3 - Low', 'Application', 'Cynthus Health',
     'Keep `cynthus-health-api` the read-only clinical edge: consent token verification and audit emission before any PHI is returned. No personal logging here.',
     ['Consent token verification', 'Audit event before response', 'No write endpoints'], ADD + ' section 8.1'),
    ('cynthus', 'Retire the Node.js prototype once the Python services reach parity', WEB, APP, 'P3 - Low', 'Administration', 'Cynthus Platform',
     'Compare the prototype\'s integration suite against the Python stack, then archive `cynthus-web`.', ['Parity checklist signed off', 'Prototype archived'], PLAN),
]


def body(summary: str, criteria: list[str], docs: str) -> str:
    items = '\n'.join(f'- [ ] {item}' for item in criteria)

    return f'## Summary\n{summary}\n\n## Acceptance criteria\n{items}\n\n## Docs\n`{docs}`\n'


def existing_titles(repo: str) -> set[str]:
    out = gh('api', f'repos/{ORG}/{repo}/issues?state=all&per_page=100')

    return {item['title'] for item in json.loads(out)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--create', action='store_true')
    args = parser.parse_args()

    if not args.create:
        for repo, title, milestone, *_ in ISSUES:
            print(f'{repo:32} {milestone[:34]:34} {title}')

        print(f'\n{len(ISSUES)} issues')

        return 0

    tracker = Tracker()
    known: dict[str, set[str]] = {}

    for repo, title, milestone, issue_type, priority, subtype, applies, summary, criteria, docs in ISSUES:
        known.setdefault(repo, existing_titles(repo))

        if title in known[repo]:
            print(f'skip   {repo}: {title}')
            continue

        number = tracker.create_issue(repo, title=title, body=body(summary, criteria, docs), issue_type=issue_type, milestone=milestone,
                                      priority=priority, subtype=subtype, applies_to=applies,
                                      labels=('Feature',) if issue_type != BUG else ('bug',), status='Backlog')
        print(f'#{number:<4} {repo}: {title}', flush=True)

    return 0


if __name__ == '__main__':
    sys.exit(main())
