"""Reach files inside the installed ``middlewared`` package on a host.

Mostly for the stock ``etc_files`` templates: taking one as a baseline lets a
patch layer onto what TrueNAS itself generates instead of replacing it with a
hand-written file that then drifts from every future release.

Was in ``ops/midclt.py`` alongside the systemd code, which it has nothing to do
with.
"""

from __future__ import annotations

import typing as _ty

from .systemd.files import SystemFile

if _ty.TYPE_CHECKING:  # pragma: no cover - typing only
    from ..host import TrueNASHost as TrueNASClient

__all__ = ["MiddlewareFiles", "middlewared_path"]

#: Asks the host's own interpreter where the package is, rather than hardcoding
#: a path. On 26.0 it is ``/usr/lib/python3/dist-packages/middlewared``, but
#: that is a Debian-layout detail that a base-OS change would move -- and the
#: interpreter always knows.
_LOCATE_SOURCE = "import middlewared, os; print(os.path.dirname(middlewared.__file__))"


def middlewared_path(client: "TrueNASClient"):
    """Where the ``middlewared`` package lives on ``client``, as a path.

    Requires the host to be able to *run* something: the middleware API exposes
    no method reporting its own install location (checked against 26.0 --
    nothing in ``core.get_methods`` answers it), so this asks Python. That is a
    weaker requirement than it sounds: a remote TrueNAS with no SSH still
    executes through the web shell over the same websocket, so this works
    wherever ``run`` is in ``client.capabilities``.
    """
    result = client.run(
        ["python3", "-c", _LOCATE_SOURCE],
        capture_output="stdout",
        encoding="utf-8",
        check=True,
    )
    located = result.stdout.strip()
    if not located:
        raise RuntimeError(
            "could not locate the middlewared package on the host: "
            "`import middlewared` produced no path"
        )
    return client.path(located)


class MiddlewareFiles:
    """Locate files under the host's ``middlewared`` package."""

    #: Searched in order by :meth:`find_template`; the first match wins.
    #: ``local`` holds templates for other outputs, not overrides of the ones
    #: in ``etc_files``.
    TEMPLATE_DIRS = ("etc_files", "etc_files/local")

    def __init__(
        self,
        client: "TrueNASClient | None" = None,
        module_path: "str | None" = None,
    ) -> None:
        if client is None:
            from ..host import TrueNASHost

            client = TrueNASHost()
        self.client = client
        self._module_path = client.path(module_path) if module_path else None

    @property
    def module_path(self):
        """The middlewared package directory, located on first use.

        Lazy because locating it runs a command on the host: constructing a
        `MiddlewareFiles` should not require a working shell, only using one
        should. (It also means passing `module_path=` explicitly skips the
        round trip entirely.)
        """
        if self._module_path is None:
            self._module_path = middlewared_path(self.client)
        return self._module_path

    def __repr__(self) -> str:
        # Never resolves: locating the package runs a command on the host.
        shown = self._module_path if self._module_path is not None else "<unresolved>"
        return f"{type(self).__name__}({shown})"

    def find_template(
        self,
        template: str,
        etc: "str | _ty.Sequence[str] | None" = None,
        services: "str | _ty.Sequence[str] | None" = None,
        baseline: bool = True,
        writable: bool = False,
    ) -> SystemFile:
        """Find an ``etc_files`` template by name, with or without ``.mako``.

        Returns a :class:`~pytruenas.patch.systemd.SystemFile` for the first
        match in :attr:`TEMPLATE_DIRS`; ``etc``, ``services``, ``baseline``
        and ``writable`` are passed to it.

        ``baseline`` defaults to **True**: the original ships in the
        middlewared package, so overwriting it with no snapshot beside it
        leaves no way back short of reinstalling. The package is on a
        read-only dataset (``boot-pool/ROOT/<version>/usr`` on 26.0), which
        :meth:`~pytruenas.patch.templates.FileTarget.read` never writes to;
        the snapshot is taken by the first changing write, which needs the
        dataset writable anyway -- pass ``writable=True`` for that.

        Raises ``FileNotFoundError`` naming every location tried, rather than
        just the template name -- on a host where the middlewared layout has
        moved, the paths are the useful half of the message.
        """
        tried: "list[str]" = []
        for directory in self.TEMPLATE_DIRS:
            base = self.module_path / directory / template
            candidates = [base]
            if base.suffix != ".mako":
                candidates.append(base.with_name(base.name + ".mako"))
            for candidate in candidates:
                tried.append(str(candidate))
                try:
                    return self.find_file(
                        candidate,
                        etc=etc,
                        services=services,
                        baseline=baseline,
                        writable=writable,
                    )
                except FileNotFoundError:
                    continue
        raise FileNotFoundError(f"no template {template!r}; tried: {', '.join(tried)}")

    def find_file(
        self, path, *args, cls: "type[SystemFile] | None" = None, **kwargs
    ) -> SystemFile:
        """Wrap an existing file under the middlewared package as a target.

        ``args`` and ``kwargs`` reach ``cls`` (default ``SystemFile``) after
        the path and client. A file with only its baseline beside it (under
        the target's own baseline suffix) still counts as present: a previous
        patch may have replaced the original, and the baseline is what that
        patch templates from. Raises ``FileNotFoundError`` otherwise.
        """
        resolved = self.module_path / path
        target = (cls or SystemFile)(str(resolved), self.client, *args, **kwargs)
        snapshot = target.baseline_path
        if not target.path.exists() and not (
            snapshot is not None and snapshot.exists()
        ):
            raise FileNotFoundError(str(resolved))
        return target
