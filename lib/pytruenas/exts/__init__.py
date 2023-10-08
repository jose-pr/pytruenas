import typing as _ty
from enum import Enum as _Enum

from ..base import Namespace
from .. import _utils

T = _ty.TypeVar("T")
D = _ty.TypeVar("D", bound=_ty.TypedDict)


class UpdateReturn(_Enum):
    NewValue = 0
    Diff = 1
    Both = 2


class Config(_ty.Generic[D]):
    def config(self, normalize: bool = True) -> D:
        config = self("config")
        if normalize:
            f = getattr(D, "_nomalize", None)
            if f:
                config = f(config)
        return config

    @_ty.overload
    def update(
        self,
        __partial: _utils._Dict = None,
        /,
        _return: _ty.Literal[UpdateReturn.NewValue] = UpdateReturn.NewValue,
        _force: bool = False,
        **__named: D,
    ) -> "D":
        ...

    @_ty.overload
    def update(
        self,
        __partial: _utils._Dict = None,
        /,
        _return: _ty.Literal[UpdateReturn.Diff] = UpdateReturn.Diff,
        _force: bool = False,
        **__named: D,
    ) -> "_utils._Dict":
        ...

    @_ty.overload
    def update(
        self,
        __partial: _utils._Dict = None,
        /,
        _return: _ty.Literal[UpdateReturn.Both] = UpdateReturn.Both,
        _force: bool = False,
        **__named: D,
    ) -> "tuple[_utils._Dict,D]":
        ...

    def update(
        self,
        __partial: _utils._Dict = None,
        /,
        _return: UpdateReturn = UpdateReturn.NewValue,
        _force: bool = False,
        **__named: D,
    ) -> "tuple[_utils._Dict,D]|D|_utils._Dict":
        partial = _utils.merge(__partial, __named)
        config = self.config(normalize=True)
        diff = config if _force else _utils.diff(config, partial)
        if diff:
            config = self("update", diff)
        if _return == UpdateReturn.Diff:
            return diff
        elif _return == UpdateReturn.Both:
            return diff, config
        else:
            return config


class Map(_ty.Generic[D]):
    _idattr = "id"

    def query(self) -> list[D]:
        return self("query")

    def _as_dict(self, __key=None) -> "_utils._Dict[D]":
        key = __key or self._idattr
        return {item[key]: item for item in self.query()}

    def _parseid(self, id: str | D):
        if isinstance(id, _ty.Mapping):
            id = id[self._idattr]
        return id

    def get_instance(self, id: str | D):
        id = self._parseid(id)
        return self("get_instance", id)

    def __getitem__(self, __key: str) -> D:
        return self.get_instance(__key)

    def __iter__(self) -> _ty.Iterator[str]:
        return self._as_dict().__iter__()

    def __len__(self) -> int:
        return self("query", [], {"count": True})

    @_ty.overload
    def update(
        self,
        id: str | D,
        __partial: _utils._Dict = None,
        /,
        _return: _ty.Literal[UpdateReturn.NewValue] = UpdateReturn.NewValue,
        _force: bool = False,
        **__named: D,
    ) -> "D":
        ...

    @_ty.overload
    def update(
        self,
        id: str | D,
        __partial: _utils._Dict = None,
        /,
        _return: _ty.Literal[UpdateReturn.Diff] = UpdateReturn.Diff,
        _force: bool = False,
        **__named: D,
    ) -> "_utils._Dict":
        ...

    @_ty.overload
    def update(
        self,
        id: str | D,
        __partial: _utils._Dict = None,
        /,
        _return: _ty.Literal[UpdateReturn.Both] = UpdateReturn.Both,
        _force: bool = False,
        **__named: D,
    ) -> "tuple[_utils._Dict,D]":
        ...

    def update(
        self,
        id: str | D,
        __partial: _utils._Dict = None,
        /,
        _return: UpdateReturn = UpdateReturn.NewValue,
        _force: bool = False,
        **__named: D,
    ) -> "tuple[_utils._Dict,D]|D|_utils._Dict":
        partial = _utils.merge(__partial, __named)
        if isinstance(id, _ty.Mapping):
            config = id
        else:
            config = self.get_instance(id)
        id = self._parseid(id)
        diff = config if _force else _utils.diff(config, partial)
        if diff:
            config = self("update", id, diff)
        if _return == UpdateReturn.Diff:
            return diff
        elif _return == UpdateReturn.Both:
            return diff, config
        else:
            return config


class MapExtended(Map[D], _ty.Mapping[str, D], _ty.Generic[D]):
    ...
