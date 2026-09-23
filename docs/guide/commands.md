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
  given as a `list`/`tuple` is shell-quoted piece by piece. For a program run
  with **no shell layer**, pass `hostctl.Exec("/bin/ls", "-l")`; a path object
  anywhere else is an ordinary value that stringifies, so one command in a
  sequence cannot silently become the executable.
- `capture_output` may be `True` (both streams), `"stdout"`, `"stderr"`, or
  `False`.
- `input=` feeds stdin (str or bytes); a file-like `stdin=` is drained.
- `cwd=`, `timeout=`, `encoding=`/`errors=` behave as with `subprocess.run`.
  **`check` and `capture_output` do not: both default to `True`** here, so a
  non-zero exit raises `CalledProcessError` unless you pass `check=False`, and
  output is captured rather than inherited.
- `env=` adds to the target's environment rather than replacing it, on every
  transport (a local target included): `env={"A": "1"}` still leaves `PATH` set.
- `executable=` overrides the shell.

```python
client.run("cat > /tmp/x", input="hello\n", encoding="utf-8")
```

## Which transport ran it

`client.last_selection` records what was tried and why, with credentials
redacted — useful when a command took an unexpected route:

```python
client.run("uptime")
[t["provider"] for t in client.last_selection if t["chosen"]]
# ['ssh']
```

`client.capabilities` reports whether `run` is available at all, so a
caller can check up front instead of discovering it mid-command.

## The web shell

A remote host reachable on the API port but **not** on 22 — NAT without a
forwarded port, a firewall allowing only 443, an appliance behind a reverse
proxy — has no SSH to fall back on. For those, `run()` uses `/websocket/shell`,
the same PTY the web UI's Shell page drives.

It is ranked below SSH deliberately: SSH has real channels, while the web
shell drives an interactive terminal. It behaves like any other executor for
`capture_output`, `stdout=`/`stderr=`, `input=`, `text`/`encoding`, `check` and
`timeout`, with these differences:

- **Output is exact.** The command and its input are sent base64-encoded and its
  output is framed by markers the command itself prints, so nothing typed is
  interpreted by the terminal and nothing the terminal draws (the echo, the
  prompt, the login banner) reaches your result. Captured `.stdout` is the
  program's own bytes.
- **Uncaptured stdout is streamed as it arrives** to its target (default
  `sys.stdout.buffer`), within about 0.1 s — a long-running command reports
  progress live.
- **stderr is captured separately** in any POSIX login shell. It is written to
  the remote side and delivered when the command finishes, so a stderr
  *target* receives it at the end rather than live. `stderr=subprocess.STDOUT`
  merges the two as they are produced.
- **stdin is always a file, never the terminal.** `input=` (bytes or str) and a
  readable `stdin=` object — read to EOF first — are delivered through a
  temporary file; with neither, stdin is `/dev/null`, so a command that prompts
  gets EOF instead of hanging. Streaming stdin incrementally is not supported:
  bytes typed into a terminal that the program does not read would be run by
  the shell as the next command. A file *descriptor* (`subprocess.PIPE`) is
  rejected.

    ```python
    client.run("cat", input="hello\n", encoding="utf-8")
    client.run("cat", stdin=open("big.bin", "rb"))   # read in full, then sent
    ```

- `timeout=None` waits indefinitely; on a timeout the command is interrupted,
  the session is closed, and `subprocess.TimeoutExpired` carries the partial
  output (and `orphaned=False`).

## Choosing the transport yourself

`executor=` and `path=` override the defaults, naming providers in preference
order. Each takes a single name or a sequence:

```python
from pytruenas.host import TrueNASConfig

# SSH only -- never fall back to the web shell
TrueNASConfig.from_target("wss://nas", executor=["ssh"], path=["sftp"])

# Prefer the web shell over SSH, for whatever reason
TrueNASConfig.from_target("wss://nas", executor=["webshell", "ssh"])

# Force the websocket filesystem leg on a local target (not offered by default)
TrueNASConfig.from_target(None, path=["local", "tnasws"])

# Refuse to run commands at all
TrueNASConfig.from_target("wss://nas", executor=[])
```

Valid names are `local`, `ssh`, and `webshell` for executors, and `local`,
`sftp`, and `tnasws` for paths. An unknown name raises rather than quietly
composing a host with no provider, and asking for `ssh`/`sftp` without an
`SshConfig` raises too. Omit them (the default) to decide from the target.

!!! note
    SSH execution and the SFTP leg of `client.path(...)` need the `ssh` extra:
    `pip install pytruenas[ssh]`. The web shell does not — it runs over the
    same websocket connection as the API.
