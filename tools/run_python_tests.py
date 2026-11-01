"""Run every Cynthus Python test suite with coverage and print one combined report.

Several containers define packages with the same name (`api`, `web`, `chat`, `auth`, `analysis`), so
each suite has to run in its own interpreter. This script runs them one at a time, collects line
coverage for each suite's `src/` tree, and reports per-suite and overall figures.

Files that cannot be parsed (syntax errors) cannot be measured by coverage.py. They are listed
separately and are counted as fully uncovered in the "including unparsable" figure so they cannot
quietly flatter the result.

Usage:
    python tools/run_python_tests.py                    # everything
    python tools/run_python_tests.py --unit health      # suites whose name contains "health"
    python tools/run_python_tests.py --threshold 75     # exit 1 when overall coverage is below 75 %
    python tools/run_python_tests.py --report tools/latest-report.md
"""

import argparse
import ast
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'cynthus-core').is_dir())
PYTHON = sys.executable
LIST_LIMIT = 25

COVERAGE_RC = """[run]
relative_files = False

[report]
ignore_errors = True
"""


def discover():
    """Return (name, project_dir, src_dir) for every suite."""

    units = []

    for repo in sorted(ROOT.glob('cynthus-*')):
        containers = repo / 'containers'

        if containers.is_dir():
            for container in sorted(containers.iterdir()):
                if (container / 'src').is_dir() and (container / 'test').is_dir():
                    units.append((f'{repo.name}/{container.name}', container, container / 'src'))

        elif (repo / 'src').is_dir() and (repo / 'test').is_dir():
            units.append((repo.name, repo, repo / 'src'))

    return units


def python_files(src_dir):
    return sorted(path for path in src_dir.rglob('*.py') if '__pycache__' not in path.parts)


def logical_lines(path):
    """Approximate statement count for a file coverage.py cannot parse."""

    count = 0

    for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
        stripped = line.strip()

        if stripped and not stripped.startswith('#'):
            count += 1

    return count


def estimated_statements(path):
    """Statement count for a file coverage.py cannot parse.

    The service entry points fail only because `def` is missing after `async`; repairing that in memory lets
    coverage.py's own parser count the statements. Anything still unparsable falls back to counting code lines.
    """

    text = path.read_text(encoding='utf-8', errors='replace')
    repaired = re.sub(r'^async (?!def\b)(\w+\()', r'async def \1', text, flags=re.M)

    try:
        from coverage.parser import PythonParser

        parser = PythonParser(text=repaired)
        parser.parse_source()

        return len(parser.statements)
    except Exception:
        return logical_lines(path)


def is_parsable(path):
    try:
        ast.parse(path.read_text(encoding='utf-8'))
    except SyntaxError:
        return False

    return True


def parse_outcomes(output):
    """Pull the counts from pytest's final summary line."""

    counts = {'passed': 0, 'failed': 0, 'xfailed': 0, 'xpassed': 0, 'skipped': 0, 'error': 0}
    summary = ''

    for line in reversed(output.strip().splitlines()):
        if re.search(r'\b(passed|failed|error|errors|xfailed|skipped|no tests ran)\b', line) and ' in ' in line:
            summary = line

            break

    for number, word in re.findall(r'(\d+) (passed|failed|xfailed|xpassed|skipped|errors?)', summary):
        counts['error' if word.startswith('error') else word] += int(number)

    return counts


def run_unit(name, project, src, extra_args):
    with tempfile.TemporaryDirectory() as tmp:
        rc = Path(tmp) / 'coveragerc'
        rc.write_text(COVERAGE_RC, encoding='utf-8')
        data = Path(tmp) / 'coverage.json'
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', COVERAGE_FILE=str(Path(tmp) / '.coverage'))
        command = [
            PYTHON, '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
            f'--cov={src}', f'--cov-config={rc}', f'--cov-report=json:{data}',
            *extra_args,
        ]
        result = subprocess.run(command, cwd=project, env=env, capture_output=True, text=True)
        output = result.stdout + result.stderr
        measured = {}

        if data.exists():
            report = json.loads(data.read_text(encoding='utf-8'))

            for filename, info in report['files'].items():
                summary = info['summary']
                # coverage.py reports paths relative to the directory pytest ran in
                measured[(project / filename).resolve()] = (summary['num_statements'], summary['covered_lines'])

    statements = covered = 0
    unparsable = []
    unmeasured = []

    for path in python_files(src):
        resolved = path.resolve()

        if resolved in measured:
            total, hit = measured[resolved]
            statements += total
            covered += hit
        elif not is_parsable(path):
            unparsable.append((path, estimated_statements(path)))
        elif path.stat().st_size and logical_lines(path):
            unmeasured.append(path)

    return {
        'name': name,
        'returncode': result.returncode,
        'outcomes': parse_outcomes(output),
        'statements': statements,
        'covered': covered,
        'unparsable': unparsable,
        'unmeasured': unmeasured,
        'output': output,
    }


def run_web():
    """Run the Node suite for cynthus-web with its built-in coverage and return (summary line, ok)."""

    web = ROOT / 'cynthus-web'

    if not (web / 'package.json').exists():
        return 'cynthus-web: not found', True

    result = subprocess.run(['node', '--test', '--test-concurrency=1', '--experimental-test-coverage'], cwd=web,
                            capture_output=True, text=True, encoding='utf-8', errors='replace')
    output = result.stdout + result.stderr
    count = {key: int(m.group(1)) for key in ('tests', 'pass', 'fail') if (m := re.search(rf'ℹ {key} (\d+)', output))}
    cover = re.search(r'all files\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)', output)
    line = (f'cynthus-web (node): {count.get("pass", 0)} passed, {count.get("fail", 0)} failed; '
            + (f'line coverage {cover.group(1)} %, branch {cover.group(2)} %, functions {cover.group(3)} %' if cover else 'coverage not reported'))

    return line, result.returncode == 0


def percent(covered, statements):
    return 100.0 if statements == 0 else 100.0 * covered / statements


def render(results, threshold):
    lines = []
    header = f'{"suite":<46} {"passed":>6} {"failed":>6} {"xfail":>5} {"skip":>4} {"stmts":>6} {"miss":>5} {"cover":>7}'
    lines.append(header)
    lines.append('-' * len(header))

    total_statements = total_covered = total_unparsable = 0
    totals = {'passed': 0, 'failed': 0, 'xfailed': 0, 'skipped': 0, 'error': 0}

    for result in results:
        out = result['outcomes']
        failed = out['failed'] + out['error']
        miss = result['statements'] - result['covered']
        lines.append(
            f'{result["name"]:<46} {out["passed"]:>6} {failed:>6} {out["xfailed"]:>5} {out["skipped"]:>4} '
            f'{result["statements"]:>6} {miss:>5} {percent(result["covered"], result["statements"]):>6.1f}%'
        )
        total_statements += result['statements']
        total_covered += result['covered']
        total_unparsable += sum(count for _, count in result['unparsable'])

        for key in totals:
            totals[key] += out[key]

    lines.append('-' * len(header))
    lines.append(
        f'{"TOTAL (parsable source)":<46} {totals["passed"]:>6} {totals["failed"] + totals["error"]:>6} '
        f'{totals["xfailed"]:>5} {totals["skipped"]:>4} {total_statements:>6} '
        f'{total_statements - total_covered:>5} {percent(total_covered, total_statements):>6.1f}%'
    )

    overall = percent(total_covered, total_statements + total_unparsable)
    lines.append(
        f'{"TOTAL incl. unparsable files as 0 %":<46} {"":>6} {"":>6} {"":>5} {"":>4} '
        f'{total_statements + total_unparsable:>6} {total_statements + total_unparsable - total_covered:>5} {overall:>6.1f}%'
    )

    unparsable = [(result['name'], path, count) for result in results for path, count in result['unparsable']]

    if unparsable:
        lines.append('')
        lines.append(f'Files coverage.py cannot parse (syntax errors) - {len(unparsable)} files, ~{total_unparsable} statements:')

        for name, path, count in unparsable:
            lines.append(f'  {path.relative_to(ROOT)}  (~{count} statements)')

    unmeasured = [(result['name'], path) for result in results for path in result['unmeasured']]

    if unmeasured:
        lines.append('')
        lines.append(f'Parsable files coverage.py did not report on - {len(unmeasured)} files:')

        for _, path in unmeasured[:LIST_LIMIT]:
            lines.append(f'  {path.relative_to(ROOT)}')

        if len(unmeasured) > LIST_LIMIT:
            lines.append(f'  ... and {len(unmeasured) - LIST_LIMIT} more')

    lines.append('')
    lines.append(
        f'Threshold {threshold:.0f} %: parsable source {"MEETS" if percent(total_covered, total_statements) >= threshold else "BELOW"}'
        f', including unparsable {"MEETS" if overall >= threshold else "BELOW"}'
    )

    return '\n'.join(lines), percent(total_covered, total_statements), overall


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--unit', help='only run suites whose name contains this text')
    parser.add_argument('--threshold', type=float, default=75.0)
    parser.add_argument('--enforce', action='store_true', help='exit 1 when below the threshold or on any failure')
    parser.add_argument('--report', help='also write the report to this file (markdown code block)')
    parser.add_argument('--web', action='store_true', help='also run the cynthus-web (Node) suite with coverage')
    parser.add_argument('--verbose', action='store_true', help='print pytest output for suites with failures')
    parser.add_argument('pytest_args', nargs='*', help='extra arguments passed to pytest (after --)')
    args = parser.parse_args()

    results = []

    for name, project, src in discover():
        if args.unit and args.unit not in name:
            continue

        print(f'running {name} ...', file=sys.stderr, flush=True)
        results.append(run_unit(name, project, src, args.pytest_args))

    text, parsable, overall = render(results, args.threshold)
    web_ok = True

    if args.web:
        print('running cynthus-web ...', file=sys.stderr, flush=True)
        web_line, web_ok = run_web()
        text += '\n\n' + web_line

    print(text)

    if args.verbose:
        for result in results:
            if result['outcomes']['failed'] or result['outcomes']['error']:
                print(f'\n===== {result["name"]} =====\n{result["output"]}')

    if args.report:
        Path(args.report).write_text(f'```\n{text}\n```\n', encoding='utf-8')

    failures = sum(r['outcomes']['failed'] + r['outcomes']['error'] for r in results)

    if args.enforce and (failures or parsable < args.threshold or not web_ok):
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
