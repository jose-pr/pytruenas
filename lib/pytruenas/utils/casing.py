import keyword as _kw


def pysafe(name:str, separator:str = '.'):
        return separator.join(
            [(f"{n}_" if _kw.iskeyword(n) else n) for n in name.split(separator)]
        )

def camelspace(name:str, separator:str = '.'):
    return separator.join([p.capitalize() for p in pysafe(name).split(separator)])