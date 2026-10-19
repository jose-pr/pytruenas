# Connecting

`TrueNASClient(target, credentials=None, ...)` opens (lazily) a websocket to the
middleware. The transport is chosen from `target`:

| `target` | Transport |
| --- | --- |
| `"nas.example.com"` | `wss://nas.example.com/api/current` (TLS) |
| `"wss://nas/api/current"` | explicit TLS websocket |
| `"ws+unix:///var/run/middleware/middlewared.sock"` | local unix socket |
| `"/var/run/middleware/middlewared.sock"` | the same socket, as a path |
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
(`ssh-keyscan nas >> ~/.ssh/known_hosts`) or name the file of trusted keys with
`known_hosts=`:

```python
TrueNASClient("nas", api_key, shell="ssh://root@nas", known_hosts="/srv/known_hosts")
```

For a lab box with a self-signed certificate and an unrecorded host key,
`verify=False` turns off both checks at once (TLS certificate verification
everywhere, and SSH host-key verification). It is the only way to skip the
host-key check; `known_hosts=None` raises `ValueError`.

```python
TrueNASClient("nas", api_key, shell="ssh://root@nas", verify=False)                  # check nothing
TrueNASClient("nas", api_key, shell="ssh://root@nas", verify=False, sslverify=True)  # TLS only
TrueNASClient("nas", api_key, shell="ssh://root@nas", sslverify=False)               # host keys only
```

`sslverify=` overrides `verify` for TLS. Keys named with `known_hosts=` are
checked even under `verify=False`: the stricter setting wins.

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
`install_sshcreds()` wires in; an `ssh=SSHConfig(...)` you build yourself keeps
its own `known_hosts`, and `verify=False` reaches it on a copy. When the key cannot be verified (or SSH is unreachable),
commands and file operations fall back to the websocket transports, and the
client logs a warning the first time `run()` does so.

The SSH leg reads your `~/.ssh/config`, as `ssh` does: a host alias,
`HostName`, `Port`, `User`, `IdentityFile`, `ProxyJump` or `ProxyCommand` there
applies to commands and file operations alike. A user or port written in
`shell=` wins over the file; with no user in either, pytruenas logs in as
`root`, TrueNAS's administrative account, on port 22.

```python
TrueNASClient("nas", api_key, shell="nas")                 # ~/.ssh/config's User, else root
TrueNASClient("nas", api_key, shell="ssh://admin@nas")     # admin, whatever the file says
```

For a connection that depends on no personal file, build the leg yourself with
`ssh_config=None`, or name another file with a `pathlib.Path` (a plain string
is configuration *text*, not a file name):

```python
from pathlib import Path
from hostctl import SSHConfig

TrueNASClient("nas", api_key, ssh=SSHConfig("nas", username="root", ssh_config=None))
TrueNASClient("nas", api_key, ssh=SSHConfig("nas", ssh_config=Path("lab/ssh_config")))
```

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
