"""Higher-level operations built on top of :class:`~pytruenas.TrueNASClient`.

* :mod:`.main` -- construct a client from a small YAML config.
* :mod:`.template` -- render + apply file templates to remote paths with an
  optional baseline snapshot.
* :mod:`.midclt` -- systemd unit / etc-file management on a TrueNAS host.
* :mod:`.host` -- local (non-API) helpers: adapter discovery, directory
  packaging (needs the optional ``host`` extra).

Submodules are imported lazily so a missing optional dependency (e.g. ``ifaddr``
for :mod:`.host`) never breaks importing the package as a whole.
"""

from .main import init
from .template import (
    BaseTemplate,
    BasicTemplate,
    FileTarget,
    TemplateTarget,
    TextTemplate,
    render_basic_template,
)

__all__ = [
    "init",
    "BaseTemplate",
    "BasicTemplate",
    "FileTarget",
    "TemplateTarget",
    "TextTemplate",
    "render_basic_template",
]
