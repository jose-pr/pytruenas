import pathlib as _pathlib
import typing as _ty
import io as _io
import functools as _ftools

if _ty.TYPE_CHECKING:
    from .. import TrueNASClient
    from pathlib import PosixPath as _Path
else:

    class _Path: ...


from ..utils.target import Target as _Tgt

from . import api
from . import local
from . import sftp

BACKENDS = {_n: _v for _n, _v in globals().items() if not _n.startswith("_")}


class Path(_Path):
    def __init__(
        self,
        *args: _pathlib.PurePath | str,
        client: "TrueNASClient",
        backend: _ty.Sequence[str] | str = "auto",
    ):
        backend = backend or "auto"
        if backend == "auto":
            backend = "local" if client._api.is_local else ("sftp", "api")
        if isinstance(backend, str):
            backend = (backend,)
        self._backends = backend
        self._client = client
        self._path = _pathlib.PurePosixPath(*args)

    @_ftools.cache
    def __str__(self):
        return self._path.as_posix()

    @_ftools.cache
    def __repr__(self):
        _src = self._client._api
        uri = _Tgt(
            scheme="+".join(self._backends),
            username="",
            password="",
            host=_src.host,
            port=0,
            path=self._path.as_posix(),
        ).uri

        return f"{self.__class__.__name__}({uri})"

    @_ftools.cache
    def __fspath__(self):
        return self._path.as_posix()

    def _with_path(self, path):
        return self.__class__(path, client=self._client, backend=self._backends)

    def with_backend(self, *backend):
        return self.__class__(self._path, client=self._client, backend=backend)

    def __truediv__(self, key):
        return self._with_path(self._path.__truediv__(key))

    def __rtruediv__(self, key):
        return self._with_path(self._path.__rtruediv__(key))

    def _fsmethod(self, name: str):
        for backend in self._backends:
            try:
                method = getattr(BACKENDS[backend], name)

                def bounded_method(*args, **kwargs):
                    return method(self, *args, **kwargs)

                return bounded_method
            except (AttributeError, NotImplementedError, KeyError):
                pass
        return NotImplemented

    @_ftools.cache
    def __getattr__(self, name: str):

        if name.startswith("_"):
            raise AttributeError(name)

        attr = NotImplementedError

        if hasattr(self._path, name):
            attr = getattr(self._path, name)
        else:
            attr = self._fsmethod(name)

        if attr is NotImplemented:
            _default = getattr(_pathlib.Path, name)
            raise NotImplementedError(name)

        if callable(attr):

            def _attr(*args, **kwargs):
                val = attr(*args, **kwargs)
                return (
                    self._with_path(val)
                    if isinstance(val, _pathlib.PurePath)
                    and not isinstance(val, self.__class__)
                    else val
                )

            return _attr
        else:
            return (
                self._with_path(attr)
                if isinstance(attr, _pathlib.PurePath)
                and not isinstance(attr, self.__class__)
                else attr
            )

    def write(self, data: bytes | str):
        encode = getattr(data, "encode", None)
        if callable(encode):
            data = encode()
        return self.write_bytes(data)

    def read(self):
        self.read_bytes()

    def chmod(self, mode: int | str, *args, **kwargs):
        if isinstance(mode, str):
            mode = int(mode, 8)
        return self._fsmethod("chmod")(mode, *args, **kwargs)

    def chown(
        self,
        uid: int = None,
        gid: int = None,
        *args,
        follow_symlinks: bool = True,
        **kwargs,
    ):
        if uid == None:
            uid = -1
        if gid == None:
            gid = -1
        return self._fsmethod("chown")(
            uid, gid, *args, follow_symlinks=follow_symlinks, **kwargs
        )

    def open(
        self,
        mode: str = "r",
        buffering=-1,
        encoding: str = None,
        errors: str = None,
        newline=None,
        *args,
        **kwargs,
    ):
        method = self._fsmethod("open")
        if method is NotImplemented:
            raise NotImplementedError("open")
        try:
            return method(mode, buffering, encoding, errors, newline, *args, **kwargs)
        except (NotImplementedError, TypeError) as e:
            fh = method(
                mode + "b" if "b" not in mode else mode, buffering, *args, **kwargs
            )
            if "b" not in mode:
                fh = _io.TextIOWrapper(fh, encoding, errors, newline)
            return fh


def _makeproxy(name: str):
    defaultmethod = getattr(_pathlib.Path, name)

    def proxy(self: Path, *args, **kwargs):
        method = self._fsmethod(name)
        if method is not NotImplemented:
            return method(*args, **kwargs)

        return defaultmethod(self, *args, **kwargs)

    return proxy


for _method in ["read_bytes", "read_text", "write_bytes", "write_text", "stat"]:
    setattr(Path, _method, _makeproxy(_method))
