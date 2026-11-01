"""Finish a rollout branch prepared by rollout_repo.py: tidy Markdown, commit, push, open the PR and request review.

Usage:  python tools/finish_rollout.py <repo-name> "<test evidence line>"
"""

import re
import subprocess
import sys
from pathlib import Path

from rollout_repo import LOCAL_NAMES, ROOT, find_issue, git, run
from tracker import ORG, gh

MILESTONE = 'Cynthus 1.0 — Platform Foundation Complete'
BODY = """## GitHub issue

Closes #{number}

## What changed

Adds the shared Cynthus workflow files (`ci.yml`, `docs.yml`, pull request template, `pyproject.toml` ruff configuration,
markdownlint configuration, `CLAUDE.md`, `requirements-dev.txt`) and fixes the existing lint findings.

## Why

Implements `docs/engineering-standards.md` in the Cynthus documentation repository (sections 3 and 7).

## Verification

- [x] `ruff check .` passes
- [x] {evidence}
- [x] markdownlint passes on the repository's Markdown files

## Deviations from standards

None.

## Scope check

Tooling and lint fixes only; no behaviour change.
"""


def tidy_markdown(local: Path) -> None:
    """Give bare code fences a language and strip trailing whitespace so markdownlint passes."""

    for path in list(local.glob('docs/**/*.md')) + list(local.glob('*.md')):
        text = path.read_text(encoding='utf-8')
        newline = '\r\n' if '\r\n' in text else '\n'
        lines, fenced = [], False

        for line in text.split(newline):
            if line.startswith('```'):
                if not fenced and line.strip() == '```':
                    line = '```text'

                fenced = not fenced

            lines.append(re.sub(r'[ \t]+$', '', line) if not line.endswith('  ') or fenced else line)

        updated = newline.join(lines)

        if updated != text:
            path.write_text(updated, encoding='utf-8', newline='')


def verify(local: Path) -> None:
    """Run the lint checks the PR body claims; raise if either fails."""

    for command in ([sys.executable, '-m', 'ruff', 'check', str(local)],
                    ['npx', '--yes', 'markdownlint-cli2', '--config', '.markdownlint-cli2.jsonc', 'docs/**/*.md', '.github/**/*.md', '*.md']):
        result = subprocess.run(command, cwd=local, capture_output=True, text=True, encoding='utf-8', shell=sys.platform == 'win32')

        if result.returncode != 0:
            name = ' '.join(command[:3])

            raise SystemExit(f'{name} failed:\n{result.stdout}{result.stderr}')


def main() -> int:
    repo, evidence = sys.argv[1], sys.argv[2]
    local = ROOT / LOCAL_NAMES.get(repo, repo)
    number = find_issue(repo)
    tidy_markdown(local)
    verify(local)

    lint = run([sys.executable, '-m', 'markdownlint'], cwd=local) if False else ''
    del lint
    git(local, 'add', '-A')
    git(local, 'commit', '-m', 'Adopt the Cynthus CI, lint and pull-request workflow', '-m',
        f'Adds the shared workflow files and fixes existing lint findings. Closes #{number}.', '-m',
        'Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>')
    branch = git(local, 'branch', '--show-current')
    git(local, 'push', '-u', 'origin', branch)
    body = BODY.format(number=number, evidence=evidence)
    url = gh('pr', 'create', '-R', f'{ORG}/{repo}', '--base', 'dev', '--head', branch, '--title',
             f'Adopt the Cynthus CI, lint and pull-request workflow (#{number})', '--body', body, '--assignee',
             'blindtechmage', '--milestone', MILESTONE).strip()
    gh('pr', 'edit', url, '--add-reviewer', '@copilot')
    print(url)

    return 0


if __name__ == '__main__':
    sys.exit(main())
