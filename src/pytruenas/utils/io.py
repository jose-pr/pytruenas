from __future__ import annotations

# NOTE: a `STAT_FIELDS` constant used to live here, derived by stat-ing this
# very file at import time and regex-parsing the repr of the result. It was
# already dead -- the `fs/api.py` code that consumed it is gone -- and it made
# importing this module do filesystem I/O, which is why it was found: from a
# zipapp `__file__` is a path INSIDE the archive, so the stat raised
# `NotADirectoryError` and pytruenas could not be imported at all once
# deployed. If something needs the field names again, `os.stat_result` exposes
# them directly (mind that it lists the `_ns` variants and platform extras,
# which the old repr-scrape did not).


def isbytelike(obj):
    return isinstance(obj, (memoryview, bytes, bytearray))


def bytes_(txt: "bytes|str") -> bytes:
    if isinstance(txt, str):
        return txt.encode()
    return txt


def str_(txt: "bytes|str") -> str:
    if isinstance(txt, str):
        return txt
    return txt.decode()
