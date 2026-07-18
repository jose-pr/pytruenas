# pytruenas

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
pip install pytruenas
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
pytruenas -t nas.example.com query -q username=root user
pytruenas -t nas.example.com dump-api > api.json
pytruenas -t nas.example.com generate-typings --path typings --api-version v26.0.0
```

`-t/--target` may be repeated or comma-separated and supports `[A-Z]`/`[0-9]`
range expansion (e.g. `-t nas[1-3].example.com`); `--parallel N` runs several
targets concurrently.

## Typings generator

`generate-typings` turns a host's API definition into a package of `.pyi` stubs
so editors and type checkers understand `client.api.<namespace>.<method>(...)`.
It is validated against the full real API (every version in a live dump).

```sh
pytruenas -t nas.example.com generate-typings --path truenasapi_typings/current
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
