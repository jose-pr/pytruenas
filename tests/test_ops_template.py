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
