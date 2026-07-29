"""Higher-level operations built on top of :class:`~pytruenas.TrueNASClient`.

* :mod:`.template` -- render + apply file templates to remote paths with an
  optional baseline snapshot.
* :mod:`.systemd` -- systemd units and system files, written idempotently.
  Formerly ``midclt.py``, which was a misnomer: ``midclt`` is TrueNAS's own CLI
  binary and nothing in the module invokes it.

Three things that used to live here are gone, none of which was an "operation
against a host":

* ``ops.main.init`` (build a client from a YAML config) was imported by
  nothing, duplicated the CLI's own config loading, and documented a
  ``pytruenas.client`` module deleted in 0.2.0. It is now
  ``examples/simple_client_from_yaml.py`` -- a worked example rather than a
  half-maintained API.
* ``ops.host``'s directory packaging is now
  :func:`pytruenas.utils.bundle.tar_tree` / ``tar_digest``, beside the code
  that builds the trees it archives.
* ``ops.host``'s network helpers (``is_localhost``, ``is_local_ip``,
  ``find_adapter_in_network``) are deleted outright. They were thin wrappers
  over :mod:`netimps` and :mod:`ipaddress` that nothing in the package
  imported -- only their own tests did. Call ``netimps.interface_for`` /
  ``get_interfaces`` and ``ipaddress.ip_address(...).is_loopback`` directly.
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
