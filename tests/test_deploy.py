"""``deploy``'s ``--source repo`` axis: CLI wiring, PYTHONPATH detection, and
the pyz/repo combination that cannot work.

The failure mode this guards against is the same shape as ``test_bundle.py``'s:
a deploy that builds and runs the `tar -xf`/launcher-write pipeline
successfully and then does not IMPORT on the target, because the launcher's
PYTHONPATH does not point at wherever the repo's package actually lives.
"""

import logging
from unittest.mock import patch

import pytest

import pytruenas.cmd.deploy as deploy_cmd
import pytruenas.main as main
from pytruenas.utils.bundle import BundleError


def _logger():
    logger = logging.getLogger("test-deploy")
    logger.addHandler(logging.NullHandler())
    return logger


def _parse(argv):
    captured = {}

    def fake_dispatch(command, instance):
        captured["args"] = instance
        captured["targets"] = instance._expanded_targets_()
        return 0

    with patch.object(main, "_dispatch", fake_dispatch):
        main.main("pytruenas", argv)
    return captured


# -- CLI parsing --------------------------------------------------------


def test_source_defaults_to_installed():
    c = _parse(["deploy", "nas1"])
    assert c["args"].source == "installed"


def test_source_repo_is_accepted():
    c = _parse(["deploy", "--source", "repo", "nas1"])
    assert c["args"].source == "repo"


def test_repo_root_defaults_to_current_directory():
    c = _parse(["deploy", "nas1"])
    assert c["args"].repo_root == "."


def test_include_exclude_ignore_flags_are_repeatable():
    c = _parse(
        [
            "deploy",
            "--include",
            "requests",
            "--include",
            "[ssh]",
            "--exclude",
            "click",
            "--ignore-file",
            ".gitignore",
            "--ignore-pattern",
            "*.log",
            "--pythonpath",
            "src",
            "nas1",
        ]
    )
    args = c["args"]
    assert args.include == ["requests", "[ssh]"]
    assert args.exclude == ["click"]
    assert args.ignore_files == [".gitignore"]
    assert args.ignore_pattern == ["*.log"]
    assert args.pythonpath == ["src"]


def test_targets_still_trail_after_the_new_flags():
    """The new flags must not swallow the trailing TARGET positional --
    see AGENTS.md's note on greedy list options and register_targets."""
    c = _parse(["deploy", "--source", "repo", "nas1", "nas2"])
    assert c["targets"] == ["nas1", "nas2"]


def test_mode_choices_are_unchanged():
    """--mode still only accepts pyz/dir -- 'repo' belongs to --source, not
    --mode; see the CLI-wiring design note in the module docstring."""
    with pytest.raises(SystemExit):
        _parse(["deploy", "--mode", "repo", "nas1"])


# -- _detect_pythonpath ---------------------------------------------------


def test_detect_pythonpath_finds_src_layout(tmp_path):
    (tmp_path / "src" / "pkg").mkdir(parents=True)
    (tmp_path / "src" / "pkg" / "__init__.py").write_text("")
    assert deploy_cmd._detect_pythonpath(tmp_path, "pkg") == ["src"]


def test_detect_pythonpath_finds_flat_layout(tmp_path):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "__init__.py").write_text("")
    assert deploy_cmd._detect_pythonpath(tmp_path, "pkg") == [""]


def test_detect_pythonpath_finds_a_single_module_file(tmp_path):
    """A single-file module (pkg.py), not a package directory."""
    (tmp_path / "lib").mkdir()
    (tmp_path / "lib" / "pkg.py").write_text("")
    assert deploy_cmd._detect_pythonpath(tmp_path, "pkg") == ["lib"]


def test_detect_pythonpath_returns_every_match():
    """A repo vendoring under lib/ while its own code lives in src/ needs
    both on PYTHONPATH -- taking only the first hit would silently drop one."""
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for base in ("src", "lib"):
            (root / base / "pkg").mkdir(parents=True)
            (root / base / "pkg" / "__init__.py").write_text("")
        assert deploy_cmd._detect_pythonpath(root, "pkg") == ["src", "lib"]


def test_detect_pythonpath_finds_nothing(tmp_path):
    assert deploy_cmd._detect_pythonpath(tmp_path, "pkg") == []


# -- _repo_contents ---------------------------------------------------------


def _args(**overrides):
    args = deploy_cmd.Args()
    for key, value in {
        "repo_root": ".",
        "ignore_files": [],
        "ignore_pattern": [],
        "extras": [],
        "include": [],
        "exclude": [],
        "pythonpath": [],
    }.items():
        setattr(args, key, overrides.get(key, value))
    return args


def test_repo_contents_detects_pythonpath_automatically(tmp_path):
    (tmp_path / "src" / "pkg").mkdir(parents=True)
    (tmp_path / "src" / "pkg" / "__init__.py").write_text("X = 1\n")

    contents, pythonpath = deploy_cmd._repo_contents(
        _args(repo_root=str(tmp_path)), "pkg", _logger()
    )
    assert pythonpath == ["src"]
    names = [a for a, _ in contents]
    assert any(n.endswith("src/pkg/__init__.py") for n in names)


def test_repo_contents_explicit_pythonpath_overrides_detection(tmp_path):
    (tmp_path / "src" / "pkg").mkdir(parents=True)
    (tmp_path / "src" / "pkg" / "__init__.py").write_text("")
    (tmp_path / "custom").mkdir()

    _, pythonpath = deploy_cmd._repo_contents(
        _args(repo_root=str(tmp_path), pythonpath=["custom"]), "pkg", _logger()
    )
    assert pythonpath == ["custom"]


def test_repo_contents_raises_when_package_cannot_be_found(tmp_path):
    (tmp_path / "unrelated.txt").write_text("x")
    with pytest.raises(BundleError, match="could not find"):
        deploy_cmd._repo_contents(
            _args(repo_root=str(tmp_path)), "nosuchpkg", _logger()
        )


def test_repo_contents_survives_a_repo_with_no_declared_dependencies(tmp_path):
    """Advisory logging must not turn into a hard failure for a repo with
    neither pyproject.toml nor requirements.txt -- copying the tree is the
    only thing this mode promises to do."""
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "__init__.py").write_text("")
    contents, _ = deploy_cmd._repo_contents(
        _args(repo_root=str(tmp_path)), "pkg", _logger()
    )
    assert contents


# -- --source repo + --mode pyz is rejected ---------------------------------


def test_source_repo_rejects_mode_pyz():
    args = deploy_cmd.Args()
    args.source = "repo"
    args.mode = "pyz"
    with pytest.raises(BundleError, match="does not support --mode pyz"):
        deploy_cmd.run(None, args, _logger())


def test_source_repo_mode_pyz_never_touches_the_client():
    """The rejection must happen before any client interaction -- a caller
    should not need a reachable target to find out the combination is invalid."""
    args = deploy_cmd.Args()
    args.source = "repo"
    args.mode = "pyz"
    sentinel = object()  # anything -- if this is touched, it will AttributeError
    with pytest.raises(BundleError):
        deploy_cmd.run(sentinel, args, _logger())


# -- end-to-end: --source repo --mode dir against a fake client -------------


class _FakePath:
    def __init__(self, path, store):
        self.path = path
        self.store = store

    def exists(self):
        return self.path in self.store

    def mkdir(self, **_kwargs):
        pass

    def write_bytes(self, data):
        self.store[self.path] = data


class _FakeResult:
    returncode = 0
    stdout = ""  # `_probe` reads this for --source installed's PROBE_SOURCE call


class _FakeClient:
    def __init__(self):
        self.store = {}
        self.ran = []

    def path(self, path):
        return _FakePath(path, self.store)

    def run(self, cmd, **_kwargs):
        self.ran.append(cmd)
        return _FakeResult()


def test_source_repo_mode_dir_deploys_a_working_launcher(tmp_path):
    (tmp_path / "src" / "pkg").mkdir(parents=True)
    (tmp_path / "src" / "pkg" / "__init__.py").write_text("X = 1\n")

    args = deploy_cmd.Args()
    args.source = "repo"
    args.mode = "dir"
    args.repo_root = str(tmp_path)
    args.pkg_root = "pkg"
    args.pkg_name = "pkg"
    args.force = True

    client = _FakeClient()
    rc = deploy_cmd.run(client, args, _logger())
    assert rc == 0

    import io
    import tarfile

    payload = client.store["/var/db/system/pytruenas.incoming.tar"]
    tf = tarfile.open(fileobj=io.BytesIO(payload))
    [launcher_name] = [n for n in tf.getnames() if n.endswith("bin/pkg")]
    launcher = tf.extractfile(launcher_name).read().decode()
    repo_name = tmp_path.name
    assert f"lib/{repo_name}/src" in launcher
    assert tf.getmember(launcher_name).mode & 0o111, "launcher is not executable"


def test_source_installed_path_never_calls_repo_contents(monkeypatch):
    """The default axis must behave exactly as before -- --source repo's
    machinery (pythonpath detection, collect_repo) must not run at all.

    Patches `_repo_contents` itself rather than driving `run()` all the way
    through a real dependency-closure build: that closure depends on what
    happens to be installed in the environment running this test (e.g.
    `charset-normalizer`'s compiled extension, which `bundle.build` correctly
    refuses -- exactly what `test_bundle.py`'s own `TRUENAS_HAS` fixture
    exists to route around), which is irrelevant to what this test checks.
    """

    def _boom(*_a, **_k):
        raise AssertionError("_repo_contents must not run for --source installed")

    monkeypatch.setattr(deploy_cmd, "_repo_contents", _boom)

    args = deploy_cmd.Args()  # source defaults to "installed"
    assert args.source == "installed"
    # Calling run() this far would need a real target; asserting the branch
    # taken is enough -- see `test_source_repo_rejects_mode_pyz` above for
    # the same "check the guard without needing a client" shape.
    monkeypatch.setattr(
        deploy_cmd,
        "_probe",
        lambda client, logger: (_ for _ in ()).throw(
            AssertionError("stop: reached the installed path, as expected")
        ),
    )
    with pytest.raises(AssertionError, match="reached the installed path"):
        deploy_cmd.run(_FakeClient(), args, _logger())
