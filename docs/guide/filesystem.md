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

Choose a backend explicitly with `client.path(..., backend="sftp")` or set the
client's `fsbackend` (default `"auto"`).

!!! note
    SFTP concurrency and transport details come from `pathlib_next`; pytruenas
    just selects and wires the backend. The `ssh` extra requires
    `pathlib_next[sftp-async] >= 0.8.3`.

See the [Filesystem API](../api/fs.md).
