# Running commands

The middleware's JSON-RPC API has no generic command-exec method, so
`client.run(...)` reaches the target over whichever transport is actually
available. Rather than a fixed local-or-SSH branch, the client composes a list
of executors and picks the first usable one:

| target | executors, in order |
| --- | --- |
| the NAS you are running on | `local` |
| remote, SSH configured | `ssh`, then `webshell` |
| remote, no SSH | `webshell` |

```python
result = client.run("zpool status", capture_output="stdout", encoding="utf-8")
print(result.stdout)
```

`run()` returns a `subprocess.CompletedProcess`. Highlights:

- Multiple positional commands are joined by the shell's separator. A command
  given as a `list`/`tuple` is shell-quoted piece by piece; a leading
  `pathlib.PurePath` marks a direct executable whose trailing values are argv.
- `capture_output` may be `True` (both streams), `"stdout"`, `"stderr"`, or
  `False`.
- `input=` feeds stdin (str or bytes); a file-like `stdin=` is drained.
- `cwd=`, `env=`, `check=`, `timeout=`, `encoding=`/`errors=` behave as with
  `subprocess.run`.
- `executable=` overrides the shell.

```python
client.run("cat > /tmp/x", input="hello\n", encoding="utf-8")
```

## Which transport ran it

`client.host.last_selection` records what was tried and why, with credentials
redacted — useful when a command took an unexpected route:

```python
client.run("uptime")
[t["provider"] for t in client.host.last_selection if t["chosen"]]
# ['ssh']
```

`client.host.capabilities` reports whether `run` is available at all, so a
caller can check up front instead of discovering it mid-command.

## The web shell

A remote host reachable on the API port but **not** on 22 — NAT without a
forwarded port, a firewall allowing only 443, an appliance behind a reverse
proxy — has no SSH to fall back on. For those, `run()` uses `/websocket/shell`,
the same PTY the web UI's Shell page drives.

It is ranked below SSH deliberately, because a PTY is a single terminal stream
rather than a pair of clean channels:

- **stdout and stderr are merged.** `capture_output="stderr"` cannot be
  honoured; everything arrives on `stdout`.
- **`input=` is not supported.** Encode the payload into the command itself —
  a pipe or a here-string works, being ordinary shell syntax:

    ```python
    client.run("tr a-z A-Z <<< 'shout'")     # fine
    client.run("printf 'x\\n' | tr a-z A-Z")  # also fine
    ```

- **Commands must be single-line.** An embedded newline submits a partial line
  to the terminal and desynchronises the session, so it is rejected rather than
  silently mangled.
- The exit status is recovered from the terminal stream, and terminal escape
  sequences are stripped from the output.

Pass `webshell=False` when building the configuration to decline it — a remote
host without SSH then honestly reports no `run` capability instead of falling
back to a PTY:

```python
from pytruenas.host import TrueNASConfig

config = TrueNASConfig.from_target("wss://nas", webshell=False)
```

!!! note
    SSH execution and the SFTP leg of `client.path(...)` need the `ssh` extra:
    `pip install pytruenas[ssh]`. The web shell does not — it runs over the
    same websocket connection as the API.
