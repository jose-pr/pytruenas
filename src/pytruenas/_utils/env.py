"""The one accessor every ``PYTRUENAS_*`` setting is read through."""

from duho.env import Env as _Env

#: Every ``PYTRUENAS_*`` setting, read through one accessor, so the full set is
#: enumerable (``list(ENV)``). ``.paths()`` splits on ``os.pathsep``, so a
#: Windows ``C:\...`` entry keeps its drive colon.
#:
#: ``autoload=False``: the companion-module feature would import a
#: ``pytruenas_env`` module from anywhere on ``sys.path``, including the CWD.
#: This app ships no such defaults, so the import is pure attack surface --
#: and a CLI is routinely run from a directory the user does not control.
ENV = _Env("pytruenas", autoload=False)

__all__ = ["ENV"]
