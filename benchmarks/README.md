# pytruenas benchmarks

Micro-benchmarks for the pure-CPU hot paths hit on every middleware call —
extended-JSON (ejson) encode/decode, API namespace method-name building, and
query-filter construction. **No network or server is involved**; these measure
per-call CPU cost, not the round-trip latency that dominates real use.

## Running

```bash
# print summary only (from an installed package, or PYTHONPATH=src)
python benchmarks/run.py

# also write benchmarks/results/pytruenas-<ver>-py<XY>-<platform tag>.json
python benchmarks/run.py --save

# report each median as a ratio to a saved result (above 1.0 is slower)
python benchmarks/run.py --compare benchmarks/results/<earlier result>.json
```

`--name <x>` overrides the filename stem and `--results-dir <dir>` the
directory. The default name carries the package version, the interpreter and
the platform tag (`sysconfig.get_platform()`), so one file holds one release on
one interpreter and kind of machine, and no result overwrites another.

Compare only results measured on the **same machine**.
A hosted CI runner is not one fixed machine: two runs of byte-identical code on
`ubuntu-latest` differed by 20-40 % on every metric. That is why the `benchmark`
job in `.github/workflows/test.yml` measures the checkout and the latest PyPI
release **in the same job**, prints the ratio between them, and uploads both
results; that ratio, not either absolute number, is what release notes quote.

Results are committed: at a release, the job's `-linux-x86_64` result for the
new version goes into `results/`. Files are written as UTF-8 with LF line
endings on every platform.

## Schema

Each `results/<name>.json`: `name`, `pytruenas_version`, `python`, `platform`,
`platform_tag`, `processor`, `timestamp` (UTC), `iterations` (inner counts +
`repeat`), and `metrics`. Each metric reports `min_ms`/`median_ms`/`max_ms`
**per call**, sampled `repeat` times — compare on `median_ms`; min/max show
run-to-run noise. The two `0.1.0` files predate `platform_tag` and the platform
suffix in the name; they were measured on an Intel x86-64 Windows laptop.

Metrics:
- `ejson.dumps.plain` / `ejson.loads.plain` — a 20-row `user.query`-shaped
  response with no extended types (the common case).
- `ejson.dumps.extended` / `ejson.loads.extended` — a payload exercising every
  extended type (datetime/date/time/set/IPv4Interface).
- `namespace.methodname` — building `pool.dataset.snapshot` from an attribute
  walk (a fresh chain each call, so a hit in the namespace's child cache is
  not what's measured).
- `query.filter_from_kwargs` — turning `username="root", uid=GT(0), locked=False`
  into middleware filter tuples.

## Findings (2026-07-19, baseline)

The ejson paths dominate (~0.02–0.05 ms/call) and are **already near
stdlib-optimal**. Two candidate optimizations were measured and rejected:

- Swapping `json.dumps(cls=Encoder)` for `json.dumps(default=func)` to avoid
  re-instantiating the encoder: **~1.02x**, within noise. Python's `json` drops
  to the pure-Python `iterencode` whenever any custom type handling is present,
  regardless of `cls=` vs `default=`, so there's no C-encoder fast path to
  recover here.
- A fast-path bail in `_object_hook` for single-key dicts whose key doesn't
  start with `$`: **~1.02x**. Real response dicts are multi-key, so the existing
  `len(obj) == 1` guard already short-circuits them.

Conclusion: the client's CPU hot paths are not a bottleneck worth
micro-optimizing; real-world cost is I/O-bound (network round-trips). This
baseline exists to catch a future *regression*, not because a speedup is
pending. The per-release before/after narrative lives in the repo-root
`RELEASENOTES.md`.
