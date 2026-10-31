"""Sanity-check that the test suites actually fail when the code under test is broken.

Each mutation copies a suite (source + tests) into a temporary directory that mirrors the repository
layout, applies one small change to the *copy*, runs pytest there, and reports whether the suite noticed.
A mutation that "survives" means the tests would not catch that kind of regression. The real sources are
never modified.

Usage:  python tools/mutation_check.py [--only TEXT]
"""

import argparse
import shutil
import subprocess
import sys
import tempfile

from pathlib import Path


ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'cynthus-core').is_dir())
PYTHON = sys.executable

# (label, unit directory relative to ROOT, file relative to the unit, old text, new text)
MUTATIONS = [
    ('web: index returns data', 'cynthus-core/containers/web', 'src/web/routes/system.py', 'return {}', "return {'ok': True}"),
    ('web: wrong channel', 'cynthus-core/containers/web', 'src/web/routes/event.py', "'user.login'", "'user.logout'"),
    ('web: wrong redis db', 'cynthus-core/containers/web', 'src/web/routes/event.py', "/0'", "/1'"),
    ('web: redis never closed', 'cynthus-core/containers/web', 'src/web/__init__.py',
     'await application.state.redis.close()', 'pass'),
    ('web: system router not included', 'cynthus-core/containers/web', 'src/web/__init__.py',
     'application.include_router(system)', 'pass'),
    ('web: event router not included', 'cynthus-core/containers/web', 'src/web/__init__.py',
     'application.include_router(event)', 'pass'),
    ('api signal: wait time', 'cynthus-core/containers/api', 'src/api/routes/signal.py', 'max_wait_time=30', 'max_wait_time=60'),
    ('api signal: dead-letter reason', 'cynthus-core/containers/api', 'src/api/routes/signal.py',
     "reason='processing_failed'", "reason='failed'"),
    ('api signal: message never completed', 'cynthus-core/containers/api', 'src/api/routes/signal.py',
     'await receiver.complete_message(message)', 'pass'),
    ('api signal: content type', 'cynthus-core/containers/api', 'src/api/routes/signal.py',
     "content_type='application/json'", "content_type='text/plain'"),
    ('api signal: cancellation swallowed', 'cynthus-core/containers/api', 'src/api/routes/signal.py',
     '            except asyncio.CancelledError:\n                raise\n', '            except asyncio.CancelledError:\n                pass\n'),
    ('logistics signal: health payload', 'cynthus-core/containers/logistics', 'src/logistics/routes/signal.py',
     "return {'subscription': _subscription.name, 'topic': _topic.name}", "return {'subscription': _topic.name, 'topic': _subscription.name}"),
    ('scheduler: args stay lists', 'cynthus-core/containers/scheduler', 'src/scheduler/__init__.py',
     "value['args'] = tuple(args)", "value['args'] = args"),
    ('scheduler: exchange', 'cynthus-core/containers/scheduler', 'src/scheduler/__init__.py',
     "'periodic'", "'default'"),
    ('worker: broker host', 'cynthus-core/containers/worker', 'src/worker/__init__.py',
     "host = environ.get('CACHE_HOST')", "host = 'localhost'"),
    ('mock: index returns data', 'cynthus-mocks/containers/auth', 'src/auth/routes/system.py', 'return {}', 'return {"a": 1}'),
    ('chat event: handler log', 'cynthus-intelligence/containers/chat', 'src/chat/routes/event.py',
     "'Received a suggestion accepted event'", "'Got it'"),
    ('core: plan aggregate', 'cynthus-messaging-core', 'src/cynthus/messaging/common/signal/public_meal_plan_base.py',
     "aggregate = 'plan'", "aggregate = 'plans'"),
    ('core: schema_version lower bound', 'cynthus-messaging-core', 'src/cynthus/messaging/common/signal/payload.py',
     'ge=1', 'ge=0'),
    ('core: enum value', 'cynthus-messaging-core', 'src/cynthus/messaging/common/signal/action_type.py',
     "CAST: str = 'cast'", "CAST: str = 'casted'"),
    ('core: signal name format', 'cynthus-messaging-core', 'src/cynthus/messaging/common/signal/base.py',
     "f'{cls.visibility}.{cls.domain.value}.{cls.aggregate}.{cls.action.value}'",
     "f'{cls.domain.value}.{cls.aggregate}.{cls.action.value}'"),
    ('core: component validation', 'cynthus-messaging-core', 'src/cynthus/messaging/common/signal/base.py',
     'if missing:', 'if False:'),
    ('core: frozen parts', 'cynthus-messaging-core', 'src/cynthus/messaging/common/signal/model_config.py',
     'frozen=frozen,', 'frozen=False,'),
    ('core: vote tally type', 'cynthus-messaging-core', 'src/cynthus/messaging/component/meal/payload/meal_vote_cast.py',
     'Dict[str, int]', 'Dict[str, str]'),
    ('core: rating score optional', 'cynthus-messaging-core', 'src/cynthus/messaging/component/meal/payload/meal_rating_created.py',
     "score: int = Field(...,", "score: int = Field(1,"),
    ('core: topic name', 'cynthus-messaging-core', 'src/cynthus/messaging/topic/core_signal_topic.py',
     "'cynthus-topic-public'", "'cynthus-topic'"),
    ('core: subscription name', 'cynthus-messaging-core', 'src/cynthus/messaging/subscription/chat_public_subscription.py',
     "'cynthus-chat-public-sub'", "'cynthus-chat-sub'"),
    ('core: message event type', 'cynthus-messaging-core', 'src/cynthus/messaging/component/meal/message/meal_vote_cast.py',
     'PublicMealVoteCastSignal.name', 'PublicMealVoteResolvedSignal.name'),
    ('messaging: event type', 'cynthus-messaging', 'src/cynthus/messaging/component/auth/message/auth_session_invalidated.py',
     "'auth.session.invalidated'", "'auth.session.ended'"),
    ('messaging: payload field', 'cynthus-messaging', 'src/cynthus/messaging/component/clinical/payloads/clinical_signal_created.py',
     'raw_value: str', 'raw_value: str = ""'),
]


def run_mutation(label, unit, relative_file, old, new):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        source = ROOT / unit
        target = tmp / unit
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target, ignore=shutil.ignore_patterns('__pycache__', '.pytest_cache', '.git'))

        # suites that reach into sibling repositories need them next to the copy
        for sibling in ('cynthus-messaging-core',):
            if unit != sibling and not (tmp / sibling).exists():
                shutil.copytree(ROOT / sibling, tmp / sibling, ignore=shutil.ignore_patterns('__pycache__', '.git'))

        path = target / relative_file
        text = path.read_text(encoding='utf-8')

        if old not in text:
            return 'NOT APPLIED', f'text not found in {relative_file}'

        path.write_text(text.replace(old, new, 1), encoding='utf-8', newline='')
        result = subprocess.run(
            [PYTHON, '-m', 'pytest', '-q', '-x', '-p', 'no:cacheprovider', '--tb=no'],
            cwd=target, capture_output=True, text=True, env={**__import__('os').environ, 'PYTHONDONTWRITEBYTECODE': '1'},
        )
        tail = (result.stdout.strip().splitlines() or ['(no output)'])[-1]

        return ('KILLED' if result.returncode != 0 else 'SURVIVED'), tail


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--only', help='only run mutations whose label contains this text')
    args = parser.parse_args()

    outcomes = []

    for mutation in MUTATIONS:
        if args.only and args.only not in mutation[0]:
            continue

        status, detail = run_mutation(*mutation)
        outcomes.append(status)
        print(f'{status:<11} {mutation[0]:<40} {detail}', flush=True)

    survived = [s for s in outcomes if s != 'KILLED']
    print(f'\n{outcomes.count("KILLED")} of {len(outcomes)} mutations were caught')

    return 1 if survived else 0


if __name__ == '__main__':
    sys.exit(main())
