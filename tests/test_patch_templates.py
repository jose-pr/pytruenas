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
