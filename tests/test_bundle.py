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


# -- repo mode: collect_repo -------------------------------------------------
#
# The failure mode here is different from the installed-metadata path above:
# not "imports after deployment", but "the copied tree does not match what a
# clone of the repo would actually have" -- either because something ignored
# leaked in, or because something that should survive (a negation) did not.

pytest.importorskip("pathspec")


def test_collect_repo_excludes_gitignored_files(tmp_path):
    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    (repo / ".gitignore").write_text("*.log\n")
    (repo / "src" / "keep.py").write_text("x")
    (repo / "a.log").write_text("x")

    names = {arcname for arcname, _ in bundle.collect_repo(repo)}
    assert "repo/src/keep.py" in names
    assert "repo/a.log" not in names


def test_collect_repo_negation_un_ignores_a_file():
    """The reason this uses pathspec rather than a hand-rolled matcher: a
    later `!pattern` line must be able to override an earlier ignore, and a
    naive "does any pattern match" matcher gets this specific case wrong."""
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        (repo / ".gitignore").write_text("*.log\n!keep.log\n")
        (repo / "a.log").write_text("x")
        (repo / "keep.log").write_text("x")

        names = {arcname for arcname, _ in bundle.collect_repo(repo)}
        assert "repo/keep.log" in names
        assert "repo/a.log" not in names


def test_collect_repo_prunes_ignored_directories_without_descending(tmp_path):
    """A directory-anchored pattern (`.venv*/`) must match the DIRECTORY's own
    path, not just filter its files out one by one after the fact -- this repo's
    own .gitignore uses exactly this pattern for .venv*/."""
    repo = tmp_path / "repo"
    (repo / ".venv3" / "lib").mkdir(parents=True)
    (repo / ".gitignore").write_text(".venv*/\n")
    (repo / ".venv3" / "lib" / "x.py").write_text("y")
    (repo / "src").mkdir()
    (repo / "src" / "ok.py").write_text("z")

    names = {arcname for arcname, _ in bundle.collect_repo(repo)}
    assert names == {"repo/.gitignore", "repo/src/ok.py"}


def test_collect_repo_always_excludes_dot_git(tmp_path):
    """VCS metadata is never "the files a clone would have", regardless of
    what any ignore file does or does not say."""
    repo = tmp_path / "repo"
    (repo / ".git").mkdir(parents=True)
    (repo / ".git" / "HEAD").write_text("ref: refs/heads/main\n")
    (repo / "src.py").write_text("x")

    names = {arcname for arcname, _ in bundle.collect_repo(repo)}
    assert not [n for n in names if ".git/" in n or n.endswith(".git")]
    assert "repo/src.py" in names


def test_collect_repo_ignore_files_selects_a_subset(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".gitignore").write_text("a.txt\n")
    (repo / ".bundleignore").write_text("b.txt\n")
    (repo / "a.txt").write_text("x")
    (repo / "b.txt").write_text("x")
    (repo / "c.txt").write_text("x")

    only_gitignore = {
        n for n, _ in bundle.collect_repo(repo, ignore_files=[".gitignore"])
    }
    assert "repo/a.txt" not in only_gitignore
    assert "repo/b.txt" in only_gitignore  # .bundleignore not selected

    both = {n for n, _ in bundle.collect_repo(repo)}  # default: all three
    assert "repo/a.txt" not in both
    assert "repo/b.txt" not in both
    assert "repo/c.txt" in both


def test_collect_repo_missing_ignore_files_are_silently_skipped(tmp_path):
    """A repo with only .gitignore should not need an override to avoid an
    error for .ignore/.bundleignore it was never going to have."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "x.txt").write_text("x")
    names = {n for n, _ in bundle.collect_repo(repo)}
    assert "repo/x.txt" in names


def test_collect_repo_extra_ignores_layer_after_ignore_files(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".gitignore").write_text("")
    (repo / "secret.txt").write_text("x")
    (repo / "kept.txt").write_text("x")

    names = {
        n for n, _ in bundle.collect_repo(repo, extra_ignores=["secret.txt"])
    }
    assert "repo/secret.txt" not in names
    assert "repo/kept.txt" in names


def test_collect_repo_prefix_overrides_the_default_directory_name(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "f.txt").write_text("x")
    names = {n for n, _ in bundle.collect_repo(repo, prefix="myapp")}
    assert names == {"myapp/f.txt"}


def test_collect_repo_rejects_a_non_directory(tmp_path):
    not_a_dir = tmp_path / "f.txt"
    not_a_dir.write_text("x")
    with pytest.raises(bundle.BundleError, match="not a directory"):
        bundle.collect_repo(not_a_dir)


def test_collect_repo_feeds_a_working_zipapp(tmp_path):
    """The whole point of matching _collect's output shape: build()/export()
    need no changes to accept it."""
    repo = tmp_path / "repo"
    (repo / "pkg").mkdir(parents=True)
    (repo / "pkg" / "__init__.py").write_text("VALUE = 1\n")

    items = bundle.collect_repo(repo)
    target = tmp_path / "out.pyz"
    bundle.build(target, contents=items, package="pkg")

    data = target.read_bytes()
    assert data.startswith(b"#!")
    stripped = tmp_path / "out.zip"
    stripped.write_bytes(data[data.index(b"PK") :])
    with zipfile.ZipFile(stripped) as archive:
        names = set(archive.namelist())
    assert "repo/pkg/__init__.py" in names
    assert "__main__.py" in names


def test_collect_repo_feeds_export(tmp_path):
    repo = tmp_path / "repo"
    (repo / "pkg").mkdir(parents=True)
    (repo / "pkg" / "__init__.py").write_text("VALUE = 1\n")

    items = bundle.collect_repo(repo)
    out = tmp_path / "tree"
    bundle.export(out, contents=items)
    assert (out / "repo" / "pkg" / "__init__.py").is_file()


def test_build_requires_exactly_one_of_distributions_or_contents(tmp_path):
    with pytest.raises(TypeError, match="exactly one"):
        bundle.build(tmp_path / "out.pyz", package="pkg")
    with pytest.raises(TypeError, match="exactly one"):
        bundle.build(tmp_path / "out.pyz", {}, contents=[], package="pkg")


def test_export_requires_exactly_one_of_distributions_or_contents(tmp_path):
    with pytest.raises(TypeError, match="exactly one"):
        bundle.export(tmp_path / "tree")
    with pytest.raises(TypeError, match="exactly one"):
        bundle.export(tmp_path / "tree", {}, contents=[])


def test_build_requires_package_when_using_contents(tmp_path):
    """`package` staying required is the point: a wrong entry point produces
    a bundle that builds and does nothing useful, repo mode included."""
    with pytest.raises(TypeError, match="package"):
        bundle.build(tmp_path / "out.pyz", contents=[])


def test_repo_mode_without_pathspec_raises_a_clear_error(tmp_path, monkeypatch):
    """The 'repo' extra is optional; every other bundling path must keep
    working with nothing extra installed, and a repo-mode call without it
    must fail with a message naming the fix, not an ImportError traceback."""
    import builtins

    real_import = builtins.__import__

    def blocked(name, *a, **k):
        if name == "pathspec":
            raise ImportError("blocked for test")
        return real_import(name, *a, **k)

    monkeypatch.setattr(builtins, "__import__", blocked)
    (tmp_path / "f.txt").write_text("x")
    with pytest.raises(bundle.BundleError, match="repo.*extra"):
        bundle.collect_repo(tmp_path)


# -- repo mode: repo_requirements --------------------------------------------


def test_repo_requirements_reads_pyproject_dependencies(tmp_path):
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "x"\ndependencies = ["requests>=2.0", "click"]\n'
    )
    names = bundle.repo_requirements(tmp_path)
    assert set(names) == {"requests", "click"}


def test_repo_requirements_extras_are_excluded_unless_asked_for(tmp_path):
    """Mirrors requirements()'s own extras contract (test_extras_are_excluded_
    unless_asked_for above): an extra nobody requested must not silently
    enlarge the result."""
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "x"\ndependencies = ["requests"]\n'
        '[project.optional-dependencies]\nssh = ["asyncssh"]\n'
    )
    core = bundle.repo_requirements(tmp_path)
    assert "asyncssh" not in core
    with_ssh = bundle.repo_requirements(tmp_path, extras=("ssh",))
    assert "asyncssh" in with_ssh


def test_repo_requirements_falls_back_to_requirements_txt(tmp_path):
    (tmp_path / "requirements.txt").write_text(
        "requests>=2.0\n# a comment\n\n-e ./local\nclick\n"
    )
    assert set(bundle.repo_requirements(tmp_path)) == {"requests", "click"}


def test_repo_requirements_prefers_pyproject_over_requirements_txt(tmp_path):
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "x"\ndependencies = ["fromtoml"]\n'
    )
    (tmp_path / "requirements.txt").write_text("fromtxt\n")
    assert bundle.repo_requirements(tmp_path) == ["fromtoml"]


def test_repo_requirements_raises_when_neither_file_exists(tmp_path):
    with pytest.raises(bundle.BundleError, match="pyproject.toml or requirements.txt"):
        bundle.repo_requirements(tmp_path)


def test_repo_requirements_include_bare_name_is_a_dependency(tmp_path):
    (tmp_path / "requirements.txt").write_text("requests\n")
    result = bundle.repo_requirements(tmp_path, include=["extra-dep"])
    assert "extra-dep" in result
    assert "requests" in result


def test_repo_requirements_include_bracketed_name_is_an_extra(tmp_path):
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "x"\ndependencies = []\n'
        '[project.optional-dependencies]\nssh = ["asyncssh"]\n'
    )
    result = bundle.repo_requirements(tmp_path, include=["[ssh]"])
    assert "asyncssh" in result


def test_repo_requirements_exclude_wins_over_include(tmp_path):
    """An explicit 'never ship this' must not be silently overridable by an
    equally explicit 'ship this' naming the same thing."""
    (tmp_path / "requirements.txt").write_text("requests\n")
    result = bundle.repo_requirements(
        tmp_path, include=["requests"], exclude=["requests"]
    )
    assert "requests" not in result


def test_repo_requirements_exclude_removes_an_already_declared_dependency(tmp_path):
    (tmp_path / "requirements.txt").write_text("requests\nclick\n")
    result = bundle.repo_requirements(tmp_path, exclude=["requests"])
    assert result == ["click"]


def test_repo_requirements_exclude_bracketed_extra(tmp_path):
    """An excluded extra's OWN dependencies are removed even though the extra
    itself was never requested via `extras=` -- exclude reasons about names,
    not about which extras were turned on."""
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "x"\ndependencies = ["requests", "asyncssh"]\n'
        '[project.optional-dependencies]\nssh = ["asyncssh"]\n'
    )
    result = bundle.repo_requirements(tmp_path, exclude=["[ssh]"])
    assert "asyncssh" not in result
    assert "requests" in result


def test_repo_requirements_deduplicates(tmp_path):
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "x"\ndependencies = ["requests"]\n'
        '[project.optional-dependencies]\nssh = ["requests"]\n'
    )
    result = bundle.repo_requirements(tmp_path, extras=("ssh",))
    assert result.count("requests") == 1


def test_repo_requirements_missing_toml_parser_raises_a_clear_error(
    tmp_path, monkeypatch
):
    """A repo with a pyproject.toml but no TOML parser available (< 3.11,
    'repo' extra not installed) must fail with a message naming the fix, not
    a bare ImportError."""
    import builtins

    real_import = builtins.__import__

    def blocked(name, *a, **k):
        if name in ("tomllib", "tomli"):
            raise ImportError("blocked for test")
        return real_import(name, *a, **k)

    monkeypatch.setattr(builtins, "__import__", blocked)
    (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = []\n')
    with pytest.raises(bundle.BundleError, match="TOML parser"):
        bundle.repo_requirements(tmp_path)
