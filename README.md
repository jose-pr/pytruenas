# pytruenas

A typed, Pythonic client and CLI for the [TrueNAS](https://www.truenas.com/)
middleware API.

`pytruenas` speaks the middleware's JSON-RPC 2.0 websocket protocol directly —
over `ws://`/`wss://` to a remote host, or over the local unix socket
(`ws+unix://`) when running on the NAS itself. It exposes the whole API surface
through an attribute-style namespace (`client.api.user.query(...)`), a small set
of convenience helpers for the common create/update/upsert patterns, a remote
filesystem abstraction, and a CLI for scripting host configuration.

```python
from pytruenas import TrueNASClient

client = TrueNASClient("nas.example.com", "root:password")
for user in client.api.user.query():
    print(user["username"])
```

See `docs/` for details. Install with `pip install pytruenas`.

## License

MIT — see [LICENSE](LICENSE).
