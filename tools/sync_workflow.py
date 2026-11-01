"""Bring an open rollout branch up to date with the current CI template, then push and re-request the Copilot review.

Usage:  python tools/sync_workflow.py <repo-name> [--custom-ci]

``--custom-ci`` leaves ``.github/workflows/ci.yml`` alone (the documentation repository has its own variant).
"""

import shutil
import subprocess
import sys

from rollout_repo import LOCAL_NAMES, ROOT, find_issue, git
from tracker import ORG, gh

TEMPLATE = ROOT / 'cynthus-documentation' / 'templates' / 'repo'


def main() -> int:
    repo = sys.argv[1]
    local = ROOT / LOCAL_NAMES.get(repo, repo)
    number = find_issue(repo) if repo != 'cynthus' else 1
    linked = gh('issue', 'develop', '--list', str(number), '-R', f'{ORG}/{repo}').split()
    # the link is eventually consistent; fall back to the local branch GitHub generated for the issue
    branch = linked[0] if linked else git(local, 'branch', '--list', f'{number}-*', '--format=%(refname:short)').split()[0]
    git(local, 'checkout', branch)

    if '--custom-ci' not in sys.argv:
        shutil.copyfile(TEMPLATE / '.github' / 'workflows' / 'ci.yml', local / '.github' / 'workflows' / 'ci.yml')

    docs_workflow = local / '.github' / 'workflows' / 'docs.yml'

    if docs_workflow.exists():
        docs_workflow.unlink()

    ignore = local / '.gitignore'

    if ignore.exists():
        lines = ignore.read_text(encoding='utf-8').splitlines()
        kept = [line for line in lines if line.strip() not in ('*.yml', '*.yaml')]

        if kept != lines:
            ignore.write_text('\n'.join(kept) + '\n', encoding='utf-8', newline='\n')

    git(local, 'add', '-A')
    status = git(local, 'status', '--short')

    if status:
        git(local, 'commit', '-m', 'Merge the workflows into a single CI workflow with unambiguous check names', '-m',
            'Addresses review feedback: lint, test and docs-lint are owned by ci.yml, change-aware, and a container '
            'without tests fails. Refs #%d.' % number, '-m', 'Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>')
        git(local, 'push', 'origin', branch)

    pr = gh('pr', 'list', '-R', f'{ORG}/{repo}', '--head', branch, '--json', 'number', '--jq', '.[0].number').strip()
    subprocess.run(['gh', 'pr', 'edit', pr, '-R', f'{ORG}/{repo}', '--add-reviewer', '@copilot'], capture_output=True)
    print(f'{repo}: PR #{pr} updated' if status else f'{repo}: nothing to change')

    return 0


if __name__ == '__main__':
    sys.exit(main())
