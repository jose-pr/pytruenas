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
  host modification beyond the API; `utils/` shared helpers (`bundle.py` builds
  deploy payloads and knows nothing about TrueNAS).
- `tests/` — the suite, one module per area. `benchmarks/` — a runnable perf
  suite plus its tracked results. `examples/` — runnable scripts.
  `docs/` — the MkDocs site sources.

## Environments

The package targets **Python 3.9+** and is tested on 3.9, 3.13 and 3.14 across
Linux, Windows and macOS. Dependencies are installed from PyPI per
`pyproject.toml`; nothing is vendored.

```bash
python -m venv .venv
pip install -e ".[dev,config,ssh,codegen,docs,repo]"
```

Two things about the extras are easy to get wrong:

- A test whose extra is missing **skips**. A partial install still prints
  green, so install everything before judging a change.
- On Windows ARM64, `cryptography` has no source build that works; install with
  `--only-binary=cryptography`.

## Test, format, docs

```bash
python -m pytest -q                      # the suite; -rs to see skip reasons
python -m pytest -q --cov=pytruenas      # with coverage
python -m black src tests benchmarks examples
python -m mkdocs build --strict          # from the project venv, not a global one
python benchmarks/run.py                 # --save writes benchmarks/results/
```

`mkdocs` must run from the project's own environment: `mkdocstrings` imports
`pytruenas`, which a global interpreter cannot see.

Some `client.run()` tests need a POSIX shell and skip on Windows. Run the suite
on the 3.9 floor before a release — a 3.9-only breakage is invisible on 3.14.

## CI

Three workflows, one concern each (`.github/workflows/`):

- **`test.yml`** — on demand: `workflow_dispatch`, or by pushing a throwaway
  `ci-*` tag. Runs the suite on the version/OS matrix, the benchmarks, and a
  strict docs build. Delete the tag afterwards.
- **`release.yml`** — on a `v*` tag: test → build → GitHub release → PyPI
  (Trusted Publishing, `skip-existing`). It **gates** on a strict docs build
  but never deploys Pages, and publish does not depend on that gate.
- **`docs.yml`** — owns every Pages deploy: on a published release, on a push
  to `main` touching docs sources, or on demand. It enables Pages itself.

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
