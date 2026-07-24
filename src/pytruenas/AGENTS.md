# `pytruenas` — public API header

Header-file-style reference for the `pytruenas` package: every public export
with its signature, arguments, contract, and gotchas, so this module can be
consumed without reading its source. Kept current with the public API. For the
project overview and CLI usage, see the project overview doc at the repo root.

## Package root (`pytruenas`)

`__all__ = ["Namespace", "TrueNASClient", "Credentials", "Event", "Subscription", "__version__"]`

- **`__version__: str`** — resolved from installed package metadata
  (`importlib.metadata`); `"0.0.0.dev0"` when run from a bare checkout with the
  package not installed.

## `TrueNASClient` (`pytruenas.client`)

`TrueNASClient(target=None, creds=None, autologin=True, sslverify=True, *,
shell=None, logger=None, fsbackend="auto", version="current")`

- **`target`** — a host, `"host:port"`, or full `scheme://...` URI. `None` /
  omitted / local-only resolves to the local middleware unix socket
  (`ws+unix:///var/run/middleware/middlewared.sock`); for a remote target the
  scheme (`ws`/`wss`) and API path are auto-probed via an HTTP(S) request when
  not given explicitly.
- **`creds`** — passed to `Credentials(...)` (below); `None` means local-socket
  auth (no login call).
- **`autologin`** (default `True`) — the first `.websocket` access calls
  `.login()` automatically when there's no live connection.
- **`sslverify`** (default `True`) — TLS certificate verification for `wss://`
  and the HTTP(S) side channels (upload/download probing).
- **`shell`** — connection string for the SSH/local shell used by `.run()`;
  defaults to the API target's host over SSH (remote) or local exec (local).
- **`fsbackend`** — default backend for `.path()`: `"auto"` (local when the
  client is local, else `TruenasPath`), `"local"`, `"ws"`/`"api"`, or
  `"truenas"`.
- **`version`** — API path version probed when auto-resolving the websocket
  path (default `"current"`, i.e. `/api/current`).

### Attributes / properties

- **`.api`** (`cached_property`) — the root `Namespace` for this client
  (`client.api.<namespace>.<method>(...)`).
- **`.websocket`** — the live `jsonrpc.Client`; connects (and logs in, if
  `autologin`) on first access, reconnects if the prior connection closed.
- **`.ssh`** — a lazily-opened `asyncssh` connection (requires the `ssh`
  extra) built from `.shell`.
- **`.logger`** — a `logging.Logger` (default: `logging.getLogger("pytruenas")`).

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
  `path` for this client; `backend` overrides `.fsbackend` for this call. See
  `pytruenas.fs`.
- **`.run(*cmds, bufsize=-1, executable=None, stdin=None, stdout=None,
  stderr=None, cwd=None, env=None, capture_output=True, check=True,
  encoding=None, errors=None, input=None, timeout=None, loglevel=TRACE) ->
  subprocess.CompletedProcess`** — run a shell command locally or over SSH
  (per `.shell.scheme`). Each positional `cmd` is either a string (used
  as-is) or a sequence (shell-quoted and joined); commands are `;`-joined into
  one script run via `<executable> -c <script>`. `executable` defaults to
  root's login shell (looked up locally via `pwd`, or remotely via
  `user._get(username="root")["shell"]`), falling back to `/bin/bash`.
  **Gotcha**: when `encoding`/`errors` is set, a `str` `input` is passed
  through as `str` (subprocess encodes it itself) rather than pre-encoded to
  bytes — pre-encoding there crashes because `subprocess.run` calls
  `.encode()` on what it thinks is still text.
- **`.upload(file, method, *params, token=None, wait=True, **kwargs)`** —
  upload `file` (`str`/`bytes`) via the middleware's `/_upload` HTTP side
  channel, then call `method(*params, **kwargs)` server-side with it; waits on
  the resulting job by default. Auto-generates a short-lived auth token when
  none is given.
- **`.download(method, *args, filename=None, buffered=False, wait=True,
  **kwargs)`** — call `method` to get a download link/job, fetch it over
  HTTP(S), and return the bytes (when `wait=True`) or the job id.
- **`.subscribe(event, callback=None, *, maxsize=1000) -> jsonrpc.Subscription`**
  — subscribe to a middleware collection event over the live websocket.
  `client.subscribe("alert.list")` is shorthand for
  `client.api.alert.list.subscribe()`. Consume via the returned subscription's
  `.events(timeout=None)` iterator and/or the inline `callback`. Bound to the
  current connection; does **not** survive a reconnect (the `events()` iterator
  ends on disconnect — that's the re-subscribe signal). See `jsonrpc` below.
- **`.dump_api() -> dict`** — run `middlewared --dump-api` on the target and
  return the parsed JSON (see `pytruenas.models.apidump.Api`).
- **`.install_sshcreds(name=None, private_key=None)`** — generate/reuse an SSH
  keypair via `keychaincredential`, install the public half on `root`'s
  `authorized_keys`, and configure `.shell` to use it. Requires the `ssh`
  extra.

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
  jsonrpc.Subscription`** — subscribe to this namespace's collection event; the
  event name defaults to the namespace's dotted path
  (`client.api.alert.list.subscribe()` -> `alert.list`), or pass `event=` to
  override (e.g. from `client.api`). A **real method**, so it shadows any
  middleware method literally named `subscribe`; reach such a method via
  `ns(_method="subscribe", ...)`. See `jsonrpc.Subscription`/`Event` above.
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

## `jsonrpc` (`pytruenas.jsonrpc`)

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
- **`TruenasPath`** (`pytruenas.fs.truenas`) — subclasses `TnasWsPath`;
  `unlink`/`rmdir`/`rename`/`symlink_to`/`readlink`/`resolve` try an SFTP leg
  first (via `pathlib_next`'s `SftpPath`, requires the `ssh` extra +
  `client.shell` host) and fall back to `TnasWsPath`'s websocket behavior (or
  raise `NotImplementedError` for ops SFTP alone can do — rename, symlink_to,
  readlink). `symlink_to(..., force=False, onremove=None)` adds a
  pytruenas-specific convenience: `force` (bool, a file-type string, or a set
  of `"file"/"link"/"directory"`) removes a conflicting existing target first;
  `onremove(path, kind)` gates each removal.
- **`TnasWsBackend(client)`** — the backend object `TnasWsPath`/`TruenasPath`
  carry; just holds `.client`.

`backend=` values: `"local"` -> `LocalPath`, `"ws"`/`"api"` -> `TnasWsPath`,
`"truenas"`/`"auto"` -> `TruenasPath`/`LocalPath` (`"auto"` picks `LocalPath`
for a local client).

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

### RunPath step directories (`duho.runpath`)

A **RunPath** is a directory of numbered `NN-name.py` *step* files run in
order, with no `__init__.py` — placed among the command sources
(`PYTRUENAS_PATH` / `--cmdspath` / config `commandspath`, or nested one level
inside a source directory) it becomes a subcommand named after the directory.
`pytruenas` adopts `duho.runpath` (requires `duho>=0.4.0`) and fans the whole
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
- **`cmd`** — see "Writing a command module" above.
- **`runpath`** — helpers for authoring a RunPath step directory (see "RunPath
  step directories" above): `default_init(cmd, logger) -> TrueNASClient` (the
  per-target `__main__.py` client builder) and `PyTrueNASRunPathArgs` (the
  shared root every RunPath command inherits — supplies the target fields /
  fan-out methods and the trailing `TARGET` positional).
- **`async_`, `io`** — internal helpers (`async_to_sync`, byte-like checks);
  no stable external contract.

## Environment variables

- **`TN_CREDS`** — read by `Credentials.from_env()`.
- **`CALL_TIMEOUT`** — default per-call JSON-RPC timeout in seconds (read at
  import time by `pytruenas.jsonrpc`).
- **`PYTRUENAS_CFG`** — default path for the CLI's `--config` (YAML).
- **`PYTRUENAS_PATH`** — `os.pathsep`-separated extra command source(s) for
  CLI discovery.

## Optional extras and their gating imports

- **`ssh`** (`asyncssh`, `pathlib_next[sftp-async]>=0.8.3`) — required for
  `.ssh`, `.run()` over SSH, `.install_sshcreds`, and the SFTP leg of
  `TruenasPath`. Missing it raises a clear `ImportError` naming the extra at
  first use, not at import time.
- **`config`** (`pyyaml`) — required to read a CLI `--config` YAML file;
  missing it with a config file present raises `ImportError`.
- **`codegen`** (`jinja2`) — required by `pytruenas.codegen`/`generate-typings`.

(There is no `host` extra: `pytruenas.ops.host`'s local-adapter discovery uses
`netimps` — a core dependency — so it works out of the box.)
