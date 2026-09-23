# Connecting

`TrueNASClient(target, credentials=None, ...)` opens (lazily) a websocket to the
middleware. The transport is chosen from `target`:

| `target` | Transport |
| --- | --- |
| `"nas.example.com"` | `wss://nas.example.com/api/current` (TLS) |
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

Construction never touches the network, so a bad hostname raises on first
*use*, not at construction. A target that names neither scheme nor API path
resolves to **TLS and the current API**: `nas.example.com` means
`wss://nas.example.com/api/current`. Plaintext is never chosen for you — ask
for it with `ws://` (or `http://`, the same transport) — and a different API
version comes from `version=` or a path in the target.

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

### Host keys

The SSH leg — both commands and SFTP — verifies the server's host key against
`~/.ssh/known_hosts`. For a NAS that is not listed there, either add it
(`ssh-keyscan nas >> ~/.ssh/known_hosts`) or choose a policy with `known_hosts=`:

```python
TrueNASClient("nas", api_key, shell="ssh://root@nas", known_hosts=None)            # do not check
TrueNASClient("nas", api_key, shell="ssh://root@nas", known_hosts="/srv/known_hosts")  # this file
```

For a lab box with a self-signed certificate and an unrecorded host key,
`verify=False` turns off both checks at once (TLS certificate verification
everywhere, and SSH host-key verification):

```python
TrueNASClient("nas", api_key, shell="ssh://root@nas", verify=False)
```

`sslverify=` and `known_hosts=` still override it individually.

Certificates are checked against the operating system's trust store, the same
for the API websocket, uploads/downloads and the web shell. To trust a private
CA without adding it to the OS, point `sslverify=` at its bundle, or set
`SSL_CERT_FILE` (also honored: `REQUESTS_CA_BUNDLE`, `CURL_CA_BUNDLE`,
`WEBSOCKET_CLIENT_CA_BUNDLE`, first one set wins). A bundle replaces the OS
store rather than adding to it.

```python
TrueNASClient("nas", api_key, sslverify="/etc/pki/lab-ca.pem")
```

`known_hosts=` applies to the SSH leg built from `shell=` and to the one
`install_sshcreds()` wires in; an `ssh=SshConfig(...)` you build yourself keeps
its own setting. When the key cannot be verified (or SSH is unreachable),
commands and file operations fall back to the websocket transports, and the
client logs a warning the first time `run()` does so.

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
