"""Pure template rendering helpers (ops.template) -- no client/server."""

from types import SimpleNamespace

from pytruenas.ops.template import (
    BasicTemplate,
    TextTemplate,
    render_basic_template,
)


def test_text_template_returns_baseline():
    assert TextTemplate("hello").render({}) == "hello"


def test_text_template_decodes_bytes():
    assert TextTemplate(b"raw").render({}) == "raw"


def test_render_basic_template_substitutes_dict():
    out = render_basic_template("host=%{HOST} port=%{port}", {"host": "nas", "port": 443})
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
    from pytruenas.ops.template import TemplateTarget

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
    from pytruenas.ops.template import BaseTemplate, TemplateTarget

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
