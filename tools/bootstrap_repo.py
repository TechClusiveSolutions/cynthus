"""Apply the Cynthus repository template (CI, lint, PR template, standards pointer) to a repository.

Usage:  python tools/bootstrap_repo.py <path-to-repo> [--overwrite]

Existing files are left alone unless --overwrite is given, except ``.gitignore`` which only gains missing entries.
"""

import argparse
import shutil
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parents[1] / 'templates' / 'repo'
IGNORE_ENTRIES = ['__pycache__/', '.pytest_cache/', '.coverage', '.venv/', '.deps/', '.env']


def copy_template(target: Path, overwrite: bool) -> list[str]:
    """Copy every template file into ``target`` and return the relative paths written."""

    written = []

    for source in sorted(path for path in TEMPLATE.rglob('*') if path.is_file()):
        relative = source.relative_to(TEMPLATE)
        destination = target / relative

        if destination.exists() and not overwrite:
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        written.append(relative.as_posix())

    return written


def extend_gitignore(target: Path) -> bool:
    """Add the standard ignore entries that are missing. Returns True when the file changed."""

    path = target / '.gitignore'
    existing = path.read_text(encoding='utf-8').splitlines() if path.exists() else []
    missing = [entry for entry in IGNORE_ENTRIES if entry not in existing]

    if not missing:
        return False

    text = '\n'.join(existing + ([''] if existing and existing[-1] else []) + missing) + '\n'
    path.write_text(text, encoding='utf-8', newline='\n')

    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('repository', type=Path)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()

    if not (args.repository / '.git').exists():
        print(f'{args.repository} is not a git repository', file=sys.stderr)

        return 1

    for relative in copy_template(args.repository, args.overwrite):
        print(f'wrote {relative}')

    if extend_gitignore(args.repository):
        print('updated .gitignore')

    return 0


if __name__ == '__main__':
    sys.exit(main())
