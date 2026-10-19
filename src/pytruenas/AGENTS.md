# `pytruenas` — public API header

Header-file-style reference for the `pytruenas` package: every public export
with its signature, arguments, contract and gotchas, so the package can be used
without reading its source. It ships inside the package and is
self-contained. Development documentation lives with the source at
<https://github.com/jose-pr/pytruenas>; the user guide is at
<https://jose-pr.github.io/pytruenas/>.

**Imports.** Everything a caller needs is importable from `pytruenas`:
`__all__ = ["Namespace", "TrueNASClient", "TrueNASConfig",
"Credentials", "LocalAuth", "APIKeyAuth", "TokenAuth", "BasicAuth", "Event",
"Subscription", "TrueNASWSConnection", "__version__", "TrueNASError",
"ClientException", "ValidationErrors", "CallTimeout", "ConnectionClosed",
"JobFailed", "ConnectError", "AuthenticationError", "APIDumpError",
"UnknownMethod", "FieldError"]`, each defined in the module named in its
section below (every error in `pytruenas.exceptions`); `redact_call_args` (from `auth`) is importable from the root
too, outside `__all__`. The modules documented below are public. A name with a
leading underscore is private, as are `pytruenas.utils.io` and the `_`-prefixed
modules — with two deliberate exceptions: `Namespace`'s helpers and call
options (`_query`, `_get`, `_timeout`, ...), which carry the underscore so they
cannot collide with a middleware name, and the `_name_()` hook methods of the
CLI's args classes, which are duho's convention.

**Install.** `pip install pytruenas` (Python 3.9+). The core install is the
client, the websocket and HTTP transports, the web shell, the `tnasws` path
provider, the CLI and `deploy`. Extras:

| extra | brings | needed for |
| --- | --- | --- |
| `ssh` | `hostctl[ssh]>=0.4.0,<0.5` (asyncssh, sftppath) | `.ssh`, `run()` over SSH, the `sftp` path leg |
| `yaml` | `anycfg[yaml]` (PyYAML) | a CLI config file written in YAML (`#!yaml`, `.yaml`) |
| `repo` | `hostctl[deploy]` | `deploy --source repo`; the core dependency already installs it, so the extra only lets a requirement that names it resolve |

A missing extra raises `hostctl.MissingExtraError` (an `ImportError`) at first
use, never at import time: `FEATURE needs the 'EXTRA' extra: pip install
"pytruenas[EXTRA]"` for pytruenas's own (`.distribution == "pytruenas"`),
`"hostctl[EXTRA]"` for hostctl's. Without `ssh` the host has no `ssh`/`sftp`
provider and `run()`/`path()` use the websocket ones. Without `yaml`, a
YAML config file raises naming `pytruenas[yaml]` and the file.

**Version.** `pytruenas.__version__: str` is resolved from installed package
metadata (`importlib.metadata`); `"0.0.0.dev0"` when run from a bare checkout
with the package not installed.

## Client (`pytruenas.host`)

**`TrueNASClient`** is the client and the TrueNAS host in one class; its host
half (transports, configuration) is documented in the next section. There is
no second name for it.

`TrueNASClient(config=None, *, credentials=None, verify=True, shell=None,
known_hosts=(), autologin=True, version="current", timeout=Timeout(),
executor=None, path=None, ssh=None, ...)`

- **`config`** (positional) — the target: a host, `"host:port"`, or full
  `scheme://...` URI, a socket path (`"/var/run/x.sock"`), or a
  `TrueNASConfig`. There is no `target=` keyword. `None` /
  omitted / local-only resolves to the local middleware unix socket
  (`ws+unix:///var/run/middleware/middlewared.sock`). A remote target with no
  scheme or path resolves to **TLS and the current API** — `"nas"` means
  `wss://nas/api/current`; `ws://`/`http://` selects plaintext. Nothing is
  probed and building a client performs no network I/O, so a bad host raises on
  first use. A password in the userinfo must percent-encode `/`, `?`, `#` and
  `@` (`%2F`, `%3F`, `%23`, `%40`). A string that does not parse as a URI
  raises `ValueError` with the credentials stripped from the message; one that
  *does* parse is used as the URI it is (an `@` in a path is a path —
  indistinguishable from an unencoded password, so neither this package nor
  hostctl guesses).
- **`credentials`** (keyword only: a second positional argument raises
  `TypeError`) — passed to `Credentials(...)` (below). `None` means
  local-socket auth (no login call).
- **`username=`, `password=`, `otp=`, `api_key=`, `token=`** — keyword
  credentials, as hostctl's `HostConfig(uri, ...)` takes them: `username=` and
  `password=` replace the URI's own user and password (`password=""` is no
  password), so one target string serves several logins; `connection_uri` and
  `repr()` never show a password. Combined with `credentials=` they raise
  `ValueError`.
- **`autologin`** (default `True`) — the first `.conn` access calls
  `.login()` automatically when there's no live connection.
- **`verify`** (default `True`): `bool | str | os.PathLike | ssl.SSLContext`
  — one switch for every check the client makes: TLS certificates on the API
  websocket, the HTTP(S) side channels and the web shell (all through one
  context), and SSH host keys on commands and SFTP. Stored on
  `.config.verify`.
  - `True` trusts the operating system, through the platform's verifier
    (`truststore`: Windows CryptoAPI, the macOS Security framework, OpenSSL
    with the system CA paths elsewhere) on Python 3.10+ and OpenSSL's default
    store on 3.9 — what hostctl's `verify=True` means. If `$SSL_CERT_FILE`,
    `$REQUESTS_CA_BUNDLE`, `$CURL_CA_BUNDLE` or `$WEBSOCKET_CLIENT_CA_BUNDLE`
    is set, the first one set is trusted *instead*. certifi is never used.
  - A path (a PEM file or a hashed directory) is the CA bundle, trusted
    instead of the OS; it is stored as a `str`. A missing bundle raises
    `FileNotFoundError` naming the path and its source at connect time; an
    empty string or a boolean word (`"false"`, `"0"`, ...) raises
    `ValueError`, and any other type `TypeError`.
  - An `ssl.SSLContext` is used as it is on every TLS leg: a client
    certificate (mTLS, e.g. `sslcontext.create_context(certificate=, key=)`
    or `sslcontext.system_context()` for OS keystores and smart cards), a
    pinned CA. One context is shared, not copied.
  - `False` turns every check off, the SSH leg included
    (`SSHConfig(verify=False)`, also on a copy of an explicit
    `ssh=SSHConfig(...)`, never yours). With a remote `wss://` target the host
    logs one WARNING, the first time the API websocket or a side channel
    opens, that certificate verification is off.
  - For SSH, a path or a context means "verify". Keys named with
    `known_hosts=` are checked even under `verify=False`, which is "TLS off,
    SSH strict": `verify=False, known_hosts=...`. For "TLS on, SSH off", pass
    `ssh=SSHConfig(host, username="root", verify=False)`.
  - There is no `sslverify=`: it raises `TypeError` naming `verify=`.
- **Plaintext** — a credential sent over plain `ws://` to a non-loopback host
  logs one warning per host. `ws://` is not refused: it is legitimate for a
  loopback target or an already-private link.
- **`shell`** — connection string for the SSH leg (`"ssh://root@nas"`,
  `"root:pw@nas:22"`, `"nas"`). Stored as a `hostctl.SSHConfig` on
  `.config.ssh`; pass `ssh=SSHConfig(...)` to supply one directly. The user's
  `~/.ssh/config` applies, as it does for `ssh` (a `Host` alias, `HostName`,
  `Port`, `User`, `IdentityFile`, `ProxyJump`), with this precedence: a user or
  port in the string, then the file's `User`/`Port`, then `root` and 22. With
  no user in the string, `.config.ssh.username` is `None` and
  `.config.ssh.ssh_config` is configuration text that includes
  `~/.ssh/config` and then sets `User root`; with one, it is hostctl's
  `USER_SSH_CONFIG`. `.config.ssh.port` is `None` when the string names no
  port. For a leg that reads no personal file, pass
  `ssh=SSHConfig(host, username="root", ssh_config=None)`.
- **`known_hosts`** (default `()`) — the trusted host keys for the SSH leg
  built from `shell=` or by `.install_sshcreds()`, with hostctl's values: `()`
  is `~/.ssh/config`'s `UserKnownHostsFile`, else `~/.ssh/known_hosts`
  (skipped under `verify=False`); a path or list of paths names the file(s),
  checked either way. `known_hosts=None` raises `ValueError` naming
  `verify=False`. An explicit `ssh=SSHConfig(...)` keeps its own. Both the
  command and SFTP halves verify by default; an unverifiable key (or an
  unreachable SSH port) makes `run()` and `path()` fall back to the websocket
  providers, and the host logs one WARNING per skipped provider.
- **`executor`/`path`** — name the providers to use, in preference order; see
  the provider table in the next section.
- **`version`** — API path used when the target carries none (default
  `"current"`, i.e. `/api/current`).
- **`timeout`** (default `hostctl.Timeout()`) — hostctl's `Timeout`, or a
  number or `None` for `total` alone, as every hostctl config takes it:
  `connect` bounds opening the websocket (default
  `connection.CONNECT_TIMEOUT`, 30 s); `read` bounds one middleware call and
  one side-channel read (default `$PYTRUENAS_CALL_TIMEOUT`, else 60 s; a
  call's `_timeout=` overrides it); `total` is `run()`'s default, left to the
  command transport when `DEFAULT`. `write`, and `read=0`, raise `ValueError`.
  Stored on `.config.timeout`; `.config.timeouts` is it resolved, the
  variable read at that moment.
- **Other keywords** — hostctl's `PosixHost` options (`info=`,
  `initializer=`, `executor_providers=`, `path_providers=`). The port, scheme and API path are spelled in the
  target string, not as keywords: any other keyword raises `ValueError:
  unknown credential argument: 'NAME'` listing the keywords above. Given a
  `TrueNASConfig`, a configuration keyword raises `TypeError` (pass it to
  `TrueNASConfig.from_target` instead). Typing overloads list them for an
  editor.

### Attributes and properties

- **`.api`** (`cached_property`) — the root `Namespace` for this client
  (`client.api.<namespace>.<method>(...)`).
- **`.conn`** — the live
  `connection.TrueNASWSConnection`; connects (and logs in, if
  `autologin`) on first access, reconnects if the prior connection closed.
  After a successful `.login(...)`, a reconnect repeats that login (same
  credentials, `login_ex`, options, `otp_provider`) regardless of
  `autologin`. Thread-safe: concurrent first use opens one connection.
- **`.ssh`** — the `asyncssh.SSHClientConnection` that `.run()` uses over
  SSH (requires the `ssh` extra): `hostctl.transports.ssh.SSHExecutorProvider.connection`
  of the provider in `.executor_providers`. The first access connects and
  raises what connecting raises (`PermissionError`, `ConnectionError`,
  `TimeoutError`, or the `OSError` of a refused or unresolvable host);
  `RuntimeError` when the host has no SSH executor. The connection is bound to
  hostctl's process-wide event loop (the provider's `.loop`, thread
  `hostctl-asyncssh-loop`), not yours: run its coroutines with
  `asyncio.run_coroutine_threadsafe(coro, provider.loop).result()`, never await
  them on another loop, and never block that loop. `.close()` closes it; a read
  after that opens a new connection the host does not track. For the raw
  connection only (port forwarding, an SFTP client of your own);
  `.run()`/`.path()` select a transport instead of assuming this one.
- **`.config`** — the `TrueNASConfig` this host is built from. `.config.ssh` is
  the SSH leg; `.shell` means the *bound shell object* (`client.shell.run(...)`),
  as it does throughout hostctl.
- **`.capabilities`** — `{"run", "path"}` as available, plus `"spawn"`/`"tty"`
  when an SSH leg is configured; a remote target with no SSH and no web shell
  reports no `run`.
- **`.last_selection`** — the redacted provider trace for the most recent
  `run()`: hostctl `SelectionStep` records (`.provider`, `.chosen`,
  `.availability`, `.reason`, ...), not dicts.
- **`.name`** — the host's short label: the hostname, plus the port only when
  it is non-default (`nas1`, `nas1:8443`, `localhost` for the unix socket).
  It is `.config.name` (hostctl's `Host.name`); assigning either replaces it.
  This is what identifies the host in logs; `.config.connection_uri` is the
  full canonical (and credential-free) URI.
- **`.logger`** — a logger bound to the name at construction, so every record
  it emits is prefixed `[nas1]` — including records from the JSON-RPC
  connection, which shares it, and hostctl's fallback WARNING (`run() fell
  back from ssh to webshell: ssh: <reason>`, `path() fell back from sftp to
  tnasws: ...`, once per skipped provider). Defaults to
  `logging.getLogger("pytruenas")` underneath. Assign `.logger` (hostctl's
  settable attribute) a logger name or a `Logger` to redirect it, bound to
  `.name` the same way; a `LoggerAdapter` you assign is used as-is, unwrapped.
  The JSON-RPC connection takes the logger set when it opens. There is no
  `logger=` keyword.

### Methods

- **`.login(creds=None, *, login_ex=False, login_options=None,
  otp_provider=None)`** — close any existing connection, open a new one, and
  authenticate (`creds` or the client's configured credentials). Default uses
  the server's legacy `auth.login`/`login_with_*` methods. `login_ex=True` uses
  the `auth.login_ex` mechanism, handling an `OTP_REQUIRED` 2FA challenge via
  `auth.login_ex_continue` (OTP from the credential's `otp` or
  `otp_provider()`), raising `auth.AuthenticationError` on failure and returning
  the success response dict. `login_options` overrides the server defaults
  (`{"user_info": True, "reconnect_token": False}`). The legacy path returns
  the server's answer (`True`) and raises `AuthenticationError` when it is
  `False` (a wrong password or key — the server does not error). On any
  failure the new connection is closed, not left open unauthenticated. A
  reconnect repeats the login without the credential's one-time code (it is
  spent; the caller's object is unchanged), so a session that must survive a
  reconnect needs `otp_provider` — without one the reconnect raises
  `AuthenticationError("OTP_REQUIRED")`.
- **`.connect()`** — opens `.conn`, logging in when `autologin` is set (what
  the first `.conn` access does); raises what that raises. Entering
  `with TrueNASClient(...) as client:` calls it. The command and path
  transports (SSH, the web shell, SFTP) are not opened here: each connects
  when first used, so an API-only `with` block opens no shell session.
- **`.close()`** — closes the transports and then the websocket; leaving the
  `with` block calls it. A client that is
  garbage-collected without it closes its connection (socket and reader
  thread) from a finalizer, which runs whenever the collector gets to it;
  `close()` is how you decide *when*.
- **`.me() -> dict`** (`auth.me`) / **`.logout() -> None`** (`auth.logout`) /
  **`.ping() -> str`** (`core.ping` -> `"pong"`) — convenience wrappers.
- **`.path(*path, backend=None) -> pathapi.Path`** — build a path on the
  target: a hostctl `CompositePosixPath` over the path providers, which picks a
  provider per operation (annotate with `pathapi.Path`). On a remote target a
  relative path, and `path()` with no segments, is rooted at `/` on every leg
  (hostctl's own SSH hosts read it against the login directory; pytruenas
  does not, because the websocket leg has none). `backend` names one **path
  provider**, from the names in the provider table below (`"tnasws"`,
  `"sftp"`, `"local"`), and pins the returned path to it for every operation
  (hostctl's own `backend=`); it raises `ValueError: unknown path provider`
  for anything else — including a provider this host has not got (`"sftp"`
  without an SSH leg, `"local"` on a remote host) — and
  `OperationNotStartedError` when that provider is unavailable. It is the one
  path constructor; `backend="tnasws"` is the websocket leg alone. Wraps
  `hostctl.host.Host.path`. `p.symlink_to(target, force=True)` is pathapi's:
  it replaces a file or symlink in the way, never a directory, and on a host
  with no SFTP leg raises `NotImplementedError` before removing anything.
- **`.run(*cmds, **kwargs) -> subprocess.CompletedProcess`** — run commands on
  the target. Inherited from `hostctl.host.Host.run`; see that for the full
  signature (`stdin`/`stdout`/`stderr`, `cwd`, `env`, `capture_output`,
  `check`, `encoding`/`errors`, `input`, `timeout`, `text`). Each positional
  `cmd` is a string (verbatim shell text), a sequence (one quoted argv
  command), or a leading path object (a direct executable).
  **Which transport runs it is selected, not fixed** — see the provider table
  below. A *remote* target with neither SSH nor the web shell has **no `run`
  capability at all**, and `.capabilities` says so rather than failing
  mid-command.
- **`.wait(job_id, *, callback=None, timeout=None) -> object`** — block until
  middleware job `job_id` finishes and return its `result`. Polls
  `core.get_jobs` (back-off 0.25 s -> 2 s). `callback(job)` receives the job
  record (`state`, `progress` `{percent, description}`, ...) each time its
  state or progress changes — enough for a log line or a progress bar.
  `FAILED`/`ABORTED` raise `connection.JobFailed` (`.job` is the record,
  `.errno` from `exc_info`); `timeout` raises `connection.CallTimeout` (the
  job keeps running). Not `core.job_wait`: that method is itself a job and
  returns a new job id at once instead of blocking.
- **`.job_updates(job_id, *, timeout=None) -> Iterator[dict]`** — the same
  polling as a generator: yields the job record on every change of state or
  progress, the finished record last; does not raise for a failed job.
- **`.upload(file, method, *params, token=None, wait=True)`** —
  upload `file` (`str`/`bytes`) via the middleware's `/_upload` HTTP side
  channel, then call `method(*params)` server-side with it; waits on
  the resulting job by default and returns the job id. Auto-generates a
  short-lived auth token when none is given. Any other keyword is a
  `TypeError`.
- **`.download(method, *args, filename=None, buffered=False, wait=True)`** —
  call `method(*args)` to get a download link/job, fetch it over
  HTTP(S), and return the bytes. The bytes come back only once the job
  finished: `buffered=True` waits before fetching, otherwise the job streams
  into the response and is checked after it; a failed job raises
  `connection.JobFailed` instead of returning a partial body. With
  `wait=False` it returns a **`PendingDownload`** (`pytruenas.host`) instead:
  `.job_id`, and `.fetch(callback=None) -> bytes`, which does the same
  (waits for a buffered job first, checks an unbuffered one after the GET).
  Its `repr` shows only the job id; the link carries a single-use token.
  For both, `wait=` may also be a callable: it waits, and is passed to
  `.wait(callback=...)` for progress. Both side channels use the websocket's
  timeouts (`config.timeouts.connect` to connect, `.read` per read), raise
  `requests`' own exceptions for an HTTP or transport error, and never name
  a token in the message (`auth_token=<redacted>`).
- **`.dump_api(*, cache=True, refresh=False) -> dict`** — the middleware API
  definition (see `pytruenas.models.apidump.API`). The dump is built **and
  gzipped on the target**, then fetched over SFTP when the host has an SSH leg
  and in verified 256 KiB chunks through the command channel otherwise; the
  transfer is checked against the target's own sha256 and a mismatch raises
  `APIDumpError`. It is not captured from `run()`'s stdout: the
  dump is 24 MB on 26.0, which loses a web shell connection outright, and the
  `filesystem.get` HTTP side channel truncates it at both 23 MB and 2 MB.
  Building it costs ~75 s, so the result is cached per host and API version
  under `$PYTRUENAS_CACHE`; `cache=False` skips the cache entirely (and with it
  the `system.info()` version lookup), `refresh=True` re-fetches and overwrites.
  A full `core.get_methods()` is **not** an alternative — the server closes the
  websocket on it, and there is no per-method accessor.
- **`.install_sshcreds(name=None, private_key=None)`** — generate/reuse an SSH
  keypair via `keychaincredential`, install the public half on `root`'s
  `authorized_keys`, and store the private half on `.config.ssh` as a real
  `SSHConfig.client_keys` (user `root`, since that is where the key went; the
  port, host alias and proxy come from `~/.ssh/config`, else 22). An `ssh=`
  config you passed with no password or key gets the key on a **copy**
  (`.config.ssh` is then not your object; yours is unchanged); one with its own
  credentials is left as it is. Returns the private key. Needs **no** optional
  extra: provisioning runs over the middleware API and opens no SSH
  connection. Passing `private_key=` for a key the host does not already know
  is the exception — the public half is derived locally, which needs
  `cryptography` (preferred; `asyncssh` depends on it) or `asyncssh`; with
  neither, `MissingExtraError` names `pytruenas[ssh]`.
  The providers are rebuilt afterwards, so a host that had no SSH executor
  gains one. A *local* target provisions the key but wires no leg — there is
  nothing to SSH to.

## Host, transports and configuration (`pytruenas.host`)

`TrueNASClient` is constructible from a connection string, a `TrueNASConfig`,
or nothing:

```python
TrueNASClient("wss://nas")
TrueNASClient("nas", credentials="1-...", executor=["ssh"])
TrueNASClient()                       # the local middleware socket
```

It is a `hostctl.PosixHost`, so `run`, `path`, `spawn`, `info`, `close`,
`shell`, `capabilities`, and `last_selection` are all inherited; the
middleware surface (`api`, `conn`, `connect`, `login`, `logout`, `me`, `ping`,
`upload`, `download`, `dump_api`, `install_sshcreds`) is what this
class adds. Generic in `ApiVersion`: `TrueNASClient[Current]("nas").api`
completes the generated stubs.

Transports are *composed*, and the order is deliberate:

| | local target | remote + SSH | remote, no SSH |
| --- | --- | --- | --- |
| executors | `local` | `ssh`, `webshell` | `webshell` |
| paths | `local` | `sftp`, `tnasws` | `tnasws` |

**`local`** is hostctl's stock pair (`LocalExecutor` + a plain local path) —
pytruenas adds nothing. A target reached over the middleware unix socket *is*
this machine, so a command is a plain `subprocess` call and a path is a plain
local path.

A local target composes **only** that pair: no remote provider is built at all,
since every one of them is a way of reaching a machine somewhere else. `tnasws`
in particular would be a fallback that could only ever fail there —
`filesystem.get` routes reads through the HTTP side channel, which resolves to
`https://localhost` and trips the appliance's self-signed certificate.

**`webshell`** runs commands over `/websocket/shell` — the same PTY the web
UI's Shell page drives. It exists for a host reachable on the API port but not
on 22 (NAT, a firewall allowing only 443, a reverse proxy), which would
otherwise have no `run()` at all. It ranks below SSH, which has real
channels: the web shell drives a terminal, sending the command and any
`input=`/`stdin=` base64-encoded and framing output by markers the command
prints (hostctl's `PosixConsoleProfile`), so captured stdout is exact bytes
and nothing typed is interpreted. Uncaptured stdout streams live; stderr is
captured separately but delivered when the command ends (`stderr=STDOUT`
merges live); `stdin=` is read to EOF first (no incremental stdin); no input
means `/dev/null`; `timeout=None` waits forever; a timeout interrupts, closes
the session and raises `TimeoutExpired(orphaned=False)`; a connection lost
after the command line was typed raises `ConnectionError` and is not retried
on another provider. Requires a POSIX login shell with `base64`, `mktemp`,
`stty`, `cat` and `rm` (TrueNAS root's zsh qualifies).

**Overriding the selection.** `executor=` and `path=` name the providers to
use, in preference order — a single name or a sequence:

```python
TrueNASConfig.from_target("wss://nas", executor="ssh", path="sftp")   # SSH only
TrueNASConfig.from_target("wss://nas", executor=["ssh"])              # no web shell
TrueNASConfig.from_target(None, path=["local", "tnasws"])             # force tnasws locally
TrueNASConfig.from_target("wss://nas", executor=[])                   # no run capability
```

Valid names are `local`/`ssh`/`webshell` for executors and
`local`/`sftp`/`tnasws` for paths: hostctl descriptors, which `TrueNASClient`
declares in `provider_resolvers` (`ssh` and `sftp` share one resolver, so
one transport; hostctl's `winrm` is hidden) beside hostctl's global `local`.
An unknown one raises hostctl's `ValueError` listing the known names rather
than silently composing a host with nothing. Requesting `ssh`/`sftp` without
an `SSHConfig` also raises. `None` (the default) means "decide from the
target": `TrueNASClient.default_providers()` returns the table above, and
hostctl drops a default `ssh`/`sftp` when its `ssh` extra is missing (a name
you give is kept and fails at use). `TrueNASClient.resolve_providers()` builds
the providers for the current config, for `TrueNASClient.replace_providers()`.

`TrueNASConfig` is the `hostctl.host.HostConfig`. It accepts every connection
string `TrueNASClient` does and normalizes to a `truenas+*` scheme
(`truenas+auto`, `+ws`, `+wss`, `+unix`); `HostConfig("truenas+wss://nas")`
works from hostctl's own registry. A socket is `truenas+unix:///var/run/x.sock`
or `truenas+unix://var/run/x.sock` (the same path either way), or a bare
`"/var/run/x.sock"`; `TrueNASConfig()` with no arguments is the local
middleware socket. Constructing one performs **no network I/O** — the scheme
and API path are resolved from the string alone, not in the constructor.
`TrueNASConfig.from_target(target, **options)` takes the same keywords as
`TrueNASClient`.

**The URI query** carries the options that are not secrets, as hostctl's
configs carry theirs: `verify` (`true`/`false`/`1`/`0`/`yes`/`no`/`on`/`off`,
or a CA bundle path), `version`, `executor` and `path` (repeated, in
preference order; one empty value is "none"), `autologin`, and `timeout`,
`timeout_connect`, `timeout_read` (seconds; empty is no limit;
`timeout_write` is refused as the keyword is). An unknown or repeated key
raises `ValueError` (`unknown connection parameter: ...`), and so does an
option given both in the query and as a keyword.
`wss://nas?verify=false&timeout_read=10` is
`TrueNASClient("wss://nas", verify=False, timeout=Timeout(read=10))`.

**`connection_uri`** (and `str(config)`) renders every option that is not at
its default into that query, so `TrueNASConfig.from_target(str(config))` (or
hostctl's `HostConfig(str(config))`) is an equal config. Credentials, the SSH
leg (`ssh=`/`shell=`/`known_hosts=`) and an `ssl.SSLContext` given as
`verify` are never rendered. **Equality and hashing** are by
`connection_uri`: two configs for the same target and options are equal
whatever their credentials or `name`.

An OTP travels in the URI password field after a newline
(`wss://root:pw%0Aotp:123456@nas`); a raw newline works too. Unknown
credential names are rejected rather than silently dropped. The keyword form
dispatches on the names (`username`/`password`/`otp`/`api_key`/`token`), the
same selection `Credentials.from_host_credentials` makes.

Generic type parameter `ApiVersion` (bound to `Namespace`) lets a consumer
annotate `client: TrueNASClient[Current]` (from generated typings) for
IDE/type-checker completion on `client.api`; it has no runtime effect.

## API namespace (`pytruenas.namespace`)

`Namespace` is the dynamic attribute-style dispatcher for one API namespace
path (e.g. `client.api.user`, `client.api.pool.dataset`). Attribute/item
access builds child namespaces lazily and caches them per instance
(`ns.child` / `ns["child"]`); leading-underscore names other than the helpers
below raise `AttributeError` normally.

- **`Namespace(client, *name)`** — not usually constructed directly; reached
  via `client.api` and attribute/`__getitem__` traversal.
- **`__call__(*args, _retries=1, _method=None, _ioerror=False,
  _filetransfer=False, _timeout=UNSET, job=False)`** — invoke this namespace's
  middleware method (`self._namespace`, optionally suffixed with `_method`).
  Middleware methods take **positional** parameters: any other keyword raises
  `TypeError` naming it (a dropped `filters=` would query every row). The
  `_query`/`_get`/`_update` helpers below take keywords by design.
  - **`job=True`** — as in the upstream client: wait for the job the method
    starts (`TrueNASClient.wait`) and return the job's **result**; a failed job
    raises `connection.JobFailed` (the matching `OSError` with `_ioerror=True`).
    The wait has no deadline unless `_timeout` is given. A method that does not
    answer with a job id returns its answer unchanged. `job="RETURN"` returns
    the job id. The upstream client's other keywords (`background`,
    `callback`, `register_call`, `raise_`) raise `TypeError`.
  - **`_retries`** — retries on a new connection after a dropped one
    (`ECONNABORTED`); default `1` means up to 2 attempts total. Only a request
    that never reached the socket (`ConnectionClosed.sent is False`) is
    repeated. The call **always** returns or raises — never silently returns
    `None` on a connection error.
  - **`_timeout`** — per-call seconds; the default sentinel uses the client's
    configured timeout, `None` waits indefinitely. It is the only spelling: a
    bare `timeout=` is a stray keyword.
  - **`_ioerror`** — map a middleware `[ERRNO] message` error to the matching
    `OSError` (see `pytruenas.namespace.ioerror`).
  - **`_filetransfer`** — `True` routes through `client.download`; bytes/a
    readable routes through `client.upload`.
- **`.subscribe(callback=None, *, event=None, maxsize=1000) ->
  connection.Subscription`** — subscribe to this namespace's collection event;
  the event name defaults to the namespace's dotted path
  (`client.api.alert.list.subscribe()` -> `alert.list`), or pass `event=` to
  override (e.g. from `client.api`). A **real method**, so it shadows any
  middleware method literally named `subscribe`; reach such a method via
  `ns(_method="subscribe", ...)`. See `connection.Subscription`/`Event` below.
  This and `client.conn.subscribe(event)` are the two ways to subscribe; the
  client has no `subscribe()` of its own.
- **`._query(*opts, **filter) -> list[dict]`** — calls `<namespace>.query`
  with filters built from `**filter` kwargs (equality by default; wrap a value
  in `EQ`/`NE`/`RE`/`GT`/`GE`/`LT`/`LE`/`IN`/`NIN` from `pytruenas.utils.query`
  for other operators) plus any `Option`/dict in `opts`.
- **`._get(id_or_filter=None, **filter) -> dict | None`** — `.get_instance(id)`
  by id (via `_ioerror=True`, `FileNotFoundError` -> `None`), or the first
  match of a `{"limit": 1}` query by filter kwargs.
- **`._create(*opts, **fields)`** — call `.create(fields)`; raises
  `FileExistsError` if the middleware reports "already exists".
- **`._update(selector=None, *opts, **fields)`** — update by id (a bare
  int/str selector is always an id) or by a filter (mapping, or a sequence of
  field names matched against the passed values). A `!`-prefixed name is left
  out of the match and not changed on update; a selector with only `!` names
  raises `ValueError` rather than matching the first record. Diffs against the
  current record first unless `force=True` (an `Option`/tuple opt) is given, so
  a no-op update sends nothing. A field set to `None` is sent (it clears the
  value). An id with no matching record raises `FileNotFoundError` naming the
  collection and the id. A middleware **property** — reported as
  `{"value": ..., "parsed": ...}` while a caller sets the scalar — counts as
  unchanged when either half matches, so it is not rewritten on every call.
- **`._upsert(selector=None, callback=None, *opts, **fields)`** — `._update`
  if a matching record exists, else `._create`. `callback(action, id,
  result)` fires after the call when given: `action` is `DBAction.CREATE` or
  `DBAction.UPDATE`, or `None` when nothing changed, and `id` is `None` after a
  create (read it from `result`). Common opts: `idkey` (default `"id"`),
  `update_exclude`/`create_exclude` (field names to drop for that path),
  `wait` (wait for a job; default `True`; a callable gets its progress),
  `job` (`True`/`False`: whether the `create`/`update` method is a job;
  default: its schema's `job` flag, from `core.get_methods` once per namespace
  for the life of the client and in the `$PYTRUENAS_CACHE` cache — an
  unreadable schema logs one WARNING and counts as no job), `force`. Only a
  job's id is waited on: an integer answer from a method that is not a job is
  a record id and comes back as it is.
- **`DBAction`** — `str` enum, `CREATE = "create"`, `UPDATE = "update"`; the
  mutation an `_upsert`/`_update`/`_create` resolves to.
- **`ioerror(error: ClientException) -> Exception`** — map a middleware
  `[ENAME] message` or `[Errno N] message` error to an `OSError` with that
  errno (so the builtin subclass, e.g. `FileNotFoundError`); any other error
  is returned unchanged.

## Connection (`pytruenas.connection`)

The synchronous JSON-RPC 2.0 websocket transport backing `TrueNASClient`
(`client.conn`).

- **`TrueNASWSConnection(uri=None, *, verify=True, call_timeout=UNSET,
  connect_timeout=CONNECT_TIMEOUT, logger=None)`** — `call_timeout` left
  out is `default_call_timeout()`, read now; `None` waits indefinitely. It
  builds the connection and does no I/O. `uri` is `wss://`/`ws://` or
  `ws+unix://...`; `None`/bare `ws+unix://` connects to `DEFAULT_UNIX_SOCKET`
  (`/var/run/middleware/middlewared.sock`). `verify` takes the same values as
  the client's `verify` (see above). `logger` receives the connection's
  records (a host passes its own name-bound logger).
  - **`.connect() -> TrueNASWSConnection`** — opens the websocket (blocking,
    bounded by `connect_timeout`: connect, TLS and the HTTP upgrade), starts
    the background reader thread and returns the connection. Idempotent;
    `with` and the first `.call()` do it too. A closed connection is not
    reopened: `.connect()` and `.call()` raise `ConnectionClosed`.
  - **`.call(method, *params, timeout=UNSET) -> Any`** — send a
    request and block for the matching response. `timeout=None` waits
    **indefinitely**; the default sentinel uses `call_timeout`. Any other
    keyword raises `TypeError`, a misspelt `timout=` included; a job's id is
    returned (`Namespace` is what honours `job=True`). The timeout bounds the
    send as well as the wait for the answer: a send still blocked when it expires (a peer
    that stopped reading) closes the connection, since part of the request
    may be on the wire, and raises `CallTimeout`. Raises `ValidationErrors`/
    `ClientException` on a server error, `CallTimeout` on timeout,
    `ConnectionClosed` (`errno=ECONNABORTED`) if the connection dropped,
    `ClientException` with `errno=EPROTO` when the response arrived but could
    not be decoded (the call fails at once rather than waiting out its
    timeout), `TypeError` for a parameter JSON cannot encode (nothing is
    sent), and `RuntimeError` when called from the reader thread, i.e. from a
    subscription callback (it would deadlock until the call timed out —
    consume `Subscription.events()` on another thread instead).
  - **`.subscribe(event, callback=None, *, maxsize=1000) -> Subscription`** —
    issue `core.subscribe(event)` and route its `collection_update`
    notifications to a `Subscription`. The registry is keyed by event name
    (the notification's `params.collection`, the routing key — NOT the returned
    sub id); two subscribers to the same event both receive it.
  - **`.close()`** — idempotent; also usable as a context manager. Sends the
    close frame without waiting for the peer's answer, and does not wait
    behind a blocked send. Wakes every subscription's `events()` iterator (as
    does a dropped connection), and releases the socket even when the server
    closed the connection first.
    A connection whose reader ended is `._closed`, so the owning host opens a
    new one on next use; one bad message does not end it (it is logged and
    dropped).
- **`Subscription`** — one live subscription. **`.events(timeout=None)`** yields
  `Event`s from a bounded queue drained on the caller's thread (ends cleanly on
  unsubscribe/close/timeout); **`.unsubscribe()`** cancels it (idempotent, sends
  `core.unsubscribe`), also a context manager; **`.dropped`** counts events
  discarded when a full queue dropped the oldest; **`.id`** is the server
  subscription id, **`.event`** the subscribed name.
- **`Event(collection, msg, fields, id=None)`** — a `NamedTuple` for one
  `collection_update`: `msg` ∈ `added`/`changed`/`removed`, `fields` the payload
  dict (the shape TrueNAS 26.0 sends).
- **`DEFAULT_EVENT_QUEUE_SIZE`** — default `maxsize` (1000) for a subscription's
  event queue.
- **`CALL_TIMEOUT`** — `60.0`, the per-call timeout in seconds when neither
  the caller nor `$PYTRUENAS_CALL_TIMEOUT` sets one. A constant: no variable
  is read at import.
- **`default_call_timeout() -> float`** — `$PYTRUENAS_CALL_TIMEOUT` (a
  positive number of seconds) when set and not empty, else `CALL_TIMEOUT`;
  another value raises `ValueError` naming the variable. Read each time a
  connection is built.
- **`CONNECT_TIMEOUT`** — default timeout in seconds (30) for opening a
  connection. It is not the reader's timeout: an idle connection stays open.
- **`DEFAULT_UNIX_SOCKET`** — `"/var/run/middleware/middlewared.sock"`.
- `.connect()` and the first `.call()` raise **`ConnectError`** when the HTTP
  upgrade is refused (`.status` 404 for a wrong API path) or the handshake
  fails, with websocket-client's exception as `__cause__`; an `OSError` (a
  refused port, an unresolvable host, a TLS error) is raised as it is. The
  call errors are in [Exceptions](#exceptions).
- **`dumps(obj, **kwargs) -> str`** / **`loads(data, **kwargs)`** — JSON
  (de)serialization with the middleware's extended-type wrappers
  (`datetime`/`date`/`time`/`set`/`IPv4Interface`/`IPv6Interface`)
  round-tripped through `$date`/`$type`/`$time`/`$set`/`$ipv4_interface`/
  `$ipv6_interface` wrapper objects.

## Credentials (`pytruenas.auth`)

- **`Credentials(...)`** — a factory (via metaclass `__call__`), not a normal
  constructor when called on the base class directly:
  - no args -> `LocalAuth()` (local-socket auth, no login call);
  - a single `None` -> `LocalAuth()`;
  - a single `Credentials` instance -> returned as-is;
  - a single `(user, password)` list/tuple -> `BasicAuth(*it)`;
  - a single string containing `:` -> `user:password` (optionally
    `password\n<otp>` or `password\notp:<otp>`) -> `BasicAuth`;
  - a single string shaped `<numeric-id>-<64 alnum chars>` -> `APIKeyAuth`;
  - any other single string -> `TokenAuth`;
  - multiple positional args -> `BasicAuth(*args)`;
  - keywords: `username`/`password`/`otp`/`api_key`/`token`, selected as
    `from_host_credentials` does; any other keyword raises `ValueError`
    (`Credentials not supported`, values masked).
  - Instantiating a `Credentials` **subclass** directly (e.g. `BasicAuth(...)`)
    bypasses the factory and behaves like a normal constructor.
- **`.login(client)`** — the server's legacy login: `client.api.auth[self.METHOD]
  (*self._args())`, returning its result; raises
  `AuthenticationError("AUTH_ERR", {"method": METHOD})` when that is `False`.
  A no-op returning `None` when `METHOD` is `None` (`LocalAuth`). A credential
  subclass logs in through this method, not by calling `api.auth.*` itself,
  so a refusal raises.
- **`.login_ex(client, *, login_options=None, otp_provider=None) -> dict|None`**
  — `auth.login_ex` using this credential's `MECHANISM`
  (`PASSWORD_PLAIN`/`API_KEY_PLAIN`/`TOKEN_PLAIN`). Handles `OTP_REQUIRED`
  (continues with `auth.login_ex_continue`, OTP from `self.otp` or
  `otp_provider()`), returns the `SUCCESS` response dict, raises
  `AuthenticationError` otherwise. Falls back to `.login()` for a credential
  with no `login_ex` form.
- **`Credentials.from_env(env=None) -> Credentials`** —
  `Credentials($PYTRUENAS_CREDENTIALS)` (read through `utils.cmd.ENV`), or
  `env["PYTRUENAS_CREDENTIALS"]` from a mapping you pass; unset or empty is
  `LocalAuth()`.
- **`Credentials.from_host_credentials(...)`** — the keyword selection
  (`username`/`password`/`otp`/`api_key`/`token`) `TrueNASConfig` uses.
- **`LocalAuth`** — no-op auth (local socket). **`APIKeyAuth(api_key,
  username=None)`** — `login_with_api_key` (legacy) / `API_KEY_PLAIN` (login_ex,
  needs `username`). **`TokenAuth(token)`** — `login_with_token` / `TOKEN_PLAIN`.
  **`BasicAuth(username, password, otp=None)`** — `login` /
  `PASSWORD_PLAIN`; the one-time code is `.otp`.
- **`redact_call_args(method: str, args: tuple) -> tuple`** — `args` of an RPC
  call, safe to log: an `auth.*` method's arguments are reduced to type names;
  elsewhere a dict value under a secret-looking key (`password`, `*_token`,
  `private_key`, ...) is masked at any depth.
- A refused login raises **`AuthenticationError`**; see
  [Exceptions](#exceptions).

## Remote paths (`pytruenas.fs`)

`client.path(*segments, backend=None)` is the one entry point: a hostctl
`CompositePosixPath` over the host's path providers (`sftp`, then `tnasws`, for
a remote host; `local`, a `pathapi.LocalPath`, for the unix socket), with a
relative path rooted at `/`. This package holds the websocket leg's path type.
`__all__ = ["TrueNASWSPath", "TrueNASWSBackend"]`.
- **`TrueNASWSPath`** (`pytruenas.fs.tnasws`) — a `uripath.URIPath` (distribution
  `pathapi-uri`; scheme `truenas+ws`) backed entirely by the middleware
  `filesystem.*` API via a `TrueNASWSBackend(client)`. Implements
  stat/listdir/open/read/write/mkdir/chmod/chown; `unlink`/`rmdir` shell out
  (`rm --` / `rmdir --`) because `filesystem.*` has no delete op, and raise
  what pathlib would: `FileNotFoundError` (unless `missing_ok`),
  `IsADirectoryError`, `NotADirectoryError`, `OSError(ENOTEMPTY)`, else the
  errno `rm` printed (`EACCES`, `EPERM`, `EROFS`, `EBUSY`) or `EIO`.
  `chmod`/`chown` are middleware jobs: they return once the job has finished
  and raise `OSError` when it failed (`EIO` when the middleware names no
  errno). `read_bytes` (a `filesystem.get` download) raises `OSError` when the
  job behind the download failed. `stat()` follows a symlink
  (`filesystem.stat` describes the link and names its target in `realpath`);
  `stat(follow_symlinks=False)` and `is_symlink()` describe the link. A stat
  carries `st_mode`, `st_size`, `st_uid`, `st_gid` and the times. Built from a
  bare URI (no backend) raises `RuntimeError` on first use — reach one with
  `client.path(..., backend="tnasws")`, a `CompositePosixPath` whose websocket
  leg is a `TrueNASWSPath`.
  Listing calls `filesystem.listdir` with an explicit `select` projection
  (`name` for `_listdir`; `name`/`type`/`size`/`mode`/`uid`/`gid` for
  `_scandir`, which seeds each child's stat in the same round trip). That is
  load-bearing, not an optimisation: an unrestricted `listdir` computes the
  ZFS-only `zfs_attrs` column and fails with `EFAULT ... ZFS attributes are not
  supported.` on any non-ZFS path (`/tmp`, `/dev`, `/proc`, ...), so widening
  the projection to that column breaks `iterdir`/`glob`/`walk` off-pool.
  `listdir` reports no `mtime` on any filesystem, so stats seeded from a
  listing carry `st_mtime` 0; `stat()` uses `filesystem.stat`, which does
  report it.
  A write stream (`open("w")`/`"a"`, `write_bytes`) is one `filesystem.put`
  when it closes; a `with` block that raises discards it, so a failed write
  uploads nothing (`pathapi.providers.CommitOnClose`).
  `mkdir(mode=None, parents=False, exist_ok=False)` — an omitted `mode` is
  `0o755` (the middleware applies the mode it is sent, with no umask; an
  explicit mode is sent as given); `parents=True` creates missing parents.
  Two paths are the same filesystem (for pathapi's same-file and overlap
  guards) when their backends talk to the same client or to clients with the
  same `connection_uri` — not merely when they share a backend object.
- **`TrueNASWSBackend(client)`** — the backend object `TrueNASWSPath` carries; just
  holds `.client`.

**Segments are filesystem paths, not URIs.** `TrueNASWSPath` is a `URIPath`, so
the `tnasws` provider percent-encodes each segment into the `truenas+ws://` URI
it builds: a name containing `?`, `#`, `%`, a space or non-ASCII survives
`p.path` unchanged, and the host's SFTP leg is given the same decoded name.
Constructing a `TrueNASWSPath` *directly* from a URI string is URI syntax — `?`
there really is a query; encode the path yourself if you go around
`client.path()`.

## Transport providers (`pytruenas.providers`, `pytruenas.webshell`)

The objects behind the provider table. A caller never needs them to use a
host — `executor=`/`path=` name them by string — but they are public, so a
consumer can compose a host of its own.

- **`providers.local_providers()`** — `hostctl.local_providers()` unchanged: a
  fresh `(executor_provider, path_provider)` pair, both named `"local"`.
- **`providers.TrueNASWSPathProvider(client)`** — the `filesystem.*` path provider
  (`"tnasws"`), which works over the API websocket with no SSH.
- **`providers.WS_PATH_CAPABILITIES`** — the `frozenset` of path capabilities
  `TrueNASWSPathProvider` declares to hostctl.
- **`webshell.WebShellExecutorProvider(client)`** — the `"webshell"`
  executor provider. `.session` is its `WebShellSession` (created on first
  use); `.connect()` opens it, raising `hostctl.OperationNotStartedError`
  (`web shell unavailable: TYPE: message`, credentials redacted) when it
  cannot, which is a decline: the host tries its next provider.
- **`webshell.WebShellExecutor(provider)`** — `provider.executor`, a
  `hostctl.console.ConsoleExecutor` over the provider's session with
  `PosixConsoleProfile(batch=None)`, so its call surface is hostctl's
  (`capture_output`, `stdout=`/`stderr=` targets, `input=`/`stdin=` read to
  EOF, `stdin=PIPE` without `input=` raising `ValueError`, text rule, `check`,
  `TimeoutExpired`). No `args`, `cwd` or `env`: hostctl renders them into the
  command line. Uncaptured stdout is written as each websocket frame arrives;
  stderr when the command ends. Input is typed in writes of at most 2 KiB with
  no acknowledgement round trip. One command holds the terminal at a time. A
  failure before the command line is typed (the connection, or a write of the
  command's files) is a decline; a connection lost after it is a plain
  `ConnectionError`, never retried elsewhere. A timeout types ^C, closes the
  session (its hang-up ends the command) and raises
  `subprocess.TimeoutExpired(orphaned=False)` carrying what arrived; any other
  failure closes it too, and the next command reconnects.
- **`webshell.WebShellSession(client, **options)`** — one `/websocket/shell`
  session: `.connect()` (idempotent; a rejected token, or no `connected`
  message after it, raises `hostctl.OperationNotStartedError`, and a failure
  of any shape closes the websocket it opened), `.stream` (the websocket as a
  `hostctl.console.ConsoleStream`; connects first), `.close()`, `.shell_id`.
  It runs no command itself: use `WebShellExecutor`, or `client.run(...)`.
- **`webshell.clean_output(data: bytes) -> str`** — raw PTY bytes as text,
  with escape sequences, prompts and CRs removed. For bytes read outside a
  command's frame (a banner, an interactive session); command output never
  passes through it.

## Host patching (`pytruenas.patch`)

A toolkit for building your own patches to a host **beyond what the middleware
API exposes**: templates rendered into files, systemd units, the middleware's
own `etc_files` templates, and the ZFS `readonly` window that writing under
`/usr` needs. The toolkit is supported and versioned like the rest of the
package; the changes it makes are not supported by TrueNAS, and an update boots
a new environment without them — a patch is meant to be re-applied. Worked
example, runnable offline against a stand-in client: "Patching a host",
<https://jose-pr.github.io/pytruenas/guide/patch/>.

What a client must offer: `client.path(str)` (a path object with `exists`,
`read_bytes`, `write_bytes`, `with_name`, `name`, `parent`, `mkdir`; `stat`,
`chmod`, `unlink`, `lstat`, `replace` are used when present), `client.run(argv,
check=, capture_output=, encoding=)` and `client.api.<ns>.<method>(...)`. A
`TrueNASClient` offers all three; so can a test double.

- **`templates`** — rendering and targets.
  - `BaseTemplate.render(context) -> str` (abstract: raises
    `NotImplementedError`); `.apply(target, context=None) -> bool` renders and
    writes, returning whether the target changed. `TextTemplate(text: str |
    bytes)` renders `text`; `BasicTemplate(text)` substitutes `%{name}` from a
    dict or an object's attributes via `render_basic_template(template,
    context) -> str`: one pass, a name matches as given or upper-cased (exact
    wins), a substituted value is not substituted again, an unknown placeholder
    stays, a `None` context returns the template.
  - `TemplateTarget.apply_template(template, context=None, **kwargs) -> bool`:
    `template` is an instance (used as is), a `BaseTemplate` *class* (built
    with `kwargs` and the target's `read()` content, `b""` when absent), a
    `str` (literal text) or a local path (read as UTF-8). `kwargs` with any
    form but a class raise `TypeError`.
  - `FileTarget(path, baseline: bool | str = False, mode: int | None = None)`
    (`TypeError` if `path` lacks the four required methods).
    `write(content: str | bytes) -> bool` writes only when the content
    differs (`None` raises `TypeError`); an existing file keeps its mode, a new
    one gets `mode` before any content lands, missing parents are created
    `0o755`. `read() -> bytes` is the content to template *from*, never writes,
    and raises `FileNotFoundError` when there is no original.
    `would_change(content) -> bool` is the dry run. `is_patched() -> bool`
    (also `True` for a snapshotted file since deleted).
    `revert(remove_baseline=True) -> bool` restores the snapshot's content and
    mode and returns whether the file changed. `baseline()` takes the snapshot
    now; `baseline_path` is where it lives (`None` without one).
  - **Baseline files** (`baseline=True` means suffix `.baseline`; a `str` is
    the suffix). The first *changing* write copies the original to
    `<name><suffix>` (complete or not at all: written to a random sibling and
    renamed where the path has `replace`), or creates `<name><suffix>.absent`
    when there was no file — `read()` then raises `FileNotFoundError` and
    `revert()` leaves the file, returning `False`. Every changing write also
    records digests of what it writes and what it found in
    `<name><suffix>.applied`; a file matching neither was rewritten by
    something else and is the new original: `read()` returns it, the next
    write snapshots it, `is_patched()` is `False`, `revert()` leaves it. A
    baseline without that record keeps its first snapshot. Where the path has
    `lstat()`, a baseline, marker or record must be a regular file with one
    link, owned by root or by the target's owner (its directory's while it is
    absent); anything else raises `PermissionError`.
- **`systemd`**
  - `SystemFile(path: str, client, etc=None, services=None, baseline=True,
    writable=False, mode=None)` — a `FileTarget` on `client.path(path)`.
    `etc`/`services` take one name, `"a,b"` or a sequence (`as_names`). After
    a change — a write or a revert — each etc group is regenerated with its
    own `client.api.etc.generate(group)` and each service reloaded with
    `client.api.service.reload(name)`. If that fails, the previous content is
    put back (a file the write created is removed) and the error raised, so
    the next apply retries. `writable=True` wraps the change in
    `zfs.writable`, and an unchanged write opens no window. `revert()` keeps
    the snapshot until notifying succeeded.
  - `Unit(client, name, description="", enable=True, start=True, *,
    after="network.target auditd.service", wantedby="multi-user.target",
    conf=None, restart_on_change=False)` — `/etc/systemd/system/<name>`
    (`UNIT_DIR`), `baseline=False`. `name` gets the class `SUFFIX` unless it
    ends in a systemd unit type (`.service`, `.socket`, `.device`, `.mount`,
    `.automount`, `.swap`, `.target`, `.path`, `.timer`, `.slice`, `.scope`).
    `conf` (`{section: {key: value}}`) is deep-copied, then `Description`,
    `After`, `WantedBy` defaulted. `apply() -> bool` writes if changed; a
    change runs `daemon-reload` (and `systemctl try-restart` with
    `restart_on_change`, unless `start` is `False`), then `enable`/`start` are
    reconciled: `True` make it so, `False` make sure it is not, `None` leave
    alone. `uninstall() -> bool` (disable `--now`, remove, reload; `False` if
    absent), `is_active()`, `is_enabled()`, `restart()`, `daemon_reload()`,
    `configure()`, `render() -> str`, `escape(text) -> str`
    (`systemd-escape -- text` on the host).
  - `ServiceUnit(client, name, cmd=None, **kwargs)` (`ExecStart` = `cmd` or
    `name`, `Restart=always`, `RestartSec=10`, unless `conf` sets them);
    `MountUnit(client, where, what, options="", type="", **kwargs)` and
    `AutomountUnit(client, where, timeout="60", **kwargs)`, named by
    `escape_path(client, where)` (`systemd-escape --path`; `/` is `-.mount`).
  - `render_unit(conf) -> str` — `Key = value` lines; a list value is one line
    per item; a value with a line break raises `ValueError`, `None` raises
    `TypeError`. `UnitConfigParser` is a `ConfigParser` set up for unit
    syntax (case-sensitive keys, `=` only, no interpolation).
- **`middleware`**
  - `middlewared_path(client)` — the `middlewared` package directory as a
    `client.path`, by running `python3 -c "import middlewared ..."` on the host
    (no API method reports it on 26.0); `RuntimeError` on an empty answer.
  - `MiddlewareFiles(client=None, module_path=None)` — `client=None` is a
    local `TrueNASClient()`; `module_path` is located on first use (`repr()`
    never locates it). `find_template(template, etc=None, services=None,
    baseline=True, writable=False) -> SystemFile` searches `TEMPLATE_DIRS`
    (`etc_files`, then `etc_files/local`; the first match wins) for `template`
    and `template.mako`; `FileNotFoundError` names every path tried.
    `baseline` defaults to **True**: `read()` never writes, so it works on the
    read-only `/usr` dataset, and the snapshot is taken by the first changing
    write — pass `writable=True` for that write.
    `find_file(path, *args, cls=None, **kwargs)` wraps a file under the package
    (`cls` default `SystemFile`); a file whose own baseline is all that is left
    still counts as present.
- **`zfs`**
  - `writable(client, path)` — context manager: clears `readonly` on the
    dataset holding `path` and restores it however the block exits, as it was
    found (an inherited `on` is inherited again). Yields the dataset. A
    writable dataset, or a path not on ZFS (then the yield is the mount's
    source), is left alone. While open, the dataset carries the user property
    `pytruenas:restore-readonly`; a later window finding it on a writable
    dataset restores on exit. Body raises and restore fails: the body's
    exception is raised, the restore failure logged; clean body, failed
    restore: raises. Two concurrent windows on one dataset are not
    coordinated.
  - `dataset_for(client, path) -> str` — via `findmnt --raw --nofsroot -o
    FSTYPE,SOURCE`, walking up to the nearest existing ancestor (findmnt fails
    on a missing path); `ValueError` naming the filesystem type when not ZFS,
    `RuntimeError` when nothing answers.
  - `get_property(client, dataset, name, *, default=None)` (`default` when ZFS
    prints `-`: unset or not applicable), `get_properties(client, dataset,
    names) -> dict` (one `zfs get`; unset omitted), `set_property(client,
    dataset, name, value)` / `set_properties(client, dataset, mapping)` (`bool`
    as `on`/`off`), `inherit_property(client, dataset, name, *,
    received=False)`, `is_readonly`, `set_readonly`. User properties (a name
    with a colon) work throughout.
  - `host_path(path) -> str` unwraps a path for argv through `os.fspath()`: a
    `client.path(...)` composite gives its logical path, and a URI path gives
    the host path when its scheme names a host filesystem (`truenas`,
    `truenas+ws`, `sftp`); a `str` passes through. Any other scheme raises
    rather than putting a URI into a command line. Every `path` argument in
    `zfs` is a `str` or an `os.PathLike[str]`.

## Typings generator (`pytruenas.codegen`)

Backs the `generate-typings` command; not typically used directly.
`__all__ = ["Codegen", "BadAPIName"]`; the declarations and rendering behind
them are private (`codegen._declarations`, `_render`, `_types`).

- **`Codegen().generate(api: Version, root: Path | str) -> None`** — write one
  `__init__.pyi` per API namespace under `root`, built in Python (no template
  engine, no extra). `api` is one entry from
  `client.dump_api()["versions"]` (a `pytruenas.models.apidump.Version`); it
  is not modified.
  Renders into a temporary sibling and swaps it in only when complete: the
  previous tree is renamed aside and deleted after the new one is in place, so
  a failure (on Windows, a stub held open or a shell inside the tree) leaves
  the previous output intact and no temporary directory behind; a previous
  tree that cannot be deleted is logged at WARNING. `root` is replaced only if
  it is absent, empty, or a previous output (marked `.pytruenas-typings`);
  otherwise `FileExistsError` — hand-written stubs included.
- **`codegen.BadAPIName`** (`pytruenas.TrueNASError`, `ValueError`) — a
  dump name that would write outside the output directory.

## Generated typings (`generate-typings` output)

- The package root exports **`Current`**, an alias for the generated version
  class (`V2600` for v26.0.0), so the documented `TrueNASClient[Current]`
  resolves.
- Optional TypedDict keys are `NotRequired`, and an array that admits no items
  (`items: false`) is `list[Never]`; both are imported from `typing_extensions`
  below Python 3.11 (a `sys.version_info` guard in every stub), so the output
  does not depend on the interpreter that generated it. A checking target older
  than 3.11 needs `typing_extensions` installed.
- A property absent from a schema's `required` list is optional — including
  when the schema has no `required` list at all, which is most update
  payloads, query-options and `_get` filters.
- Names are sanitized to identifiers (every non-alphanumeric character is a
  word boundary; a leading digit gets an `N` prefix), and two different shapes
  wanting one TypedDict name get numbered variants rather than one silently
  replacing the other.
- A schema form this generator cannot express degrades to `JsonValue` instead
  of failing the run; `JsonValue`/`JsonObject`/`JsonArray` are real aliases.
- Generation never mutates the dump it is given, and never writes outside the
  output directory (`codegen.BadAPIName` if a dump name would escape it).
- The synthetic helpers `_create`/`_update`/`_upsert`/`_get` type a
  namespace's payload, so they narrow the runtime `Namespace` signatures; each
  carries `# type: ignore[override]`. One is omitted (logged at INFO) when the
  method has no object payload, or `get_instance` returns no object with
  properties. Parameter names are unique in a signature (`self` and a repeated
  or colliding title get a trailing `_`; an untitled one is `argN`).
- The suite compiles the stubs generated from a small fixture dump and from a
  set of unusual schema shapes, and type-checks them with pyright (3.9 and
  3.14 targets) and mypy (3.10 and 3.14) when those are installed. It does not
  run against a full live dump.
- Every method's call options (`_method`, `_ioerror`, `_filetransfer`,
  `_timeout`, `_retries`) are **keyword-only** in the stub, matching the runtime:
  middleware parameters are positional and any other keyword raises.
- `enum`/`const` become `typing.Literal[...]` (a `None` value becomes a union
  member), and an object whose `additionalProperties` is a schema becomes
  `Mapping[str, T]`.
- A middleware method whose name is also a real `Namespace` method
  (`core.subscribe`) is **not** emitted — the stub would redefine the class
  member. Call it as `ns(_method="subscribe", ...)`; generation logs each one
  it skipped at INFO.

## Schemas (`pytruenas.models`)

TypedDicts and type aliases only (no runtime behavior); import the submodules
directly. Generated stubs import `pytruenas.models.jsonschema` for
`JsonValue`/`JsonObject`/`JsonArray`/`JsonNumber`, so those names stay.

- **`pytruenas.models.apidump`** — `API` (`{"versions": [Version, ...]}`),
  `Version` (`{"version", "methods", "events"}`), `APIMethod`
  (`{"name", "roles", "doc", "schemas"}`), `MethodSchema`,
  `MethodProperties`, `APIEvent` (`{"name", "roles", "doc", "schemas"}`).
- **`pytruenas.models.jsonschema`** — the JSON-Schema-shaped TypedDicts
  (`Schema`, `BaseType`, `AnyOf`, `OneOf`, `Object`, `Array`, and one per
  scalar type: `Float`, `Null`, `Boolean`, `Integer`, `Number`, `String`,
  `Any`), `TypeDeclaration`, and the aliases `JsonValue`, `JsonObject`,
  `JsonArray`, `JsonNumber`.

## Utilities (`pytruenas.utils`)

- **`target.Target`** (`NamedTuple`: `scheme, username, password, host, port,
  path, query, fragment`) — a parsed connection string.
  `Target.parse(connectionstring, resolve_port=True, **defaults) -> Target`
  (raises `ValueError` for a string that does not parse as a URI, naming the
  characters to percent-encode and never quoting the credentials);
  `.uri` reassembles it; `.redacted` is that URI without the password;
  `.is_local` checks for `""`/`"localhost"`/`"127.0.0.1"`; `.qsl` /
  `.query_val(key, default=None, *, islist=False)` read the query string.
- **`target.redact(connectionstring) -> str`** — the string with its password
  **removed** (`wss://root:secret@nas` -> `wss://root@nas`), never masked, so
  the result is still a usable target; delegates to `hostctl.host.redact_uri`,
  so pytruenas and hostctl render a target identically. Never raises; a string
  with no userinfo comes back unchanged.
- **`query`** — `EQ`/`NE`/`RE`/`GT`/`GE`/`LT`/`LE`/`IN`/`NIN` filter-operator
  wrappers for `Namespace._query`/`_get` kwargs (bare values default to
  `EQ`); `EXCLUDE` sentinel to drop a kwarg from a filter/update entirely;
  `Option(name, value)` + `Option.options(*opts)` merge dict/tuple/`Option`
  opts passed to `_query`/`_upsert`/etc.; `diff(base, against) -> dict` (keys
  in `against` whose value differs from `base`, comparing a property-shaped
  `{"value"/"parsed"/"rawvalue"}` current against a scalar, and a partial dict
  on its own keys only); `MISSING`, the "not reported at all" sentinel (an
  instance, like `EXCLUDE`);
  `filter_from_kwargs(**kwargs) -> list[QueryFilter]`, which builds the
  middleware's filter list those kwargs stand for —
  `[("username", "=", "root"), ("uid", ">", 0)]` — what `_query` uses
  internally, and the way to build a filter without a client.
- **`cmd`** — the CLI's args root and output helpers; see
  [Command line](#command-line).
- **`runpath`** — helpers for authoring a RunPath step directory; see
  [Command line](#command-line).
- **`apicache`** — fetch and cache the API definition, two ways.
  **Preferred, over the API alone:** `services(client, *, refresh=False,
  version=None)` (`core.get_services` — the namespace index) and
  `service_methods(client, service, *, refresh=False, version=None)`
  (`core.get_methods(<service>)`). `version` keys the cache as it does for
  `load`; omitted, each call reads it with a `system.info()` round trip, so a
  caller making several reads it once and passes it. Both middleware
  methods declare **no roles** and need **no command access**, so they work for
  an API-key account with no shell, no SSH and no web shell; one namespace is a
  small answer (`user`: 13 methods / 100 KB on 26.0). The filter is by
  **service**, not method name — `core.get_methods("user.create")` returns `{}` —
  and the unfiltered call is not usable at all, because the server closes the
  websocket on that payload.
  **The whole definition:** `load(client, *, refresh=False, version=None) -> API`
  and `fetch(client, *, keep_remote=False)`, via `middlewared --dump-api`. Needs
  command access and weighs 24 MB, so it is the fallback — but it is the only
  source for an *older* API version, and what `generate-typings` consumes.
  Also `cache_root()` (the cache directory: `$PYTRUENAS_CACHE`, else the
  platform user cache directory), `path_for(host, version)`, `store(api,
  path)` (atomic); a transfer that does not reproduce the target's sha256
  raises `APIDumpError` (a `RuntimeError` too);
  `CHUNK_SIZE`/`CHUNK_ATTEMPTS`/`CHUNK_TIMEOUT`/`DUMP_TIMEOUT`/
  `SERVICE_TIMEOUT`, and `REMOTE_DIR` (`/var/db/system` — on a data pool so it
  survives an update, and not `noexec` the way `/tmp` is). Each fetch dumps
  into a `mktemp` file of its own there, so concurrent fetches of one appliance
  do not collide, and removes it afterwards. Every command carries
  a timeout on purpose: the web shell waits forever by default, which turns a
  stalled channel into an indefinite hang instead of a retry.
- **`apihelp`** — render help from a dump slice; pure functions, no client.
  `find(version, name)` (raises `UnknownMethod`, a `LookupError` too, with
  near-misses), `methods(version)`, `namespaces(names)`, `parameters(method)`,
  `returns(method)`, `payload_index(method)` (the **last** object-typed
  parameter — the payload), `fields(method)` (the `--field=value` names),
  `type_label(schema)`, `usage(name, method)`, `render(name, method)`,
  `render_namespace(version, ns)`, `render_index(version)`. A parameter list is
  `schemas.properties["Call parameters"].prefixItems`; the result is
  `["Return value"]`.
  `from_get_methods(name, entry)` and `methods_from_get_methods(found)`
  normalize the **other** envelope — what `core.get_methods` returns, where the
  parameters are `accepts`, the result is `returns` (a list), the doc is
  `description`, and a `job` flag exists that the dump does not carry. Both
  envelopes render through one path afterwards; `render` calls a job out **above**
  the doc, because a job returns an id rather than a result and some docs run to
  hundreds of words.
- **`fields`** — coerce `--field=value` text per a property's schema.
  `collect(tokens, fields) -> dict` builds a payload (dotted names nest, a
  repeated name accumulates, `name:json=` takes literal JSON, `name=@file` reads
  a file); `coerce(name, schema, raw)` casts one value; `split(token)` accepts
  both spellings via `cmd.split_assignment`; `FieldError` (a
  `ValueError` too) carries the message, and an unknown name or bad enum value
  names the alternatives. `TRUE`/`FALSE` are the accepted boolean spellings —
  strict sets, because `bool("false")` is `True` and would send the wrong
  value.
- **`io`** — internal helpers (byte-like checks); no stable external contract.

## Exceptions

Every error is defined in **`pytruenas.exceptions`** and exported from
`pytruenas`. **`TrueNASError(Exception)`** is the base of all of them, so
`except pytruenas.TrueNASError` catches any error pytruenas raises at run time:

| class | builtin base too | raised when |
| --- | --- | --- |
| `ClientException` | — | the middleware failed a call (`.errno`, `.trace`, `.extra`) |
| `ValidationErrors` (`ClientException`) | `ValueError` | the server rejected the arguments, per field |
| `CallTimeout` (`ClientException`) | — | no answer within the timeout |
| `ConnectionClosed` (`ClientException`) | — | the connection dropped before the answer |
| `JobFailed` (`ClientException`) | — | a middleware job ended `FAILED`/`ABORTED` |
| `ConnectError` | — | the websocket upgrade was refused or its handshake failed |
| `AuthenticationError` | — | a login was refused |
| `APIDumpError` | `RuntimeError` | the API definition was not fetched intact |
| `UnknownMethod` | `LookupError` | a method name the API definition lacks |
| `FieldError` | `ValueError` | a `--field=value` the schema refuses |

No error derives `OSError`, `TimeoutError` or `ConnectionError`: path code
reads any `OSError` from `exists()`/`is_dir()` as "not there", so a timeout
or a dropped connection would pass for a missing file. Catch `CallTimeout` and
`ConnectionClosed` by name.

- **`ClientException(error, errno=None, trace=None, extra=None)`** — base error
  for any call/connection failure; `errno` carries a POSIX errno when the
  middleware's `[ERRNO] message` prefix maps to one.
- **`ValidationErrors(errors)`** — per-field validation errors; `.errors` is
  `list[(attribute, errmsg, errcode)]`.
- **`JobFailed(job)`** — raised by `TrueNASClient.wait` (and `job=True`,
  `.download`) for a `FAILED`/`ABORTED` job; `.job` is the `core.get_jobs`
  record, `.errno` the middleware's errno when it reports one.
- **`CallTimeout()`** — a call exceeded its timeout, or `.wait(timeout=)` ran
  out (the job keeps running).
- **`ConnectionClosed(sent)`** (`errno` is `ECONNABORTED`) — the connection
  closed before the response arrived. **`.sent`** is `False` when the request
  never reached the socket (safe to repeat: `Namespace` retries exactly these)
  and `True` when the server may have run it — a create, a delete, a job start
  — so only the caller can decide. A plain
  `ClientException(errno=ECONNABORTED)` carries no `.sent` and is treated as
  "may have run".
- **`ConnectError(message, status=None)`** — opening the websocket failed at
  the HTTP upgrade or the websocket handshake. `.status` is the HTTP status the
  server answered (404 for a wrong API path) or `None`; `__cause__` is
  websocket-client's exception.
- **`AuthenticationError(response_type, response, method="login_ex")`** —
  raised by `login_ex` on a non-`SUCCESS` response and by the legacy `login` on
  a `False` answer; `.response_type` is the server discriminator, `.response`
  the full dict; the message names `method`.
- **`APIDumpError`**, **`UnknownMethod`**, **`FieldError`** — see
  `utils.apicache`, `utils.apihelp` and `utils.fields` above.

A caller's mistake (an unknown keyword, a malformed target) is a plain
`TypeError`/`ValueError`, not a `TrueNASError`. An `OSError` that already
describes a failure — a refused port, an unresolvable host, a TLS error while
connecting — is raised as it is. The side channels (`upload`, `download`)
raise `requests`' own exceptions for an HTTP or transport error. Other
exceptions, documented where they arise: `hostctl.MissingExtraError` (a missing
extra), `hostctl.OperationNotStartedError` (a provider declined:
`path(backend=)`, the web shell), `codegen.BadAPIName`, and `duho.UsageError`
from the CLI.

## Command line

`pytruenas = "pytruenas.main:main"` is the installed console script; `python
-m pytruenas` is the same. User guide: <https://jose-pr.github.io/pytruenas/guide/cli/>.

### Entry point (`pytruenas.main`)

- **`main(name=None, argv=None, args=None, root=None) -> int`** — build the
  `duho` app (`root`, default `PyTrueNAS`), discover commands (built-ins in
  `pytruenas.cmd` plus any `PYTRUENAS_PATH` / `--cmdspath` / config
  `commandspath` entries), parse `argv`, and dispatch the selected command
  against every target concurrently. `args` is the shared args class every
  command inherits (a `PyTrueNASArgs` subclass, default `root._ARGS_`; anything
  else raises `TypeError`); a derived tool adds global options through it or by
  subclassing `PyTrueNAS` with `_ARGS_` set. Raises `SystemExit` for `--help`,
  `--version` and a usage error found while parsing; a `--config`/
  `$PYTRUENAS_CONFIG` file that does not exist returns 2 with
  `NAME: error: config file not found: PATH`. A `hostctl.MissingExtraError`
  raised before any target runs (a YAML config file without the `yaml` extra)
  prints `NAME: MESSAGE` to stderr and returns 125.
- **`PyTrueNAS(PyTrueNASArgs, duho.Cli)`** — the app root; `--version` resolves
  from installed package metadata.

### Global options (`pytruenas.utils.cmd.PyTrueNASArgs`)

`PyTrueNASArgs` (a `duho.LoggingArgs` mixin) carries the global fields every
command sees: `config` (`--config`/`-c`, a path; `None` when not given),
`cmdspath` (`--cmdspath`,
split on `:`), `insecure` (`--insecure`/`-k`), `ca_bundle` (`--ca-bundle
FILE`), `parallel` (default `1`), `logto` (default `-`
for stderr, or a `{target}`/`{isodate}` path template; each target's file gets
only that target's records, `--parallel` included), plus `targets` (the
trailing positionals, not a flag; each command declares the field last through
`with_targets(args_cls)`, whose field type is `TargetsField`) and helper
methods `._config_path_()`/`._config_dict_()`/`._expanded_targets_()`.

The config file is `--config`, else `$PYTRUENAS_CONFIG` (either must exist:
`duho.UsageError`, exit status 2), else
`pytruenas.utils.cmd.default_config_path()` — `pytruenas/pytruenas.cfg` in
the platform's configuration directory (`%APPDATA%` on Windows,
`$XDG_CONFIG_HOME` or `~/.config` elsewhere), read only when present. The
working directory is never searched. Its format is the one a `#!<format>` first line names (`#!toml`, `#!yaml`,
`#!json`, also `#!/usr/bin/env yaml`; the line is not part of the
document), else the one the file name's suffix selects (`.toml`,
`.yaml`/`.yml`, `.json`; `.cfg` and no suffix select none), else TOML. YAML needs the `yaml` extra. `load_config(path) -> dict` reads one
(`pytruenas.utils.cmd`); a file that does not parse, is not a table, or is in
another format (INI) is a `duho.UsageError` naming it. The CLI reads four keys
— `credentials`, `insecure`, `ca_bundle` and `commandspath` (relative entries
resolve against the file's directory) — and ignores any other, which a derived
tool may read through `._config_dict_()`. Target
expansion (commas and `[A-Z]`/`[0-9]` ranges) applies to the HOST part only —
a comma or a range inside credentials is part of them — and credentials are
carried onto every expanded host.

These methods decide how a command connects, and are the only supported way
to build a client from parsed args:

- **`._config_path_() -> (Path, bool)`** — the config file and whether it
  must exist (see above).
- **`._verify_() -> bool|str`** — the `verify=` for the clients the CLI
  builds. Each layer in turn — the flags (`-k`, `--ca-bundle`), then
  `$PYTRUENAS_INSECURE`/`$PYTRUENAS_CA_BUNDLE`, then the config file's
  `insecure`/`ca_bundle` — can turn verification off (`False`) or name a CA
  bundle (its path, which must exist, else `ValueError` naming the source);
  the first that does wins, else `True`. An empty variable is unset; a
  non-boolean `$PYTRUENAS_INSECURE` or config `insecure` is a `ValueError`.
  The removed `$PYTRUENAS_SSLVERIFY` and config `sslverify` raise
  `ValueError` naming their replacements.
- **`._credentials_() -> Credentials|None`** — `$PYTRUENAS_CREDENTIALS`, else the config
  file's `credentials` (a connection string, or a mapping of keyword
  arguments), else `None`.
- **`._client_(target) -> TrueNASClient`** — the client for one target: the
  above, with the credentials applied **only** when the target string carries
  none (passing both raises). `main` and `runpath.default_init` both use it,
  so a plain command and a RunPath step connect alike.

Also in `pytruenas.utils.cmd`: **`with_targets(args_cls=None) -> type`**
(`args_cls`, default `PyTrueNASArgs`, with `targets` declared last),
**`TargetsField`** (that field's annotated type), **`register_targets(parser)`**
(adds the trailing `targets` positional to a parser you build yourself; a
command does not need it), **`CommandModule`** (a `Protocol` naming the
`run(client, args, logger)` a command module exposes), **`emit(text)`** /
**`emit_json(value, args=None)`** and **`json_default`** (below),
**`json_value(raw)`** (the decoding `call -p` and `query -f` share: a JSON
value, falling back to the raw string), and **`ENV`**, the single
`duho.env.Env("pytruenas", autoload=False)` accessor every `PYTRUENAS_*`
setting is read through (see [Environment variables](#environment-variables)).

### Built-in commands (`pytruenas.cmd`)

- **`query <namespace> [-f/--filter KEY=VALUE ...] [targets...]`** — prints
  `client.api[namespace]._query(**filters)` as JSON. Only works on queryable
  namespaces (`<namespace>.query` must exist), e.g. `user`, `pool.dataset`.
- **`call <method> [-p/--param JSON ...] [--no-schema] [--refresh-api]
  [targets...] [-- --field=value ...]`** — prints
  `client.api[method](*params)` as JSON; works for any dotted method name,
  including non-queryable ones like `system.info`.
  After a literal `--`, **fields** replace hand-written JSON:
  `--field=value` and bare `field=value` are interchangeable, and each is
  typed from the method's own schema (booleans from the strict true/false
  sets, integers, `null` for a nullable field, arrays from a comma list *or* a
  repeated flag, nested objects from dotted names). `--name:json=<json>` takes a
  literal JSON value and `--name=@path` reads one from a file. Fields fill the
  **last object-typed parameter**, so `call user.update -p 1 nas1 --
  --full_name=x` still reads its id from `-p`. An unknown field name or a bad
  enum value is an error naming the alternatives, raised **before** anything is
  called — nothing partial reaches the appliance. The separator is required
  because the valid names are only known after the method is parsed, so
  top-level flags would collide with the globals. `--no-schema` types fields the
  way `-p` does and validates nothing; `--refresh-api` re-fetches the
  definition.
- **`help NAME [--json] [--dump] [--api-version V] [--refresh-api]
  [targets...]`** — CLI-style help. `NAME` is a method (`user.create`: usage,
  every field with type/required/default/enum values, whether it is a job, and
  the return type), a namespace (`user`: its methods with their first doc line),
  or **`all`**/`.` for the index of namespaces. `NAME` is **required** and comes
  first, like `query`'s namespace: made optional, argparse would claim the lone
  token of `help nas1` and leave no target, so the index is spelled `all`.
  The source is the **API itself**, per namespace (`core.get_services` +
  `core.get_methods(<service>)`), which needs no roles and **no command access** —
  it works for an API-key account with no shell. `--dump` uses the full
  `middlewared --dump-api` instead (needs command access; required only for
  `--api-version`, which the live API cannot report). Either way it reads the
  definition, never generated stubs: a `.pyi` carries names and types only, while
  descriptions, defaults, enum values and required-ness exist solely in the
  definition the stubs are generated from.
- **`dump-api [targets...]`** — prints `client.dump_api()` as JSON.
- **`generate-typings [--api-version V] [--path DIR] [--api-cache FILE]
  [targets...]`** — dumps (or reads a cached) API definition and writes
  `.pyi` stubs via `pytruenas.codegen.Codegen().generate(version, path)`.
  `--path` defaults to `truenasapi_typings/current`; only an absent or empty
  directory, or one a previous run marked `.pytruenas-typings`, is replaced.
- **`deploy [--path PATH] [--mode pyz|dir] [--source installed|repo]
  [--pkg-root DIST] [--pkg-name PKG] [--extra E] [--skip DIST] [--force]
  [--repo-root PATH] [--ignore-file FILE] [--ignore-pattern PATTERN]
  [--include NAME] [--exclude NAME] [--pythonpath DIR] [targets...]
  [-- COMMAND ...]`** — installs pytruenas (or the caller's own distribution)
  ON the target so it can run there, through `hostctl.deploy.deploy()` (the
  probe, closure, reproducible payload, digest marker and atomic install are
  hostctl's; this command is the policy around it). Defaults to
  `/var/db/system/pytruenas.pyz` — a dataset on a *data* pool, which survives
  an update, unlike `/var/db` itself (boot environment). Anything after `--`
  runs on the target afterwards as `hostctl.Exec(*deployment.command,
  *args)` and its status is the command's, read from duho's
  `args._passthrough_` (the parsed instance carries everything after the
  first bare `--`). A `pyz` path is named `<path>.pyz` unless it already ends
  so; a `dir` path is used as given. Targets must come **before** the
  separator; a stray tail, or a command that reads none, is reported rather
  than dropped.
  An existing `--path` is replaced only if a previous deploy wrote its digest
  marker (`<path>/.digest` for `dir`, `<path>.digest` for `pyz`); anything else
  raises `FileExistsError` and is left alone — `--force` only skips the
  "already current" check. Both layouts are written beside the target and
  renamed into place, and a `dir` deploy interrupted between its renames is
  restored from `<path>.old` on the next run.

  `--source` picks **what** gets bundled and `--mode` the output **layout**
  (zipapp or unpacked tree), with one constraint: `--source repo` requires
  `--mode dir` and is refused with the default `pyz`, because a zipapp needs an
  importable package root and a working tree has none. That and a relative
  `--path` are usage errors (exit status 2) reported once, before any target.
  - `installed` (default) — the resolved dependency closure. Probes what the
    host already has (and its PEP 508 marker environment) and bundles only the
    difference. `--pkg-root`/`--pkg-name` name the distribution and its import
    name (default `PYTRUENAS_PKG_ROOT`/`PYTRUENAS_PKG_NAME`, else pytruenas);
    `--extra` adds an extra's dependencies, `--skip` never bundles a named
    distribution.
  - `repo` — a working tree copied as-is from `--repo-root` (default `.`),
    filtered by whichever of `.gitignore`/`.ignore`/`.bundleignore` exist.
    `--ignore-file` narrows that selection; `--ignore-pattern` adds a
    gitignore-style pattern applied after them (a leading `!` un-ignores).
    `--pythonpath` names directories, relative to the repo root, to put on the
    launcher's `PYTHONPATH` (default: whichever of `src/`, `lib/`, `vendor/`
    and the root itself hold an importable package, in that order). It is a
    `hostctl.deploy.SourceTree`; `pathspec` (and `tomli` below 3.11) come with
    the core dependency `hostctl[deploy]`.
    Repo mode does **not** vendor the repo's own dependencies — that needs
    them installed here, the thing repo mode exists to avoid. It *logs* what
    the repo declares as a heads-up; `--include`/`--exclude` adjust only that
    logged list (each takes a bare dependency name or a bracketed `[extra]`,
    exclude wins). `--skip` is the `installed`-mode counterpart and has no
    effect here.

### Writing a command module (`pytruenas.cmd.*` or a `--cmdspath` entry)

A command is a plain module exposing:

- **`run(client, args, logger)`** — required; the command body, called once
  per target with a connected `TrueNASClient`. A module without it is skipped
  at discovery (with a warning) rather than offered and then failing.
  `args` is a **per-target copy** carrying **`args.target`** (this target's
  connection string), so state a command writes on it cannot reach another
  target. The CLI closes a client it built when the command finishes; one an
  `init` hook returned is left alone. Return an exit code — never raise
  `SystemExit` from a command body: it runs in a fan-out worker, where raising
  it aborts the whole run and discards the other targets' codes. A
  `hostctl.MissingExtraError` out of `run` (an optional extra not installed,
  hostctl's or pytruenas's) ends that target with one ERROR line and status
  125, as hostctl's own command line does; any other exception keeps its
  traceback.
  Write results through `utils.cmd.emit_json(value, args)` (or `emit(text)`):
  one locked write, so concurrent targets cannot interleave mid-line, and with
  more than one target each line is `{"target": ..., "result": ...}` with the
  credentials removed. `utils.cmd.json_default` is the encoder fallback (sets
  become sorted lists, dates ISO strings, bytes text, anything else its
  `str()`).
- **`Args`** — optional; a `PyTrueNASArgs` subclass declaring the command's own
  CLI fields (added to the subparser before `register` runs). Preferred over
  `register`: an annotated attr + docstring + bare flags-tuple becomes a CLI
  field, e.g. `("method",)` for a positional or `("--param", "-p")` for an
  option. A `list[str]` option is repeatable as declared (`-f a -f b`, one
  value per occurrence), so it never swallows the trailing targets.
- **`register(parser, args, logger)`** — optional; the imperative escape hatch,
  for what declarations can't express (mutually-exclusive/titled groups). The
  trailing `TARGET...` positionals are declared centrally as the command's last
  field (`pytruenas.utils.cmd.with_targets`, applied by `main()` to every
  module command), so a command never declares them itself — declared and
  `register`-added positionals both land ahead of the targets, and the targets
  are part of the command's MCP tool schema.
- **`_allow_passthrough_ = True`** — optional, module level; the command reads
  the arguments after `--` (`args._passthrough_`). Without it, a `--` tail is
  reported as ignored. RunPath commands are taken to read it.
- **`validate_args(args)`** — optional; called once with the parsed args
  before any target runs or any client is built. Raise `duho.UsageError` for
  an invocation the arguments alone show cannot work: it is reported once as
  `pytruenas: error: MESSAGE` with exit status 2, instead of failing every
  target.
- **`init(args, logger) -> client`**, **`success(client, args, logger)`**,
  **`finally_(client, args, logger)`** — optional lifecycle hooks
  (`finally_` always runs).

### RunPath step directories (`pytruenas.utils.runpath`)

A **RunPath** is a directory of numbered `NN-name.py` *step* files run in
order, with no `__init__.py` — placed among the command sources
(`PYTRUENAS_PATH` / `--cmdspath` / config `commandspath`, or nested one level
inside a source directory) it becomes a subcommand named after the directory.
The discovery, ordering, filename modifiers and `--rcopts` selection are
`duho.runpath`'s (requires `duho>=0.7.5,<0.8`); pytruenas fans the whole step
directory out **once per target**, each target getting its own connected
`TrueNASClient` — the same per-target fan-out the built-in commands get.
Author one with:

- **`__main__.py`** (optional lifecycle) — `init(cmd, logger) -> ctx` builds
  the per-target client (its return is the `ctx` every 2-arg step receives);
  `success(ctx, cmd, logger)` / `finally_(ctx, cmd, logger)` run once after the
  steps. `cmd` is the parsed command instance for THIS target, carrying its
  target string and any per-target state a step needs (an attribute stashed
  in `init` and read by later steps is isolated per target). Re-export
  `default_init` as `init` to build the client from the target with no
  boilerplate.
- **`NN-name.py`** step files — each exposes a `main`/`run`/`call` entrypoint;
  written `main(cmd, ctx)` it receives the `__main__.py` context, written
  `main(cmd)` it does not (arity-detected). A step logs through
  `cmd._logger_`, already `[target]`-prefixed. A step may set module-level
  `PRIORITY`, `REQUIRED`, `BEFORE`, `AFTER` (ordering) — see `duho.runpath`.
- **`-O`/`--rcopts PATTERN[,PATTERN…]`** selects steps (fnmatch on step name):
  `!name` disables, `!*,build` = disable-all-then-enable-`build`, filename
  `!`/`!strict`/`!enable` tokens set per-step defaults. The grammar and its
  precedence are `duho.runpath`'s (see the `duho` docs for the authoritative
  description).

The module exports:

- **`default_init(cmd, logger) -> TrueNASClient`** — the per-target
  `__main__.py` client builder: the parsed instance's `_client_()` for its
  target.
- **`PyTrueNASRunPathArgs`** — the shared root every RunPath command inherits:
  `PyTrueNASArgs` (the target fields and fan-out methods, and `_logger_` via
  `LoggingArgs`) plus the trailing `TARGET` positional, which puts the hosts in
  a RunPath command's MCP tool schema.
- **`step(entrypoint)`** — decorator letting a step use the module command
  signature `run(client, args, logger)`: `client` is the `ctx` from `init`,
  `args` the per-target `cmd`, `logger` its `_logger_`. A step may declare
  fewer parameters (`(client, args)` or `(client)`) and is handed only those.
  Without it, a step written that way fails at run time (duho passes two
  positionals, in the other order). Opt-in; a duho-native step needs nothing.

## Environment variables

Every `PYTRUENAS_*` setting is read through one accessor, `utils.cmd.ENV` (a
`duho.env.Env("pytruenas")`), so the set is enumerable with `sorted(ENV)`.
`autoload=False` on purpose: the companion-module feature would import a
`pytruenas_env` module from anywhere on `sys.path` including the CWD, and a CLI
is routinely run from a directory the user does not control.

- **`PYTRUENAS_CONFIG`** — the CLI's config file when `--config` is not given;
  the file must exist. Read when the file is needed.
- **`APPDATA`** (Windows), **`XDG_CONFIG_HOME`** — where the default config file
  `pytruenas/pytruenas.cfg` is looked for (`~/.config` without the latter).
- **`PYTRUENAS_PATH`** — `os.pathsep`-separated extra command source(s) for CLI
  discovery (read with `ENV.paths`, which splits on the platform separator, so
  a Windows `C:\...` entry is not mis-split on its drive colon).
- **`PYTRUENAS_PKG_ROOT` / `PYTRUENAS_PKG_NAME`** — the distribution `deploy`
  bundles, and the package the deployed copy runs. For when pytruenas is a
  *dependency* of the thing being deployed rather than the deliverable.
- **`PYTRUENAS_CACHE`** — directory for the cached API definition (read by
  `utils.apicache`), one gzipped file per host and API version. Default: the
  platform user cache directory (`$XDG_CACHE_HOME/pytruenas`, `XDG_CACHE_HOME`
  defaulting to `~/.cache`; or `%LOCALAPPDATA%\pytruenas\cache`). A host label
  is sanitized to a single path component, so a connection string cannot
  choose where the file lands.
- **`PYTRUENAS_INSECURE`**, **`PYTRUENAS_CA_BUNDLE`** — the CLI's TLS
  defaults when no flag is given (`._verify_()` above): a boolean
  (`true`/`false`/`1`/`0`/`yes`/`no`/`on`/`off`, ...) that turns verification
  off, and an existing CA bundle path. Empty is unset (the config file's
  `insecure`/`ca_bundle`, then `True`).
- **`PYTRUENAS_MCP`** — not read by pytruenas itself, nor through `ENV`:
  `duho`'s own `<PREFIX>_MCP` launch trigger, keyed off this app's `Env`
  prefix. Setting `PYTRUENAS_MCP=stdio` makes `main()` serve MCP over stdio
  instead of the normal CLI dispatch, exposing every built-in command
  (`call`, `query`, `deploy`, ...) and RunPath command as an MCP tool, whose
  `targets` argument names the hosts (none: `localhost`). Checked in both
  `duho.main` and `duho.app`, so it applies here regardless of entry point.
  It is enabled: no opt-out is set (`_mcp_ = False` on `PyTrueNAS`, or
  `app(mcp=False)`, would disable it).
- **`PYTRUENAS_CREDENTIALS`** — **a secret**: credentials in any one-string
  form `Credentials(...)` takes (an API key, `user:password`, a token). Read by
  `Credentials.from_env()`, and by the CLI (`PyTrueNASArgs._credentials_`) for
  a target that carries no credentials of its own. Empty is unset.
- **`PYTRUENAS_CALL_TIMEOUT`** — the per-call JSON-RPC timeout in seconds (a
  positive number, fractions allowed) when neither `timeout=` nor
  `TrueNASWSConnection(call_timeout=)` sets one; default 60. Read when a
  connection is built (`connection.default_call_timeout()`), never at import;
  a value that is not a positive number raises `ValueError` then. Also the
  default of the side channels' read timeout.
- **`SSL_CERT_FILE`**, **`REQUESTS_CA_BUNDLE`**, **`CURL_CA_BUNDLE`**,
  **`WEBSOCKET_CLIENT_CA_BUNDLE`**, in that order — the first one set
  (non-empty) is the CA bundle `verify=True` trusts instead of the operating
  system. A bundle passed as `verify=` takes precedence over them.

## Gotchas

- **Middleware parameters are positional.** `client.api.user.query(filters)`,
  not `filters=`: any keyword the method does not take raises `TypeError`.
  The `_query`/`_get`/`_create`/`_update`/`_upsert` helpers take keywords.
- **Nothing connects until first use.** Building a client, a
  `TrueNASConfig` or a `TrueNASWSConnection` does no network I/O; a wrong
  host, port or credential surfaces on the first call.
- **A bare host means TLS.** `"nas"` is `wss://nas/api/current`; spell
  `ws://` for plaintext, which logs a warning when credentials go to a
  non-loopback host.
- **Percent-encode a password** containing `/`, `?`, `#` or `@` in a target
  string; an unencoded `@` after the host is read as part of the path.
- **`ConnectionClosed.sent is True` means the call may have run.** Only an
  unsent request is retried; decide yourself whether to repeat a create or a
  delete.
- **A subscription callback runs on the reader thread** and cannot make a call
  (`RuntimeError`); consume `Subscription.events()` on another thread. A
  subscription ends on a reconnect — re-subscribe when `events()` ends.
- **A 2FA session needs `otp_provider`** to survive a reconnect; the one-time
  code in the credential is spent by the first login.
- **`core.job_wait` does not block** — it is itself a job. Use `job=True`,
  `.wait()` or `.job_updates()`.
- **`core.get_methods()` with no argument closes the websocket**; pass a
  service name (`"user"`), not a method name (`"user.create"` returns `{}`).
- **A middleware method named `subscribe`** is shadowed by
  `Namespace.subscribe`; call it as `ns(_method="subscribe", ...)`.
- **`.ssh` belongs to hostctl's event loop**: never await its coroutines on
  your own loop.
- **A relative remote path is rooted at `/`**, on every leg, not at a login
  directory.
- **Stats from a listing carry `st_mtime` 0** (`filesystem.listdir` reports no
  mtime); call `stat()` when you need it.
- **`--cmdspath` splits on `:`**, which breaks a Windows drive letter; use
  `PYTRUENAS_PATH` (split on `os.pathsep`) there.
- **Never raise `SystemExit` from a command body**: return an exit code.
