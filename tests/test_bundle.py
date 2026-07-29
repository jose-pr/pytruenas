"""Bundling for deployment: what goes in, and what must never silently not.

The failure mode this guards against is a bundle that *builds* and then cannot
import on the target -- every bug found while getting this working was of that
shape, and none of them raised locally.
"""

import zipfile

import pytest

from pytruenas.utils import bundle

#: What a real TrueNAS 26.0 reports (verified live). Tests bundle against this
#: rather than the whole closure, because that is what the command actually
#: builds -- and because some of what TrueNAS already provides is NOT
#: bundleable: `charset-normalizer` ships a mypyc-compiled `.pyd`, which the
#: native-extension guard rightly refuses. Building the full closure would
#: therefore fail for a reason deployment never encounters.
TRUENAS_HAS = [
    "certifi",
    "charset-normalizer",
    "dnspython",
    "idna",
    "requests",
    "urllib3",
    "websocket-client",
]


@pytest.fixture
def deployable():
    """The distributions a real deploy to TrueNAS would actually bundle."""
    return bundle.missing_on(TRUENAS_HAS, "pytruenas")


def test_closure_is_transitive_and_includes_the_root():
    """Declared metadata, not an import scan -- see the module docstring."""
    found = bundle.requirements("pytruenas")
    assert "pytruenas" in found
    # Direct dependencies.
    for name in ("duho", "hostctl", "netimps", "pathlib-next"):
        assert name in found, f"{name} missing from the closure"
    # Transitive: these are required by requests/netimps, not by pytruenas.
    for name in ("certifi", "urllib3", "idna"):
        assert name in found, f"{name} (transitive) missing from the closure"


def test_extras_are_excluded_unless_asked_for():
    """An extra nobody requested must not silently enlarge the payload."""
    core = bundle.requirements("pytruenas")
    assert "asyncssh" not in core
    with_ssh = bundle.requirements("pytruenas", extras=("ssh",))
    assert "asyncssh" in with_ssh


def test_missing_on_subtracts_what_the_target_has():
    """The whole point of probing: ship only the difference."""
    missing = bundle.missing_on(TRUENAS_HAS, "pytruenas")
    assert set(missing) == {"duho", "hostctl", "netimps", "pathlib-next", "pytruenas"}


def test_missing_on_normalizes_names():
    """`pathlib_next` and `pathlib-next` are one distribution."""
    assert "pathlib-next" not in bundle.missing_on(["pathlib_next"], "pytruenas")


def test_skip_excludes_even_when_the_target_lacks_it():
    missing = bundle.missing_on([], "pytruenas", skip=["hostctl"])
    assert "hostctl" not in missing
    assert "pytruenas" in missing


def test_built_zipapp_contains_importable_packages(tmp_path, deployable):
    """A bundle whose packages cannot be imported is the bug to prevent.

    `pytruenas` once shipped as a lone README.md -- the archive built fine and
    failed with ModuleNotFoundError only once deployed.
    """
    target = tmp_path / "b.pyz"
    bundle.build(target, deployable, package="pytruenas")

    data = target.read_bytes()
    assert data.startswith(b"#!"), "shebang missing; not directly executable"
    stripped = tmp_path / "b.zip"
    stripped.write_bytes(data[data.index(b"PK") :])

    with zipfile.ZipFile(stripped) as archive:
        names = set(archive.namelist())

    assert "__main__.py" in names
    for package in ("pytruenas", "duho", "hostctl"):
        assert f"{package}/__init__.py" in names, f"{package} is not importable"


def test_bundle_includes_cmd_subpackage_with_its_init(tmp_path, deployable):
    """`zipimport` does not support namespace packages.

    Without `pytruenas/cmd/__init__.py` the deployed app imports cleanly and
    then offers no commands at all, which reads like a discovery bug rather
    than a packaging one.
    """
    target = tmp_path / "b.pyz"
    bundle.build(target, deployable, package="pytruenas")
    data = target.read_bytes()
    stripped = tmp_path / "b.zip"
    stripped.write_bytes(data[data.index(b"PK") :])

    with zipfile.ZipFile(stripped) as archive:
        names = set(archive.namelist())

    assert "pytruenas/cmd/__init__.py" in names
    assert "pytruenas/cmd/call.py" in names


def test_bundle_excludes_caches_and_compiled_artifacts(tmp_path, deployable):
    """`__pycache__` is per-interpreter, so it is dead weight at best."""
    target = tmp_path / "b.pyz"
    bundle.build(target, deployable, package="pytruenas")
    data = target.read_bytes()
    stripped = tmp_path / "b.zip"
    stripped.write_bytes(data[data.index(b"PK") :])

    with zipfile.ZipFile(stripped) as archive:
        names = archive.namelist()

    assert not [n for n in names if "__pycache__" in n]
    assert not [n for n in names if n.endswith((".pyc", ".pyo"))]


def test_export_writes_an_importable_tree(tmp_path, deployable):
    """`dir` mode ships the same file set, unpacked."""
    root = tmp_path / "lib"
    bundle.export(root, deployable)
    for package in ("pytruenas", "duho", "hostctl"):
        assert (root / package / "__init__.py").is_file()
    assert (root / "pytruenas" / "cmd" / "__init__.py").is_file()


def test_probe_source_is_stdlib_only_and_runs(tmp_path):
    """It executes on the target BEFORE anything has been installed there."""
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "-"],
        input=bundle.PROBE_SOURCE,
        capture_output=True,
        text=True,
        check=True,
    )
    reported = {line.strip() for line in result.stdout.splitlines() if line.strip()}
    assert "pytruenas" in reported
    # Normalized, so the caller can diff without further massaging.
    assert not [name for name in reported if name != name.lower() or "_" in name]


def test_data_only_distribution_is_refused(tmp_path, monkeypatch):
    """Fail at build time, where the cause is still visible."""

    class _DataOnly:
        def __init__(self, path):
            self._path = path / "fake-1.0.dist-info"

    readme = tmp_path / "README.md"
    readme.write_text("not a module")
    fake = _DataOnly(tmp_path)

    monkeypatch.setattr(bundle, "_top_level_paths", lambda dist: [readme])
    with pytest.raises(bundle.BundleError, match="data files only"):
        bundle.build(tmp_path / "out.pyz", {"fake": fake}, package="fake")


def test_native_extension_is_refused(tmp_path, monkeypatch):
    """A .so built here will not load on the appliance."""
    package = tmp_path / "native"
    package.mkdir()
    (package / "__init__.py").write_text("")
    (package / "_speedup.so").write_bytes(b"\x7fELF")

    monkeypatch.setattr(bundle, "_top_level_paths", lambda dist: [package])
    with pytest.raises(bundle.BundleError, match="compiled extension"):
        bundle.build(tmp_path / "out.pyz", {"native": object()}, package="native")
