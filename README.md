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

## Install

```sh
pip install pytruenas          # once published to PyPI
# or, from a checkout:
pip install .
```

Optional extras:

| Extra | Enables |
| ----- | ------- |
| `pytruenas[ssh]` | Remote shell + SFTP filesystem backend (`asyncssh`) |
| `pytruenas[config]` | YAML config/targets file for the CLI (`pyyaml`) |
| `pytruenas[codegen]` | `generate-typings` command (`jinja2`) |
| `pytruenas[host]` | Local network-adapter / packaging helpers (`ifaddr`) |

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

### Credentials

`TrueNASClient(target, creds)` accepts, for `creds`:

- an **API key** string `"<id>-<64 chars>"`,
- `"user:password"` (optionally `"user:password\n<otp>"`),
- a **token** string,
- a `(user, password)` tuple,
- `None` / omitted → local socket auth.

`Credentials.from_env()` reads `TN_CREDS`.

## CLI

```sh
pytruenas --help
pytruenas query user -f username=root nas.example.com
pytruenas dump-api nas.example.com > api.json
pytruenas generate-typings --path typings --api-version v26.0.0 nas.example.com
```

The target host(s) are the **trailing positional arguments** — a command's own
positionals (like `query`'s namespace) come first, then the hosts. Each target
may be comma-separated and supports `[A-Z]`/`[0-9]` range expansion (e.g.
`'nas[1-3].example.com'`); with no target the command runs against `localhost`.
`--parallel N` runs several targets concurrently. Filter `query` with
`-f/--filter KEY=VALUE` (repeatable).

## Typings generator

`generate-typings` turns a host's API definition into a package of `.pyi` stubs
so editors and type checkers understand `client.api.<namespace>.<method>(...)`.
It is validated against the full real API (every version in a live dump).

```sh
pytruenas generate-typings --path truenasapi_typings/current nas.example.com
```

## Development

```sh
py -3.14 -m venv .venv
.venv/Scripts/python -m pip install -e .[dev]
.venv/Scripts/python -m pytest
```

Supports Python 3.9+.

## License

MIT — see [LICENSE](LICENSE).
