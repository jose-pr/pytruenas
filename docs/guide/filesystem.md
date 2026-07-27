# Filesystem paths

`client.path(...)` returns a [`pathlib_next`](https://pypi.org/project/pathlib_next/)
`Path` object for a location on the target:

```python
p = client.path("/mnt/tank/data/report.txt")
if p.exists():
    data = p.read_bytes()
p.with_name("report.bak").write_bytes(data)
```

## Local vs remote backends

- For a **local** target, `client.path(...)` is an ordinary local `Path`.
- For a **remote** target it is a `TruenasPath`, which prefers **SFTP** (via the
  `ssh` extra's `asyncssh` backend) and falls back to the middleware
  `filesystem.*` websocket API for operations SFTP doesn't cover cleanly
  (delete/rename/symlink).

```bash
pip install pytruenas[ssh]     # enables the SFTP backend
```

Choose a provider for one call with `client.path(..., backend="sftp")`, or set
the whole preference order at construction with
`path=["sftp", "tnasws"]` — see [Running commands](commands.md#choosing-the-transport-yourself).
Valid path providers are `local`, `sftp`, and `tnasws`.

## Examples

Paths behave like `pathlib.Path`, so most of what you know transfers:

```python
p = client.path("/mnt/tank/config/app.conf")

p.read_text()
p.write_text("key = value\n")
p.exists(), p.is_file(), p.stat().st_size

# Parents, joining, and globbing all work
(p.parent / "backup.conf").write_bytes(p.read_bytes())
for conf in client.path("/mnt/tank/config").glob("*.conf"):
    print(conf.name, conf.stat().st_mtime)
```

Walking a tree and copying between hosts:

```python
src = client.path("/mnt/tank/data")
for root, dirs, files in src.walk():
    for name in files:
        print(root / name)

# `pathlib_next` copies across backends, so this crosses machines
local_copy = pathlib.Path("/tmp/app.conf")
client.path("/mnt/tank/config/app.conf").copy(local_copy)
```

Creating directories and cleaning up:

```python
d = client.path("/mnt/tank/scratch/run-42")
d.mkdir(parents=True, exist_ok=True)
(d / "log.txt").write_text("started\n")

d.rm(recursive=True, missing_ok=True)   # pytruenas convenience
```

## What needs SFTP

The middleware `filesystem.*` API has no symlink, rename, or realpath
operation, so these need the `ssh` extra and a reachable SSH leg. Without one
they raise `NotImplementedError` rather than failing silently:

| operation | `sftp` | `tnasws` |
| --- | --- | --- |
| read/write/stat/mkdir/chmod | ✅ | ✅ |
| `unlink`/`rmdir` | ✅ | ✅ (shells out) |
| `rename` | ✅ | ❌ |
| `symlink_to` / `readlink` | ✅ | ❌ |
| `resolve` | ✅ | returns the path unchanged |

`symlink_to` takes a pytruenas-specific `force=` that removes a conflicting
target first — a bool, a file-type string, or a set of
`"file"`/`"link"`/`"directory"`:

```python
link = client.path("/mnt/tank/current")
link.symlink_to("/mnt/tank/releases/v2", force="link")   # replace only a symlink
```

!!! note
    SFTP concurrency and transport details come from `pathlib_next`; pytruenas
    just selects and wires the backend. The `ssh` extra requires
    `pathlib_next[sftp-async] >= 0.8.3`.

See the [Filesystem API](../api/fs.md).
