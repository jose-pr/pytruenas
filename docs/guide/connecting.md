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

Credentials may also travel in the target itself
(`wss://root:secret@nas`). An OTP follows the password after a newline — but a
**URI must percent-encode it as `%0A`**:

```python
TrueNASClient("wss://root:secret%0Aotp:123456@nas")
```

A newline is used as the separator because a password can never contain one
(pressing Enter submits the value rather than typing into it), so it splits the
field without stealing a character or needing an escaping scheme.

## Login timing

By default the client logs in lazily on first use (`autologin=True`). Pass
`autologin=False` to construct without connecting — useful in tests, or when you
only want `client.path(...)` / `client.run(...)` and no API call.

Construction never touches the network: when the scheme (`ws` vs `wss`) or the
API path is not given explicitly, both are probed on first connect rather than
in the constructor. A bad hostname therefore raises on first *use*, not at
construction.

## The SSH leg

`client.run(...)` and the SFTP half of `client.path(...)` can use a separate SSH
connection, configured by the `shell=` argument and stored as
`client.config.ssh`:

```python
client = TrueNASClient("nas", api_key, shell="ssh://root@nas")
```

Omit it and the client falls back to the web shell for a remote target — see
[Running commands](commands.md). `client.install_sshcreds()` provisions a
keypair, installs it on root's `authorized_keys`, and wires it in for you.

!!! note
    The `shell=` argument was also readable as `client.shell` before the move
    to [hostctl](https://github.com/jose-pr/hostctl). `.shell` now means the
    *bound shell object* (`client.shell.run(...)`), as it does throughout
    hostctl, so the connection target lives on the configuration instead.

```python
local = TrueNASClient(autologin=False)   # no connection yet
local.login()                            # connect + authenticate explicitly
```

See the [Client API](../api/client.md) for the full constructor.
