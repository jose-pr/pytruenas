# Release Notes

Detailed notes per release: the narrative, the performance story, and the
validation evidence behind each version. `CHANGELOG.md` stays terse and
user-facing; this file is the durable record.

---

## [Unreleased]

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

- Tests: **113 passed / 5 skipped** on Windows Python 3.9; **118 passed / 0
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

### Publication state

Prepared and merged to `main`. **Not tagged/published** — a `v0.1.0` release is
user-gated and requires PyPI trusted-publishing + GitHub Pages setup by the repo
owner.

---
