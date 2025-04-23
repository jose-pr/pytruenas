import pathlib as _pathlib
import typing as _ty

if _ty.TYPE_CHECKING:
    from .. import TrueNASClient
    from pathlib import PosixPath as _Path
else:

    class _Path: ...


from . import api
from . import local
from . import sftp

ACCESSORS = {
    _n: _v
    for _n, _v in globals().items() if not _n.startswith('_')
}


class Path(_Path):
    def __init__(
        self,
        *args: _pathlib.PurePath | str,
        client: "TrueNASClient",
        methods: _ty.Sequence[str] | str = "auto",
    ):
        methods = methods or "auto"
        if methods == "auto":
            methods = "local" if client._api.is_local else ("sftp", "api")
        if isinstance(methods, str):
            methods = (methods,)
        self._methods = methods
        self._client = client
        self._path = _pathlib.PurePosixPath(*args)

    def __str__(self):
        return self._path.as_posix()

    def __repr__(self):
        return f"{self.__class__.__name__}(client={self._client._api.host},methods={self._methods})"

    def __fspath__(self):
        return self._path.as_posix()

    def _with_path(self, path):
        return self.__class__(path, client=self._client, methods=self._methods)

    def __truediv__(self, key):
        return self._with_path(self._path.__truediv__(key))

    def __rtruediv__(self, key):
        return self._with_path(self._path.__rtruediv__(key))

    def _fsmethod(self, name: str):
        err = NotImplementedError
        for method in self._methods:
            try:
                fs = ACCESSORS[method]
                _method = getattr(fs, name)

                def method(*args, **kwargs):
                    return _method(self, *args, **kwargs)

                return method
            except (AttributeError, NotImplementedError, KeyError):
                err = err.__class__
                pass
        return err

    def __getattr__(self, name: str):

        if name.startswith("_"):
            raise AttributeError(name)

        attr = NotImplementedError

        if hasattr(self._path, name):
            attr = getattr(self._path, name)
        else:
            attr = self._fsmethod(name)

        if attr is NotImplementedError:
            raise NotImplementedError(name)

        if callable(attr):

            def _attr(*args, **kwargs):
                val = attr(*args, **kwargs)
                return (
                    self._with_path(val)
                    if isinstance(attr, _pathlib.PurePath)
                    and not isinstance(attr, self.__class__)
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

    def chmod(self, mode: int | str):
        if isinstance(mode, str):
            mode = int(mode, 8)
        return self._fsmethod("chmod")(mode)
