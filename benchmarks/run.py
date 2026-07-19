#!/usr/bin/env python3
"""Structured benchmark runner for pytruenas.

Measures the pure-CPU hot paths hit on every middleware call — extended-JSON
(ejson) encode/decode, API namespace method-name building, and query-filter
construction — with no network or server involved. Produces a comparable JSON
result plus a human summary.

    python benchmarks/run.py            # print summary only
    python benchmarks/run.py --save     # also write benchmarks/results/<name>.json
    python benchmarks/run.py --name foo # custom result name

Each metric is sampled `REPEAT` times (each sample is `inner` iterations) and
reported as min/median/max ms-per-call, so run-to-run noise is visible rather
than averaged away. Counts are fixed so numbers stay comparable across commits.
Requires pytruenas importable (PYTHONPATH=src, or installed).
"""
import argparse
import json
import platform
import statistics
import sys
import timeit
from datetime import datetime, timezone, date, time
from ipaddress import IPv4Interface
from pathlib import Path

import pytruenas
from pytruenas import jsonrpc
from pytruenas.namespace import Namespace
from pytruenas.utils import query as q

EJSON_INNER = 20000
BUILD_INNER = 200000
FILTER_INNER = 50000
REPEAT = 5

# A response row shaped like a real middleware record (user.query element).
PLAIN_ROW = {
    "id": 1, "username": "root", "uid": 0, "gid": 0, "home": "/root",
    "shell": "/usr/bin/zsh", "full_name": "root", "builtin": True,
    "smb": False, "groups": [0, 544, 545], "sshpubkey": None,
    "email": None, "locked": False, "sudo_commands": [],
}
# A payload exercising every extended (ejson) type.
EXT_OBJ = {
    "created": datetime(2026, 7, 19, 3, 42, tzinfo=timezone.utc),
    "day": date(2026, 7, 19),
    "at": time(3, 42, 9),
    "flags": {"a", "b", "c"},
    "net": IPv4Interface("10.7.19.21/24"),
    "nested": [{"created": datetime(2026, 1, 1, tzinfo=timezone.utc)}],
}
PLAIN_JSON = jsonrpc.dumps([PLAIN_ROW] * 20)
EXT_JSON = jsonrpc.dumps(EXT_OBJ)

_client_stub = type("C", (), {"logger": None, "_api": None})()
_ns = Namespace(_client_stub, "pool")


def sample(fn, inner, repeat=REPEAT):
    """Return ms-per-call as min/median/max over `repeat` samples."""
    fn()  # warmup
    per_call = [timeit.timeit(fn, number=inner) / inner * 1000 for _ in range(repeat)]
    return {
        "median_ms": round(statistics.median(per_call), 6),
        "min_ms": round(min(per_call), 6),
        "max_ms": round(max(per_call), 6),
    }


def _build_method_name():
    # client.api.pool.dataset.snapshot -> "pool.dataset.snapshot": build a fresh
    # chain each call to measure the attribute walk + join (not the @cache hit).
    return str(Namespace(_client_stub, "pool").dataset.snapshot)


def measure():
    return {
        "ejson.dumps.plain": sample(lambda: jsonrpc.dumps([PLAIN_ROW] * 20), EJSON_INNER // 4),
        "ejson.loads.plain": sample(lambda: jsonrpc.loads(PLAIN_JSON), EJSON_INNER // 4),
        "ejson.dumps.extended": sample(lambda: jsonrpc.dumps(EXT_OBJ), EJSON_INNER),
        "ejson.loads.extended": sample(lambda: jsonrpc.loads(EXT_JSON), EJSON_INNER),
        "namespace.methodname": sample(_build_method_name, BUILD_INNER // 10),
        "query.filter_from_kwargs": sample(
            lambda: q.filter_from_kwargs(username="root", uid=q.GT(0), locked=False),
            FILTER_INNER,
        ),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Run pytruenas benchmarks")
    ap.add_argument("--save", action="store_true", help="write result to benchmarks/results/")
    ap.add_argument("--name", default=None, help="result name (default pytruenas-<ver>-py<ver>)")
    args = ap.parse_args(argv)

    pyver = f"py{sys.version_info.major}{sys.version_info.minor}"
    name = args.name or f"pytruenas-{pytruenas.__version__}-{pyver}"
    metrics = measure()
    result = {
        "name": name,
        "pytruenas_version": pytruenas.__version__,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "processor": platform.processor() or platform.machine(),
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "iterations": {"ejson_inner": EJSON_INNER, "build_inner": BUILD_INNER,
                       "filter_inner": FILTER_INNER, "repeat": REPEAT},
        "metrics": metrics,
    }

    print("=== pytruenas Benchmark ===")
    print(f"{name}  ({result['python']} on {result['processor']})")
    print(f"{'metric':24s} {'median':>11s} {'min':>11s} {'max':>11s}   (ms/call)")
    for key, m in metrics.items():
        print(f"{key:24s} {m['median_ms']:11.6f} {m['min_ms']:11.6f} {m['max_ms']:11.6f}")

    if args.save:
        dest = Path(__file__).resolve().parent / "results"
        dest.mkdir(parents=True, exist_ok=True)
        out = dest / f"{name}.json"
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(f"saved: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
