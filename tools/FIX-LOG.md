# Fix log - second pass (2026-10-31)

Record of every change made to production code after the test suites were written, why it was made, and how it was
verified. Scope: bugs whose correct fix did not need a design decision from the code owner. Nothing else was changed.

Verification for all of it: `python cynthus-documentation/tools/run_python_tests.py --web` (2058 Python tests and
64 Node tests, 0 failures, 99.0 % statement coverage), `check_test_inventory.py` (263/263 modules) and
`mutation_check.py` (30/30 deliberate bugs caught).

## cynthus-core

- `containers/{api,inventory,logistics,profile,recipe,shopping}/src/<pkg>/__init__.py`
  - Change: `async initialize_caching_client(` and `async teardown_signaling_client(` became `async def ...`
  - Why: `SyntaxError`: the package could not be imported at all
- same six files
  - Change: `teardown_caching_client()` now takes `application`
  - Why: it was called with one and read an undefined global `application`
- same six files
  - Change: `lifespan` now `await`s `initialize_caching_client`, `initialize_signaling_client`, `teardown_signaling_client`, `teardown_caching_client`
  - Why: they are coroutine functions that were called without `await`, so none of the start-up or shutdown work ran (Python warned "coroutine was never awaited")
- same six files
  - Change: `initialize()` logs "has been initialized" before `return`
  - Why: the log call sat after `return` and could never run
- `containers/api/src/api/routes/signal.py`, `profile/...`, `recipe/...`, `shopping/...`
  - Change: imports use the names the messaging library really defines: `CoreSignalTopic` (was `PublicTopic`) and `CoreAPISignalSubscription` / `CoreProfileSignalSubscription` / `CoreRecipeSignalSubscription` / `CoreShoppingSignalSubscription` (was `CoreApiPublicSubscription`, which exists nowhere). The logistics route already used the library's names
  - Why: the old names raise `ImportError` against `cynthus-messaging-core`
- `containers/inventory/src/inventory/routes/signal.py` (new), `routes/__init__.py`
  - Change: added the signal route (copy of the api route using `CoreInventorySignalSubscription`) and exported it
  - Why: the inventory entry point imports `.routes.signal`, which did not exist
- `containers/worker/src/worker/__init__.py`
  - Change: comma added between `'worker.tasks.periodic'` and `'worker.tasks.backend'`; `background=` -> `backend=`; `incllude=` -> `include=`
  - Why: the two module names were concatenated into one string; two typos meant Celery had no result backend and registered no task modules
- `containers/{api,logistics,profile,recipe,shopping}/test/test_signal.py`, `test/conftest.py`
  - Change: (first pass) import fixes, generated conftest
  - Why: see TESTING.md

## cynthus-messaging-core

- `component/meal/payload/__init__.py`
  - Change: plan payloads imported from `.plan.meal_plan_*`
  - Why: the files live in `payload/plan/`; the old import made `meal`, `meal.message`, `meal.payload`, the factories and fixtures all unimportable
- `component/meal/payload/plan/meal_plan_deleted.py`, `meal_plan_updated.py`
  - Change: `from ....common` -> `from .....common`
  - Why: one package level deeper than the sibling `meal_plan_created.py`, which was already right
- `component/meal/payload/plan/__init__.py` (new, empty)
  - Change: package marker
  - Why: consistent with the other packages
- `component/meal/payload/part/__init__.py`
  - Change: exports `Meal` and `MealSuggestion`
  - Why: it imported a class `MealPayloadPart` that does not exist
- `component/meal/payload/part/suggestion.py`
  - Change: field `_id` -> `id_` (alias `id`, as in `Meal`), description corrected
  - Why: pydantic rejects field names with a leading underscore, so the module could not be imported
- `component/meal/payload/meal_suggestion_base.py`
  - Change: indentation fixed
  - Why: `IndentationError`
- `component/meal/payload/meal_base.py` (new)
  - Change: `MealPayloadBase(SignalPayload)`
  - Why: `meal_suggestion_base.py` imports it and the module did not exist
- `subscription/core_{inventory,logistics,notification,profile,recipe,scheduler,shopping,web,worker}_signal_subscription.py` (new)
  - Change: one class each, same shape as `core_api_signal_subscription.py`, name `cynthus-sub-core-<service>`
  - Why: `subscription/__init__.py` imports all nine and `cynthus-core` services import some of them
- `subscription/public_subscription.py`
  - Change: imports `CoreSignalTopic` (was the non-existent `PublicTopic`); `name` may come from the subclass attribute
  - Why: `CoreAPISignalSubscription` and the new core subscriptions declare `name` as a class attribute but the base required `name=`
- `__init__.py`, `messaging/__init__.py`, `messaging/component/__init__.py`
  - Change: `__path__ = extend_path(__path__, __name__)`
  - Why: the same three packages exist in `cynthus-messaging`; without this only one repository's modules could be imported at a time
- `test/fixture/signal_message.py` (new)
  - Change: `default_envelope()`
  - Why: `test/factory/meal/message/plan_created.py` imports it and it did not exist
- `test/factory/meal/message/plan_created.py`
  - Change: payload import points at `payload.plan.meal_plan_created`
  - Why: the old module path no longer exists
- `test/cynthus/messaging/common/test_signal_message.py`
  - Change: current import paths, UUID ids, a payload
  - Why: the test imported modules that were since renamed and used non-UUID ids

## cynthus-messaging

`src/cynthus/messaging/__init__.py` and `.../component/__init__.py`: `extend_path`, matching the change above.

## cynthus-web

No production change in this pass (first pass added `test/ai.test.js`, `test/importer.test.js`, `test/astri.test.js`).

## Left alone on purpose

See "Open items" in `TESTING.md` (faststream.azure, router/module name shadowing, scheduler import-time file read,
half-moved payload folders, two outdated tests, folder naming). `cynthus-intelligence/containers/analysis` was not
changed: it depends on `faststream.azure`.

## Repository housekeeping

- Test tooling moved from a loose `tools/` folder into `cynthus-documentation/tools/` so it is versioned.
  The scripts find the workspace root themselves.
- Not committed: `cynthus-core-wiki` (see the commit log in the final report), `.venv/` (local environment).
