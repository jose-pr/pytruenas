"""Higher-level operations built on top of :class:`~pytruenas.TrueNASClient`.

* :mod:`.template` -- render + apply file templates to remote paths with an
  optional baseline snapshot.
* :mod:`.midclt` -- systemd unit / etc-file management on a TrueNAS host.
* :mod:`.host` -- local (non-API) helpers: network adapter discovery.

Two things that used to live here have moved, because neither was an
"operation against a host":

* ``ops.main.init`` (build a client from a YAML config) was imported by
  nothing, duplicated the CLI's own config loading, and documented a
  ``pytruenas.client`` module deleted in 0.2.0. It is now
  ``examples/simple_client_from_yaml.py`` -- a worked example rather than a
  half-maintained API.
* ``ops.host``'s directory packaging is now
  :func:`pytruenas.utils.bundle.tar_tree` / ``tar_digest``, beside the code
  that builds the trees it archives.
"""

from .template import (
    BaseTemplate,
    BasicTemplate,
    FileTarget,
    TemplateTarget,
    TextTemplate,
    render_basic_template,
)

__all__ = [
    "BaseTemplate",
    "BasicTemplate",
    "FileTarget",
    "TemplateTarget",
    "TextTemplate",
    "render_basic_template",
]
