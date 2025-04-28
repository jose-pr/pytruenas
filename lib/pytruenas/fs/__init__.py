import pathlib as _pathlib
import typing as _ty
import io as _io
import functools as _ftools

if _ty.TYPE_CHECKING:
    from .. import TrueNASClient
    from pathlib import PosixPath as _Path
    import _typeshed
else:

    class _Path: ...


from ..utils.target import Target as _Tgt

from . import api
from . import local
from . import sftp

BACKENDS = {_n: _v for _n, _v in globals().items() if not _n.startswith("_")}
_FTYPE = _ty.Literal["file", "link", "directory"]


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

    def __str__(self) -> str:
        return self._path.as_posix()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.uri.uri})"

    def as_uri(self):
        return self.uri.uri

    @_ftools.cached_property
    def uri(self):
        _src = self._client._api
        return _Tgt(
            scheme="+".join(self._backends),
            username="",
            password="",
            host=_src.host,
            port=0,
            path=self._path.as_posix(),
        )

    @_ftools.cache
    def __fspath__(self):  # type:ignore
        return self._path.as_posix()

    def __eq__(self, value):
        if not isinstance(value, (Path, _pathlib.PurePath)):
            return False
        return value.as_uri() == self.as_uri()

    def __hash__(self):
        return self.uri.__hash__()

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
            raise NotImplementedError(name)

        if callable(attr):
            attr = _ty.cast(_ty.Callable, attr)

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
            data = encode()  # type:ignore
        return self.write_bytes(data)  # type:ignore

    def read(self):
        self.read_bytes()

    def symlink_to(
        self,
        target: "Path",
        target_is_directory=False,
        *args,
        force: bool | _FTYPE | _ty.Sequence[_FTYPE] = False,
        **kwargs,
    ):
        if force and self.exists():
            if force is True:
                _force = _ty.get_args(_FTYPE)
            elif isinstance(force, str):
                _force = (force,)
            else:
                _force = []
            if not self.is_symlink():
                raise_ = False
                if self.is_dir():
                    raise_ = "directory" not in _force
                elif self.is_file():
                    raise_ = "file" not in _force
                else:
                    raise_ = True
                if raise_:
                    raise FileExistsError(self)
                self.rmtree()
            elif self.readlink() != target:
                if "link" not in _force:
                    raise FileExistsError(target)
                self.unlink()
            else:
                return
        self.__getattr__("symlink_to")(
            target, target_is_directory, *args, **kwargs
        )  # type:ignore

    def rmtree(self, ignore_errors=False, onerror=None, *args, **kwargs) -> None:
        return self.__getattr__("rmtree")(
            ignore_errors, onerror, *args, **kwargs
        )  # type:ignore

    def chmod(self, mode: int | str, *args, **kwargs) -> None:
        if isinstance(mode, str):
            mode = int(mode, 8)
        return self.__getattr__("chmod")(mode, *args, **kwargs)  # type:ignore

    def chown(
        self,
        uid: int | None = None,
        gid: int | None = None,
        *args,
        follow_symlinks: bool = True,
        **kwargs,
    ) -> None:
        if uid == None:
            uid = -1
        if gid == None:
            gid = -1
        return self.__getattr__("chown")(
            uid, gid, *args, follow_symlinks=follow_symlinks, **kwargs
        )  # type:ignore

    def open(  # type:ignore
        self,
        mode: "_typeshed.OpenTextMode" = "r",
        buffering=-1,
        encoding: str | None = None,
        errors: str | None = None,
        newline=None,
        *args,
        **kwargs,
    ) -> _ty.IO:
        method = _ty.cast(_ty.Callable[..., _ty.IO], self._fsmethod("open"))
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
            return method(*args, **kwargs)  # type:ignore

        return defaultmethod(self, *args, **kwargs)

    return proxy


for _method in ["read_bytes", "read_text", "write_bytes", "write_text", "exists"]:
    setattr(Path, _method, _makeproxy(_method))

import os as _os

_os.PathLike.register(Path)
