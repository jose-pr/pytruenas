import typing as _ty


class _Exclude: ...


EXCLUDE = _Exclude()


class QueryFilter:

    def __init__(self, operator: str, rhs):
        self._queryfilter_ = (operator, rhs)

    @classmethod
    def filter(cls, lhs: str, filter: object):
        sqlfilter = getattr(filter, "_queryfilter_", None)
        if not sqlfilter:
            sqlfilter = EQ(filter)._queryfilter_
        return sqlfilter(lhs) if callable(sqlfilter) else (lhs, *sqlfilter)


class EQ(QueryFilter):
    def __init__(self, rhs):
        super().__init__("=", rhs)


class NE(QueryFilter):
    def __init__(self, rhs):
        super().__init__("!=", rhs)


class RE(QueryFilter):
    def __init__(self, rhs):
        super().__init__("~", rhs)


class GT(QueryFilter):
    def __init__(self, rhs):
        super().__init__(">", rhs)


class GE(QueryFilter):
    def __init__(self, rhs):
        super().__init__(">=", rhs)


class LT(QueryFilter):
    def __init__(self, rhs):
        super().__init__("<", rhs)


class LE(QueryFilter):
    def __init__(self, rhs):
        super().__init__("<=", rhs)


class IN(QueryFilter):
    def __init__(self, rhs):
        super().__init__("in", rhs)


class NIN(QueryFilter):
    def __init__(self, rhs):
        super().__init__("nin", rhs)


def filter_from_kwargs(**kwargs):
    return [
        QueryFilter.filter(name, filter)
        for name, filter in kwargs.items()
        if filter is not EXCLUDE
    ]


class Option:
    def __init__(self, name: str, value):
        self.name = name
        self.value = value

    def _options_(self, dict: dict):
        dict[self.name] = self.value

    @classmethod
    def options(cls, *opts: "Option|object"):
        opts_ = {}
        for opt in opts:
            if hasattr(opt, "_options_"):
                opt._options_(opts_)
            elif isinstance(opt, _ty.Mapping):
                opts_.update(opt)
            elif isinstance(opt, (list, tuple)):
                name, val = opt
                opts_[name] = val
            else:
                raise ValueError(opt)
        return opts_
