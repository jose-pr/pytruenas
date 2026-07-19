# Connecting

`TrueNASClient(target, creds=None, ...)` opens (lazily) a websocket to the
middleware. The transport is chosen from `target`:

| `target` | Transport |
| --- | --- |
| `"nas.example.com"` | `wss://` (TLS) or `ws://`, auto-probed |
| `"wss://nas/api/current"` | explicit TLS websocket |
| `"ws+unix:///var/run/middleware/middlewared.sock"` | local unix socket |
| `None` / omitted | the local unix socket |

```python
from pytruenas import TrueNASClient

client = TrueNASClient("nas.example.com", "1-<64-char-api-key>", sslverify=False)
```

## Credentials

The `creds` argument accepts:

- an **API key** string `"<id>-<64 chars>"`,
- `"user:password"` (optionally `"user:password\n<otp>"`),
- a **token** string,
- a `(user, password)` tuple,
- `None` — local socket auth (the root-owned socket authenticates by ownership,
  so no credentials are needed when running on the NAS).

`Credentials.from_env()` reads the `TN_CREDS` environment variable.

## Login timing

By default the client logs in lazily on first use (`autologin=True`). Pass
`autologin=False` to construct without connecting — useful in tests, or when you
only want `client.path(...)` / `client.run(...)` and no API call.

```python
local = TrueNASClient(autologin=False)   # no connection yet
local.login()                            # connect + authenticate explicitly
```

See the [Client API](../api/client.md) for the full constructor.
