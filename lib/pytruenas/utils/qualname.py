from . import casing as _casing

import keyword as _kw
import typing as _ty


def pysafe(name: str, separator: str = "."):
    return separator.join(
        [(f"{n}_" if _kw.iskeyword(n) else n) for n in name.split(separator)]
    )


def camelspace(name: str, separator: str = "."):
    return separator.join([p.capitalize() for p in pysafe(name).split(separator)])


class QualName:

    @property
    def parts(self) -> _ty.Sequence[str]:
        raise NotImplementedError()

    @property
    def name(self):
        return self.parts[-1]

    @property
    def parent(self):
        return self.qualjoin(self.parts[:-1])

    @classmethod
    def _qualparts(cls, *parts: "str|_ty.Iterable[str]|QualName"):
        _parts: list[str] = []
        for part in parts:
            if hasattr(part, "parts"):
                _parts.extend(_ty.cast(QualName, part).parts)
            elif isinstance(part, str):
                _parts.append(part)
            else:
                _parts.extend(_ty.cast(list, part))
        return [part for part in _parts if part]

    @classmethod
    def qualjoin(cls, *parts: "str|_ty.Iterable[str]|QualName"):
        return cls._qualjoin(cls._qualparts(*parts))

    @classmethod
    def qualsplit(cls, name: "str|QualName"):
        if hasattr(name, "parts"):
            return _ty.cast(QualName, name).parts
        return cls._qualsplit(_ty.cast(str, name))

    def with_name(self, name: str):
        return self.qualjoin(self.parent, name)

    @classmethod
    def _qualsplit(cls, name: "str") -> list[str]:
        raise NotImplementedError()

    @classmethod
    def _qualjoin(cls, parts: list["str"]) -> "_ty.Self":
        raise NotImplementedError()

    def __truediv__(self, key):
        return self.qualjoin(self, key)

    def relative_to(self, name: "QualName"):
        parts = [*self.parts]
        other = name.parts

        if len(other) > len(parts):
            raise ValueError(other)

        idx = 0

        for idx, part in enumerate(other):
            if parts[idx] != part:
                raise ValueError(other, idx)

        return self.qualjoin(*parts[idx + 1 :])

    def camelcase(self, start=0, end: int | None = None):
        parts = self.parts
        camelcased = "".join(
            [
                part[0].upper() + part[1:]
                for part in parts[start : len(parts) if end is None else end]
            ]
        )
        if camelcased:
            for sep in [".", "_", "-"]:
                camelcased = "".join([part[0].upper() + part[1:] for part in camelcased.split(sep)])
        return camelcased


class DotQualNamed(QualName, str):
    SEPARATOR: str = "."

    @property
    def parts(self):
        return self._qualsplit(self)

    @classmethod
    def _qualsplit(cls, name: "str"):
        split = name.split(cls.SEPARATOR)
        if split == [""]:
            return []
        return split

    @classmethod
    def _qualjoin(cls, parts: list[str]):
        return cls(cls.SEPARATOR.join(parts))


class PythonName(DotQualNamed):

    @classmethod
    def new(cls, *parts: str | QualName, sanitize: bool = True):
        name = cls.qualjoin(*parts)
        if sanitize:
            name = pysafe(name)

        return PythonName(name)

    def as_path(self):
        return "/".join(self.parts)
