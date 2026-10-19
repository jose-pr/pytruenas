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
client.api.user._upsert(("username",), username="svc", full_name="Service")
```

`_upsert(selector, ...)` resolves the row by the `selector` field(s) — a tuple
or list of field names, matched against the values you pass; if it exists the
changed fields are updated (a no-op diff makes no call), otherwise the record is
created. A bare string or int selector is a **record id**, not a field name
(`_upsert("username", ...)` looks up the record whose id is `"username"`). A
`!`-prefixed name (`("username", "!uid")`) is left out of the match and is not
changed on update; a selector made only of those is rejected, since it would
match the first record in the collection. A middleware job returned by a
mutating call is waited on by default (`wait=True`; pass a callable instead to
receive progress updates).

## Waiting for jobs

Many middleware methods start a *job* and return its id. `client.wait(job_id)`
blocks until it finishes and returns its result; a failed job raises
`pytruenas.connection.JobFailed`. Pass `callback=` to follow progress, or
iterate `client.job_updates(job_id)` yourself:

```python
job_id = client.upload(data, "filesystem.put", "/mnt/tank/big.bin", wait=False)
client.wait(job_id, callback=lambda job: print(
    f"{job['progress']['percent']:3}% {job['progress']['description']}"))

for job in client.job_updates(job_id):      # same updates, as a loop
    bar.update(job["progress"]["percent"])
```

`upload()`, `download()` and the `_create`/`_update`/`_upsert` helpers accept
the same callable as `wait=`.

`job=True` on any call does the same, as it does in the upstream TrueNAS
client: the call waits for the job it starts and returns the job's result.

```python
client.api.pool.dataset.delete("tank/old", job=True)   # returns once deleted
```

Without it the call returns the job id at once. The wait has no deadline unless
`_timeout=` is given.

## Errors

Every error pytruenas raises at run time is a `pytruenas.TrueNASError`:

| Error | Raised when |
| --- | --- |
| `ClientException` | the middleware failed the call (`.errno`, `.extra`) |
| `ValidationErrors` | the server rejected the arguments, per field |
| `CallTimeout` | no answer within the timeout |
| `ConnectionClosed` | the connection dropped before the answer |
| `JobFailed` | a job ended `FAILED` or `ABORTED` |
| `AuthenticationError` | a login was refused |

```python
from pytruenas import TrueNASError, ValidationErrors

try:
    client.api.user._create(username="svc")
except ValidationErrors as error:
    print(error.errors)            # [(attribute, message, errno), ...]
except TrueNASError as error:
    print("TrueNAS refused:", error)
```

A mistake in the call itself — an unknown keyword, a malformed target — is a
plain `TypeError` or `ValueError`. Because `CallTimeout` and `ConnectionClosed`
are `OSError`s, a path's `exists()` reads them as "not there", as it does any
`OSError`.

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
