# Release Notes

Detailed notes per release: the narrative, the performance story, and the
validation evidence behind each version. `CHANGELOG.md` stays terse and
user-facing; this file is the durable record.

---

## [0.1.1] - 2026-07-24

### What changed

`call`/`query`/`generate-typings` drop now-redundant `NS(...)` overrides on
their `Args` fields — `NS(type=...)` on a plain `str`/`Path` field (duho
already derives `type=` from the annotation) and `NS(action='append',
nargs=...)` on a `list[str]` option (duho ≥0.5.0 already defaults a list-typed
option to `action="append"`, `nargs=None`). Only `NS(metavar=...)` remains
where the display name isn't inferable. No CLI-surface or dependency-floor
change from 0.1.0 — the `duho>=0.4.1` floor is unchanged since this
simplification is purely cosmetic against an installed 0.4.1 (duho's own
default already matches what the explicit overrides asked for).

### Validation evidence

- Tests: **187 passed / 5 skipped** on Windows Python 3.9.13 (unchanged
  count/shape from 0.1.0 — this release touches only `Args` declarations, no
  behavior).
- Build: `python -m build` produces `pytruenas-0.1.1.tar.gz` and
  `pytruenas-0.1.1-py3-none-any.whl` cleanly.
- Not re-validated live against a real TrueNAS host for this release (0.1.0's
  live evidence below still describes the exercised code paths; this release
  doesn't touch client/namespace/jsonrpc).

### Publication state

Committed to `main` (`ff56cdb`). **Not tagged/published** — same as 0.1.0,
publishing a `v0.1.1` tag is user-gated.

---

## [0.1.0] - 2026-07-24

### What changed

- **`client.run()` text-mode input fix.** `str` input together with a text
  `encoding`/`errors` used to be pre-encoded to bytes *and* handed to
  `subprocess.run` with the encoding, which then tried to `.encode()` bytes and
  crashed. Text mode now keeps `str` as-is (and decodes `bytes` input); binary
  mode encodes. Found by live testing against a real TrueNAS 26.0 host — the
  unit tests mock `subprocess.run`, so only a real POSIX run exercised it.
- **`pytruenas.__version__`** now exposed (resolved from installed metadata).
- **Dependency floors** raised to the tested versions: `duho>=0.3.2` (CLI parser
  fixes) and the `ssh` extra's `pathlib_next[sftp-async]>=0.8.3` (SFTP
  concurrency 8→16).
- **Repo brought to standard:** benchmark suite (`benchmarks/run.py`), docs site
  (`mkdocs.yml` + `docs/`), `CONTRIBUTING.md`, and this file.
- **Everything else accumulated since `0.0.0`** (auth.login_ex/2FA login, client
  convenience wrappers, event subscriptions, netimps-based adapter discovery,
  password redaction in logs, RunPath support) is covered in `CHANGELOG.md`'s
  `[0.1.0]` section, not repeated here.
- **CLI: the trailing `targets` positional is registered centrally**, not by
  each command calling `register_targets(parser)` — `main._with_targets` wraps
  every module command's `register` hook (even a command with none of its own)
  and adds `targets` after it, so an external `--cmdspath` command gets the
  same `<command> [args...] [TARGET ...]` grammar for free.
- **Commands declare their CLI fields via `Args`** instead of an imperative
  `register()` that hand-synced against an otherwise-inert `Args` class (duho
  ≥0.4.1 adds a module command's declared `Args` fields before `register`
  runs). `register()` remains for what a declaration can't express. No
  CLI-surface change (`call method [TARGET ...]`, `query namespace [TARGET
  ...]`, repeatable `-f`/`-p`, `--api-version`/`--api-cache` unchanged).
- **Known gap, not fixed in this release:** an option placed between a
  command's own positional and the trailing targets still fails to parse
  (`query user -f x nas1` → `unrecognized arguments: nas1`) — argparse's own
  greedy positional-run matching. `call.py`'s docstring documents the
  workaround; filed upstream against duho (its own flag-reorder fix doesn't
  reach a module command's subparser).

### Performance

First benchmark baseline (see `benchmarks/results/`). These are **local**
numbers (Intel i7-1065G7 class, Windows) for regression-catching, not a CI
figure. The suite measures pure-CPU hot paths — no network.

| metric | py3.9 median (ms/call) | py3.14 median (ms/call) |
| --- | --- | --- |
| `ejson.dumps.plain` (20-row response) | 0.048 | 0.045 |
| `ejson.loads.plain` | 0.048 | 0.050 |
| `ejson.dumps.extended` | 0.020 | 0.021 |
| `ejson.loads.extended` | 0.020 | 0.020 |
| `namespace.methodname` | 0.004 | 0.004 |
| `query.filter_from_kwargs` | 0.003 | 0.002 |

**Hot-path analysis:** the ejson encode/decode paths dominate and are already
near stdlib-optimal. Two candidate micro-optimizations were measured and
**rejected** (each ~1.02x, within noise): swapping `json.dumps(cls=Encoder)` for
`default=func` (Python's `json` uses the pure-Python encoder whenever any custom
type handling is present, regardless), and a fast-path bail in `_object_hook`
(real response dicts are multi-key, already short-circuited). The client's cost
is I/O-bound; there is no pending CPU speedup. This baseline exists to catch a
future regression.

**Performance target for the next release:** no regression on the medians above
(compare same machine + interpreter).

### Validation evidence

- Tests (as of this file's earlier entries, predating the CLI/`Args` work
  above): **113 passed / 5 skipped** on Windows Python 3.9; **118 passed / 0
  skipped** on Python 3.13 on a real TrueNAS 26.0 host (the POSIX-shell-gated
  `run()` tests that skip on Windows run there).
- Live integration on TrueNAS 26.0.0-BETA.1 via the local middleware socket:
  `system.info`, `user.query`, `pool.dataset.query`, `_get`, fs `Path`
  exists/read, `client.run()` shell paths, and the `dump-api` / `query` /
  `generate-typings` CLI subcommands (129 valid `.pyi` stubs generated).
- Build: `python -m build` + `twine check` PASS; wheel carries `py.typed`, no
  agent-file leakage.
- Docs: `mkdocs build --strict` clean.
- Coverage: TOTAL 70% (client 62%, namespace 79%, jsonrpc 84%, main 80%).
- **Re-verified for the final `0.1.0` tree** (CLI centralization + `Args`
  declarations included): **187 passed / 5 skipped** on Windows Python 3.9.13
  (no environment with a live TrueNAS host or `twine`/`mkdocs` available in
  this pass — the sections above are the last live-host/docs-build evidence on
  record; only the automated-test count and `python -m build` were re-run).

### Publication state

Prepared and merged to `main`. **Not tagged/published** — a `v0.1.0` release is
user-gated and requires PyPI trusted-publishing + GitHub Pages setup by the repo
owner.

---
