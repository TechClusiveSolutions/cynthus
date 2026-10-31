"""List every Python module that has no corresponding test script.

A module is matched when the suite contains a script named for it:
  * `pkg/mod.py`           ->  test_mod.py, or test_<parent>_mod.py (for example test_routes_system.py)
  * `pkg/__init__.py`      ->  test_<pkg>_init.py or test_init.py in the mirrored directory
Empty placeholder modules (zero bytes) are accepted when a package-structure script imports them by name.

Usage:  python tools/check_test_inventory.py            # report, exit 1 when anything is unmatched
        python tools/check_test_inventory.py --list     # also print the matches
"""

import argparse
import sys

from pathlib import Path


ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'cynthus-core').is_dir())


def units():
    for repo in sorted(ROOT.glob('cynthus-*')):
        containers = repo / 'containers'

        if containers.is_dir():
            for container in sorted(containers.iterdir()):
                if (container / 'src').is_dir():
                    yield f'{repo.name}/{container.name}', container / 'src', container / 'test'
        elif (repo / 'src').is_dir() and repo.name != 'cynthus-web':
            yield repo.name, repo / 'src', repo / 'test'


def dotted(src, path):
    parts = list(path.relative_to(src).with_suffix('').parts)

    if parts[-1] == '__init__':
        parts = parts[:-1]

    return '.'.join(parts), path.name == '__init__.py'


def test_names(test_dir):
    return {path.name: path for path in test_dir.rglob('test_*.py')} if test_dir.is_dir() else {}


def structure_text(test_dir):
    texts = [path.read_text(encoding='utf-8') for path in test_dir.rglob('test_package_structure.py')]

    return '\n'.join(texts)


def candidates(src, path):
    name, is_init = dotted(src, path)
    parts = name.split('.')
    options = set()

    if is_init:
        options.add('test_init.py')
        options.add(f'test_{parts[-1]}_init.py' if parts else 'test_init.py')
        options.add('test_routes_init.py' if parts[-1] == 'routes' else 'test_init.py')
        options.add('test_' + '_'.join(parts) + '.py')
        options.add('test_' + '_'.join(parts[1:]) + '_init.py')
    else:
        stem = parts[-1]
        options.add(f'test_{stem}.py')

        if len(parts) > 1:
            options.add(f'test_{parts[-2]}_{stem}.py')

        options.add(f'test_{stem}_message.py')
        options.add(f'test_{stem}_payload.py')

    return options


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--list', action='store_true')
    args = parser.parse_args()

    missing = []
    matched = 0

    for name, src, test_dir in units():
        names = test_names(test_dir)
        structure = structure_text(test_dir)

        for path in sorted(src.rglob('*.py')):
            if '__pycache__' in path.parts:
                continue

            module, is_init = dotted(src, path)
            options = candidates(src, path)
            hit = next((names[option] for option in options if option in names), None)

            if hit is None and not is_init:
                stem = module.split('.')[-1]
                hit = next((path_ for file, path_ in names.items() if file.endswith(f'_{stem}.py')), None)

            # same-named scripts in different directories: prefer one that mirrors the module's directory
            if hit is None and path.stat().st_size == 0 and f"'{module}'" in structure:
                hit = test_dir / 'test_package_structure.py'

            if hit is None and is_init and f"'{module}'" in structure and path.stat().st_size == 0:
                hit = test_dir / 'test_package_structure.py'

            if hit is None:
                missing.append((name, path.relative_to(ROOT)))
            else:
                matched += 1

                if args.list:
                    print(f'ok   {path.relative_to(ROOT)}  <-  {hit.name}')

    for name, path in missing:
        print(f'MISSING  {path}')

    print(f'\n{matched} modules have a test script, {len(missing)} do not')

    return 1 if missing else 0


if __name__ == '__main__':
    sys.exit(main())
