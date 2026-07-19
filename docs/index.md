# pytruenas

**pytruenas** is a typed, Pythonic client and CLI for the
[TrueNAS](https://www.truenas.com/) middleware API.

It speaks the middleware's JSON-RPC 2.0 websocket protocol directly — over
`wss://`/`ws://` to a remote host, or over the local unix socket (`ws+unix://`)
when running on the NAS itself — and exposes the whole API surface through an
attribute-style namespace.

## Highlights

- **The whole API, attribute-style.** `client.api.pool.dataset.query(...)` maps
  straight to the middleware method `pool.dataset.query`. No per-endpoint
  wrappers to maintain.
- **Convenience helpers.** `_get`/`_query`/`_create`/`_update`/`_upsert` cover
  the common create-or-update-by-selector patterns without hand-writing the
  query/diff logic each time.
- **Local *and* remote.** The same client talks to a remote host with an API
  key, or to the root-owned local socket with no auth when run on the NAS.
- **Extended-JSON aware.** `datetime`/`date`/`time`/`set`/IP-interface values
  round-trip transparently through the middleware's `ejson` wire format.
- **A filesystem, not just an API.** `client.path("/mnt/tank/x")` returns a
  `pathlib`-style object backed by SFTP (preferred) or the middleware
  `filesystem.*` API.
- **Typings on demand.** `generate-typings` produces `.pyi` stubs for the whole
  API so editors and type checkers understand every call.
- **Python 3.9+**, tested on 3.9 and 3.14, and validated live against a real
  TrueNAS 26.0 host.

## Install

```bash
pip install pytruenas          # once published to PyPI
# or from a checkout:
pip install .
```

Optional extras: `pytruenas[ssh]` (remote shell + SFTP), `pytruenas[config]`
(YAML CLI config), `pytruenas[codegen]` (`generate-typings`), `pytruenas[host]`
(local network/packaging helpers).

## Quickstart

```python
from pytruenas import TrueNASClient

# Remote host (API key, "user:password", or a token):
client = TrueNASClient("nas.example.com", "1-<64-char-api-key>", sslverify=False)
for user in client.api.user.query():
    print(user["username"])

# Running ON the NAS talks to the local socket, no auth:
local = TrueNASClient()      # ws+unix:///var/run/middleware/middlewared.sock
print(local.api.system.info())
```

Continue with the [Connecting](guide/connecting.md) guide.
