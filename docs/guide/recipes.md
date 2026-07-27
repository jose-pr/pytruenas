# Recipes

Worked examples for things people actually do with a TrueNAS box. Each one is
complete enough to paste and adapt.

## Connect once, reuse

A client opens its websocket lazily and reconnects if the connection drops, so
build one and keep it. As a context manager it also closes the transports it
opened:

```python
from pytruenas import TrueNASClient

with TrueNASClient("nas.example.com", "1-<api-key>") as nas:
    print(nas.ping())                    # "pong"
    print(nas.me()["pw_name"])           # the authenticated session's user
    print(nas.api.system.info()["version"])
```

!!! note
    `me()` returns the *session* user (`auth.me`, keyed `pw_name`), while
    `api.user.query()` returns account records (keyed `username`). They are
    different shapes — an easy mix-up.

## Find things: `query` and its helpers

`query` takes middleware filters directly, but the helpers cover the common
shapes with less ceremony:

```python
# Every dataset on a pool
nas.api.pool.dataset.query([["pool", "=", "tank"]])

# Exactly one, or None
root = nas.api.user._get(username="root")
root["username"], root["uid"]

# One field off each row
names = [u["username"] for u in nas.api.user.query([], {"select": ["username"]})]

# Does it exist?
if nas.api.sharing.smb._get(name="media") is None:
    ...
```

## Create or update, idempotently

`_upsert` picks the selector fields, looks for a match, and creates or updates
accordingly — so a script can run twice without erroring:

```python
nas.api.user._upsert(
    "username",
    username="svc-backup",
    full_name="Backup service",
    group_create=True,
    home="/nonexistent",
)

# Multiple selector fields, as a tuple
nas.api.sharing.nfs._upsert(("path", "enabled"), path="/mnt/tank/media", enabled=True)
```

## Watch for changes

Subscriptions are bounded queues fed by the live connection. Consume with the
iterator, a callback, or both:

```python
sub = nas.subscribe("alert.list")
for event in sub.events(timeout=30):
    print(event.msg, event.fields.get("klass"))
    if event.msg == "removed":
        break
sub.unsubscribe()
```

A subscription is bound to the connection it was made on and does **not**
survive a reconnect — the `events()` iterator ending is that signal, so
re-subscribe there rather than assuming a permanent stream.

## Run a command

```python
result = nas.run("zpool status tank", capture_output="stdout", encoding="utf-8")
print(result.stdout)

# Non-zero is an error unless you say otherwise
nas.run("zpool scrub tank", check=False).returncode
```

Check first if the target might not have a command channel at all:

```python
if "run" in nas.capabilities:
    nas.run("uptime")
else:
    print("no SSH and no web shell — API only")
```

## Upload and download

The side channels move file content through HTTP(S) rather than the websocket:

```python
# Push a config file into a middleware method that takes an upload
nas.upload(open("cert.pem", "rb").read(), "certificate.create", {"name": "web"})

# Pull a debug bundle
data = nas.download("system.debug", filename="debug.tgz")
open("debug.tgz", "wb").write(data)
```

!!! note
    A client connected over the **local unix socket** cannot use `download()`:
    the side channel resolves to `https://localhost` and trips the appliance's
    self-signed certificate. Connect over `wss://` for that.

## Several hosts at once

Nothing special is needed — a client per host, and threads if you want them in
parallel:

```python
from concurrent.futures import ThreadPoolExecutor

HOSTS = ["nas1.example.com", "nas2.example.com", "nas3.example.com"]

def version(host):
    with TrueNASClient(host, api_key) as nas:
        return host, nas.api.system.info()["version"]

with ThreadPoolExecutor() as pool:
    for host, ver in pool.map(version, HOSTS):
        print(f"{host}: {ver}")
```

The CLI does this for you — see [CLI](cli.md) for `--parallel` and target
range expansion.

## Provision SSH for yourself

`install_sshcreds()` generates (or reuses) a keypair in `keychaincredential`,
installs the public half on root's `authorized_keys`, and wires the private
half into this client's SSH leg — so a client that had only the web shell gains
real SSH:

```python
nas = TrueNASClient("nas.example.com", api_key)
nas.capabilities            # {"path", "run"} -- run via the web shell

nas.install_sshcreds()
nas.config.ssh              # now an SshConfig with client_keys set
nas.last_selection          # subsequent run() calls report 'ssh'
```

## Fail loudly on a typo

Unknown credential names and unknown provider names raise rather than being
ignored, which turns a silent misconfiguration into an immediate error:

```python
TrueNASClient("wss://nas", passwrd="s3cret")   # ValueError: unknown credential argument
TrueNASClient("wss://nas", executor=["shh"])   # ValueError: unknown executor provider
```
