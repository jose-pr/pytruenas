class SqlFilter:

    def __init__(self, operator: str, rhs):
        self._sqlfilter_ = (operator, rhs)

    @classmethod
    def filter(cls, lhs: str, filter: object):
        sqlfilter = getattr(filter, "_sqlfilter_", None)
        if not sqlfilter:
            sqlfilter = EQ(filter)._sqlfilter_
        return sqlfilter(lhs) if callable(sqlfilter) else (lhs, *sqlfilter)


class EQ(SqlFilter):
    def __init__(self, rhs):
        super().__init__("=", rhs)

class NE(SqlFilter):
    def __init__(self, rhs):
        super().__init__("!=", rhs)

class RE(SqlFilter):
    def __init__(self, rhs):
        super().__init__('~', rhs)

class GT(SqlFilter):
    def __init__(self, rhs):
        super().__init__('>', rhs)

class GE(SqlFilter):
    def __init__(self, rhs):
        super().__init__('>=', rhs)
class LT(SqlFilter):
    def __init__(self, rhs):
        super().__init__('<', rhs)

class LE(SqlFilter):
    def __init__(self, rhs):
        super().__init__('<=', rhs)

class IN(SqlFilter):
    def __init__(self, rhs):
        super().__init__('in', rhs)

class NIN(SqlFilter):
    def __init__(self, rhs):
        super().__init__('nin', rhs)

def filter_from_kwargs(**kwargs):
    return [SqlFilter.filter(name, filter) for name, filter in kwargs.items()]
