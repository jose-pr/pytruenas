# Contributing to pytruenas

Thanks for your interest in contributing! Here's how to get started.

## Development Setup

```bash
git clone https://github.com/jose-pr/pytruenas.git
cd pytruenas

# Create a virtual environment (project targets Python 3.9+)
python -m venv .venv
.venv/Scripts/activate        # Windows; on Unix: source .venv/bin/activate

# Install in development mode with every extra the tests exercise
pip install -e ".[dev,config,ssh,codegen]"
```

The optional extras are `ssh` (remote commands and the SFTP filesystem leg),
`config` (YAML config files), `codegen` (generating typings), `docs` and
`repo` (`deploy --source repo`). The `dev` extra already carries the SSH
dependencies, so a plain `-e ".[dev]"` runs the whole suite; the others turn on
the features those tests cover. Tests for a missing extra **skip**, so a
partial install still reports green -- install them all before concluding
anything about a change.

## Running Tests

```bash
pytest -q
```

Before a release or a large change, run the floor too (Python 3.9) — a
3.9-only breakage does not show up on a newer interpreter.

With coverage:

```bash
pytest -q --cov=pytruenas --cov-report=term-missing
```

Some `client.run()` tests require a POSIX shell and skip on Windows; they run on
Linux/macOS (and on a real NAS). "0 failures" with those skipped is expected on
Windows — run `pytest -rs` to see skip reasons.

## Running Benchmarks

```bash
python benchmarks/run.py            # print summary
python benchmarks/run.py --save     # write benchmarks/results/<name>.json
```

See [`benchmarks/README.md`](benchmarks/README.md) for the schema and what the
numbers mean.

## Docs

```bash
pip install -e ".[docs]"
mkdocs serve            # live preview at http://127.0.0.1:8000
mkdocs build --strict   # what CI gates on
```

## Code Style

- Follow PEP 8; use type hints.
- `from __future__ import annotations` in any module using `X | Y` unions in
  annotations — the floor is Python 3.9, which cannot evaluate them. Where an
  annotation is evaluated at runtime anyway (a `duho` args field, a
  `TypedDict` built by a call), write `typing.Optional[X]` / `typing.Union`
  instead: the future import does not help there.
- Keep the vendored-free, minimal-dependency posture: guard optional imports and
  degrade gracefully rather than hard-crashing on a missing extra.

## Commit Guidelines

Format: `type: description`

- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `test:` tests
- `chore:` build, CI, deps, or tooling

Keep commits logical and separate (a feature and its tests together; docs/config
apart from behavior changes).

## Pull Request Process

1. Branch: `git checkout -b feat/my-feature`
2. Make changes and add tests.
3. `pytest -q` green; `mkdocs build --strict` clean if docs changed.
4. Commit with a clear message and open a PR.

## Reporting Issues

Include your Python version, pytruenas version, the TrueNAS version, a minimal
reproducer, and expected vs. actual behavior.
