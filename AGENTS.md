# pytruenas — repository orientation

How this checkout is laid out, how to build and check it, and how it ships.
This file is for someone (or something) working **on** the repository; it is
not packaged. User-facing documentation lives in [`docs/`](docs/) and on the
docs site; [`CONTRIBUTING.md`](CONTRIBUTING.md) covers the human workflow.

| Shipped header | Covers |
| --- | --- |
| [`src/pytruenas/AGENTS.md`](src/pytruenas/AGENTS.md) | the whole public API — every export with its signature, contract and gotchas, plus the CLI, its command-module contract, environment variables and exceptions — so a consumer never has to open the source |

## Layout

- `src/pytruenas/` — the package. `host.py` is the entry point
  (`TrueNASClient`, a hostctl `PosixHost`); `connection.py` the JSON-RPC
  websocket transport; `namespace.py` the dynamic API dispatcher; `auth.py` credentials; `exceptions.py` the
  `TrueNASError` base; `providers.py` and `webshell.py` the transport
  providers; `fs/` remote path objects; `main.py` the CLI and `cmd/` its
  built-in command modules; `codegen/` the typings generator; `models/` the
  API-dump TypedDicts; `patch/` host modification beyond the API; `utils/`
  shared helpers. `deploy` runs on `hostctl.deploy`; `cmd/deploy.py` holds
  only pytruenas's policy.
- `tests/` — the suite, one module per area. `benchmarks/` — a runnable perf
  suite plus its tracked results. `examples/` — runnable scripts.
  `docs/` — the MkDocs site sources.
- `CHANGELOG.md` (current series), `CHANGELOG-0.x.md` (0.0.0–0.4.6),
  `RELEASENOTES.md` — see [Releasing](#releasing).

## Environment

The package targets **Python 3.9+**. Dependencies are installed from PyPI per
`pyproject.toml`; nothing is vendored.

One venv per interpreter, named `.venv/<python>-<os>-<arch>` after the
interpreter it holds. On Windows ARM64:

```sh
py -V:3.14-arm64 -m venv .venv/3.14-nt-arm64
.venv/3.14-nt-arm64/Scripts/python -m pip install --only-binary=cryptography -e ".[dev,docs]"
.venv/3.14-nt-arm64/Scripts/python -m pytest -q -rs
```

The floor venv is the same with `3.9`. Elsewhere, create the venv with that
interpreter (`python3.14 -m venv .venv/3.14-posix-x86_64`) and use `bin/`
where Windows has `Scripts/`. This is the recipe the README's Development
section and `CONTRIBUTING.md` give.

Two things about the extras are easy to get wrong:

- `dev` carries every extra that has tests (`config`, `ssh`, `codegen`). A
  test whose extra is missing **skips**, so a partial install still prints
  green; `-rs` lists the skips.
- On Windows ARM64, recent `cryptography` releases have no wheel and the
  source build fails; `--only-binary=cryptography` picks the newest release
  that has one. It changes nothing where a wheel exists.

## Checks

```bash
python -m pytest -q -rs                  # the suite; -rs lists skip reasons
python -m pytest -q --cov=pytruenas      # with coverage
python -m black src tests benchmarks examples   # CI runs it with --check
python -m mkdocs build --strict          # from the project venv, not a global one
python benchmarks/run.py                 # --save writes benchmarks/results/<name>.json
```

`mkdocs` must run from the project's own environment: `mkdocstrings` imports
`pytruenas`, which a global interpreter cannot see.

Warnings are errors and an `xfail` that passes fails (`pyproject.toml`). Some
`client.run()` tests need a POSIX shell and skip on Windows. Run the suite on
the 3.9 floor before a release — a 3.9-only breakage is invisible on 3.14.

CI is three workflows, one concern each (`.github/workflows/`):

- **`test.yml`** — on demand: `workflow_dispatch` (optionally at a given
  ref), or by pushing a throwaway `ci-*` tag; delete the tag afterwards.
  Jobs: the suite (`pytest -q -rs`, `.[dev]`) on every supported Python
  (3.9–3.14) on Linux and on 3.9 and 3.14 on Windows and macOS; `floors`, the
  suite on 3.9 with every runtime dependency and feature extra pinned to the
  floor `pyproject.toml` declares; `no-extras`, the bare package plus pytest
  on 3.14 (it must import, and every extra-gated test must skip); `format`
  (`black --check`); `benchmark` on 3.9 and 3.14, measuring the latest PyPI
  release and the checkout in the same job; and a strict docs build.
- **`release.yml`** — on a `v*` tag: the test matrix (3.9 and 3.14 on all
  three OSes) and `floors` → `build` (the tag must equal the built version;
  `twine check`) → `wheel-smoke` (the wheel, no extras, in a clean venv on 3.9
  and 3.14: import, the shipped `py.typed`/`AGENTS.md`/`README.md`, the
  console script, then the suite against it) and `docs-gate` (a strict docs
  build) → GitHub release (notes scraped from `CHANGELOG.md`) → PyPI (Trusted
  Publishing, `skip-existing`) and a dispatch of `docs.yml` at the tag. The
  GitHub release needs `build`, `wheel-smoke` and `docs-gate`, and PyPI needs
  the GitHub release, so a broken docs build blocks publishing. A pre-release
  tag (one with a `-`) gets a GitHub pre-release only: no PyPI upload, no docs
  deploy.
- **`docs.yml`** — owns every Pages deploy: on a push to `main` touching docs
  sources (`docs/`, `mkdocs.yml`, `src/`, `CHANGELOG.md`, the workflow), or on
  `workflow_dispatch` (which is how a release deploys its docs). It enables
  Pages itself; the `github-pages` environment must allow `v*` tag refs.

## Conventions

- **Format** with black; `target-version` is the 3.9 floor.
- **3.9-safe annotations**: `from __future__ import annotations` in any module
  using `X | Y`; where an annotation is evaluated at run time anyway (a `duho`
  args field, a `TypedDict` built by a call), write `typing.Optional[X]` /
  `typing.Union`.
- **Optional extras** are imported at first use, never at import time, and a
  missing one raises `hostctl.MissingExtraError` naming the extra.
- **Dependency ranges**: a 0.x dependency is capped below its next minor and
  floored at the base of the series, unless the package's own code needs a
  later patch — then the comment above the spec names that API and patch.
  1.x+ dependencies are major-scoped. Version history goes in the changelog,
  not in `pyproject.toml`.
- **The shipped header is current in the same commit** as the API change it
  describes; it states the API as it is, with no history (that is the
  changelog's job) and no repository-relative links.
- **Comments** say what the code cannot — the constraint, the reason, the
  unit — about the code as it is.
- **Line endings** are LF everywhere (`.gitattributes`: `* text=auto eol=lf`).
- **Commits**: `type: description` (`feat:`, `fix:`, `docs:`, `test:`,
  `chore:`), one logical change each — a feature with its tests, docs and
  config apart from behaviour.

## Releasing

`CHANGELOG.md` is the source of the release notes — the release workflow
scrapes the section matching the tag, so the heading must exist before tagging.
Entries for 0.0.0–0.4.6 live in `CHANGELOG-0.x.md`. `RELEASENOTES.md` is the
longer companion: benchmark tables, migration detail and validation evidence.

Versions are SemVer for tags and the changelog, PEP 440 in `pyproject.toml`
(`1.0.0rc1`, not `1.0.0-rc.1`); never "fix" one to match the other. **Pre-1.0,
the minor slot means the documented API broke** — new methods, new optional
keyword arguments and fixes are all patch releases, so a `~=0.4.0` consumer
gets additions without re-reading anything.

Pushing a `v*` tag publishes irreversibly. Get everything else done first, and
ask the owner for that specific release. `ci-*` tags are always safe.
