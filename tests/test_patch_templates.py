"""Pure template rendering helpers (patch.templates) -- no client/server."""

from types import SimpleNamespace

from pytruenas.patch.templates import (
    BasicTemplate,
    TextTemplate,
    render_basic_template,
)


def test_text_template_returns_baseline():
    assert TextTemplate("hello").render({}) == "hello"


def test_text_template_decodes_bytes():
    assert TextTemplate(b"raw").render({}) == "raw"


def test_render_basic_template_substitutes_dict():
    out = render_basic_template(
        "host=%{HOST} port=%{port}", {"host": "nas", "port": 443}
    )
    assert out == "host=nas port=443"


def test_render_basic_template_accepts_object():
    ctx = SimpleNamespace(name="svc")
    assert render_basic_template("n=%{NAME}", ctx) == "n=svc"


def test_render_basic_template_none_context():
    assert render_basic_template("plain", None) == "plain"


def test_basic_template_render():
    assert BasicTemplate("%{X}-%{Y}").render({"x": "a", "y": "b"}) == "a-b"


def test_render_basic_template_object_without_dict_is_noop():
    # vars() raises TypeError for objects without __dict__ (e.g. int) -> the
    # template is returned unchanged rather than crashing.
    assert render_basic_template("keep %{X}", 5) == "keep %{X}"


def test_apply_template_renders_and_writes():
    from pytruenas.patch.templates import TemplateTarget

    class MemTarget(TemplateTarget):
        def __init__(self):
            self.written = None

        def read(self):
            raise FileNotFoundError

        def write(self, content):
            self.written = content
            return True

    t = MemTarget()
    # a str template routes through TextTemplate; apply() renders + writes.
    modified = t.apply_template("static content")
    assert modified is True
    assert t.written == "static content"


def test_apply_template_baseline_read_missing_ok():
    from pytruenas.patch.templates import BaseTemplate, TemplateTarget

    class MemTarget(TemplateTarget):
        def read(self):
            raise FileNotFoundError

        def write(self, content):
            return False

    class T(BaseTemplate):
        def __init__(self, baseline, **kw):
            self.baseline = baseline

        def render(self, context):
            return "rendered"

    # a BaseTemplate subclass reads the (missing) baseline without crashing.
    assert MemTarget().apply_template(T, context={}) is False


# -- soundness fixes ------------------------------------------------------


def test_base_render_raises_instead_of_returning_none():
    """A subclass that forgets render() must not silently write None.

    The base used to be `def render(...): ...`, so the None flowed straight
    into write() as the file's new content.
    """
    import pytest

    from pytruenas.patch.templates import BaseTemplate

    class Forgot(BaseTemplate):
        pass

    with pytest.raises(NotImplementedError, match="must implement render"):
        Forgot().render({})


def test_apply_template_rejects_kwargs_for_a_built_template():
    """Silently dropping them left the caller's option with no effect."""
    import pytest

    from pytruenas.patch.templates import TemplateTarget, TextTemplate

    class Mem(TemplateTarget):
        def write(self, content):
            return True

    with pytest.raises(TypeError, match="already-constructed"):
        Mem().apply_template(TextTemplate("x"), unexpected=1)


def _fake_path_factory():
    """A minimal in-memory path good enough for FileTarget."""

    class P:
        def __init__(self, store, path):
            self._store, self._path = store, path

        def exists(self):
            return self._path in self._store

        def read_bytes(self):
            if self._path not in self._store:
                raise FileNotFoundError(self._path)
            return self._store[self._path]

        def write_bytes(self, data):
            self._store[self._path] = data

        def with_name(self, name):
            return P(self._store, self._path.rsplit("/", 1)[0] + "/" + name)

        @property
        def name(self):
            return self._path.rsplit("/", 1)[-1]

        @property
        def parent(self):
            return P(self._store, self._path.rsplit("/", 1)[0])

        def mkdir(self, mode=None, parents=False, exist_ok=False):
            self._store.setdefault(self._path, None)

        def unlink(self, missing_ok=False):
            self._store.pop(self._path, None)

        def resolve(self):
            return self

        def __eq__(self, other):
            return isinstance(other, P) and self._path == other._path

    return P


def test_baseline_on_a_file_that_does_not_exist_yet():
    """ "Create this config if absent" must work, not raise.

    baseline() used to read_bytes() the missing original, so a first write to a
    new path raised FileNotFoundError from inside write().
    """
    from pytruenas.patch.templates import FileTarget

    P = _fake_path_factory()
    store = {}
    target = FileTarget(P(store, "/etc/new.conf"), baseline=True)

    assert target.write("content\n") is True
    assert store["/etc/new.conf"] == b"content\n"
    # Nothing to snapshot, so no baseline was fabricated.
    assert "/etc/new.conf.baseline" not in store


def test_baseline_snapshots_an_existing_file_once():
    from pytruenas.patch.templates import FileTarget

    P = _fake_path_factory()
    store = {"/etc/c.conf": b"original\n"}
    target = FileTarget(P(store, "/etc/c.conf"), baseline=True)

    target.write("changed\n")
    assert store["/etc/c.conf.baseline"] == b"original\n"
    # read() templates from the ORIGINAL, which is what makes layering
    # idempotent -- a second apply sees the stock content, not its own output.
    assert target.read() == b"original\n"

    target.write("changed again\n")
    assert store["/etc/c.conf.baseline"] == b"original\n"  # not re-snapshotted


def test_write_returns_false_when_content_is_unchanged():
    from pytruenas.patch.templates import FileTarget

    P = _fake_path_factory()
    store = {}
    target = FileTarget(P(store, "/etc/c.conf"))
    assert target.write("same\n") is True
    assert target.write("same\n") is False


def test_write_refuses_none():
    """Rather than encoding it or writing the literal b'None'."""
    import pytest

    from pytruenas.patch.templates import FileTarget

    P = _fake_path_factory()
    target = FileTarget(P({}, "/etc/c.conf"))
    with pytest.raises(TypeError, match="rendered nothing"):
        target.write(None)


def test_directory_mode_is_octal():
    """The old code passed a bare 755, which Python reads as DECIMAL.

    0o1363 -- setuid plus the wrong permission bits -- on any directory it had
    to create.
    """
    from pytruenas.patch.templates.targets import DIRECTORY_MODE

    assert DIRECTORY_MODE == 0o755
    assert DIRECTORY_MODE != 755


def test_file_target_rejects_a_non_path_naming_what_is_missing():
    import pytest

    from pytruenas.patch.templates import FileTarget

    with pytest.raises(TypeError, match="not path-like"):
        FileTarget(object())


# -- inspection and undo --------------------------------------------------


def test_revert_restores_the_original_and_clears_the_baseline():
    """The counterpart the baseline mechanism exists for."""
    from pytruenas.patch.templates import FileTarget

    P = _fake_path_factory()
    store = {"/etc/c.conf": b"original\n"}
    target = FileTarget(P(store, "/etc/c.conf"), baseline=True)

    target.write("patched\n")
    assert store["/etc/c.conf"] == b"patched\n"

    assert target.revert() is True
    assert store["/etc/c.conf"] == b"original\n"
    assert "/etc/c.conf.baseline" not in store  # snapshot cleaned up


def test_revert_can_keep_the_baseline_for_a_re_apply():
    from pytruenas.patch.templates import FileTarget

    P = _fake_path_factory()
    store = {"/etc/c.conf": b"original\n"}
    target = FileTarget(P(store, "/etc/c.conf"), baseline=True)
    target.write("patched\n")

    target.revert(remove_baseline=False)
    assert store["/etc/c.conf.baseline"] == b"original\n"


def test_revert_is_a_noop_without_a_baseline():
    """A file this target CREATED is not ours to delete."""
    from pytruenas.patch.templates import FileTarget

    P = _fake_path_factory()
    store = {}
    target = FileTarget(P(store, "/etc/new.conf"), baseline=True)
    target.write("created\n")

    assert target.revert() is False
    assert store["/etc/new.conf"] == b"created\n"  # left alone


def test_revert_reports_false_when_already_at_the_baseline():
    from pytruenas.patch.templates import FileTarget

    P = _fake_path_factory()
    store = {"/etc/c.conf": b"original\n"}
    target = FileTarget(P(store, "/etc/c.conf"), baseline=True)
    target.write("patched\n")
    target.revert(remove_baseline=False)

    assert target.revert() is False  # nothing left to undo


def test_is_patched_tracks_the_difference_from_the_baseline():
    from pytruenas.patch.templates import FileTarget

    P = _fake_path_factory()
    store = {"/etc/c.conf": b"original\n"}
    target = FileTarget(P(store, "/etc/c.conf"), baseline=True)

    assert target.is_patched() is False  # no baseline taken yet
    target.write("patched\n")
    assert target.is_patched() is True
    target.revert(remove_baseline=False)
    assert target.is_patched() is False


def test_would_change_is_a_dry_run_with_no_side_effects():
    from pytruenas.patch.templates import FileTarget

    P = _fake_path_factory()
    store = {"/etc/c.conf": b"original\n"}
    target = FileTarget(P(store, "/etc/c.conf"))

    assert target.would_change("different\n") is True
    assert target.would_change("original\n") is False
    assert store == {"/etc/c.conf": b"original\n"}  # untouched


def test_would_change_is_true_for_a_file_that_does_not_exist():
    from pytruenas.patch.templates import FileTarget

    P = _fake_path_factory()
    assert FileTarget(P({}, "/etc/new.conf")).would_change("x") is True


# -- permissions ----------------------------------------------------------


class _ModedPath:
    """A fake path that tracks a mode, like a real filesystem."""

    def __init__(self, store, modes, path):
        self._store, self._modes, self._path = store, modes, path

    def exists(self):
        return self._path in self._store

    def read_bytes(self):
        return self._store[self._path]

    def write_bytes(self, data):
        created = self._path not in self._store
        self._store[self._path] = data
        if created:
            self._modes[self._path] = 0o644  # umask default on create

    def with_name(self, name):
        return _ModedPath(
            self._store, self._modes, self._path.rsplit("/", 1)[0] + "/" + name
        )

    @property
    def name(self):
        return self._path.rsplit("/", 1)[-1]

    @property
    def parent(self):
        return _ModedPath(self._store, self._modes, self._path.rsplit("/", 1)[0])

    def mkdir(self, *args, **kwargs):
        pass

    def stat(self):
        import types

        return types.SimpleNamespace(st_mode=0o100000 | self._modes[self._path])

    def chmod(self, mode):
        self._modes[self._path] = mode

    def unlink(self, missing_ok=False):
        self._store.pop(self._path, None)
        self._modes.pop(self._path, None)


def test_rewriting_preserves_an_existing_files_mode():
    """Silently widening /etc/shadow from 0640 to 0644 is a security bug."""
    from pytruenas.patch.templates import FileTarget

    store = {"/etc/shadow": b"original\n"}
    modes = {"/etc/shadow": 0o640}
    target = FileTarget(_ModedPath(store, modes, "/etc/shadow"))

    target.write("patched\n")
    assert modes["/etc/shadow"] == 0o640


def test_mode_applies_to_a_file_this_target_creates():
    from pytruenas.patch.templates import FileTarget

    store, modes = {}, {}
    target = FileTarget(_ModedPath(store, modes, "/etc/new.conf"), mode=0o600)

    target.write("secret\n")
    assert modes["/etc/new.conf"] == 0o600


def test_an_existing_mode_wins_over_the_declared_one():
    """`mode=` is for creation; an existing file's own mode is authoritative."""
    from pytruenas.patch.templates import FileTarget

    store = {"/etc/c.conf": b"x\n"}
    modes = {"/etc/c.conf": 0o600}
    target = FileTarget(_ModedPath(store, modes, "/etc/c.conf"), mode=0o644)

    target.write("y\n")
    assert modes["/etc/c.conf"] == 0o600


def test_a_backend_without_chmod_warns_rather_than_failing(caplog):
    """The websocket filesystem leg has no chmod; a write must still succeed."""
    import logging

    from pytruenas.patch.templates import FileTarget

    P = _fake_path_factory()  # no chmod/stat on this one
    store = {}
    target = FileTarget(P(store, "/etc/new.conf"), mode=0o600)

    with caplog.at_level(logging.WARNING, logger="pytruenas.patch.templates.targets"):
        assert target.write("content\n") is True
    assert store["/etc/new.conf"] == b"content\n"
    assert any("could not set mode" in r.getMessage() for r in caplog.records)
