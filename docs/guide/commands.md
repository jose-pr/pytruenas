# Running commands

The middleware API has no generic command-exec method, so `client.run(...)`
executes shell commands either **locally** (when the client targets the NAS it
runs on) or **over SSH** (remote targets, via the `ssh` extra's `asyncssh`).

```python
result = client.run("zpool status", capture_output="stdout", encoding="utf-8")
print(result.stdout)
```

`run()` returns a `subprocess.CompletedProcess`. Highlights:

- Multiple positional commands are joined with `;`. A command given as a
  `list`/`tuple` is shell-quoted piece by piece.
- `capture_output` may be `True` (both streams), `"stdout"`, `"stderr"`, or
  `False`.
- `input=` feeds stdin (str or bytes); a file-like `stdin=` is drained.
- `cwd=`, `env=`, `check=`, `timeout=`, `encoding=`/`errors=` behave as with
  `subprocess.run`.
- `executable=` overrides the shell; otherwise the target root's login shell is
  used (falling back to `/bin/bash`).

!!! note
    Remote execution needs the `ssh` extra: `pip install pytruenas[ssh]`.

```python
# feed a heredoc-style payload to a remote command
client.run("cat > /tmp/x", input="hello\n", encoding="utf-8")
```
