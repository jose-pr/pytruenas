# The API namespace

`client.api` is a dynamic namespace: attribute access builds a dotted method
name, and calling it invokes that middleware method.

```python
client.api.system.info()                       # -> system.info
client.api.pool.dataset.query([["type", "=", "FILESYSTEM"]])   # -> pool.dataset.query
```

Any method the middleware exposes is reachable this way — there are no
per-endpoint wrappers to keep in sync with TrueNAS.

## Convenience helpers

On top of the raw methods, each namespace offers helpers (prefixed `_`) for the
patterns you'd otherwise hand-write:

| Helper | Does |
| --- | --- |
| `._query(**filters)` | `query` with filters built from keyword args |
| `._get(id)` / `._get(**filters)` | one record by id or filter, or `None` |
| `._create(**fields)` | `create` |
| `._update(selector, **fields)` | `update`, diffing against current state |
| `._upsert(selector, **fields)` | create if absent, else update the diff |

```python
# Filters from kwargs, with operator helpers:
from pytruenas.utils import query as q
admins = client.api.user._query(uid=q.GT(0), locked=False)

# Fetch-or-None:
root = client.api.user._get(username="root")     # dict, or None if missing

# Create-or-update by a selector field:
client.api.user._upsert("username", username="svc", full_name="Service")
```

`_upsert(selector, ...)` resolves the row by the `selector` field(s); if it
exists the changed fields are updated (a no-op diff makes no call), otherwise the
record is created. A middleware job returned by a mutating call is waited on by
default (`wait=True`).

## Query filters

`pytruenas.utils.query` provides operator wrappers so kwargs map to middleware
filter tuples:

```python
from pytruenas.utils import query as q
q.filter_from_kwargs(username="root", uid=q.GT(0))
# -> [("username", "=", "root"), ("uid", ">", 0)]
```

Available: `EQ`, `NE`, `RE`, `GT`, `GE`, `LT`, `LE`, `IN`, `NIN`.

See the [Namespace API](../api/namespace.md).
