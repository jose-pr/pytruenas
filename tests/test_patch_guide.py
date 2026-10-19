"""docs/guide/patch.md: its example patch runs, offline, as printed.

Every ``python`` block of the page is executed in order in one namespace,
except a block whose first line is ``# needs a NAS``. The page's own
assertions are the test.
"""

from __future__ import annotations

import pathlib
import re

import pytest

GUIDE = pathlib.Path(__file__).resolve().parent.parent / "docs" / "guide" / "patch.md"

_BLOCK = re.compile(r"^```python\n(.*?)^```", re.MULTILINE | re.DOTALL)


def _blocks():
    text = GUIDE.read_text(encoding="utf-8")
    return [
        block for block in _BLOCK.findall(text) if not block.startswith("# needs a NAS")
    ]


def test_the_guide_has_the_example_and_the_offline_run():
    blocks = _blocks()
    assert len(blocks) == 3
    assert "def install(" in blocks[0]
    assert "class FakeNAS" in blocks[1]
    assert "install(nas)" in blocks[2]


def test_the_guides_example_patch_runs_against_its_fake_nas(tmp_path, monkeypatch):
    import tempfile

    # The page makes its directory with tempfile.mkdtemp(); keep it in tmp_path.
    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path))
    namespace: dict = {"__name__": "patch_guide"}
    for number, block in enumerate(_blocks(), 1):
        try:
            exec(compile(block, f"{GUIDE.name}[block {number}]", "exec"), namespace)
        except Exception:
            pytest.fail(f"block {number} of {GUIDE.name} failed:\n{block}")

    # The page ends uninstalled: nothing of the patch is left on the fake host.
    nas = namespace["nas"]
    assert not nas.path("/etc/agent.conf").exists()
    leftovers = [p.name for p in nas.root.rglob("*") if ".baseline" in p.name]
    assert leftovers == []
