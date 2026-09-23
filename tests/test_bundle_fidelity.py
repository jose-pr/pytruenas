"""What actually lands on the target: the closure, and the repo tree.

A wrong payload is discovered late -- on the appliance, at import time -- so
each of these is checked here rather than found there.
"""

import json
import logging
import subprocess
import sys

import pytest

from pytruenas.utils import bundle

pytestmark = pytest.mark.requires("pathspec")


# -- the closure ----------------------------------------------------------


def test_a_requirements_own_extras_are_followed():
    """pytruenas depends on `pathlib_next[uri]`; that extra's own requirement
    (uritools) was dropped, and the appliance does not have it -- so a deployed
    bundle could not import `pathlib_next.uri`, which every remote path uses."""
    closure = bundle.requirements("pytruenas")
    assert "uritools" in closure
    assert "pathlib-next" in closure


def test_the_roots_extras_are_not_applied_to_everything():
    """`extras=("ssh",)` used to be offered to every distribution in the
    closure, so anything with an extra of that name contributed too."""
    core = bundle.requirements("pytruenas")
    with_ssh = bundle.requirements("pytruenas", extras=("ssh",))
    assert "asyncssh" not in core and "asyncssh" in with_ssh
    # pathlib_next has `sftp`/`s3`/`az` extras; none of them are pulled in.
    assert not {"paramiko", "boto3", "azure-identity"} & set(with_ssh)


def test_markers_are_evaluated_against_the_target():
    """They were evaluated against the machine RUNNING deploy, so a
    platform-gated dependency was decided by the wrong environment."""
    linux = {"sys_platform": "linux", "os_name": "posix", "python_version": "3.11"}
    windows = {"sys_platform": "win32", "os_name": "nt", "python_version": "3.11"}
    for env in (linux, windows):
        closure = bundle.requirements("pytruenas", environment=env)
        assert "pytruenas" in closure  # the root is always there
    # The probe reports that environment, and parse_probe reads it back.
    names, environment = bundle.parse_probe(
        json.dumps({"__marker_environment__": linux}) + "\nrequests\nidna\n"
    )
    assert names == ["requests", "idna"] and environment == linux


def test_the_probe_still_reads_as_names_only_for_an_older_caller():
    names, environment = bundle.parse_probe("requests\nidna\n")
    assert names == ["requests", "idna"] and environment == {}


def test_the_probe_reports_the_environment_it_runs_in():
    result = subprocess.run(
        [sys.executable, "-"],
        input=bundle.PROBE_SOURCE,
        capture_output=True,
        text=True,
        check=True,
    )
    _, environment = bundle.parse_probe(result.stdout)
    assert environment["sys_platform"] == sys.platform
    assert environment["python_version"] == ".".join(
        str(p) for p in sys.version_info[:2]
    )


# -- the repo tree --------------------------------------------------------


def _repo(tmp_path):
    """A repo shaped like the ones that broke this: a nested ignore file, a
    nested checkout, and a symlink pointing outside."""
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.env").write_text("TOKEN=hunter2\n")

    root = tmp_path / "repo"
    (root / "src" / "pkg").mkdir(parents=True)
    (root / ".git").mkdir()
    (root / ".git" / "config").write_text("[core]\n")
    (root / ".gitignore").write_text("*.log\n")
    (root / "src" / ".gitignore").write_text("generated/\n")
    (root / "src" / "generated").mkdir()
    (root / "src" / "generated" / "big.py").write_text("# generated\n")
    (root / "src" / "pkg" / "__init__.py").write_text("x = 1\n")
    (root / "keep.py").write_text("y = 2\n")
    (root / "noisy.log").write_text("noise\n")
    # A nested checkout: its history must not ship.
    (root / "vendor" / "dep" / ".git").mkdir(parents=True)
    (root / "vendor" / "dep" / ".git" / "HEAD").write_text("ref: refs/heads/main\n")
    (root / "vendor" / "dep" / "mod.py").write_text("z = 3\n")
    return root, outside


def _arcnames(contents):
    return sorted(arc for arc, _ in contents)


def test_a_repo_ships_what_a_clone_would(tmp_path):
    root, _ = _repo(tmp_path)
    names = _arcnames(bundle.collect_repo(root, prefix="repo"))
    assert "repo/keep.py" in names
    assert "repo/src/pkg/__init__.py" in names
    assert "repo/vendor/dep/mod.py" in names
    # The root ignore file, as before.
    assert "repo/noisy.log" not in names
    # A nested ignore file applies below its own directory (git's rule).
    assert not [n for n in names if "generated" in n]
    # No .git anywhere -- the root's or a nested checkout's.
    assert not [n for n in names if ".git/" in n]


def test_a_nested_ignore_file_is_anchored_to_its_directory(tmp_path):
    root, _ = _repo(tmp_path)
    # `generated/` in src/.gitignore must not hide a top-level generated/.
    (root / "generated").mkdir()
    (root / "generated" / "keepme.py").write_text("w = 4\n")
    names = _arcnames(bundle.collect_repo(root, prefix="repo"))
    assert "repo/generated/keepme.py" in names
    assert "repo/src/generated/big.py" not in names


def test_a_symlink_out_of_the_repo_is_not_followed(tmp_path, caplog):
    root, outside = _repo(tmp_path)
    try:
        (root / "link").symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError):  # pragma: no cover - needs privilege
        pytest.skip("cannot create a symlink here")
    with caplog.at_level(logging.DEBUG, logger="pytruenas.bundle"):
        names = _arcnames(bundle.collect_repo(root, prefix="repo"))
    assert not [n for n in names if "secret.env" in n or n.startswith("repo/link")]


def test_a_named_ignore_file_that_is_absent_is_an_error(tmp_path):
    """It silently disabled ALL filtering, so a gitignored secret shipped."""
    root, _ = _repo(tmp_path)
    with pytest.raises(bundle.BundleError, match="nothing would be filtered"):
        bundle.collect_repo(root, ignore_files=["  .bundleignore"], prefix="repo")
    with pytest.raises(bundle.BundleError, match="not found"):
        bundle.collect_repo(root, ignore_files=[".nope"], prefix="repo")
    # The defaults stay forgiving: a repo need not have all three.
    assert bundle.collect_repo(root, prefix="repo")


# -- the advisory dependency list -----------------------------------------


def test_a_requirements_file_survives_its_own_oddities(tmp_path, caplog):
    """One unparseable line aborted the whole deploy, though this list is only
    printed as a heads-up."""
    text = (
        "# a comment\n"
        "requests>=2\n"
        "duho  # inline comment\n"
        "pathlib_next[uri]; python_version >= '3.9'\n"
        "some-\\\n"
        "package==1.0\n"
        "-r other.txt\n"
        "!!! not a requirement !!!\n"
    )
    with caplog.at_level(logging.WARNING, logger="pytruenas.bundle"):
        names = bundle._parse_requirements_txt(text)
    assert "requests" in names and "duho" in names
    assert "pathlib_next" in names  # the raw declared name, not canonicalized
    assert "some-package" in names  # the backslash continuation is one line
    assert "ignoring unparseable requirement" in caplog.text
