# pytruenas — repository orientation

How this checkout is laid out, how to build and test it, and how it ships. This
file is for someone (or something) working **on** the repository; it is not
packaged.

For the public API, read the shipped header
[`src/pytruenas/AGENTS.md`](src/pytruenas/AGENTS.md) — every export with its
signature, contract and gotchas, written so a consumer never has to open the
source. User-facing documentation lives in [`docs/`](docs/) and on the docs
site; [`CONTRIBUTING.md`](CONTRIBUTING.md) covers the human workflow.

## Layout

- `src/pytruenas/` — the package. `host.py` is the entry point
  (`TrueNASHost`, and `TrueNASClient` as an alias for it — one class, two
  names); `connection.py` the JSON-RPC websocket transport; `namespace.py` the
  dynamic API dispatcher; `auth.py` credentials; `fs/` remote path objects;
  `cmd/` the CLI's command modules; `codegen/` the typings generator; `patch/`
  host modification beyond the API; `utils/` shared helpers. `deploy` runs on
  `hostctl.deploy`; `cmd/deploy.py` holds only pytruenas's policy.
- `tests/` — the suite, one module per area. `benchmarks/` — a runnable perf
  suite plus its tracked results. `examples/` — runnable scripts.
  `docs/` — the MkDocs site sources.

## Environments

The package targets **Python 3.9+**. CI tests every version from 3.9 to 3.14
on Linux, and 3.9 and 3.14 on Windows and macOS. Dependencies are installed
from PyPI per `pyproject.toml`; nothing is vendored.

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

## Test, format, docs

```bash
python -m pytest -q -rs                  # the suite; -rs lists skip reasons
python -m pytest -q --cov=pytruenas      # with coverage
python -m black src tests benchmarks examples   # CI runs it with --check
python -m mkdocs build --strict          # from the project venv, not a global one
python benchmarks/run.py                 # --save writes benchmarks/results/<name>.json
```

`mkdocs` must run from the project's own environment: `mkdocstrings` imports
`pytruenas`, which a global interpreter cannot see.

Some `client.run()` tests need a POSIX shell and skip on Windows. Run the suite
on the 3.9 floor before a release — a 3.9-only breakage is invisible on 3.14.

## CI

Three workflows, one concern each (`.github/workflows/`):

- **`test.yml`** — on demand: `workflow_dispatch`, or by pushing a throwaway
  `ci-*` tag. Runs the suite (`pytest -q -rs`) on every supported Python on
  Linux and on 3.9 and 3.14 on Windows and macOS; at every declared
  dependency floor on 3.9 (`floors`); with no extras installed (`no-extras`);
  `black --check`; the benchmarks against the latest PyPI release in the same
  job; and a strict docs build. Delete the tag afterwards.
- **`release.yml`** — on a `v*` tag: test and `floors` → build (the tag must
  equal `project.version`; `twine check`) → `wheel-smoke` (the wheel, no
  extras, in a clean venv on 3.9 and 3.14: import, shipped files, console
  script, the suite) and a strict docs build gate → GitHub release → PyPI
  (Trusted Publishing, `skip-existing`) and a dispatch of `docs.yml` at the
  tag. A broken docs build blocks the release. A pre-release tag (one with a
  `-`) gets a GitHub pre-release only: no PyPI upload, no docs deploy.
- **`docs.yml`** — owns every Pages deploy: on a push to `main` touching docs
  sources, or on `workflow_dispatch` (which is how a release deploys its
  docs). It enables Pages itself.

## Release

`CHANGELOG.md` is the source of the release notes — the release workflow
scrapes the section matching the tag, so the heading must exist before tagging.
`RELEASENOTES.md` is the longer companion: benchmark tables, migration detail
and validation evidence.

Versions are SemVer for tags and the changelog, PEP 440 in `pyproject.toml`
(`1.0.0rc1`, not `1.0.0-rc.1`); never "fix" one to match the other. **Pre-1.0,
the minor slot means the documented API broke** — new methods, new optional
keyword arguments and fixes are all patch releases, so a `~=0.4.0` consumer
gets additions without re-reading anything.

Pushing a `v*` tag publishes irreversibly. Get everything else done first, and
ask the owner for that specific release. `ci-*` tags are always safe.
