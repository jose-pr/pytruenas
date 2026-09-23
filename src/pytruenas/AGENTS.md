# `pytruenas` — public API header

Header-file-style reference for the `pytruenas` package: every public export
with its signature, arguments, contract, and gotchas, so this module can be
consumed without reading its source. Kept current with the public API. For the
project overview and CLI usage, see the project overview doc at the repo root.

## Package root (`pytruenas`)

`__all__ = ["Namespace", "TrueNASClient", "TrueNASHost", "TrueNASConfig",
"Credentials", "Event", "Subscription", "TrueNASWSConnection", "__version__"]`

- **`__version__: str`** — resolved from installed package metadata
  (`importlib.metadata`); `"0.0.0.dev0"` when run from a bare checkout with the
  package not installed.

## `TrueNASClient` (`pytruenas.host`)

**`TrueNASClient` is `TrueNASHost`** — one class, two names. They were briefly
two objects forwarding halves of their surface to each other (`client.run()`
called `client.host.run()`; `host.api` called `host.client.api`); that is gone.
`client` is the friendlier word at a call site, `TrueNASHost` is where the
host half of the API is documented, and `.client`/`.host` both return the
object itself.

`TrueNASClient(target=None, credentials=None, *, verify=True, sslverify=None,
shell=None, known_hosts=<follows verify>, logger=None, autologin=True,
version="current", executor=None, path=None, ssh=None, ...)`

- **`target`** — a host, `"host:port"`, or full `scheme://...` URI. `None` /
  omitted / local-only resolves to the local middleware unix socket
  (`ws+unix:///var/run/middleware/middlewared.sock`). A remote target with no
  scheme or path resolves to **TLS and the current API** — `"nas"` means
  `wss://nas/api/current`; `ws://`/`http://` selects plaintext. Nothing is
  probed and building a client performs no network I/O, so a bad host raises on
  first use. A password in the
  userinfo must percent-encode `/`, `?` and `#` (`%2F`, `%3F`, `%23`); a raw
  one raises `ValueError` (message redacted) instead of being split into a
  host/port/path.
- **`credentials`** (positional as `creds` historically) — passed to
  `Credentials(...)` (below); `None` means local-socket auth (no login call).
- **`autologin`** (default `True`) — the first `.conn` access calls
  `.login()` automatically when there's no live connection.
- **`verify`** (default `True`) — one switch for every check the client
  makes. `verify=False` turns off TLS certificate verification (the API
  websocket, the HTTP(S) side channels, the web shell) **and** SSH host-key
  verification (commands and SFTP): `sslverify` becomes `False` and
  `known_hosts` becomes `None`, including on an explicit `ssh=SshConfig(...)`
  still at its `()` default (a copy is changed, not yours). A specific
  `sslverify=` or `known_hosts=` overrides it.
- **`sslverify`** (default: follows `verify`) — TLS certificate verification
  for `wss://`, the HTTP(S) side channels and the web shell, all through one
  context (`pytruenas.utils.tls.context`). `True` trusts the OS store only
  (never certifi), unless `$SSL_CERT_FILE`, `$REQUESTS_CA_BUNDLE`,
  `$CURL_CA_BUNDLE` or `$WEBSOCKET_CLIENT_CA_BUNDLE` is set — the first one
  set is trusted *instead*. A path (`str` / `PathLike`, a PEM file or hashed
  directory) is the CA bundle, trusted instead of the OS store; it is stored
  as a `str`. A missing bundle raises `FileNotFoundError` naming the path and
  its source at connect time.
- **`shell`** — connection string for the SSH leg (`"ssh://root@nas"`,
  `"root:pw@nas:22"`). Stored as an `SshConfig` on `.config.ssh`; pass
  `ssh=SshConfig(...)` to supply one directly.
- **`known_hosts`** (default: `()`, or `None` under `verify=False`) —
  host-key policy for the SSH leg built from
  `shell=` or by `.install_sshcreds()`, with hostctl's values: `()` verifies
  against `~/.ssh/known_hosts`, `None` does not verify, a path or list of paths
  names the file(s). An explicit `ssh=SshConfig(...)` keeps its own. Both the
  command and SFTP halves verify by default; an unverifiable key (or an
  unreachable SSH port) makes `run()` and `path()` fall back to the websocket
  providers, and `run()` logs one WARNING per host when it does.
- **`executor`/`path`** — name the providers to use, in preference order.
  Replaces `fsbackend`, which could only pick a filesystem backend; see the
  provider table below.
- **`version`** — API path used when the target carries none (default
  `"current"`, i.e. `/api/current`).

### Attributes / properties

- **`.api`** (`cached_property`) — the root `Namespace` for this client
  (`client.api.<namespace>.<method>(...)`).
- **`.conn`** (alias `.websocket`) — the live
  `connection.TrueNASWSConnection`; connects (and logs in, if
  `autologin`) on first access, reconnects if the prior connection closed.
  After a successful `.login(...)`, a reconnect repeats that login (same
  credentials, `login_ex`, options, `otp_provider`) regardless of
  `autologin`. Thread-safe: concurrent first use opens one connection.
- **`.ssh`** — a lazily-opened `asyncssh` connection (requires the `ssh`
  extra), reached through the composed SSH transport. Raises if none is
  configured. For the raw connection only; `.run()`/`.path()` select a
  transport instead of assuming this one.
- **`.config`** — the `TrueNASConfig` this was built from. `.config.ssh` is the
  SSH leg; `.shell` means the *bound shell object* (`client.shell.run(...)`),
  as it does throughout hostctl.
- **`.client`** / **`.host`** — both return the object itself, kept so code
  written against the two-object model keeps working.
- **`.capabilities`** — `{"run", "path"}` as available, plus `"spawn"`/`"tty"`
  when an SSH leg is configured; a remote target with no SSH and no web shell
  honestly reports no `run`.
- **`.last_selection`** — the redacted provider trace for the most recent
  `run()`: what was tried, what was chosen, and why.
- **`.name`** — the host's short label: the hostname, plus the port only when
  it is non-default (`nas1`, `nas1:8443`, `localhost` for the unix socket).
  This is what identifies the host in logs; `.config.connection_uri` is the
  full canonical (and credential-free) URI.
- **`.logger`** — a logger bound to `.name`, so every record it emits is
  prefixed `[nas1]` — including records from the JSON-RPC connection, which
  shares it. Defaults to `logging.getLogger("pytruenas")` underneath; pass
  `logger=` (a name or a `Logger`) to redirect it. A `LoggerAdapter` you pass
  in yourself is used as-is, unwrapped.

### Methods

- **`.login(creds=None, *, login_ex=False, login_options=None,
  otp_provider=None)`** — close any existing connection, open a new one, and
  authenticate (`creds` or the client's configured credentials). Default uses
  the legacy `auth.login`/`login_with_*` path. `login_ex=True` uses the modern
  `auth.login_ex` mechanism, handling an `OTP_REQUIRED` 2FA challenge via
  `auth.login_ex_continue` (OTP from the credential's `otp_token` or
  `otp_provider()`), raising `auth.AuthenticationError` on failure and returning
  the success response dict. `login_options` overrides the server defaults
  (`{"user_info": True, "reconnect_token": False}`). The legacy path returns
  the server's answer (`True`) and raises `AuthenticationError` when it is
  `False` (a wrong password or key — the server does not error). On any
  failure the new connection is closed, not left open unauthenticated. A
  one-time OTP is not replayable, so a session that must survive a reconnect
  needs `otp_provider`.
- **`.me() -> dict`** (`auth.me`) / **`.logout() -> None`** (`auth.logout`) /
  **`.ping() -> str`** (`core.ping` -> `"pong"`) — convenience wrappers.
- **`.path(*path, backend=None)`** — build a `pathlib_next` path rooted at
  `path`. `backend` names one **path provider** for this call, from the names
  in the provider table below (`"tnasws"`, `"sftp"`, `"local"`), and raises
  `ValueError: unknown path provider` for anything else — including a provider
  this host has not got (`"sftp"` without an SSH leg, `"local"` on a remote
  host). Not the `pytruenas.fs.path()` vocabulary (`"ws"`/`"api"`/`"truenas"`),
  which is a different function documented under `fs` below. Inherited from
  `hostctl.host.Host`.
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
- **`.upload(file, method, *params, token=None, wait=True, **kwargs)`** —
  upload `file` (`str`/`bytes`) via the middleware's `/_upload` HTTP side
  channel, then call `method(*params, **kwargs)` server-side with it; waits on
  the resulting job by default. Auto-generates a short-lived auth token when
  none is given.
- **`.download(method, *args, filename=None, buffered=False, wait=True,
  **kwargs)`** — call `method` to get a download link/job, fetch it over
  HTTP(S), and return the bytes (when `wait=True`) or the job id.
  For both, `wait=` may also be a callable: it waits, and is passed to
  `.wait(callback=...)` for progress.
- **`.subscribe(event, callback=None, *, maxsize=1000) -> connection.Subscription`**
  — subscribe to a middleware collection event over the live websocket.
  `client.subscribe("alert.list")` is shorthand for
  `client.api.alert.list.subscribe()`. Consume via the returned subscription's
  `.events(timeout=None)` iterator and/or the inline `callback`. Bound to the
  current connection; does **not** survive a reconnect (the `events()` iterator
  ends on disconnect — that's the re-subscribe signal). See `connection` below.
- **`.dump_api() -> dict`** — run `middlewared --dump-api` on the target and
  return the parsed JSON (see `pytruenas.models.apidump.Api`).
- **`.install_sshcreds(name=None, private_key=None)`** — generate/reuse an SSH
  keypair via `keychaincredential`, install the public half on `root`'s
  `authorized_keys`, and store the private half on `.config.ssh` as a real
  `SshConfig.client_keys`. Returns the private key. Needs **no** optional
  extra: provisioning runs over the middleware API and opens no SSH
  connection. Passing `private_key=` for a key the host does not already know
  is the exception — the public half is derived locally, which needs
  `cryptography` (preferred) or `asyncssh`.
  The providers are rebuilt afterwards, so a host that had no SSH executor
  gains one. A *local* target provisions the key but wires no leg — there is
  nothing to SSH to.

## `TrueNASHost` / `TrueNASConfig` (`pytruenas.host`)

`TrueNASHost` **is** `TrueNASClient` (same class). Constructible from a
connection string, a `TrueNASConfig`, or nothing:

```python
TrueNASHost("wss://nas")
TrueNASHost("nas", credentials="1-...", executor=["ssh"])
TrueNASHost()                       # the local middleware socket
```

It is a `hostctl.host.PosixHost`, so `run`, `path`, `spawn`, `info`, `connect`,
`close`, `shell`, `capabilities`, and `last_selection` are all inherited; the
middleware surface (`api`, `websocket`, `login`, `logout`, `me`, `ping`,
`subscribe`, `upload`, `download`, `dump_api`, `install_sshcreds`) is what this
class adds. Generic in `ApiVersion`: `TrueNASHost[Current]("nas").api`
completes like `TrueNASClient[Current]`.

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
prints, so captured stdout is exact bytes and nothing typed is interpreted.
Uncaptured stdout streams live; stderr is captured separately but delivered
when the command ends (`stderr=STDOUT` merges live); `stdin=` is read to EOF
first (no incremental stdin); no input means `/dev/null`; `timeout=None`
waits forever; a timeout interrupts, closes the session and raises
`TimeoutExpired(orphaned=False)`. Requires a POSIX login shell with
`base64`, `mktemp` and `stty` (TrueNAS root's zsh qualifies).

**Overriding the selection.** `executor=` and `path=` name the providers to
use, in preference order — a single name or a sequence:

```python
TrueNASConfig.from_target("wss://nas", executor="ssh", path="sftp")   # SSH only
TrueNASConfig.from_target("wss://nas", executor=["ssh"])              # no web shell
TrueNASConfig.from_target(None, path=["local", "tnasws"])             # force tnasws locally
TrueNASConfig.from_target("wss://nas", executor=[])                   # no run capability
```

Valid names are `local`/`ssh`/`webshell` for executors and
`local`/`sftp`/`tnasws` for paths; an unknown one raises rather than silently
composing a host with nothing. Requesting `ssh`/`sftp` without an `SshConfig`
also raises. `None` (the default) means "decide from the target".

`TrueNASConfig` is the `hostctl.host.HostConfig`. It accepts every connection
string `TrueNASClient` does and normalizes to a `truenas+*` scheme
(`truenas+auto`, `+ws`, `+wss`, `+unix`); `HostConfig("truenas+wss://nas")`
works from hostctl's own registry. Constructing one performs **no network
I/O** — the scheme and API path are resolved from the string alone, not in the
constructor.

An OTP travels in the URI password field after a newline
(`wss://root:pw%0Aotp:123456@nas`); a raw newline works too on recent hostctl.
Unknown credential names are rejected rather than silently dropped. The
keyword form dispatches on the names (`username`/`password`/`otp`/`api_key`/
`token`), the same selection `Credentials.from_host_credentials` makes.

Generic type parameter `ApiVersion` (bound to `Namespace`) lets a consumer
annotate `client: TrueNASClient[Current]` (from generated typings) for
IDE/type-checker completion on `client.api`; it has no runtime effect.

## `Namespace` (`pytruenas.namespace`)

Dynamic attribute-style dispatcher for one API namespace path (e.g.
`client.api.user`, `client.api.pool.dataset`). Attribute/item access builds
child namespaces lazily and caches them per-instance
(`namespace.child` / `namespace["child"]`); leading-underscore names other
than the dunder-safe helpers below raise `AttributeError` normally.

- **`Namespace(client, *name)`** — not usually constructed directly; reached
  via `client.api` and attribute/`__getitem__` traversal.
- **`__call__(*args, _tries=1, _method=None, _ioerror=False,
  _filetransfer=False, _timeout=UNSET, **kwds)`** — invoke this namespace's
  middleware method (`self._namespace`, optionally suffixed with `_method`).
  Middleware methods take **positional** parameters: any other keyword raises
  `TypeError` naming it. (It used to be swallowed, so
  `client.api.user.query(filters=[...])` sent no filters and returned every
  row.) `timeout` and the upstream-compatibility names are still accepted, and
  the `_query`/`_get`/`_update` helpers below take keywords by design.
  - **`_tries`** — reconnect retries after a dropped connection
    (`ECONNABORTED`); default `1` means up to 2 attempts total. The call
    **always** returns or raises — never silently returns `None` on a
    connection error.
  - **`_timeout`** — per-call seconds; the default sentinel uses the client's
    configured timeout, `None` waits indefinitely.
  - **`_ioerror`** — map a middleware `[ERRNO] message` error to the matching
    `OSError` (see `pytruenas.namespace.ioerror`).
  - **`_filetransfer`** — `True` routes through `client.download`; bytes/a
    readable routes through `client.upload`.
- **`.subscribe(callback=None, *, event=None, maxsize=1000) ->
  connection.Subscription`** — subscribe to this namespace's collection event; the
  event name defaults to the namespace's dotted path
  (`client.api.alert.list.subscribe()` -> `alert.list`), or pass `event=` to
  override (e.g. from `client.api`). A **real method**, so it shadows any
  middleware method literally named `subscribe`; reach such a method via
  `ns(_method="subscribe", ...)`. See `connection.Subscription`/`Event` above.
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
  result)` (`action` is a `DbAction` — `CREATE`/`UPDATE`/`UPSERT`) fires after
  the mutation when given. Common opts: `idkey` (default `"id"`),
  `update_exclude`/`create_exclude` (field names to drop for that path),
  `wait` (wait on a returned job id; default `True`), `force`.

## `connection` (`pytruenas.connection`)

The synchronous JSON-RPC 2.0 websocket transport backing `TrueNASClient`
(re-exported as `pytruenas._conn`). All annotations are quoted so the module
imports on Python 3.9.

- **`Client(uri=None, *, verify_ssl=True, call_timeout=CALL_TIMEOUT,
  connect_timeout=CONNECT_TIMEOUT, py_exceptions=False)`** — opens the
  websocket immediately (blocking, bounded by `connect_timeout`: connect, TLS
  and the HTTP upgrade) and starts a background reader thread. `uri` is `wss://`/`ws://` or
  `ws+unix://...`; `verify_ssl` takes the same values as the host's
  `sslverify` (bool or CA bundle path; see above); `None`/bare `ws+unix://` connects to
  `DEFAULT_UNIX_SOCKET` (`/var/run/middleware/middlewared.sock`).
  - **`.call(method, *params, timeout=UNSET, **_ignored) -> Any`** — send a
    request and block for the matching response. `timeout=None` waits
    **indefinitely**; the default sentinel uses `call_timeout`. Unknown
    kwargs in `{"job", "background", "callback", "register_call", "raise_"}`
    are silently accepted (upstream-client compatibility); any other unknown
    kwarg is logged at debug level. Raises `ValidationErrors`/
    `ClientException` on a server error, `CallTimeout` on timeout,
    `ConnectionClosed` (`errno=ECONNABORTED`) if the connection dropped,
    `ClientException` with `errno=EPROTO` when the response arrived but could
    not be decoded (the call fails at once rather than waiting out its
    timeout),
    `TypeError` for a parameter JSON cannot encode (nothing is sent), and
    `RuntimeError` when called from the reader thread, i.e. from a
    subscription callback (it would deadlock until the call timed out —
    consume `Subscription.events()` on another thread instead).
  - **`.subscribe(event, callback=None, *, maxsize=1000) -> Subscription`** —
    issue `core.subscribe(event)` and route its `collection_update`
    notifications to a `Subscription`. The registry is keyed by event name
    (the notification's `params.collection`, the routing key — NOT the returned
    sub id); two subscribers to the same event both receive it.
  - **`.close()`** — idempotent; also usable as a context manager. Wakes every
    subscription's `events()` iterator (as does a dropped connection), and
    releases the socket even when the server closed the connection first.
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
  dict. Verified against TrueNAS 26.0.
- **`DEFAULT_EVENT_QUEUE_SIZE`** — default `maxsize` (1000) for a subscription's
  event queue.
- **`CALL_TIMEOUT`** — default per-call timeout in seconds (int; overridable
  via the `CALL_TIMEOUT` env var, read at import time).
- **`CONNECT_TIMEOUT`** — default timeout in seconds (30) for opening a
  connection. It is not the reader's timeout: an idle connection stays open.
- **`ClientException(error, errno=None, trace=None, extra=None)`** — base
  error for any call/connection failure; `errno` carries a POSIX errno when
  the middleware's `[ERRNO] message` prefix maps to one.
- **`ValidationErrors(errors)`** (`ClientException` subclass) — per-field
  validation errors; `.errors` is `list[(attribute, errmsg, errcode)]`.
- **`JobFailed(job)`** (`ClientException` subclass) — raised by
  `TrueNASHost.wait` for a `FAILED`/`ABORTED` job; `.job` is the
  `core.get_jobs` record, `.errno` the middleware's errno when it reports one.
- **`CallTimeout()`** (`ClientException` subclass) — raised when a call
  exceeds its timeout.
- **`ConnectionClosed(sent)`** (`ClientException` subclass, `errno` is
  `ECONNABORTED`) — the connection closed before the response arrived.
  **`.sent`** is `False` when the request never reached the socket (safe to
  repeat: `Namespace` retries exactly these) and `True` when the server may
  have run it — a create, a delete, a job start — so only the caller can
  decide. A plain `ClientException(errno=ECONNABORTED)` carries no `.sent` and
  is treated as "may have run".
- **`dumps(obj, **kwargs) -> str`** / **`loads(data, **kwargs)`** — JSON
  (de)serialization with the middleware's extended-type wrappers
  (`datetime`/`date`/`time`/`set`/`IPv4Interface`/`IPv6Interface`)
  round-tripped through `$date`/`$type`/`$time`/`$set`/`$ipv4_interface`/
  `$ipv6_interface` wrapper objects.

## `auth` (`pytruenas.auth`)

- **`Credentials(...)`** — a factory (via metaclass `__call__`), not a normal
  constructor when called on the base class directly:
  - no args -> `LocalAuth()` (local-socket auth, no login call);
  - a single `None` -> `LocalAuth()`;
  - a single `Credentials` instance -> returned as-is;
  - a single `(user, password)` list/tuple -> `BasicAuth(*it)`;
  - a single string containing `:` -> `user:password` (optionally
    `password\notp_token`) -> `BasicAuth`;
  - a single string shaped `<numeric-id>-<64 alnum chars>` -> `ApiKeyAuth`;
  - any other single string -> `TokenAuth`;
  - multiple positional args -> `BasicAuth(*args)`.
  - Instantiating a `Credentials` **subclass** directly (e.g. `BasicAuth(...)`)
    bypasses the factory and behaves like a normal constructor.
- **`.login(client)`** — legacy path: `client.api.auth[self.METHOD]
  (*self._args())`, returning its result; raises
  `AuthenticationError("AUTH_ERR", {"method": METHOD})` when that is `False`.
  A no-op returning `None` when `METHOD` is `None` (`LocalAuth`).
- **`.login_ex(client, *, login_options=None, otp_provider=None) -> dict|None`**
  — modern path via `auth.login_ex` using this credential's `MECHANISM`
  (`PASSWORD_PLAIN`/`API_KEY_PLAIN`/`TOKEN_PLAIN`). Handles `OTP_REQUIRED`
  (continues with `auth.login_ex_continue`, OTP from `self.otp_token` or
  `otp_provider()`), returns the `SUCCESS` response dict, raises
  `AuthenticationError` otherwise. Falls back to legacy `.login()` for a
  credential with no login_ex form.
- **`AuthenticationError(response_type, response, method="login_ex")`** —
  raised by `login_ex` on a non-`SUCCESS` response and by legacy `login` on a
  `False` answer; `.response_type` is the server discriminator, `.response`
  the full dict; the message names `method`.
- **`Credentials.from_env(env=None) -> Credentials`** — `Credentials(env.get("TN_CREDS"))`, defaulting `env` to `os.environ`.
- **`LocalAuth`** — no-op auth (local socket). **`ApiKeyAuth(api_key,
  username=None)`** — `login_with_api_key` (legacy) / `API_KEY_PLAIN` (login_ex,
  needs `username`). **`TokenAuth(token)`** — `login_with_token` / `TOKEN_PLAIN`.
  **`BasicAuth(username, password, otp_token=None)`** — `login` /
  `PASSWORD_PLAIN`.

## `fs` (`pytruenas.fs`)

`client.path(*segments, backend=None)` is the intended entry point; the
module-level `path(client, *segments, backend=None)` is what it delegates to.

- **`LocalPath`** — re-exported `pathlib_next.LocalPath`, used for a local
  client with no client-specific behavior.
- **`TnasWsPath`** (`pytruenas.fs.tnasws`) — a `pathlib_next` `UriPath`
  (scheme `truenas+ws`) backed entirely by the middleware `filesystem.*` API
  via a `TnasWsBackend(client)`. Implements stat/listdir/open/read/write/
  mkdir/chmod/chown; `unlink`/`rmdir` shell out (`rm -f` / `rmdir`) because
  `filesystem.*` has no delete op. Built from a bare URI (no backend) raises
  `RuntimeError` on first use — always construct via `client.path(...)`.
  Listing calls `filesystem.listdir` with an explicit `select` projection
  (`name` for `_listdir`; `name`/`type`/`size`/`mode` for `_scandir`, which
  seeds each child's stat in the same round trip). That is load-bearing, not
  an optimisation: an unrestricted `listdir` computes the ZFS-only `zfs_attrs`
  column and fails with `EFAULT ... ZFS attributes are not supported.` on any
  non-ZFS path (`/tmp`, `/dev`, `/proc`, ...), so widening the projection to
  that column breaks `iterdir`/`glob`/`walk` off-pool. `listdir` reports no
  `mtime` on any filesystem, so stats seeded from a listing carry `st_mtime`
  0; `stat()` uses `filesystem.stat`, which does report it.
  `mkdir(mode=None, parents=False, exist_ok=False)` — an omitted `mode` is
  `0o755` (the middleware applies the mode it is sent, with no umask; an
  explicit mode is sent as given); `parents=True` creates missing parents.
  Two paths are the same filesystem (for pathlib_next's same-file and overlap
  guards) when their backends talk to the same client or to clients with the
  same `connection_uri` — not merely when they share a backend object.
- **`TruenasPath`** (`pytruenas.fs.truenas`) — subclasses `TnasWsPath`; five
  operations — `unlink`/`rmdir`/`rename`/`symlink_to`/`readlink` — try an SFTP
  leg first (via `pathlib_next`'s `SftpPath`, requires the `ssh` extra +
  `client.config.ssh` host) and fall back to `TnasWsPath`'s websocket behavior (or
  raise `NotImplementedError` for ops SFTP alone can do — rename, symlink_to,
  readlink). **`resolve` is not one of them**: `SftpPath` has no `resolve`, so
  the attempt always raises `NotImplementedError` and `resolve()` returns
  `self` on every host, SFTP configured or not. `rename(target)` accepts a
  `str` or a path on the SAME host and returns the new `TruenasPath`; a target
  on another host (or of another type) raises `NotImplementedError`, so
  `move()` copies and deletes instead of renaming on the source host.
  `symlink_to(..., force=False, onremove=None)` adds a
  pytruenas-specific convenience: `force` (bool, a file-type string, or a set
  of `"file"/"link"/"directory"`) removes a conflicting existing target first;
  `onremove(path, kind)` gates each removal. The SFTP leg is resolved *before*
  `force` removes anything, so a host that cannot create the link raises
  `NotImplementedError` with the existing target still in place.
- **`TnasWsBackend(client)`** — the backend object `TnasWsPath`/`TruenasPath`
  carry; just holds `.client`.

`backend=` values: `"local"` -> `LocalPath`, `"ws"`/`"api"` -> `TnasWsPath`,
`"truenas"`/`"auto"` -> `TruenasPath`/`LocalPath` (`"auto"` picks `LocalPath`
for a local client).

**Segments are filesystem paths, not URIs** (since 0.4.5). Both remote types are
`UriPath`s, so `path()` percent-encodes each segment into the `truenas://` /
`truenas+ws://` URI it builds: a name containing `?`, `#`, `%`, a space or
non-ASCII survives `p.path` unchanged, and the SFTP leg re-encodes the decoded
name exactly once. Before 0.4.5 the segments were interpolated raw and
`client.path("/mnt/tank/cache?v=2")` addressed `/mnt/tank/cache` silently, on
**both** legs. Constructing a path type *directly* from a URI string
(`TruenasPath("truenas://nas/...")`) is unchanged and still URI syntax — `?`
there really is a query; encode the path yourself if you go around `path()`.

## `main` (`pytruenas.main`) — CLI entry point

- **`main(name=None, argv=None) -> int`** — build the `duho` app
  (`PyTrueNAS`), discover commands (built-ins in `pytruenas.cmd` plus any
  `PYTRUENAS_PATH` / `--cmdspath` / config `commandspath` entries), parse
  `argv`, and dispatch the selected command against every target
  concurrently. `pytruenas = "pytruenas.main:main"` is the installed console
  script.
- **`PyTrueNAS(PyTrueNASArgs, duho.Cli)`** — the app root; `--version` resolves
  from installed package metadata.

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
  it aborts the whole run and discards the other targets' codes.
  Write results through `utils.cmd.emit_json(value, args)` (or `emit(text)`):
  one locked write, so concurrent targets cannot interleave mid-line, and with
  more than one target each line is `{"target": ..., "result": ...}` with the
  credentials removed. `utils.cmd.json_default` is the encoder fallback (sets
  become sorted lists, dates ISO strings).
- **`Args`** — optional; a `PyTrueNASArgs` subclass declaring the command's own
  CLI fields (duho ≥0.4.1 adds them to the subparser before `register` runs).
  Preferred over `register`: an annotated attr + docstring + bare flags-tuple
  becomes a CLI field, e.g. `("method",)` for a positional or `("--param",
  "-p")` for an option. For a repeatable `list[str]` option use
  `NS(action='append', nargs=None)` — duho otherwise infers `nargs='*'`, and a
  greedy option swallows the trailing targets.
- **`register(parser, args, logger)`** — optional; the imperative escape hatch,
  for what declarations can't express (mutually-exclusive/titled groups). The
  trailing `TARGET...` positionals are added centrally, after this hook runs
  (`main._with_targets`), so a command never registers them itself — declared
  and `register`-added positionals both land ahead of the targets.
- **`init(args, logger) -> client`**, **`success(client, args, logger)`**,
  **`finally_(client, args, logger)`** — optional lifecycle hooks
  (`finally_` always runs).

`pytruenas.utils.cmd.PyTrueNASArgs` (a `duho.LoggingArgs` mixin) carries the
global fields every command sees: `config` (path, default
`$PYTRUENAS_CFG` or `./pytruenas.yaml`), `cmdspath`, `sslverify`
(`--sslverify`/`--no-sslverify`, unset by default), `insecure`
(`--insecure`/`-k`), `parallel` (default `1`), `logto` (default `-` for
stderr, or a `{target}`/`{isodate}` path template), plus `targets` (the
trailing positionals, not a flag) and helper methods
`._config_dict_()`/`._expanded_targets_()`. Target expansion (commas and
`[A-Z]`/`[0-9]` ranges) applies to the HOST part only -- a comma or a range
inside credentials is part of them -- and credentials are carried onto every
expanded host.

Three more methods decide how a command connects, and are the only supported
way to build a client from parsed args:

- **`._config_is_implicit_() -> bool`** — whether the config file was found
  (`./pytruenas.yaml`) rather than named by `--config`/`$PYTRUENAS_CONFIG`.
  `main` refuses `commandspath` from an implicit file: that key names code to
  import, and a CLI often runs in a directory its user does not control.
- **`._sslverify_() -> bool|str`** — `-k`/`--insecure`, else
  `--sslverify`/`--no-sslverify`, else `$PYTRUENAS_SSLVERIFY`, else the config
  file's `sslverify`, else `True`. A string is a CA bundle path.
- **`._credentials_() -> Credentials|None`** — `$TN_CREDS`, else the config
  file's `credentials` (a connection string, or a mapping of keyword
  arguments), else `None`.
- **`._client_(target) -> TrueNASClient`** — the client for one target: the
  above, with the credentials applied **only** when the target string carries
  none (passing both raises). `main` and `runpath.default_init` both use it,
  so a plain command and a RunPath step connect alike.

### Built-in commands (`pytruenas.cmd`)

- **`query <namespace> [-f/--filter KEY=VALUE ...] [targets...]`** — prints
  `client.api[namespace]._query(**filters)` as JSON. Only works on queryable
  namespaces (`<namespace>.query` must exist), e.g. `user`, `pool.dataset`.
- **`call <method> [-p/--param JSON ...] [targets...]`** — prints
  `client.api[method](*params)` as JSON; works for any dotted method name,
  including non-queryable ones like `system.info`.
- **`dump-api [targets...]`** — prints `client.dump_api()` as JSON.
- **`generate-typings [--api-version V] [--path DIR] [--api-cache FILE]
  [targets...]`** — dumps (or reads a cached) API definition and writes
  `.pyi` stubs via `pytruenas.codegen.Codegen().generate(version, path)`.
- **`deploy [--path PATH] [--mode pyz|dir] [--source installed|repo]
  [--pkg-root DIST] [--pkg-name PKG] [--extra E] [--skip DIST] [--force]
  [--repo-root PATH] [--ignore-file FILE] [--ignore-pattern PATTERN]
  [--include NAME] [--exclude NAME] [--pythonpath DIR] [targets...]
  [-- COMMAND ...]`** — installs pytruenas (or the caller's own distribution)
  ON the target so it can run there. Defaults to
  `/var/db/system/pytruenas.pyz` — a dataset on a *data* pool, which survives
  an update, unlike `/var/db` itself (boot environment). Anything after `--`
  runs on the target afterwards, read from duho's `args._passthrough_` (the
  parsed instance carries everything after the first bare `--`). Targets must
  come **before** the separator; a stray tail, or a command that reads none,
  is reported rather than dropped.
  An existing `--path` is replaced only if a previous deploy wrote its digest
  marker (`<path>/.digest` for `dir`, `<path>.digest` for `pyz`); anything else
  raises `FileExistsError` and is left alone — `--force` only skips the
  "already current" check. Both layouts are written beside the target and
  renamed into place, and a `dir` deploy interrupted between its renames is
  restored from `<path>.old` on the next run.

  `--source` picks **what** gets bundled and `--mode` the output **layout**
  (zipapp or unpacked tree), with one constraint: `--source repo` requires
  `--mode dir` and is refused with the default `pyz`, because a zipapp needs an
  importable package root and a working tree has none.
  - `installed` (default) — the resolved dependency closure. Probes what the
    host already has via `utils.bundle.PROBE_SOURCE` and bundles only the
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
    and the root itself hold an importable package, in that order). Requires
    the `repo` extra (`pathspec`, plus `tomli` below 3.11).
    Repo mode does **not** vendor the repo's own dependencies — that needs
    them installed here, the thing repo mode exists to avoid. It *logs* what
    the repo declares as a heads-up; `--include`/`--exclude` adjust only that
    logged list (each takes a bare dependency name or a bracketed `[extra]`,
    exclude wins). `--skip` is the `installed`-mode counterpart and has no
    effect here.

### RunPath step directories (`duho.runpath`)

A **RunPath** is a directory of numbered `NN-name.py` *step* files run in
order, with no `__init__.py` — placed among the command sources
(`PYTRUENAS_PATH` / `--cmdspath` / config `commandspath`, or nested one level
inside a source directory) it becomes a subcommand named after the directory.
`pytruenas` adopts `duho.runpath` (declared floor `duho>=0.5.2,<0.6`; `runpath`
itself arrived in 0.4.0, `register(step_adapter=...)` in 0.5.2) and fans the whole
step directory out **once per target**, each target getting its own connected
`TrueNASClient` — the same per-target fan-out the built-in commands get. Author
one with:

- **`__main__.py`** (optional lifecycle) — `init(cmd, logger) -> ctx` builds
  the per-target client (its return is the `ctx` every 2-arg step receives);
  `success(ctx, cmd, logger)` / `finally_(ctx, cmd, logger)` run once after the
  steps. `cmd` is the parsed command instance for THIS target (carrying
  `cmd.target`, and any per-target state a step needs — e.g. `cmd.context = …`
  stashed in `init` and read by later steps, isolated per target). Re-export
  `pytruenas.utils.runpath.default_init` as `init` to build
  `cmd._client_(cmd.target)` with no boilerplate.
- **`NN-name.py`** step files — each exposes a `main`/`run`/`call` entrypoint;
  written `main(cmd, ctx)` it receives the `__main__.py` context, written
  `main(cmd)` it does not (arity-detected). A step may set module-level
  `PRIORITY`, `REQUIRED`, `BEFORE`, `AFTER` (ordering) — see `duho.runpath`.
- **`-O`/`--rcopts PATTERN[,PATTERN…]`** selects steps (fnmatch on step name):
  `!name` disables, `!*,build` = disable-all-then-enable-`build`, filename
  `!`/`!strict`/`!enable` tokens set per-step defaults. The grammar and its
  precedence are `duho.runpath`'s (see the `duho` docs / CHANGELOG for the
  authoritative description — not restated here to avoid drift).

**Fidelity to the private predecessor (grammar is `duho`'s, two original bugs
FIXED not reproduced).** This RunPath support restores the predecessor's
per-target `RunPathCmd` *capability*; the step signature is `duho`'s native
`main(cmd, ctx)` rather than the predecessor's literal
`run(client, args, logger)` (the logger travels on `cmd`, the client is `ctx`)
— capability-parity, not signature-parity. The filename-modifier / `--rcopts`
grammar follows the predecessor's `RcOptions.from_matchstring` *intent*, with
two confirmed original bugs deliberately **fixed, not reproduced**: (1) the
predecessor's disable token was misspelled `:!enable` and set a nonexistent
`.enable` attribute instead of the real `.enabled` field, so filename-driven
leading-`!` disable was silently broken — `duho` uses the consistent
`enable`/`!enable` spelling throughout; (2) the predecessor's `Extend(",")`
had a latent nested-list double-collection bug (dormant only because its own
arg layer never built a `list[T]` splitter) — `duho`'s richer list-type
dispatch would have made it live, and it is already fixed there (the same fix
that flattens `--cmdspath a:b` to `['a', 'b']`). Do not read this support as
exact behavioral parity where `duho` intentionally improved on the original.

## Transport providers (`pytruenas.providers`, `pytruenas.webshell`)

The objects behind the table above. A caller never needs them to use a host --
`executor=`/`path=` name them by string -- but they are public, so a consumer
can compose a host of its own.

- **`providers.local_providers()`** — hostctl's stock local executor/path pair,
  as this package configures them.
- **`providers.TnasWsPathProvider(client)`** — the `filesystem.*` path provider
  (`"tnasws"`), which works over the API websocket with no SSH.
- **`webshell.WebShellExecutorProvider(client)`** — the `"webshell"` executor.
- **`webshell.WebShellSession(client, **options)`** — one `/websocket/shell`
  session. `.execute(command, input=None, merge_stderr=False, timeout=None,
  sink=None, errsink=None) -> (stdout, stderr, returncode)` runs one command
  and can stream: `sink`/`errsink` are called with decoded chunks as they
  arrive. `.command_lines(...)` yields output lines. A `timeout` raises
  `subprocess.TimeoutExpired` carrying whatever arrived; a connection lost
  before the command starts raises `OperationNotStarted`.
- **`webshell.clean_output(text)`** — strips the terminal's own control
  sequences from captured output.

## `patch` (`pytruenas.patch`)

Modifying a host **beyond what the middleware API exposes** — unsupported by
definition, since TrueNAS owns its own configuration and a boot-environment
swap on update discards anything outside the persistent datasets. Was
`pytruenas.ops`, a name that said neither what it does nor what it costs.

Everything is built to be repeatable and undoable:

- **`templates`** — `base` renders (`BaseTemplate`/`TextTemplate`/
  `BasicTemplate`, `%{NAME}` substitution); `targets` writes (`TemplateTarget`,
  `FileTarget`). `write()` compares content first and returns whether anything
  changed; every caller keys expensive follow-up work off that boolean.
  `FileTarget(path, baseline=True)` snapshots the original on first write and
  `read()`s *that* thereafter, so a patch layers onto the stock file rather
  than onto its own previous output. The snapshot keeps the original's mode
  (it is created empty, chmod'ed, then filled, so a copy of `/etc/shadow` is
  never readable at a wider mode). When the file did not exist at the first
  write, a `<name><suffix>.absent` marker records that instead, and `read()`
  raises `FileNotFoundError` from then on (the original was "no file"), so
  re-applying a layering template to a file it created is idempotent. Also
  `revert(remove_baseline=True)` (restore content and mode + clear the
  snapshot; for a file the target created it removes only the marker and
  leaves the file, which returns `False`), `is_patched()` (also `True` for a
  snapshotted file that was deleted), `would_change(content)` (dry run), and
  `mode=` for a created file — applied before the content is written — while
  an *existing* file keeps its own mode across a rewrite, so patching
  `/etc/shadow` cannot silently widen it from `0640`.
- **`systemd`** — `unitfile` (pure text: unit syntax is case-sensitive,
  `=`-only, and `%` belongs to systemd, so all three `ConfigParser` defaults
  are wrong); `files.SystemFile` (a file plus the `etc` groups and services to
  notify); `units.Unit`/`ServiceUnit`/`MountUnit`/`AutomountUnit`. Unit
  `enable`/`start` are three-valued — `None` means "not mine to manage", which
  a bool could not express.
- **`middleware.MiddlewareFiles`** — locate files in the host's `middlewared`
  package, chiefly to take a stock `etc_files` template as a baseline.
  `module_path` is resolved lazily by running `import middlewared` on the host
  (no API method reports it, checked against 26.0). `find_template` defaults to
  `baseline=False`: that package is on a **read-only mount**, so snapshotting
  beside it cannot work.
- **`zfs.writable(client, path)`** — a context manager that clears `readonly`
  on the backing dataset and **restores it however the block exits**. Required
  for anything under `/usr`. `dataset_for` walks up to an existing ancestor,
  because `findmnt --target` fails on a path that does not exist yet — the
  ordinary "create this file" case. `host_path` unwraps a path for argv: a
  `UriPath` renders as a URI via `str()`, scp syntax via `as_posix()`, and
  raises from `os.fspath()`, so only `.path` is usable (filed upstream as
  `2026-07-29_uripath_fspath_refuses_remote_schemes`).

## `codegen` (`pytruenas.codegen`)

Backs the `generate-typings` command; not typically used directly.

- **`Codegen().generate(api: Version, root: Path | str)`** — write one
  `__init__.pyi` per API namespace under `root`, rendered from the
  `namespace.pyi.j2` Jinja template. `api` is one entry from
  `client.dump_api()["versions"]` (see `pytruenas.models.apidump`). Renders
  into a temporary sibling and swaps it in only when complete, so a failure
  leaves the previous output intact. `root` is replaced only if it is absent,
  empty, a previous output (marked `.pytruenas-typings`), or holds nothing but
  `.pyi` files; otherwise `FileExistsError`. Missing `jinja2` raises
  `ImportError` naming the `codegen` extra before anything is touched.

## `models` (`pytruenas.models`)

TypedDict schemas only (no runtime behavior); import the submodules directly.

- **`pytruenas.models.apidump`** — `Api` (`{"versions": [Version, ...]}`),
  `Version` (`{"version", "methods", "events"}`), `Method`
  (`{"name", "roles", "doc", "schemas"}`), `Event`.
- **`pytruenas.models.jsonschema`** — the JSON-Schema-shaped `Schema`/`Object`/
  `Array` TypedDicts used by `Method.schemas`.

## `utils` (`pytruenas.utils`)

- **`target.Target`** (`NamedTuple`: `scheme, username, password, host, port,
  path, query, fragment`) — a parsed connection string.
  `Target.parse(connectionstring, resolve_port=True, **defaults) -> Target`;
  `.uri` reassembles it; `.is_local` checks for
  `""`/`"localhost"`/`"127.0.0.1"`; `.qsl` / `.query_val(key, default=None,
  *, islist=False)` read the query string.
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
- **`cmd`** — see "Writing a command module" above. Also holds
  **`json_value(raw)`**, the decoding `call -p` and `query -f` share (a JSON
  value, falling back to the raw string), and **`ENV`**, the
  single `duho.env.Env("pytruenas")` accessor every `PYTRUENAS_*` setting is
  read through (`autoload=False`; see "Environment variables").
- **`bundle`** — see also `parse_probe(output) -> (names, marker_environment)`,
  which reads what `PROBE_SOURCE` printed on the target: the first line is that
  machine's PEP 508 marker environment (pass it as `requirements(...,
  environment=...)` so a gated dependency is resolved for the target), the rest
  are distribution names. `requirements()` follows each requirement's OWN
  extras; `collect_repo()` never follows a symlink out of the tree, honours a
  nested ignore file below its own directory, excludes `.git` at any depth, and
  raises `BundleError` for an `ignore_files` entry that does not exist.
  Deliberately generic, and knows nothing about pytruenas or
  TrueNAS so it can be lifted out later. `requirements(root, extras)` resolves
  a transitive closure from installed *distribution metadata* (not an import
  scan — `import yaml` does not name `pyyaml`); `PROBE_SOURCE` is stdlib-only
  source to run on the target to list what it has; `missing_on(installed,
  root, ...)` subtracts; `build(dest, dists, package=...)` writes a zipapp and
  `export(dest, dists)` an unpacked tree; `tar_tree`/`tar_digest` archive one
  with normalized ownership and `bin/*` made executable. Refuses a
  distribution carrying a compiled extension, and one that resolves to data
  files only — both would build cleanly and fail to import on the target.

  The repo-mode half (`deploy --source repo`; needs the `repo` extra):
  - `collect_repo(root, *, ignore_files=None, extra_ignores=(), prefix=None)
    -> [(arcname, source_path)]` — a working tree filtered the way a clone
    would be. `ignore_files` defaults to `DEFAULT_IGNORE_FILES`
    (`.gitignore`, `.ignore`, `.bundleignore`, layered in that order so the
    most bundle-specific negations win); `extra_ignores` are additional
    gitignore-style patterns applied after them.
  - `build(...)` and `export(...)` take that list directly as
    **`contents=`**, instead of resolving one from installed metadata —
    `distributions` becomes optional, and the two are mutually exclusive.
    `tar_tree` archives the result unchanged.
  - `repo_requirements(root, extras=(), *, include=(), exclude=())
    -> list[str]` — the dependency NAMES a repo *declares*
    (`pyproject.toml`, else `requirements.txt`). Static: nothing is imported
    and nothing need be installed, which is the point. It does not resolve a
    transitive closure or return `Distribution` objects the way
    `requirements()` does. `include`/`exclude` accept a bare name or a
    bracketed `[extra]`; exclude wins.
- **`runpath`** — helpers for authoring a RunPath step directory (see "RunPath
  step directories" above): `default_init(cmd, logger) -> TrueNASClient` (the
  per-target `__main__.py` client builder) and `PyTrueNASRunPathArgs` (the
  shared root every RunPath command inherits — supplies the target fields /
  fan-out methods and the trailing `TARGET` positional).
- **`tls`** — the one TLS trust decision every leg uses.
  **`context(sslverify) -> ssl.SSLContext | None`** (`None` when verification
  is off) and **`ca_bundle(sslverify) -> (path, source) | None`**, which says
  which bundle is trusted and where it came from (`"sslverify"` or the
  environment variable's name). `CA_BUNDLE_ENV` is that variable list, in
  precedence order.
- **`io`** — internal helpers (byte-like checks); no stable external contract.

## Environment variables

Every `PYTRUENAS_*` setting is read through one accessor,
`utils.cmd.ENV` (a `duho.env.Env("pytruenas")`), so the set is enumerable with
`sorted(ENV)` rather than by grepping. Reading `os.environ` directly at each
site is how this app once had three names for two settings. `autoload=False`
on purpose: the companion-module feature would import a `pytruenas_env` module
from anywhere on `sys.path` including the CWD, and a CLI is routinely run from
a directory the user does not control.

- **`PYTRUENAS_CONFIG`** — default path for the CLI's `--config` (YAML).
  `PYTRUENAS_CFG` is still accepted as the older spelling.
- **`PYTRUENAS_PATH`** — `os.pathsep`-separated extra command source(s) for CLI
  discovery (read with `ENV.paths`, which splits on the platform separator, so
  a Windows `C:\...` entry is not mis-split on its drive colon).
- **`PYTRUENAS_PKG_ROOT` / `PYTRUENAS_PKG_NAME`** — the distribution `deploy`
  bundles, and the package the deployed copy runs. For when pytruenas is a
  *dependency* of the thing being deployed rather than the deliverable.
- **`TN_CREDS`** — read by `Credentials.from_env()`, and by the CLI
  (`PyTrueNASArgs._credentials_`) for a target that carries no credentials of
  its own. Not prefixed, and not routed through `ENV`.
- **`PYTRUENAS_SSLVERIFY`** — the CLI's TLS default when no flag is given:
  `true`/`false`/`1`/`0`/`yes`/`no`/`on`/`off`, or a CA bundle path.
- **`CALL_TIMEOUT`** — default per-call JSON-RPC timeout in seconds, read at
  import time by `pytruenas.connection`. Also unprefixed.

### Generated typings (`generate-typings` output)

- The package root exports **`Current`**, an alias for the generated version
  class (`V26000`), so the documented `TrueNASClient[Current]` resolves.
- Optional TypedDict keys are `NotRequired`, imported from `typing_extensions`
  below Python 3.11 (a `sys.version_info` guard in every stub). A checking
  target older than 3.11 needs `typing_extensions` installed.
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
  output directory (`codegen.BadApiName` if a dump name would escape it).
- Every method's call options (`_method`, `_ioerror`, `_filetransfer`,
  `_timeout`, `_tries`) are **keyword-only** in the stub, matching the runtime:
  middleware parameters are positional and any other keyword raises.

## Optional extras and their gating imports

- **`ssh`** (`hostctl[ssh]>=0.3.1,<0.4`, i.e. asyncssh + pathlib_next's
  sftp-async) — required for
  `.ssh`, `.run()` over SSH, and the SFTP leg of `TruenasPath`. Missing it
  raises a clear `ImportError` naming the extra at first use, not at import
  time. **Not** required by `.install_sshcreds`, which provisions over the
  middleware API; only deriving a public key from a caller-supplied
  `private_key=` needs a key library, and `cryptography` (which `asyncssh`
  itself depends on) is preferred over `asyncssh` for that.
- **`config`** (`pyyaml`) — required to read a CLI `--config` YAML file;
  missing it with a config file present raises `ImportError`.
- **`codegen`** (`jinja2`) — required by `pytruenas.codegen`/`generate-typings`.
- **`repo`** (`pathspec`, plus `tomli` below 3.11) — required by
  `deploy --source repo` and `utils.bundle.collect_repo`/`repo_requirements`.
  `pathspec` does the gitignore-style matching (`**` and negation are what a
  hand-rolled matcher gets wrong); `tomli` reads `pyproject.toml` where stdlib
  `tomllib` does not exist yet. Missing it raises `ImportError` naming the
  extra at first use.

(There is no `host` extra. It existed for `pytruenas.ops.host`'s adapter
discovery, which moved from `ifaddr` to `netimps` — a core dependency — and the
module has since been removed outright.)
