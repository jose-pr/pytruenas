from __future__ import annotations

import logging as _logging
from pathlib import Path as LocalPath
from pathlib_next import Path

LOGGER = _logging.getLogger()


class TemplateTarget:
    def read(self) -> bytes:
        raise NotImplementedError()

    def write(self, content) -> bool:
        raise NotImplementedError()

    def apply_template(self, template: "BaseTemplate|str|type", context=None, **kwargs):
        if isinstance(template, type) and issubclass(template, BaseTemplate):
            # A BaseTemplate *class*: instantiate it with the target's current
            # content as the baseline (empty if the target does not exist yet).
            try:
                baseline = self.read()
            except FileNotFoundError:
                baseline = b""
            template = template(baseline, **kwargs)
        elif isinstance(template, str):
            # A plain string is the template's literal content.
            template = TextTemplate(template, **kwargs)
        elif not isinstance(template, BaseTemplate):
            # Anything else (e.g. a path-like) is read as a file's content.
            template = TextTemplate(LocalPath(template).read_text(), **kwargs)

        return template.apply(self, context)


class BaseTemplate:
    DEBUG_START = "#################### START {path} ####################"
    DEBUG_END = "#################### END   {path} ####################"

    @property
    def source(self):
        return "mem"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.source})"

    def render(self, context) -> str: ...

    def apply(self, target: TemplateTarget, context=None):
        LOGGER.info(f"Applying {self} to {target}")
        rendered = self.render(context if context is not None else {})
        modified = target.write(rendered)
        if modified:
            LOGGER.info(f"Target: {target} modified")
        return modified


class TextTemplate(BaseTemplate):
    def __init__(self, baseline: str):
        self.baseline = baseline.decode() if isinstance(baseline, bytes) else baseline

    def render(self, context):
        return self.baseline


class BasicTemplate(TextTemplate):
    def render(self, context):
        return render_basic_template(self.baseline, context)


def render_basic_template(template: str, context: object | dict):
    if context is None:
        return template
    if not isinstance(context, dict):
        # A non-dict, non-None context: use its attribute namespace. ``vars()``
        # raises TypeError for objects without ``__dict__`` -- treat those as no
        # substitutions rather than crashing.
        try:
            context = vars(context)
        except TypeError:
            return template
    for prop, val in context.items():
        template = template.replace(f"%{{{prop.upper()}}}", str(val))
        template = template.replace(f"%{{{prop}}}", str(val))

    return template


class FileTarget(TemplateTarget):

    def __init__(self, path: 'Path', baseline: bool = False):
        if not isinstance(path, Path):
            raise ValueError(path)
        self.path = path
        if baseline is True:
            baseline = ".baseline"
        self._baseline = str(baseline or "")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.path})"

    def baseline(self):
        baseline = self.path.with_name(self.path.name + self._baseline)
        if not baseline.exists() and baseline.resolve() != self.path.resolve():
            LOGGER.info(f"Creating baseline for: {self.path} at: {baseline}")
            baseline.write_bytes(self.path.read_bytes())
        return baseline

    def read(self) -> bytes:
        if self._baseline:
            return self.baseline().read_bytes()
        return self.path.read_bytes()
    
    def write(self, content) -> bool:
        if isinstance(content, str):
            content = content.encode()
        if not self.path.parent.exists():
            self.path.parent.mkdir(755, True, True)
        if self._baseline:
            _ = self.baseline()
        if not self.path.exists() or self.path.read_bytes() != content:
            self.path.write_bytes(content)
            return True
        return False