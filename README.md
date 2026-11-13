# cynthus

## Description

Design documents, engineering standards and shared tooling for the Cynthus Life platform. This repository holds the
product requirements, architecture, roadmap, decision records, the CI and lint files every repository copies, and the
scripts that create and check repositories.

## Prerequisites

- Git and Python 3.11 or later (the tools in `tools/` and the check in `.github/scripts/` are plain Python).
- [Node.js](https://nodejs.org/) only if you want to run `markdownlint-cli2` yourself.

## Installation

```bash
git clone https://github.com/TechClusiveSolutions/cynthus.git
cd cynthus
python .github/scripts/check_markdown.py
```

The last command checks the Markdown for screen readers and prints `0 problem(s)` when it is clean.

## Minimal configuration

None. The tools take their settings from the command line.

## Gotchas

- Markdown must be ASCII only, with no pipe tables, a language on every code block, and relative links that resolve.
  `.github/scripts/check_markdown.py` enforces this in CI.
- The README of every repository has the same headings, in the same order, and CI checks them. See the standards.
- Feature branches come from an issue (`gh issue develop <number> --base dev`) and merge into `dev`; `dev` merges
  into `main`.

## More documentation

- [`docs/README.md`](docs/README.md): index of the PRD, architecture, roadmap, feature map and signal map.
- [`docs/engineering-standards.md`](docs/engineering-standards.md): how we write, test, review and merge code.
- [`docs/adr/`](docs/adr): architecture decision records.
- [`templates/repo/`](templates/repo): the files every repository carries, including a model README.
- [`tools/`](tools): test runner, test generators, mutation and inventory checks, and `bootstrap_repo.py`.
- The [Cynthus Engineering Tracker](https://github.com/orgs/TechClusiveSolutions/projects/6) tracks the work.
