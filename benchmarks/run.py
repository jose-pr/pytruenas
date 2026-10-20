#!/usr/bin/env python3
"""Structured benchmark runner for pytruenas.

Measures the pure-CPU hot paths hit on every middleware call — extended-JSON
(ejson) encode/decode, API namespace method-name building, and query-filter
construction — with no network or server involved. Produces a comparable JSON
result plus a human summary.

    python benchmarks/run.py                   # print summary only
    python benchmarks/run.py --save            # also write benchmarks/results/<name>.json
    python benchmarks/run.py --name foo        # custom result name
    python benchmarks/run.py --compare B.json  # each median as a ratio to result B

Each metric is sampled `REPEAT` times (each sample is `inner` iterations) and
reported as min/median/max ms-per-call, so run-to-run noise is visible rather
than averaged away. Counts are fixed so numbers stay comparable across commits.
Requires pytruenas importable (PYTHONPATH=src, or installed); the result
describes whichever pytruenas that import finds.
"""

import argparse
import json
import platform
import statistics
import sys
import sysconfig
import timeit
from datetime import datetime, timezone, date, time
from ipaddress import IPv4Interface
from pathlib import Path

import pytruenas
from pytruenas import connection as ejson
from pytruenas.namespace import Namespace

# The script also measures the latest release, which may predate the move of
# `query` out of `pytruenas.utils`.
try:
    from pytruenas import query as q
except ImportError:
    from pytruenas.utils import query as q

EJSON_INNER = 20000
BUILD_INNER = 200000
FILTER_INNER = 50000
REPEAT = 5

# A response row shaped like a real middleware record (user.query element).
PLAIN_ROW = {
    "id": 1,
    "username": "root",
    "uid": 0,
    "gid": 0,
    "home": "/root",
    "shell": "/usr/bin/zsh",
    "full_name": "root",
    "builtin": True,
    "smb": False,
    "groups": [0, 544, 545],
    "sshpubkey": None,
    "email": None,
    "locked": False,
    "sudo_commands": [],
}
# A payload exercising every extended (ejson) type.
EXT_OBJ = {
    "created": datetime(2026, 7, 19, 3, 42, tzinfo=timezone.utc),
    "day": date(2026, 7, 19),
    "at": time(3, 42, 9),
    "flags": {"a", "b", "c"},
    "net": IPv4Interface("192.0.2.21/24"),
    "nested": [{"created": datetime(2026, 1, 1, tzinfo=timezone.utc)}],
}
PLAIN_JSON = ejson.dumps([PLAIN_ROW] * 20)
EXT_JSON = ejson.dumps(EXT_OBJ)

_client_stub = type("C", (), {"logger": None, "_api": None})()
_ns = Namespace(_client_stub, "pool")


def sample(fn, inner, repeat=REPEAT):
    """Return ms-per-call as min/median/max over `repeat` samples."""
    fn()  # warmup
    per_call = [
        t / inner * 1000 for t in timeit.repeat(fn, number=inner, repeat=repeat)
    ]
    return {
        "median_ms": round(statistics.median(per_call), 6),
        "min_ms": round(min(per_call), 6),
        "max_ms": round(max(per_call), 6),
    }


def _build_method_name():
    # client.api.pool.dataset.snapshot -> "pool.dataset.snapshot": build a fresh
    # chain each call to measure the attribute walk + join, not a hit in the
    # namespace's child cache.
    return str(Namespace(_client_stub, "pool").dataset.snapshot)


def measure():
    return {
        "ejson.dumps.plain": sample(
            lambda: ejson.dumps([PLAIN_ROW] * 20), EJSON_INNER // 4
        ),
        "ejson.loads.plain": sample(lambda: ejson.loads(PLAIN_JSON), EJSON_INNER // 4),
        "ejson.dumps.extended": sample(lambda: ejson.dumps(EXT_OBJ), EJSON_INNER),
        "ejson.loads.extended": sample(lambda: ejson.loads(EXT_JSON), EJSON_INNER),
        "namespace.methodname": sample(_build_method_name, BUILD_INNER // 10),
        "query.filter_from_kwargs": sample(
            lambda: q.filter_from_kwargs(username="root", uid=q.GT(0), locked=False),
            FILTER_INNER,
        ),
    }


def default_name():
    """`pytruenas-<version>-py<XY>-<platform tag>`: one file per release,
    interpreter and kind of machine, so no result overwrites another's."""
    pyver = f"py{sys.version_info.major}{sys.version_info.minor}"
    tag = sysconfig.get_platform().replace(".", "_")
    return f"pytruenas-{pytruenas.__version__}-{pyver}-{tag}"


def compare(baseline, metrics):
    """Print each metric's median as a ratio to `baseline`, a saved result;
    above 1.0 is slower than the baseline."""
    print(f"against {baseline['name']} ({baseline['pytruenas_version']}):")
    for key, m in metrics.items():
        base = baseline["metrics"].get(key)
        if base:
            print(f"{key:24s} {m['median_ms'] / base['median_ms']:10.3f}x")
        else:
            print(f"{key:24s} (not in the baseline)")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Run pytruenas benchmarks")
    ap.add_argument(
        "--save", action="store_true", help="write the result to --results-dir"
    )
    ap.add_argument(
        "--name",
        default=None,
        help="result name (default pytruenas-<ver>-py<XY>-<platform tag>)",
    )
    ap.add_argument(
        "--results-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "results",
        help="where --save writes (default benchmarks/results/)",
    )
    ap.add_argument(
        "--compare",
        type=Path,
        default=None,
        metavar="RESULT",
        help="a saved result to report each median against, as a ratio",
    )
    args = ap.parse_args(argv)

    name = args.name or default_name()
    metrics = measure()
    result = {
        "name": name,
        "pytruenas_version": pytruenas.__version__,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "platform_tag": sysconfig.get_platform(),
        "processor": platform.processor() or platform.machine(),
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "iterations": {
            "ejson_inner": EJSON_INNER,
            "build_inner": BUILD_INNER,
            "filter_inner": FILTER_INNER,
            "repeat": REPEAT,
        },
        "metrics": metrics,
    }

    print("=== pytruenas Benchmark ===")
    print(f"{name}  ({result['python']} on {result['processor']})")
    print(f"{'metric':24s} {'median':>11s} {'min':>11s} {'max':>11s}   (ms/call)")
    for key, m in metrics.items():
        print(
            f"{key:24s} {m['median_ms']:11.6f} {m['min_ms']:11.6f} {m['max_ms']:11.6f}"
        )

    if args.compare:
        compare(json.loads(args.compare.read_bytes()), metrics)

    if args.save:
        args.results_dir.mkdir(parents=True, exist_ok=True)
        out = args.results_dir / f"{name}.json"
        # Bytes: results are committed, and write_text would make them CRLF
        # on Windows.
        text = json.dumps(result, indent=2, sort_keys=True) + "\n"
        out.write_bytes(text.encode("utf-8"))
        print(f"saved: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
