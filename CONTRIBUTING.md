# Contributing to pytruenas

Thanks for your interest in contributing! Here's how to get started.

## Development Setup

```sh
git clone https://github.com/jose-pr/pytruenas.git
cd pytruenas
py -V:3.14-arm64 -m venv .venv/3.14-nt-arm64
.venv/3.14-nt-arm64/Scripts/python -m pip install --only-binary=cryptography -e ".[dev,docs]"
.venv/3.14-nt-arm64/Scripts/python -m pytest -q -rs
```

That is the recipe on Windows ARM64, and the same one the README and the
repo-root `AGENTS.md` give. A venv is named `.venv/<python>-<os>-<arch>` after
the interpreter it holds: on Linux, for example,
`python3.14 -m venv .venv/3.14-posix-x86_64`, with `bin/` where Windows has
`Scripts/`. `--only-binary=cryptography` stops pip from building
`cryptography` from source, which fails on Windows ARM64, where recent
releases ship no wheel; on a platform with a wheel it changes nothing.

The `dev` extra carries every extra that has tests (`config`, `ssh`,
`codegen`); `docs` adds the site tooling. Tests for a missing extra **skip**,
so a partial install still reports green -- read the `-rs` summary before
concluding anything about a change.

## Running Tests

```sh
python -m pytest -q -rs
```

Warnings are errors and an `xfail` that passes fails, both set in
`pyproject.toml`. Before a release or a large change, run the floor too
(Python 3.9, `.venv/3.9-nt-arm64`) — a 3.9-only breakage does not show up on a
newer interpreter.

With coverage:

```sh
python -m pytest -q --cov=pytruenas --cov-report=term-missing
```

Some `client.run()` tests require a POSIX shell and skip on Windows; they run on
Linux/macOS (and on a real NAS). "0 failures" with those skipped is expected on
Windows; `-rs` names them.

## Running Benchmarks

```sh
python benchmarks/run.py                       # print summary
python benchmarks/run.py --save                # write benchmarks/results/<name>.json
python benchmarks/run.py --compare <result>    # each median as a ratio to a saved result
```

Compare results from the same machine only. See
[`benchmarks/README.md`](benchmarks/README.md) for the naming, the schema and
what the numbers mean.

## Docs

```sh
python -m pip install -e ".[dev,docs]"
mkdocs serve            # live preview at http://127.0.0.1:8000
mkdocs build --strict   # what CI gates on
```

## Code Style

- Format with black (`python -m black src tests benchmarks examples`); CI
  checks it.
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
3. `pytest -q -rs` green; `mkdocs build --strict` clean if docs changed.
4. Commit with a clear message and open a PR.

## Reporting Issues

Include your Python version, pytruenas version, the TrueNAS version, a minimal
reproducer, and expected vs. actual behavior.
