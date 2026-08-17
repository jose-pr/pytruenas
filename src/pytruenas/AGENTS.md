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

`TrueNASClient(target=None, credentials=None, *, sslverify=True, shell=None,
logger=None, autologin=True, version="current", executor=None, path=None,
ssh=None, ...)`

- **`target`** — a host, `"host:port"`, or full `scheme://...` URI. `None` /
  omitted / local-only resolves to the local middleware unix socket
  (`ws+unix:///var/run/middleware/middlewared.sock`); for a remote target the
  scheme (`ws`/`wss`) and API path are probed on first connect, **not** in the
  constructor — building a client performs no network I/O.
- **`credentials`** (positional as `creds` historically) — passed to
  `Credentials(...)` (below); `None` means local-socket auth (no login call).
- **`autologin`** (default `True`) — the first `.conn` access calls
  `.login()` automatically when there's no live connection.
- **`sslverify`** (default `True`) — TLS certificate verification for `wss://`
  and the HTTP(S) side channels (upload/download probing).
- **`shell`** — connection string for the SSH leg (`"ssh://root@nas"`,
  `"root:pw@nas:22"`). Stored as an `SshConfig` on `.config.ssh`; pass
  `ssh=SshConfig(...)` to supply one directly.
- **`executor`/`path`** — name the providers to use, in preference order.
  Replaces `fsbackend`, which could only pick a filesystem backend; see the
  provider table below.
- **`version`** — API path version probed when auto-resolving the websocket
  path (default `"current"`, i.e. `/api/current`).

### Attributes / properties

- **`.api`** (`cached_property`) — the root `Namespace` for this client
  (`client.api.<namespace>.<method>(...)`).
- **`.conn`** (alias `.websocket`) — the live
  `connection.TrueNASWSConnection`; connects (and logs in, if
  `autologin`) on first access, reconnects if the prior connection closed.
- **`.ssh`** — a lazily-opened `asyncssh` connection (requires the `ssh`
  extra), reached through the composed SSH transport. Raises if none is
  configured. For the raw connection only; `.run()`/`.path()` select a
  transport instead of assuming this one.
- **`.config`** — the `TrueNASConfig` this was built from. `.config.ssh` is the
  SSH leg; `.shell` means the *bound shell object* (`client.shell.run(...)`),
  as it does throughout hostctl.
- **`.client`** / **`.host`** — both return the object itself, kept so code
  written against the two-object model keeps working.
- **`.capabilities`** — `{"run", "path"}` as available; a remote target with no
  SSH and no web shell honestly reports no `run`.
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
  (`{"user_info": True, "reconnect_token": False}`).
- **`.me() -> dict`** (`auth.me`) / **`.logout() -> None`** (`auth.logout`) /
  **`.ping() -> str`** (`core.ping` -> `"pong"`) — convenience wrappers.
- **`.path(*path, backend=None)`** — build a `pathlib_next` path rooted at
  `path`; `backend` names one provider for this call. Inherited from
  `hostctl.host.Host`. See `pytruenas.fs`.
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
- **`.upload(file, method, *params, token=None, wait=True, **kwargs)`** —
  upload `file` (`str`/`bytes`) via the middleware's `/_upload` HTTP side
  channel, then call `method(*params, **kwargs)` server-side with it; waits on
  the resulting job by default. Auto-generates a short-lived auth token when
  none is given.
- **`.download(method, *args, filename=None, buffered=False, wait=True,
  **kwargs)`** — call `method` to get a download link/job, fetch it over
  HTTP(S), and return the bytes (when `wait=True`) or the job id.
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
otherwise have no `run()` at all. It ranks below SSH because a PTY merges
stdout and stderr and cannot take piped input.

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
I/O** — the ws-vs-wss and API-path probes happen on first connect, not in the
constructor.

An OTP travels in the URI password field after a newline
(`wss://root:pw%0Aotp:123456@nas`); a raw newline works too on recent hostctl.
Unknown credential names are rejected rather than silently dropped.

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
  - **`_tries`** — reconnect retries after a dropped connection
    (`ECONNABORTED`); default `1` means up to 2 attempts total. The call
    **always** returns or raises — never silently returns `None` on a
    connection error.
  - **`_timeout`** — per-call seconds; the default sentinel uses the client's
    configured timeout, `None` waits indefinitely (used by `core.job_wait`).
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
- **`._update(selector=None, *opts, **fields)`** — update by id (int/str) or
  by a filter (mapping, or a sequence of field names to match on, each
  optionally `!`-prefixed to require *absence*). Diffs against the current
  record first unless `force=True` (an `Option`/tuple opt) is given, so a
  no-op update sends nothing.
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
  py_exceptions=False)`** — opens the websocket immediately (blocking) and
  starts a background reader thread. `uri` is `wss://`/`ws://` or
  `ws+unix://...`; `None`/bare `ws+unix://` connects to
  `DEFAULT_UNIX_SOCKET` (`/var/run/middleware/middlewared.sock`).
  - **`.call(method, *params, timeout=UNSET, **_ignored) -> Any`** — send a
    request and block for the matching response. `timeout=None` waits
    **indefinitely**; the default sentinel uses `call_timeout`. Unknown
    kwargs in `{"job", "background", "callback", "register_call", "raise_"}`
    are silently accepted (upstream-client compatibility); any other unknown
    kwarg is logged at debug level. Raises `ValidationErrors`/
    `ClientException` on a server error, `CallTimeout` on timeout,
    `ClientException(errno=ECONNABORTED)` if the connection dropped.
  - **`.subscribe(event, callback=None, *, maxsize=1000) -> Subscription`** —
    issue `core.subscribe(event)` and route its `collection_update`
    notifications to a `Subscription`. The registry is keyed by event name
    (the notification's `params.collection`, the routing key — NOT the returned
    sub id); two subscribers to the same event both receive it.
  - **`.close()`** — idempotent; also usable as a context manager. Wakes every
    subscription's `events()` iterator (as does a dropped connection).
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
- **`ClientException(error, errno=None, trace=None, extra=None)`** — base
  error for any call/connection failure; `errno` carries a POSIX errno when
  the middleware's `[ERRNO] message` prefix maps to one.
- **`ValidationErrors(errors)`** (`ClientException` subclass) — per-field
  validation errors; `.errors` is `list[(attribute, errmsg, errcode)]`.
- **`CallTimeout()`** (`ClientException` subclass) — raised when a call
  exceeds its timeout.
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
  (*self._args())`; a no-op when `METHOD` is `None` (`LocalAuth`).
- **`.login_ex(client, *, login_options=None, otp_provider=None) -> dict|None`**
  — modern path via `auth.login_ex` using this credential's `MECHANISM`
  (`PASSWORD_PLAIN`/`API_KEY_PLAIN`/`TOKEN_PLAIN`). Handles `OTP_REQUIRED`
  (continues with `auth.login_ex_continue`, OTP from `self.otp_token` or
  `otp_provider()`), returns the `SUCCESS` response dict, raises
  `AuthenticationError` otherwise. Falls back to legacy `.login()` for a
  credential with no login_ex form.
- **`AuthenticationError(response_type, response)`** — raised by `login_ex` on a
  non-`SUCCESS` response; `.response_type` is the server discriminator,
  `.response` the full dict.
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
- **`TruenasPath`** (`pytruenas.fs.truenas`) — subclasses `TnasWsPath`; five
  operations — `unlink`/`rmdir`/`rename`/`symlink_to`/`readlink` — try an SFTP
  leg first (via `pathlib_next`'s `SftpPath`, requires the `ssh` extra +
  `client.config.ssh` host) and fall back to `TnasWsPath`'s websocket behavior (or
  raise `NotImplementedError` for ops SFTP alone can do — rename, symlink_to,
  readlink). **`resolve` is not one of them**: `SftpPath` has no `resolve`, so
  the attempt always raises `NotImplementedError` and `resolve()` returns
  `self` on every host, SFTP configured or not.
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
  per target with a connected `TrueNASClient`.
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
`$PYTRUENAS_CFG` or `./pytruenas.yaml`), `cmdspath`, `sslverify` (default
`False`), `parallel` (default `1`), `logto` (default `-` for stderr, or a
`{target}`/`{isodate}` path template), plus `targets` (the trailing
positionals, not a flag) and helper methods
`._config_dict_()`/`._expanded_targets_()`.

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
  runs on the target afterwards (read from `main.PASSTHROUGH`, split before
  argparse; see there for why it cannot be an argparse field).

  `--source` picks **what** gets bundled; `--mode` is orthogonal and picks the
  output **layout** (zipapp or unpacked tree) either way.
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
  `TrueNASClient(cmd.target, sslverify=cmd.sslverify)` with no boilerplate.
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
  than onto its own previous output. Also `revert(remove_baseline=True)`
  (restore + clear the snapshot; a no-op without a baseline, since a file the
  patch created is not provably ours to delete), `is_patched()`,
  `would_change(content)` (dry run), and `mode=` for a created file — an
  *existing* file keeps its own mode across a rewrite, so patching
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
  `client.dump_api()["versions"]` (see `pytruenas.models.apidump`).

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
  in `against` whose value differs from `base`).
- **`cmd`** — see "Writing a command module" above. Also holds **`ENV`**, the
  single `duho.env.Env("pytruenas")` accessor every `PYTRUENAS_*` setting is
  read through (`autoload=False`; see "Environment variables").
- **`bundle`** — deliberately generic, and knows nothing about pytruenas or
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
- **`async_`, `io`** — internal helpers (`async_to_sync`, byte-like checks);
  no stable external contract.

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
- **`TN_CREDS`** — read by `Credentials.from_env()`. Not prefixed, and not
  routed through `ENV`.
- **`CALL_TIMEOUT`** — default per-call JSON-RPC timeout in seconds, read at
  import time by `pytruenas.connection`. Also unprefixed.

## Optional extras and their gating imports

- **`ssh`** (`asyncssh`, `pathlib_next[sftp-async]>=0.9.0,<0.10`) — required for
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
