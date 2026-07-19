# pytruenas benchmarks

Micro-benchmarks for the pure-CPU hot paths hit on every middleware call —
extended-JSON (ejson) encode/decode, API namespace method-name building, and
query-filter construction. **No network or server is involved**; these measure
per-call CPU cost, not the round-trip latency that dominates real use.

## Running

```bash
# print summary only
PYTHONPATH=src .venv39/Scripts/python benchmarks/run.py

# also write benchmarks/results/pytruenas-<ver>-py<ver>.json
PYTHONPATH=src .venv39/Scripts/python benchmarks/run.py --save
PYTHONPATH=src .venv314/Scripts/python benchmarks/run.py --save
```

Run without `--save` to just print. `--name <x>` overrides the filename stem.
Compare files only across the **same machine + interpreter**, or the numbers
aren't meaningful.

## Schema

Each `results/<name>.json`: `name`, `pytruenas_version`, `python`, `platform`,
`processor`, `timestamp` (UTC), `iterations` (inner counts + `repeat`), and
`metrics`. Each metric reports `min_ms`/`median_ms`/`max_ms` **per call**,
sampled `repeat` times — compare on `median_ms`; min/max show run-to-run noise.

Metrics:
- `ejson.dumps.plain` / `ejson.loads.plain` — a 20-row `user.query`-shaped
  response with no extended types (the common case).
- `ejson.dumps.extended` / `ejson.loads.extended` — a payload exercising every
  extended type (datetime/date/time/set/IPv4Interface).
- `namespace.methodname` — building `pool.dataset.snapshot` from an attribute
  walk (fresh chain each call, so the `@cache` hit is not what's measured).
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
