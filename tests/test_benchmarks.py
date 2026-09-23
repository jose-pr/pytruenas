"""The benchmark runner must stay runnable.

It imported `pytruenas.jsonrpc`, removed in 0.2.0, so it had been dead since --
including its CI job, which nothing noticed because benchmarks run on demand.
Importing it here is what makes that visible.
"""

import ast
from pathlib import Path

RUNNER = Path(__file__).resolve().parent.parent / "benchmarks" / "run.py"


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
