"""Roll the Cynthus workflow template out to one repository through the normal issue -> branch -> PR -> merge flow.

Usage:  python tools/rollout_repo.py <repo-name> [--no-merge]

Bootstrap only: this is the one place that pushes to ``dev`` directly (creating or fast-forwarding it so the first
feature branch has a base). Every later change reaches ``dev`` through a pull request.

The repository must already have the issue titled ``Adopt the Cynthus CI, lint and pull-request workflow``.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from tracker import ORG, gh

ROOT = next(path for path in Path(__file__).resolve().parents if (path / 'cynthus-core').is_dir())
TITLE = 'Adopt the Cynthus CI, lint and pull-request workflow'
LOCAL_NAMES = {'cynthus-messaging-components': 'cynthus-messaging'}
GENERATORS = {
    'cynthus-core': [['generate_service_tests.py', '--repo', 'cynthus-core']],
    'cynthus-trust': [['generate_service_tests.py', '--repo', 'cynthus-trust']],
    'cynthus-health': [['generate_service_tests.py', '--repo', 'cynthus-health']],
    'cynthus-intelligence': [['generate_service_tests.py', '--repo', 'cynthus-intelligence']],
    'cynthus-mocks': [['generate_service_tests.py', '--repo', 'cynthus-mocks']],
    'cynthus-messaging-core': [['generate_messaging_core_tests.py']],
    'cynthus-messaging-components': [['generate_messaging_tests.py']],
}


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True, encoding='utf-8')

    if result.returncode != 0:
        raise RuntimeError(f'git {" ".join(args)} failed: {result.stderr.strip()}')

    return result.stdout.strip()


def run(command: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, encoding='utf-8')

    return (result.stdout + result.stderr).strip()


def find_issue(repo: str) -> int:
    for item in json.loads(gh('api', f'repos/{ORG}/{repo}/issues?state=open&per_page=100')):
        if item['title'] == TITLE:
            return item['number']

    raise SystemExit(f'{repo}: issue {TITLE!r} not found')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('repo')
    parser.add_argument('--no-merge', action='store_true')
    args = parser.parse_args()

    repo, local = args.repo, ROOT / LOCAL_NAMES.get(args.repo, args.repo)
    tools = Path(__file__).resolve().parent
    python = sys.executable
    number = find_issue(repo)

    git(local, 'remote', 'set-url', 'origin', f'gh-btm:{ORG}/{repo}')
    git(local, 'fetch', 'origin')
    git(local, 'checkout', 'main')
    git(local, 'pull', '--ff-only', 'origin', 'main')

    remote_branches = git(local, 'branch', '-r')

    if 'origin/dev' not in remote_branches:
        git(local, 'push', 'origin', 'main:dev')
    elif git(local, 'rev-list', '--count', 'origin/main..origin/dev') == '0':
        git(local, 'push', 'origin', 'main:dev')
    elif not git(local, 'diff', '--stat', 'origin/main...origin/dev'):
        # dev only holds merge commits of an older main: bring it up to date with a merge, never a force-push
        git(local, 'checkout', '-B', 'dev', 'origin/dev')
        git(local, 'merge', '--no-edit', 'origin/main')
        git(local, 'push', 'origin', 'dev')
        git(local, 'checkout', 'main')
    else:
        raise SystemExit(f'{repo}: origin/dev has changes that main lacks; reconcile before rolling out')

    gh('issue', 'develop', str(number), '-R', f'{ORG}/{repo}', '--base', 'dev')
    branch = gh('issue', 'develop', '--list', str(number), '-R', f'{ORG}/{repo}').split()[0]
    git(local, 'fetch', 'origin')
    git(local, 'checkout', '-B', branch, f'origin/{branch}')

    print(run([python, str(tools / 'bootstrap_repo.py'), str(local), '--overwrite']))

    for generator in GENERATORS.get(repo, []):
        print(run([python, str(tools / generator[0]), *generator[1:]], cwd=tools))

    print(run([python, '-m', 'ruff', 'check', str(local), '--fix', '-q']))
    print(run([python, '-m', 'ruff', 'check', str(local)]))
    print(f'branch {branch} prepared for {repo}; issue #{number}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
