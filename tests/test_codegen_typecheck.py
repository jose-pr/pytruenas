"""Generated stubs pass a real type checker, and so do the calls they promise.

Generates the stubs for ``fixtures/api_min.json`` and for every unusual shape in
``test_codegen_fidelity.EDGE_SHAPES``, then runs pyright (3.9 and 3.14 targets)
and mypy (3.10, its lowest, and 3.14) over them and a consumer module. The
consumer's valid calls must check clean and each line marked ``# E`` must be
reported. A checker that is not installed skips its tests, saying so.
"""

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import pytruenas
from pytruenas import codegen

from test_codegen_fidelity import EDGE_SHAPES, edge_dump

pytestmark = pytest.mark.requires("jinja2")

FIXTURE = Path(__file__).parent / "fixtures" / "api_min.json"

#: The directory that holds the `pytruenas` package under test, so a checker
#: resolves it rather than whichever copy the environment has installed.
SOURCE = Path(pytruenas.__file__).resolve().parent.parent

CONSUMER = """\
from truenasapi_typings.current import Current

from pytruenas import TrueNASClient


def valid(client: "TrueNASClient[Current]") -> None:
    client.api.user.query()
    client.api.user.query([], {"limit": 1})
    client.api.user.query(_timeout=5.0, _retries=2)
    client.api.user.create({"username": "svc"})
    client.api.user._create(username="svc", full_name="Service")
    client.api.user._update(1, full_name="x")
    client.api.user._upsert(1, shell="/bin/sh")
    client.api.user._get(username="svc")
    client.api.system.info()


def invalid(client: "TrueNASClient[Current]") -> None:
    client.api.user._update(1, no_such_field="x")  # E
    client.api.user._create(full_name="no username")  # E
    client.api.user.query([], {"limit": "1"})  # E
    client.api.user.query([], [], True)  # E
    client.api.system.info("unexpected")  # E
"""


@pytest.fixture(scope="module")
def project(tmp_path_factory):
    """A directory holding the generated trees and the consumer module."""
    root = tmp_path_factory.mktemp("typecheck")
    api = json.loads(FIXTURE.read_text(encoding="utf-8"))["versions"][0]
    codegen.Codegen().generate(api, root / "truenasapi_typings" / "current")
    for label in EDGE_SHAPES:
        codegen.Codegen().generate(edge_dump(label), root / "shapes" / label)
    (root / "consumer.py").write_text(CONSUMER, encoding="utf-8")
    return root


def _expected(root: Path) -> "set[tuple[str, int]]":
    lines = (root / "consumer.py").read_text(encoding="utf-8").splitlines()
    return {("consumer.py", n) for n, line in enumerate(lines, 1) if "# E" in line}


def _report(errors: "list[tuple[str, int, str]]") -> str:
    return "\n".join(f"{path}:{line}: {message}" for path, line, message in errors)


def _assert_only_expected(root: Path, errors: "list[tuple[str, int, str]]") -> None:
    found = {(path, line) for path, line, _ in errors}
    assert found == _expected(root), _report(errors)


# -- pyright ---------------------------------------------------------------


def _pyright() -> "list[str]":
    if importlib.util.find_spec("pyright") is not None:
        command = [sys.executable, "-m", "pyright"]
    elif shutil.which("pyright"):
        command = [shutil.which("pyright")]
    else:
        pytest.skip("pyright is not installed (pip install pyright)")
    probe = subprocess.run(
        [*command, "--version"], capture_output=True, text=True, timeout=600
    )
    if probe.returncode != 0:
        pytest.skip(f"pyright cannot run: {(probe.stderr or probe.stdout).strip()}")
    return command


@pytest.mark.parametrize("target", ["3.9", "3.14"])
def test_pyright_accepts_the_stubs_and_checks_calls(project, target):
    command = _pyright()
    config = {
        "include": ["truenasapi_typings", "shapes", "consumer.py"],
        "extraPaths": [str(SOURCE)],
        "typeCheckingMode": "standard",
    }
    (project / "pyrightconfig.json").write_text(json.dumps(config), encoding="utf-8")
    run = subprocess.run(
        [
            *command,
            "--outputjson",
            "--pythonpath",
            sys.executable,
            "--pythonversion",
            target,
        ],
        cwd=project,
        capture_output=True,
        text=True,
        timeout=600,
    )
    try:
        report = json.loads(run.stdout)
    except ValueError:
        pytest.fail(f"pyright gave no report: {run.stdout}{run.stderr}")
    errors = [
        (
            Path(d["file"]).resolve().relative_to(project.resolve()).as_posix(),
            d["range"]["start"]["line"] + 1,
            d["message"],
        )
        for d in report["generalDiagnostics"]
        if d["severity"] == "error"
    ]
    _assert_only_expected(project, errors)


# -- mypy ------------------------------------------------------------------

_MYPY_LINE = re.compile(r"^(?P<path>.+?):(?P<line>\d+): error: (?P<msg>.*)$")


@pytest.mark.parametrize("target", ["3.10", "3.14"])
def test_mypy_accepts_the_stubs_and_checks_calls(project, target, tmp_path):
    if importlib.util.find_spec("mypy") is None:
        pytest.skip("mypy is not installed (pip install mypy)")
    run = subprocess.run(
        [
            sys.executable,
            "-m",
            "mypy",
            "--python-version",
            target,
            "--explicit-package-bases",
            "--follow-imports=silent",
            "--no-error-summary",
            "--hide-error-context",
            "--cache-dir",
            str(tmp_path / "cache"),
            "truenasapi_typings",
            "shapes",
            "consumer.py",
        ],
        cwd=project,
        capture_output=True,
        text=True,
        timeout=600,
        env={**os.environ, "MYPYPATH": str(SOURCE)},
    )
    if run.returncode not in (0, 1):
        if "is not supported" in run.stderr + run.stdout:
            pytest.skip(f"this mypy cannot target {target}")
        pytest.fail(f"mypy did not run: {run.stdout}{run.stderr}")
    errors = []
    for line in run.stdout.splitlines():
        match = _MYPY_LINE.match(line)
        if match:
            path = Path(match["path"]).as_posix()
            errors.append((path, int(match["line"]), match["msg"]))
    _assert_only_expected(project, errors)
