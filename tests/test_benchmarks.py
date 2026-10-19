"""The benchmark runner must stay runnable, and its results comparable.

Benchmarks run on demand, never on every push, so nothing else notices a
runner that no longer imports against the package it measures.
"""

import ast
import json
from pathlib import Path

import pytest

import pytruenas

RUNNER = Path(__file__).resolve().parent.parent / "benchmarks" / "run.py"

# The sdist ships tests/ but not benchmarks/.
pytestmark = pytest.mark.skipif(
    not RUNNER.is_file(), reason="benchmarks/ is not in this tree (an sdist)"
)


def _module():
    """The runner's namespace, imported but not run: a real run takes seconds
    and measures nothing meaningful under a test runner."""
    namespace = {"__name__": "benchmarks_run_probe", "__file__": str(RUNNER)}
    source = RUNNER.read_text(encoding="utf-8")
    exec(compile(source, str(RUNNER), "exec"), namespace)  # noqa: S102
    return namespace


def _metric_names() -> "set[str]":
    """The keys of the dict `measure()` returns, read without running it."""
    tree = ast.parse(RUNNER.read_text(encoding="utf-8"))
    measure = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "measure"
    )
    return {
        key.value
        for node in ast.walk(measure)
        if isinstance(node, ast.Dict)
        for key in node.keys
        if isinstance(key, ast.Constant) and isinstance(key.value, str)
    }


def test_the_runner_imports():
    namespace = _module()
    assert callable(namespace["main"]) and callable(namespace["measure"])


def test_every_metric_is_documented():
    """A renamed metric silently breaks comparison with the tracked baselines
    in benchmarks/results/, so the README has to name each one."""
    readme = (RUNNER.parent / "README.md").read_text(encoding="utf-8")
    names = _metric_names()
    assert names, "no metric names found in measure()"
    missing = sorted(name for name in names if f"`{name}`" not in readme)
    assert not missing, f"undocumented metrics: {missing}"


def _stub_metrics(median=1.0):
    return {
        "ejson.dumps.plain": {"median_ms": median, "min_ms": median, "max_ms": median}
    }


def test_a_saved_result_is_lf_and_named_for_its_release(tmp_path):
    """Results are committed; a CRLF file or one without the version in its
    name cannot be compared release to release."""
    namespace = _module()
    namespace["measure"] = _stub_metrics
    assert namespace["main"](["--save", "--results-dir", str(tmp_path)]) == 0
    (saved,) = tmp_path.glob("*.json")
    assert saved.name.startswith(f"pytruenas-{pytruenas.__version__}-py")
    assert b"\r\n" not in saved.read_bytes()
    assert json.loads(saved.read_bytes())["platform_tag"]


def test_compare_prints_each_median_as_a_ratio(tmp_path, capsys):
    baseline = tmp_path / "baseline.json"
    baseline.write_bytes(
        json.dumps(
            {"name": "base", "pytruenas_version": "0", "metrics": _stub_metrics(2.0)}
        ).encode()
    )
    namespace = _module()
    namespace["measure"] = _stub_metrics
    assert namespace["main"](["--compare", str(baseline)]) == 0
    assert "0.500x" in capsys.readouterr().out
