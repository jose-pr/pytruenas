# pytruenas

[![PyPI version](https://img.shields.io/pypi/v/pytruenas.svg)](https://pypi.org/project/pytruenas/)
[![Python versions](https://img.shields.io/pypi/pyversions/pytruenas.svg)](https://pypi.org/project/pytruenas/)
[![Documentation](https://img.shields.io/badge/docs-jose--pr.github.io%2Fpytruenas-blue.svg)](https://jose-pr.github.io/pytruenas/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/jose-pr/pytruenas/blob/main/LICENSE)

A typed, Pythonic client and CLI for the [TrueNAS](https://www.truenas.com/)
middleware API.

`pytruenas` speaks the middleware's JSON-RPC 2.0 websocket protocol directly —
over `wss://`/`ws://` to a remote host, or over the local unix socket
(`ws+unix://`) when running on the NAS itself. It exposes the whole API surface
through an attribute-style namespace, adds convenience helpers for the common
create/update/upsert patterns, a remote-filesystem abstraction, an optional
typings generator, and a small CLI for scripting host configuration.

Running commands and reading files is delegated to
[hostctl](https://github.com/jose-pr/hostctl): a client is a `hostctl` host, so
`run()` and `path()` pick whichever transport a target actually offers rather
than assuming one.

## Install

```sh
pip install pytruenas
```

Optional extras:

| Extra | Enables |
| ----- | ------- |
| `pytruenas[ssh]` | SSH commands + the SFTP filesystem leg (`asyncssh`) |
| `pytruenas[config]` | YAML config/targets file for the CLI (`pyyaml`) |
| `pytruenas[codegen]` | `generate-typings` command (`jinja2`) |
| `pytruenas[repo]` | `deploy --source repo` (`pathspec`, `tomli` below 3.11) |

## Quickstart

```python
from pytruenas import TrueNASClient

# Remote host (api key, or "user:password", or a token)
client = TrueNASClient("nas.example.com", "1-<64-char-api-key>", sslverify=False)

# Attribute-style access to any API namespace/method:
for user in client.api.user.query():
    print(user["username"])

# Convenience helpers for common DB patterns:
client.api.user._upsert("username", username="svc", full_name="Service", group_create=True)

# Running on the NAS itself talks to the local unix socket, no auth:
local = TrueNASClient()            # ws+unix:///var/run/middleware/middlewared.sock
print(local.api.system.info())
```

### Commands and files

`run()` and `path()` are inherited from `hostctl`, which selects a transport
rather than assuming one:

```python
client = TrueNASClient("nas.example.com", api_key, shell="ssh://root@nas.example.com")

client.run("zpool status", capture_output="stdout", encoding="utf-8").stdout
client.path("/mnt/tank/notes.txt").read_text()

client.capabilities      # {"run", "path"} -- what this target can actually do
client.last_selection    # which transport served the last run(), and why
```

| target | commands | files |
| --- | --- | --- |
| on the NAS | `local` (plain `subprocess`) | `local` |
| remote, SSH configured | `ssh`, then `webshell` | `sftp`, then `tnasws` |
| remote, no SSH | `webshell` | `tnasws` |

`webshell` runs commands over `/websocket/shell` — the same PTY the web UI's
Shell page uses — so a host reachable on the API port but **not** on 22 (NAT, a
firewall allowing only 443) can still run commands. Name providers explicitly
with `executor=` / `path=` to force or exclude one.

Because it is a real terminal rather than a pipe, a few things are worth
knowing:

- **Output you do not capture is streamed** to `stdout` (default
  `sys.stdout.buffer`) as it arrives, in raw bytes — so a long command reports
  progress, and colour survives. A captured `.stdout` is cleaned text.
- **stderr is separated when it can be.** A PTY has one stream, so pytruenas
  wraps the command to fence its stderr in terminal escape markers and splits
  them back out. This needs a shell with process substitution (bash/zsh/ksh);
  the shell is read from `auth.me()`, and output stays merged when it is
  something else — `.stderr` is then `None`.
- **Input works in two shapes.** `input=` is delivered as a here-document and
  is the reliable one. `stdin=` accepts a readable object and pumps it in the
  background, for data you are still producing; it races the terminal's echo,
  so prefer `input=` when the data is known up front.

### Credentials

`TrueNASClient(target, credentials)` accepts, for the second argument:

- an **API key** string `"<id>-<64 chars>"`,
- `"user:password"` (optionally `"user:password\n<otp>"`),
- a **token** string,
- a `(user, password)` tuple,
- `None` / omitted → local socket auth.

`Credentials.from_env()` reads `TN_CREDS`. Credentials may also travel in the
target (`wss://root:secret@nas`); an OTP follows the password after a newline,
percent-encoded in a URI as `%0A`.

## CLI

```sh
pytruenas --help
pytruenas query user -f username=root nas.example.com
pytruenas call system.info nas.example.com          # any method by dotted name
pytruenas dump-api nas.example.com > api.json
pytruenas generate-typings --path typings --api-version v26.0.0 nas.example.com
pytruenas deploy nas.example.com                    # install pytruenas ON the host
```

The target host(s) are the **trailing positional arguments** — a command's own
positionals (like `query`'s namespace) come first, then the hosts. Each target
may be comma-separated and supports `[A-Z]`/`[0-9]` range expansion (e.g.
`'nas[1-3].example.com'`); with no target the command runs against `localhost`.
`--parallel N` runs several targets concurrently. Filter `query` with
`-f/--filter KEY=VALUE` (repeatable).

## Running on the appliance

TrueNAS has a read-only root and no `pip`, so `deploy` bootstraps instead: it
asks the target which distributions it already has, bundles only the
difference, and copies that over. In practice that is five pure-Python packages
under a megabyte — the appliance already ships `requests`, `websocket-client`,
`pyyaml`, `asyncssh` and `jinja2`.

```sh
pytruenas deploy nas.example.com                 # a single executable .pyz
pytruenas deploy --mode dir nas.example.com      # an unpacked bin/ + lib/ tree
pytruenas deploy nas.example.com -- call system.info   # install, then run there
```

Everything after `--` runs on the target once it is installed. The default
destination is under `/var/db/system`, which is a dataset on a *data* pool and
so survives an update — unlike `/var/db` itself, `/root` or `/data`, which live
in the boot environment and are replaced by one. A digest is recorded beside
the payload, so redeploying verifies instead of re-copying; `--force` overrides.

When pytruenas is a *dependency* of your own tool rather than the thing being
deployed, name yours as the root: `--pkg-root mytool` (or `PYTRUENAS_PKG_ROOT`),
and your package ships with pytruenas bundled underneath it.

`--source repo` ships a working tree as-is instead of an installed dependency
closure — the files a clone would have, filtered by whichever of `.gitignore`,
`.ignore` and `.bundleignore` are present, with nothing needing to be installed
locally first (needs `pytruenas[repo]`):

```sh
pytruenas deploy --source repo --repo-root . nas.example.com
```

## Typings generator

`generate-typings` turns a host's API definition into a package of `.pyi` stubs
so editors and type checkers understand `client.api.<namespace>.<method>(...)`.
It is validated against the full real API (every version in a live dump).

```sh
pytruenas generate-typings --path truenasapi_typings/current nas.example.com
```

## Development

```sh
py -3.14 -m venv .venv/3.14-nt-amd64
.venv/3.14-nt-amd64/Scripts/python -m pip install -e ".[dev,ssh,config,codegen]"
.venv/3.14-nt-amd64/Scripts/python -m pytest
```

Supports Python 3.9+. The `run()` tests need a POSIX shell and skip on Windows,
so verify anything touching command or path dispatch on a real target.

## License

MIT — see [LICENSE](LICENSE).
