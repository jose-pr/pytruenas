# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.7.1] - 2026-10-21

### Changed

- Requires `duho>=0.7.8,<0.8`. A library caller who runs `duho.fanout.run_targets` over
  connection strings without a `label=` now sees the host's own `[name]` prefix as well as
  duho's tag of the target; the CLI, which labels each target with the host's name, is
  unchanged.

## [0.7.0] - 2026-10-20

### Upgrade notes

- **`sslverify=` is `verify=`**, one switch for TLS and SSH host keys alike:
  `TrueNASClient(..., verify=True | False | "<CA bundle>" | ssl.SSLContext)`.
  `sslverify=` is an unknown keyword (`ValueError`); `client.sslverify` and
  `config.sslverify` are gone (read `client.config.verify`), and
  `TrueNASWSConnection(verify_ssl=)` is `verify=`. A path or a context means
  "verify" for SSH. "TLS off, SSH strict" is `verify=False, known_hosts=<file>`;
  "TLS on, SSH off" is `ssh=SSHConfig(host, username="root", verify=False)`.
- **`verify=True` trusts what the operating system trusts, through its own
  verifier**: `truststore` on Python 3.10+ (Windows CryptoAPI, the macOS
  keychain, the system CA paths elsewhere) — what hostctl's `verify=True`
  means — and OpenSSL's default store on 3.9 as before. On Windows a public
  root the system fetches on demand, and on macOS a CA only in the keychain,
  are now trusted. The CA-bundle variables (`SSL_CERT_FILE`,
  `REQUESTS_CA_BUNDLE`, `CURL_CA_BUNDLE`, `WEBSOCKET_CLIENT_CA_BUNDLE`) still
  replace that trust.
- **The CLI's TLS options are `-k/--insecure` and `--ca-bundle FILE`.**
  `--sslverify`/`--no-sslverify` are gone; `$PYTRUENAS_SSLVERIFY` and the config
  file's `sslverify` are replaced by `$PYTRUENAS_INSECURE`/`$PYTRUENAS_CA_BUNDLE`
  and `insecure`/`ca_bundle`; the old names are no longer read.
  `-k` also skips the SSH host-key check, as `verify=False` does.
  `PyTrueNASArgs._sslverify_()` is `._verify_()`.
- **`TrueNASWSConnection(...)` does no I/O.** It opened the websocket and
  started its reader in the constructor; `.connect()` (returning the
  connection), `with` or the first `.call()` does that now.
- **`download(..., wait=False)` returns a `PendingDownload`** (`.job_id`,
  `.fetch()`), not the job id: the link was discarded, so the bytes could
  never be fetched.
- **The CLI's config file is read by anycfg, and is TOML by default.** It is
  `--config`, else `$PYTRUENAS_CONFIG`, else `pytruenas.cfg` in the
  user's configuration directory (`%APPDATA%`, `$XDG_CONFIG_HOME` or
  `~/.config`); `./pytruenas.yaml` in the working directory is no longer read,
  and `$PYTRUENAS_CFG` is gone. The suffix picks the format, and a `.cfg`
  file is the format its `#!<format>` first line names, else TOML. A YAML
  file keeps working as `pytruenas.yaml`, or
  as a `.cfg` starting with `#!yaml`, with the new `yaml` extra, which replaces
  `config`. A file that does not read is now an error naming it (exit status
  2) instead of being ignored. `cmdspath` (below) is
  read from any config file. `PyTrueNASArgs._config_is_implicit_()` is gone;
  `._config_path_()` and `pytruenas.cli.default_config_path()` are new.
- **`pytruenas.utils.tls` is gone** (`context`, `ca_bundle`, `CA_BUNDLE_ENV`,
  `SslVerify`); the decision is private now. Pass `verify=` instead.
- **`TrueNASHost` is gone: the class is `TrueNASClient`.** It was the same class
  under a second name; `from pytruenas import TrueNASHost` and
  `pytruenas.host.TrueNASHost` raise `ImportError`/`AttributeError`. Replace
  the name with `TrueNASClient` (`TrueNASClient[Current]` for typed `.api`);
  nothing else about the class changed with it.
- **The client's compatibility shims are gone.** Callers change:
  - `TrueNASClient(target, creds)` → `TrueNASClient(target, credentials=creds)`:
    `credentials` is keyword-only, and a second positional argument raises
    `TypeError`.
  - `client.websocket` → `client.conn`; `client.client` → `client`.
  - `client=` (accepted and ignored) and `logger=` raise `ValueError: unknown
    credential argument`. For `logger=`, assign `client.logger = <name or
    Logger>` instead, which binds it to the host's name as `logger=` did;
    `TrueNASConfig(logger=)` and `config.logger` are gone too.
  - `client.subscribe("alert.list")` → `client.api.alert.list.subscribe()`, or
    `client.conn.subscribe("alert.list")` for an event name that is not a
    namespace path.
- **`client.path()` is the one path constructor.** `pytruenas.fs.path`,
  `pytruenas.fs.LocalPath` and `pytruenas.fs.symlink_to` are gone:
  - `fs.path(client, *segments)` → `client.path(*segments)`;
    `fs.path(client, ..., backend="ws")` → `client.path(..., backend="tnasws")`.
  - `fs.LocalPath` → `pathapi.LocalPath`.
  - `fs.symlink_to(p, target, force=True)` → `p.symlink_to(target, force=True)`
    (pathapi's), which replaces a file or a symlink but never removes a
    directory: remove a directory in the way yourself (`p.rm(recursive=True)`)
    where that is what you mean. `onremove=` has no replacement.
- **`upload()` and `download()` take no `**kwargs`.** No keyword could work —
  each reached `auth.generate_token`/`core.download` and was refused — so a
  stray keyword is now Python's own `TypeError` naming it. Pass the method's
  parameters positionally after `method`, as before.
- **Every error is defined in `pytruenas.exceptions` and derives
  `TrueNASError`**, and every one is exported from `pytruenas`:
  - `pytruenas.utils.apicache.ApiDumpError` is **`APIDumpError`** (still a
    `RuntimeError`); `UnknownMethod` (still a `LookupError`) and `FieldError`
    (still a `ValueError`) are `TrueNASError`s now.
  - `ValidationErrors` is also a `ValueError`. A `try` that catches
    `ValueError` around a middleware call now catches a server-side
    validation failure too; catch `ValidationErrors` first if the two need
    different handling.
  - A refused websocket upgrade or a failed handshake (a wrong API path is a
    404) raises **`ConnectError`** (`.status`, websocket-client's exception as
    `__cause__`) instead of `websocket.WebSocketBadStatusException` and the
    other websocket-client exceptions; catch `ConnectError` or
    `TrueNASError`. A refused port, an unresolvable host and a TLS error are
    still the `OSError`s they were.
  - Import them from `pytruenas` or `pytruenas.exceptions`;
    `pytruenas.connection` and `pytruenas.auth` no longer list them in
    `__all__`.
- **CapWords names spell their acronyms in capitals.** Rename:
  `ApiKeyAuth` → `APIKeyAuth`; `pytruenas.fs.TnasWsPath` → `TrueNASWSPath`;
  `pytruenas.fs.TnasWsBackend` → `TrueNASWSBackend`;
  `pytruenas.providers.TnasWsPathProvider` → `TrueNASWSPathProvider`;
  `pytruenas.namespace.DbAction` → `DBAction`. The old names are gone.
- **A call option has one spelling, and no keyword is ignored.**
  - `client.api.<method>(..., _tries=N)` → `_retries=N` (the same count: the
    retries after the first attempt). A bare `timeout=` → `_timeout=`.
  - The upstream client's no-op keywords `background=`, `callback=`,
    `register_call=` and `raise_=` raise `TypeError`, on a namespace call and
    on `client.conn.call(...)`; drop them. `job=True` and `job="RETURN"` keep
    working on a namespace call.
  - `TrueNASWSConnection.call(method, *params, timeout=)` raises `TypeError`
    for any other keyword (`job=` included) instead of logging a misspelt one
    at debug and running the call with the default timeout.
  - `TrueNASWSConnection(py_exceptions=)` and `.py_exceptions` are gone; the
    option did nothing.
- **The one-time code is `otp`, everywhere.** `BasicAuth(user, pw,
  otp_token=)` → `BasicAuth(user, pw, otp=)`, and the attribute
  `credential.otp_token` → `credential.otp`. `Credentials(...,
  otp_token=)` raises `ValueError` (`otp=` is the keyword, as on
  `TrueNASClient`), and any keyword outside `username`/`password`/`otp`/
  `api_key`/`token` does too.
- **`_create`/`_update`/`_upsert` wait only on a job.** Whether the
  `create`/`update` method is a job comes from its schema (`core.get_methods`,
  read once per namespace and cached), not from the answer being an integer:
  a method answering with a record id returns that id instead of waiting on an
  unrelated job of the same number. Pass `{"job": True}` for a method whose
  schema cannot be read (the lookup logs a WARNING and waits on nothing).
  `pytruenas.apicache.service_methods` raises `UnknownMethod` (still a
  `LookupError`) for an unknown service.
- **`with TrueNASClient(...)` opens the API connection, not a shell.**
  Entering (and `client.connect()`) opens and authenticates `client.conn`;
  it no longer opens the first command and path transports, which on a host
  without SSH was a root web-shell session. Those connect when first used, so
  a wrong password now fails on entry, and an SSH or web-shell problem on the
  first `run()`/`path()` operation instead.
- **The environment variables are `PYTRUENAS_CREDENTIALS` and
  `PYTRUENAS_CALL_TIMEOUT`.** `TN_CREDS` and `CALL_TIMEOUT` are no longer read:
  rename them. `PYTRUENAS_CALL_TIMEOUT` takes a fraction and is read when a
  connection is built, so it can change at run time, and a bad value raises
  `ValueError` naming the variable then — not at `import pytruenas`, which
  reads no variable. `connection.CALL_TIMEOUT` is the constant `60.0`;
  `TrueNASWSConnection(call_timeout=)` left out is
  `connection.default_call_timeout()`. `PYTRUENAS_CREDENTIALS` is documented
  as a secret.
- **A connection URI's query is read, strictly, and `connection_uri` renders
  the options.** `?verify=false`, `?version=`, `?executor=`, `?path=`,
  `?autologin=` and `?timeout`/`timeout_connect`/`timeout_read` set the
  options; any other key (a misspelt `?verfiy=0`) raises `ValueError`, where it
  was dropped. `connection_uri`/`str(config)` now carries every non-default
  option (`truenas+wss://nas?verify=false`), so it round-trips; code that
  compared it to a bare `truenas+wss://host` string, or parsed it, sees the
  query. `TrueNASConfig` compares and hashes by `connection_uri` (it compared
  by identity): credentials and `name` are not part of equality.
- **The `codegen` extra is gone**: `pip install pytruenas` runs
  `generate-typings`, which builds the stubs in Python (byte for byte the
  same output) and no longer needs jinja2. Drop `[codegen]` from a
  requirement; pip warns about an extra that does not exist.
  `pytruenas.codegen.jinja`, its template and `codegen.Renderer` are gone.
- **`pytruenas.models` holds TypedDicts and type aliases only.**
  `Schema.get_type`, every `python_declaration`, `TYPES` and `_typeddict_name`
  leave `models.jsonschema`; turning a schema into a type is private to
  `codegen`. Stubs already generated keep working: they import
  `pytruenas.models.jsonschema` for `JsonValue`/`JsonObject`/`JsonArray`/
  `JsonNumber`, which stay.
- **Renamed:** `models.apidump.Api` → `API`, `models.apidump.Method` →
  `APIMethod`, `models.apidump.Event` → `APIEvent`, and `codegen.BadApiName` →
  `codegen.BadAPIName`, which is now a `pytruenas.TrueNASError` as well as a
  `ValueError`.
- **`pytruenas.codegen` exports `Codegen` and `BadAPIName` only.** `Namespace`,
  `Method`, `Parameter`, `PyDeclaration` and `Source`, and `docstring()`, are
  private to it.
- **Removed from `pytruenas.patch`:** `zfs.PathLike`, which was
  `Union[str, Any]` (the `zfs` functions take `str | os.PathLike[str]`), and
  `systemd.parse_unit()`; `render_unit()` and `UnitConfigParser` stay.
- **`pytruenas.utils` is gone, and the command line is `pytruenas.cli`.**
  Change the imports:
  - `pytruenas.utils.query` → `pytruenas.query`; `pytruenas.utils.target` →
    `pytruenas.target`; `pytruenas.utils.apicache` → `pytruenas.apicache`.
  - `pytruenas.utils.cmd` (`PyTrueNASArgs`, `with_targets`, `TargetsField`,
    `emit`, `emit_json`, `json_default`, `ENV`, `default_config_path`) and
    `pytruenas.main` (`main`, `PyTrueNAS`) → `pytruenas.cli`.
    `register_targets` is gone (`with_targets` declares the positional) and
    `json_value` is private.
  - `pytruenas.utils.runpath` → `pytruenas.cli.runpath`.
  - `pytruenas.cmd.*` → `pytruenas.cli.commands.*`.
  - `pytruenas.utils.apihelp`, `pytruenas.utils.fields` and
    `pytruenas.utils.io` are private now; `UnknownMethod` and `FieldError`
    stay in `pytruenas.exceptions`. `utils.cmd.CommandModule` is gone.
  - The console script is `pytruenas.cli:main`; a wrapper that named
    `pytruenas.main:main` must change.
- **`pytruenas.cli.main(argv=None, *, name=None, args=None, root=None)`**:
  `argv` is the one positional. `main("mytool", argv)` becomes
  `main(argv, name="mytool")`.
- **`--cmdspath` is repeated, not split**: `--cmdspath a --cmdspath b`, not
  `--cmdspath a:b`, which cut a Windows drive letter off its path. The
  config file's `commandspath` is `cmdspath`; the old key is no longer
  read. `$PYTRUENAS_PATH` is unchanged (`os.pathsep`-separated).
- **`generate-typings --api-cache FILE` is `--from FILE`**, which only reads:
  a `dump-api` output, or a gzipped file from `$PYTRUENAS_CACHE`. Without it
  the definition comes from `client.dump_api()`, which already caches it per
  host and API version.
- **Uploads and downloads raise no `requests` exception.** A TLS or socket
  failure is the `OSError` beneath it (`ssl.SSLCertVerificationError`,
  `ConnectionRefusedError`, ...), as the API websocket raises for the same
  failure; a read that timed out is `CallTimeout`; an HTTP error status (a
  refused upload) is `ClientException`. Code that caught
  `requests.RequestException` around `upload()`/`download()` catches those
  instead.
- **`deploy` is not an MCP tool** under `PYTRUENAS_MCP=stdio`: installing
  software on an appliance is for a person to choose. The command line is
  unchanged.
- **`client.dump_api()` returns the API version the appliance runs, not every
  version it serves**: the dump is pruned on the target before the transfer,
  so `"versions"` has one entry. Pass `all_versions=True` (CLI: `dump-api
  --all-versions`) for all of them; `generate-typings --api-version` and
  `help --api-version` do so themselves. `apicache.load()`/`fetch()` take the
  same keyword.
- **`redact_call_args` is imported from `pytruenas.auth`**, not from the
  package root, where it was importable outside `__all__`.
- **`known_hosts=None`** is refused by hostctl when the SSH leg is built, not
  by `TrueNASClient` itself: a client with no SSH leg accepts it.
- **`pytruenas.patch.zfs.host_path` is gone**: it was `os.fspath()`, which
  is what to call.
- **The `repo` extra is gone**: `deploy --source repo` needs nothing beyond
  the core install, which already carries `hostctl[deploy]`. Drop `[repo]`
  from a requirement.

### Changed

- **Dependency floor raised to `duho>=0.7.7,<0.8`.** The command line names a
  failed target by its host name through duho's own `run_targets(label=)`, and
  `client.logger.trace()` is duho's `LoggerAdapter.trace`; neither changes
  what is printed.
- **Dependency `anycfg>=0.15.0,<0.16`** (its `cfg` format reads the CLI's
  config file); pytruenas no longer declares `tomli` itself, which anycfg
  brings below Python 3.11.
- **Dependency floor raised to `websocket-client>=1.3.3,<2`.** Below 1.2.2
  the API websocket ignores the TLS context `verify=` builds, so the OS trust,
  a CA bundle and a caller's `ssl.SSLContext` never applied there; below
  1.3.3 a refused connection leaks its socket.

### Added

- `TrueNASClient(..., timeout=)` / `TrueNASConfig(timeout=)` take hostctl's
  `Timeout`: `connect` opens the websocket, `read` bounds one call and a
  side-channel read, `total` is `run()`'s default; `config.timeouts` resolves
  them.
- `verify=` takes an `ssl.SSLContext`, used as it is on the API websocket, the
  side channels and the web shell: a client certificate for a NAS behind an
  mTLS reverse proxy (e.g. from `sslcontext.create_context(certificate=, key=)`
  or `sslcontext.system_context()`), or a pinned CA.
- Dependency `truststore>=0.10.5,<0.11` on Python 3.10+.

### Fixed

- Uploads and downloads time out (the websocket's connect and read
  timeouts); a side channel that accepted the connection and then said nothing
  blocked them for good.
- A failed download's error message no longer carries the link's `auth_token`.
- Opening the web shell closes its websocket on every failure (a token that
  could not be minted leaked it), reads a refusal of any shape (a string
  `error` raised `AttributeError`), and declines when no `connected` message
  arrives instead of returning a session with no shell behind it.
- Turning TLS verification off logs one WARNING per host.
- `TrueNASWSConnection.close()` sends the close frame without waiting for the
  peer's answer: the wait read the socket the reader thread was blocked on, so
  a peer that never answered held `close()` for good.
- A call's timeout bounds its send: a peer that stopped reading held
  `call(..., timeout=)` -- and a `close()` behind it -- forever once the socket
  buffers filled. The send is aborted and the connection closed (part of the
  request may be on the wire), and the call raises `CallTimeout`.
- A host, a `--logto` target or an API name that is a Windows device name
  (`nul`, `con`, `com1`, ...) no longer names a device: the cache directory and
  the log file get a `_` prefix, and `generate-typings` refuses the name.
- `pytruenas.patch.zfs` decodes a non-ASCII mount path from `findmnt` as
  UTF-8 (`é` came back as `Ã©`).
- The plaintext-credentials warning knows every loopback address
  (`127.0.0.0/8`, `::1`, this machine's own), not only `127.0.0.1`.
- An idle API connection stays open: it pings every 30 s
  (`TrueNASWSConnection(keepalive=)`, `connection.KEEPALIVE_INTERVAL`). The
  middleware closes a websocket that sends nothing for 60 s, which dropped a
  client left idle during a long command and logged `connection lost`.
- Behind an HTTPS proxy (`HTTPS_PROXY`), uploads and downloads verify with the
  same trust as the websockets; they ignored a CA bundle and failed (or trusted
  certifi) while the API connected.
- `generate-typings` writes LF stubs on every platform; on Windows they were
  CRLF, so one dump gave different bytes there than on Linux.


## [0.6.1] - 2026-10-20

### Changed

- Dependency floors that hold, measured by installing every floor on Python
  3.9 and running the suite: `pathapi>=0.1.2` (what hostctl 0.4.0 requires;
  `0.1.0` could not be installed with it), `requests>=2.32.3` (older releases
  drop the side channels' TLS context, so uploads and downloads ignored
  `sslverify`), a new `urllib3>=2.0.2,<3` (1.26 fails on an IP-address target),
  and `pytruenas[config]` now `pyyaml>=6.0.1,<7`.

- The package root imports its names explicitly instead of
  `from .auth import *`, and lists `Credentials`, `LocalAuth`, `ApiKeyAuth`,
  `TokenAuth` and `BasicAuth` in `__all__`, so a type checker accepts
  `from pytruenas import ApiKeyAuth`. Every name importable from the root
  before still is. `auth`, `namespace`, `fs.tnasws`, `models.apidump`,
  `models.jsonschema` and `utils.io` declare `__all__`.
- `pytruenas call --help`, `help --help` and `deploy --help` (and their MCP
  tool descriptions) are one paragraph on what the command does, instead of
  1.7-2.5 KB of design notes.
- `help`, `call --field` and `generate-typings` read a method's parameters,
  return value, payload and enum values through one private module
  (`pytruenas.utils._schema`). `apihelp` and `fields` keep every public
  function and its signature; the generated stubs for the test fixture are
  byte-identical apart from the entries below.
- The sdist no longer ships the repository-root `AGENTS.md` or `benchmarks/`,
  and neither the sdist nor the wheel ships a `CLAUDE*` or `*.local.*` file at
  any depth, even from a tree copied without its `.gitignore`. The build
  requires `hatchling>=1.27`, and the project URLs name the documentation site.
- The `dev` extra requires `pytruenas[config,ssh,codegen]` instead of copying
  their requirements; an install of `.[dev]` resolves to the same packages.
- The test run treats a warning as an error and an `xfail` that passes as a
  failure (`filterwarnings = ["error"]`, `xfail_strict = true`).
- Releases: a `v*` tag now builds only after the suite passes at every declared
  dependency floor on Python 3.9; the tag must equal the built version; the
  wheel is installed with no extras into a clean environment on 3.9 and 3.14,
  imported, checked for `py.typed`, `AGENTS.md` and `README.md`, its console
  script run and the suite run against it; and a broken strict docs build
  blocks the release. A pre-release tag (`v1.0.0-rc.1`) makes a GitHub
  pre-release only: no PyPI upload, no docs deploy.
- `benchmarks/run.py` names a saved result
  `pytruenas-<version>-py<XY>-<platform tag>` and records `platform_tag`, so
  results from different machines for one release no longer share a file;
  results are written with LF line endings on every platform. New
  `--results-dir` and `--compare RESULT` (each median as a ratio to a saved
  result). The CI benchmark job measures the latest PyPI release and the
  checkout in the same job.
- The `dev` extra installs `pyright` and `mypy` (from Python 3.10), which
  the generated-stub type check needs; without them that test skips.

### Added

- `pytruenas.utils.cmd.with_targets(args_cls)` and `TargetsField`: an `Args`
  class with the trailing `targets` positional declared as its last field.

- `pytruenas.TrueNASError`, the base of every error pytruenas raises at run
  time: `ClientException` (and with it `ValidationErrors`, `CallTimeout`,
  `ConnectionClosed`, `JobFailed`) and `AuthenticationError` now derive from
  it. The package root exports all of them; each keeps its module and its
  existing bases.
- `TrueNASHost(...)` / `TrueNASClient(...)` has typing overloads that list the
  keywords it accepts (`verify=`, `api_key=`, `executor=`, ...), so an editor
  shows them; construction is unchanged.
- A command module may define `validate_args(args)`, called once with the
  parsed arguments before any target runs; a `duho.UsageError` raised there is
  reported once as `pytruenas: error: MESSAGE` with exit status 2.
- `apicache.services()` and `apicache.service_methods()` take an optional
  `version=`, as `load()` does, so a caller making several lookups reads the
  appliance's version once.
- `tests/test_codegen_typecheck.py` runs pyright (3.9 and 3.14 targets) and
  mypy (3.10 and 3.14) over the stubs generated from the fixture and from a
  set of unusual schema shapes, plus a consumer whose valid calls must pass and
  invalid ones must be reported. It skips, saying which checker is missing,
  when pyright or mypy is not installed.
- `Unit(..., restart_on_change=True)` runs `systemctl try-restart` after a
  changed unit is reloaded, so a running service picks up its new definition.
  Off by default: a restart interrupts the service.
- `MiddlewareFiles.find_template(..., writable=False)`: every template it finds
  is on the read-only `/usr` dataset, and there was no way to ask for the
  `zfs.writable` window the write needs.
- A guide page, "Patching a host", presenting `pytruenas.patch` as a toolkit
  for building your own host patches, with a complete patch (a config file
  from a template, a systemd unit, a change layered onto a middleware
  template with its etc regeneration and service reload) and a stand-in client
  that runs it offline. The API header's `patch` section now lists every
  export with its signature and contract.

### Fixed

- A lost connection says why: the reader logs `connection lost: <cause>` (or
  `connection closed by the server`) as a WARNING, and the `ConnectionClosed`
  each waiting call raises carries the cause as `__cause__`. Any `recv()`
  failure used to end the connection silently, so a dropped socket looked like
  a slow server.
- Every MCP tool takes `targets`. The hosts were added to each command's parser
  by hand, so they were missing from the tool schema: naming one was refused as
  an unknown argument, and every tool call ran against `localhost`.
- `call METHOD nas -- --field=value` and a RunPath flow's `-- --apply` no longer
  log "ignoring the argument(s) after '--'" while using them. A command module
  now says it reads the tail with a module-level `_allow_passthrough_ = True`
  (as `call` and `deploy` do); RunPath commands are never warned about.
- A comma list of targets where a later part has its own scheme or user is
  split there: `wss://nas1,wss://nas2` was `wss://wss://nas2`, and in
  `nas1,root:pw@nas2` the second host logged in as user `nas1,root`.
- An empty `PYTRUENAS_SSLVERIFY` no longer turns TLS verification off: it is
  unset, as an empty variable should be. A value that is neither a boolean nor
  an existing CA bundle path (here or as the config file's `sslverify`) is an
  error naming where it came from, instead of a bundle path that verified
  nothing.
- `generate-typings` no longer deletes a directory of hand-written stubs. A
  directory holding only `.pyi` files was taken for an old output and replaced,
  and the default `--path` was `typings/`, where pyright looks for a project's
  own stubs. Only an absent or empty directory, or one marked
  `.pytruenas-typings` by a previous run, is replaced, and the default `--path`
  is `truenasapi_typings/current`.
- Generated `_create`/`_update`/`_upsert` stubs type `**fields` with the
  method's payload again (`Unpack[UpdateUserUpdate]`), not `Unpack[bool]`
  (wrong since 0.5.1); the payload is found as `call` finds it.
- Generated stubs import `sys` unaliased, so mypy reads the
  `sys.version_info >= (3, 11)` guard and stops treating every optional key as
  required on a target below 3.11.
- A `logging.LoggerAdapter` passed as `logger=` (or assigned to
  `client.logger`) no longer makes every API call raise `AttributeError`: the
  per-call TRACE record is written with `logger.log()`, which any logger has.
- `client.path("/mnt", "/etc")` names `/etc` on every leg. Its websocket
  (`tnasws`) leg joined the segments with `/` and operated on `/mnt//etc`, so
  on a host without SSH a read, write or `unlink()` reached a different file;
  `fs.path()` joins as the composite path does.
- A reconnect after a login with a one-time code asks `otp_provider` for a new
  code instead of sending the spent one again (which the server refused, so the
  session never came back); without a provider it raises
  `AuthenticationError("OTP_REQUIRED")`.
- The shipped API header documented names that do not exist: a `target=`
  keyword (the first parameter is positional `config`), `.host`,
  `connection.Client` and `pytruenas._conn` (the class is `TrueNASWSConnection`,
  which also takes `logger=`), `client.path()` returning a `TnasWsPath`, and an
  `UPSERT` action passed to `_upsert`'s callback. It now points at the project
  URL rather than a file an installed copy does not have.
- The suite passes with no extras installed: one SSH test lacked its
  `asyncssh` guard.
- `examples/simple_client_from_yaml.py` moved to `examples/scripts/`, so
  `--cmdspath examples` no longer warns that it is not a command.

- `client.api.<method>(..., job=True)` waits for the job and returns its
  result, as the upstream client does. It was accepted and dropped, so the call
  returned the job id while a delete or replication was still running and its
  failure was never seen. A failed job raises `JobFailed` (the matching
  `OSError` with `_ioerror=True`).
- On a host without SFTP, `path.chmod()` and `path.chown()` wait for the
  middleware job behind them and raise `OSError` when it fails; they returned
  before the change was made and reported success for a job that then failed.
- On a host without SFTP, `path.unlink()` of a missing file raises
  `FileNotFoundError` (it ran `rm -f`, which succeeds), and `unlink()`/`rmdir()`
  raise `IsADirectoryError`, `NotADirectoryError`, `OSError(ENOTEMPTY)` or the
  errno `rm` reports instead of `subprocess.CalledProcessError`, so pathapi's
  `rm()` and `move()` handle them.
- On a host without SFTP, `path.stat()` follows a symlink, so `is_dir()` of a
  link to a directory is true; `stat(follow_symlinks=False)` and
  `is_symlink()` describe the link. Its result carries the owner and the access
  and change times (every file read as owned by root).
- `download()` (and so `read_bytes()` on a host without SFTP) checks the job
  that streamed the content and raises when it failed, instead of returning
  what arrived before the failure; `read_bytes()` raises it as an `OSError`.
- `TrueNASHost("/var/run/x.sock")`, a bare socket path the docs list, connects
  to that socket; it was read as a remote host with an empty name.
  `HostConfig("truenas+unix://var/run/x.sock")` keeps the `var` segment, and
  `TrueNASConfig()` is the local middleware socket rather than a remote target
  with no host.
- The error for an unknown keyword to `TrueNASHost(...)` lists only keywords
  it accepts; it offered `port`, `secure`, `socket_path` and `api_path`, which
  are spelled in the connection string.
- `install_sshcreds()` puts the key on a copy of an `ssh=` config you passed,
  rather than on your object, which another host may share.
- A websocket-leg path on an IPv6 host renders its authority bracketed
  (`truenas+ws://[fd00::1]/...`), not `truenas+ws://fd00%3A:1/...`.
- `typing.get_type_hints()` resolves the public annotations of the client,
  connection, auth, path and model modules on Python 3.9 and on every version;
  quoted `X | None` unions, `typing.NotRequired` before 3.11, and names
  imported only for type checkers made it raise.
- `--logto {target}.log` gives each target only its own records under
  `--parallel`. Every target's file handler sat on the same loggers, so each
  file received the records of every target running at the same time.
- `--loglevel websocket:DEBUG` (or `requests`, `urllib3`, `asyncssh`) takes
  effect: those loggers were set to WARNING after `--loglevel` was applied.
- A `./pytruenas.yaml` found in the current directory can no longer name
  command sources (`commandspath`), as documented. The check never recognised
  the implicit file on a real run, so its `commandspath` was imported.
- A config file named with `--config` or `$PYTRUENAS_CONFIG` that does not
  exist stops the run with exit status 2 (`config file not found: PATH`)
  instead of running without its credentials and TLS setting. The implicit
  `./pytruenas.yaml` may still be absent.
- `deploy --source repo --mode pyz` and a relative `deploy --path` are refused
  once, with exit status 2, before any client is built, instead of failing
  every target with status 1.
- `help` makes one `system.info` round trip per invocation instead of three,
  cached or not.
- `call METHOD nas -- --field=value` sends the fields untyped, with a warning,
  when reading the method's schema raises `KeyError`; it failed the target
  with an `UnboundLocalError`.
- `deploy nas -- COMMAND` no longer logs a password contained in `COMMAND`
  (`Running: ...` is redacted; the command runs as given).
- Two fetches of one appliance's API dump (two processes, or one host named
  twice) no longer overwrite and delete each other's file on the target: each
  fetch dumps into a `mktemp` file of its own and removes only that one.
- A target that does not parse as a URI is refused with a message naming every
  character to percent-encode in the credentials, `[` and `]` included
  (`%5B`, `%5D`), and no longer quotes part of the password: urlsplit's own
  error ("Port could not be cast to integer value as '...'") was what the CLI
  logged.
- The CLI guide describes the config file as it is: it supplies
  `credentials`, `sslverify` and `commandspath`, nothing else. The API header
  gives `main()`'s full signature and the `$PYTRUENAS_CONFIG` default, and the
  RunPath example's "TLS verification is on" line logs when it is.
- `generate-typings` no longer aborts with `KeyError: 'properties'` when a
  `get_instance` returns an optional object (`anyOf[object, null]`), a bare
  object or an array. `_get` reads its filters through the union and returns
  that union; with no properties to filter on it is not emitted (logged at
  INFO), and the runtime helper's own signature applies. `_create`/`_update`/
  `_upsert` are likewise skipped when the method has no object payload,
  instead of unpacking a call option.
- Generated signatures no longer repeat a parameter name: two titles that
  sanitize to one (`a-b` and `a_b`, or the same title twice) and a parameter
  titled `self` produced a stub that does not compile. A repeat gets a trailing
  `_`, and an untitled parameter is `argN`, as `help` shows it.
- An array that admits no items (`items: false`) is `list[Never]` whatever
  Python runs the generator. It was `list[typing.Never]` from 3.11 and a bare
  `list` on 3.9, so stubs generated on 3.14 did not resolve for a 3.9 or 3.10
  target. `Never` comes from `typing_extensions` below 3.11, beside
  `NotRequired` and `Unpack`.
- Regenerating typings over a tree that is in use keeps the previous output
  whole. On Windows a stub held open by an editor, or a shell inside the
  directory, made the swap delete the old tree part-way (or entirely) and left
  the new one in a `.typings.*` sibling; the old tree is now renamed aside and
  deleted only once the new one is in place, and a failure removes the
  temporary directory.
- `generate-typings` without the `codegen` extra fails before dumping the API
  from the host, not after (about 24 MB on 26.0).
- A project that type-checks its generated `truenasapi_typings/` no longer
  gets an incompatible-override error for every `_create`/`_update`/
  `_upsert`/`_get` stub: they narrow the runtime helpers on purpose and say so
  with `# type: ignore[override]`.
- The typings guide and API header name the generated root class `V2600` for
  v26.0.0 (not `V26000`), say `--api-version` defaults to the newest version in
  the dump, and no longer describe a `src/truenasapi_typings/` package that
  does not exist. The README no longer claims the generator is validated
  against a full live dump; it says what the tests check.
- `SystemFile(etc="a,b")` regenerated only `a`: both groups went to one
  `etc.generate` call, whose second parameter is a checkpoint. Each group now
  gets its own call.
- Two units built from one `conf` dict no longer share settings. The second
  kept the first one's `ExecStart` and `Description`, so it ran the other
  program; the dict passed in is no longer modified.
- A patch whose follow-up fails (`daemon-reload`, `etc.generate`, a service
  reload) is retried by the next apply. The file was already written, so the
  next apply found nothing to change and the follow-up never ran; the previous
  content is now put back before the error is raised.
- A file rewritten by something else since a patch wrote it -- TrueNAS
  regenerating an `/etc` file after a settings change -- is taken as the new
  original. Re-applying layered the patch onto the stale snapshot and
  `revert()` put the stale content back, undoing that change. Each changing
  write now records digests beside the snapshot (`<name>.baseline.applied`).
- A `.baseline` or `.absent` file found beside a target is no longer trusted
  blindly: a symlink there was read from, written through and restored into
  the target. Where the path backend has `lstat()`, it must be a regular file
  with one link, owned by root or by the target's owner, or `PermissionError`
  is raised. The snapshot is written to a temporary sibling and renamed into
  place, so an interrupted copy is never taken for the original.
- An unchanged write no longer takes a snapshot, and with
  `SystemFile(writable=True)` no longer clears and restores `readonly` on the
  dataset. A rewrite also makes fewer remote calls.
- `zfs.writable()`: when the block raised and the restore failed, the caller
  got the restore's error instead of the block's; it now gets the block's, and
  the restore failure is logged. An inherited `readonly=on` is restored by
  inheriting it again rather than set locally. A path that is not on ZFS is
  left alone (it failed in `zfs get`), and `dataset_for()` raises `ValueError`
  naming the filesystem type instead of returning its mount source. A window
  that never closed is marked on the dataset (`pytruenas:restore-readonly`)
  and closed by the next one.
- Unit names and files systemd reads as intended: a dotted name (`my.agent`)
  gets its `.service` suffix, the root mount unit is `-.mount` (was `.mount`),
  a list value in `conf` renders as repeated keys (was a Python repr), and a
  value with a line break raises `ValueError`. `parse_unit()` reads repeated
  keys and sections and backslash continuations.
- `MiddlewareFiles` no longer runs a command on the host from `repr()`, and
  `find_file()` honours a target's own baseline suffix instead of a hardcoded
  `.baseline`.
- `TemplateTarget.apply_template()` raises a clear `TypeError` for keyword
  arguments with a text or path template (it said they were accepted).
- `render_basic_template()` substitutes in one pass: a value containing
  `%{...}` was substituted again, depending on the context's order.
- The API header said `MiddlewareFiles.find_template` defaults to
  `baseline=False`; the default is `True`.
- `examples/scripts/simple_client_from_yaml.py` verifies TLS certificates
  unless its config file sets `sslverify: false` (or a CA file path); it turned
  verification off for every host.
- README: links are absolute, so the `LICENSE` link works on PyPI; the
  development setup creates a venv named for the interpreter it uses and
  installs with `--only-binary=cryptography`, which Windows ARM64 needs.
- A connection string that does not parse names `[` and `]` (`%5B`, `%5D`)
  among the characters to percent-encode in the credentials.
- Inside a CLI fan-out, a record logged through `client.logger` names its
  host once (`[nas1] ...`), not twice.
- The `config` extra is described as what it is: the CLI's YAML config
  file (credentials, TLS and command sources), not a targets file.

## [0.6.0] - 2026-10-19

### Upgrade notes

pytruenas now runs on hostctl 0.4, which moves from `pathlib_next` to
`pathapi`. These change what a caller sees:

- **Path types are `pathapi` paths.** `pytruenas.fs.LocalPath` is
  `pathapi.LocalPath`; `TnasWsPath` and `TruenasPath` are `uripath.URIPath`
  subclasses (distribution `pathapi-uri`); `client.path()` returns hostctl's
  `CompositePosixPath` on `pathapi`. Code importing `pathlib_next`, or testing
  `isinstance(..., pathlib_next.Path)` against these, must use `pathapi.Path`.
- **`TruenasPath` is gone, and `pytruenas.fs.path(client, ...)` of a remote
  client is `client.path(...)`**: hostctl's composite path over the host's
  providers, whose SFTP leg is the host's own. `TruenasPath` kept a second SFTP
  leg (its own connection and login) only so a path built without a host could
  fall back to the websocket. `fs.path(..., backend="ws")` still builds a
  `TnasWsPath`, which is what the `tnasws` provider returns now; an unknown
  `backend=` raises `ValueError`. `symlink_to(force=, onremove=)` is the
  function `pytruenas.fs.symlink_to(path, target, ..., force=, onremove=)`,
  which works on any path, `client.path()` included (the method form never
  reached a composite path's SFTP leg).
- **hostctl 0.4 names.** `hostctl.host.SshConfig` is `hostctl.SSHConfig`
  (keyword arguments after the host); the "not started" error a web shell
  connection raises is `hostctl.OperationNotStartedError`, a `ConnectionError`
  where `hostctl.provider.OperationNotStarted` was a `RuntimeError`. The rest
  of hostctl's renames are in its own changelog, "Migrating from 0.3".
- **`verify=False` is the one way to skip the SSH host-key check.**
  `known_hosts=None` raises `ValueError`; pass `verify=False` (add
  `sslverify=True` to keep checking TLS). `verify=False` reaches the SSH leg
  as `SSHConfig(verify=False)`, so `verify=False, known_hosts=()` no longer
  checks `~/.ssh/known_hosts`; keys named with `known_hosts=` are still
  checked. For host keys checked with TLS off, pass `sslverify=False`.
- **`client.last_selection` holds hostctl `SelectionStep` records**, not
  dicts: read `step.provider`/`step.chosen`, not `step["provider"]`.
- **The web shell runs hostctl's framed console protocol.** Its executor,
  `webshell.WebShellExecutor`, is hostctl's `hostctl.console.ConsoleExecutor`
  over the websocket, with no thread per command.
  `WebShellSession.command_lines()` and `WebShellSession.execute()` are gone:
  run a command with `client.run(...)` or
  `WebShellExecutorProvider(client).executor(command, ...)`, hostctl's
  `subprocess`-shaped call. What a caller can see: a connection lost after the
  command line was typed raises `ConnectionError` (it raised
  `OperationNotStartedError` until the command's first marker arrived, which
  let the host replay a command that may have run) and a command that exits
  the shell raises `ConnectionError` instead of `SubprocessError`; a failure
  before the command line was typed, including a failed write, is a decline,
  so `run()` falls back to the next provider; `stdin=subprocess.PIPE` without
  `input=` raises `ValueError` and a file descriptor is read to EOF, where both
  raised `NotImplementedError`; an unknown `run()` option raises `TypeError`.
  Uncaptured stdout is written per websocket frame, where it was batched up to
  4 KiB or 0.1 s.
- **`deploy` runs on `hostctl.deploy`**, which came from pytruenas's own
  bundler; `pytruenas.utils.bundle` is gone (import `hostctl.deploy`:
  `bundle()`, `deploy()`, `SourceTree`, `Deployment`), and `BundleError` is
  `hostctl.BundleError`. The command line, the default path, the `.pyz` name,
  `PYTRUENAS_PKG_ROOT`/`PYTRUENAS_PKG_NAME` and the digest markers are
  unchanged, so a previous deploy is recognised (and replaced once: the
  payload's digest differs). What differs: the `dir` launcher adds no empty `PYTHONPATH`
  entry (the working directory is never importable); each step on the target is an argv with
  `--` before its paths; a package name that is not a dotted identifier
  raises `ValueError`; and a missing extra raises `hostctl.MissingExtraError`.
- **The SSH leg reads `~/.ssh/config`, as `ssh` does**, for commands and
  file operations alike: a host alias, `HostName`, `Port`, `User`,
  `IdentityFile` or `ProxyJump` there now applies. A user or port written in
  `shell=` wins over the file; with no user in either the login is still
  `root`, and with no port 22 (`install_sshcreds()` always logs in as `root`,
  where it installed the key). So `.config.ssh.port` is `None` and, for a
  `shell=` with no user, `.config.ssh.username` is `None` and
  `.config.ssh.default_username` is `"root"`, where both read 22 and `"root"`.
  For a leg that reads no personal file, pass
  `ssh=SSHConfig(host, username="root", ssh_config=None)`. An `SSHConfig` you
  build yourself defaults to the local account name rather than `root`, as in
  hostctl 0.4, and its `ssh_config=` takes a `pathlib.Path` for a file (a
  string is configuration text).

### Added

- **`username=` and `password=` override the target's own credentials**, in
  `TrueNASClient(...)`/`TrueNASHost(...)` and `TrueNASConfig.from_target()`:
  hostctl applies them over the URI's user and password (`password=""` is no
  password), so `TrueNASClient("wss://admin@nas", password=pw)` and
  `TrueNASClient("wss://nas", username="admin", password=pw)` work. The
  constructor now takes `password=`, `otp=`, `api_key=` and `token=` as
  `from_target()` did; a password given both in the URI and as `password=`
  takes the keyword instead of raising.
- **A command that needs a missing optional extra fails its target in one
  line, with status 125**: the CLI reports `hostctl.MissingExtraError` (`FEATURE
  needs the 'EXTRA' extra: pip install "hostctl[EXTRA]"`) as hostctl's own
  command line does, instead of a traceback. pytruenas's own extras raise it
  too, naming `pytruenas[...]`: `config` for a `--config` file (reported by
  `main()` as `pytruenas: MESSAGE` with status 125, since it is read before
  any target), `codegen` for `generate-typings`, and `ssh` for deriving a
  public key with neither `cryptography` nor `asyncssh` installed. Each was a
  plain `ImportError`; `MissingExtraError` is one, so `except ImportError`
  still catches it.

### Changed

- **`hostctl[deploy]>=0.4.0,<0.5` replaces `hostctl` and `packaging`** in the
  core dependencies, so `deploy` (both sources) works out of the box; it adds
  `pathspec`. The `repo` extra is that same requirement, and `dev` no longer
  lists `pathspec`/`tomli`.
- **Dependencies: `hostctl>=0.4.0,<0.5`, `netimps>=0.4.0,<0.5`,
  `pathapi>=0.1.0,<0.2` and `pathapi-uri>=0.1.0,<0.2`**, replacing
  `hostctl<0.4`, `netimps<0.4` and `pathlib_next[uri]`. The `ssh` extra is
  `hostctl[ssh]>=0.4.0,<0.5` alone: pytruenas no longer imports `sftppath`. A deploy
  payload carries `pathapi` and `pathapi-uri` where it carried `pathlib-next`
  and `uritools`.
- **One SSH connection and one login per host.** Commands and SFTP paths
  share the connection hostctl opens (it was three with `TruenasPath`'s own
  SFTP leg), so `ssh_config`, `connect_options` and the connect timeout apply
  once.
- A `TnasWsPath` write stream whose `with` block raises uploads nothing; it
  uploaded what had been written.
- A relative path on a remote target, and `client.path()` with no segments,
  stay rooted at `/` on every leg (hostctl 0.4's SSH hosts read them against
  the login directory instead).
- `install_sshcreds()` swaps the providers through hostctl's
  `resolve_providers()` and `replace_providers()`, which closes each replaced
  transport once.
- The provider names `executor=`/`path=` take are hostctl descriptors
  (`TrueNASHost.provider_resolvers`), and `TrueNASHost.default_providers()`
  answers which a target gets. An unknown name raises hostctl's `ValueError`
  (`unknown executor provider descriptor: 'shh' (known: ...)`), and the module
  constants `pytruenas.host.EXECUTOR_NAMES` and `PATH_NAMES` are gone.
- The fallback WARNING comes from hostctl: `[nas] run() fell back from ssh
  to webshell: ssh: <reason>`, once per skipped provider, and now also for a
  path operation served by `tnasws` after `sftp` declined. Its message no
  longer suggests a `known_hosts` setting.
- `client.ssh` is hostctl's `SSHExecutorProvider.connection`: the same
  asyncssh connection, bound to hostctl's own event-loop thread (see the API
  header for how to run its coroutines).

- **Dependency floor `duho>=0.6.0,<0.7` → `duho>=0.7.3,<0.8`.** The command
  line is unchanged: its help, flags, `--version` and exit statuses are the same
  as under duho 0.6. Internally, field metadata is written `Meta(...)` (duho
  removed `NS`), and the RunPath base's `_initparser_` forwards its build
  keywords by name, as duho now requires. A derived tool that imports `NS` from
  `duho` or overrides `_initparser_(cls, parser, *args, **kwargs)` must make the
  same two changes.
- **Dependency floor raised to `duho>=0.7.5,<0.8`.** `main()` now goes through
  `duho.run(..., exit="parse")`: `--help`, `--version` and usage errors still
  raise `SystemExit` from `main()`, and every other outcome is still returned as
  an `int`. New for the program: Ctrl-C ends with status 130 and a broken pipe
  (the reader of standard output went away) with status 1, both without a
  traceback.
- The test suite restores the RunPath registration with
  `duho.runpath.preserve_registration()` and reads it with
  `duho.runpath.registration()`, and tests the step arity with
  `duho.runpath.step_wants_context`, instead of duho's private names.

### Fixed

- **`client.path(..., backend=name)` uses that provider for every operation.**
  It chose the provider that built the path, and each operation then selected
  again from the first capable one: on a host with an SSH leg,
  `backend="tnasws"` wrote over SFTP.
- **A lost connection during a patch template's `chmod` stops the write.**
  `FileTarget` took any `OSError` from `stat()`/`chmod()` for "this backend
  has no modes" and wrote the content anyway, which a reconnect could leave at
  the wider mode the `chmod` was meant to prevent.

## [0.5.4] - 2026-10-01

### Fixed

- **`-v`/`-q` now change the `pytruenas` logger.** The root command had no
  declared name, so the verbosity flags set the level on a logger named after
  the class (`PyTrueNAS`) that nothing logs to. The command now declares its
  name, `pytruenas`, so `-v` makes the package's own logging more verbose and
  `-q` quieter. The CLI's usage and `--version` output are unchanged.

## [0.5.3] - 2026-09-28

### Changed

- **Dependency floor `duho>=0.5.2,<0.6` → `duho>=0.6.0,<0.7`.** Every
  documented `[minor]` break was checked against actual pytruenas usage and
  against the full test suite on both supported interpreters; none apply, and
  no pytruenas code changed. Since 0.6.0, `PYTRUENAS_MCP=stdio` makes
  `pytruenas` serve MCP over stdio instead of its normal CLI dispatch,
  exposing `call`/`query`/`deploy`/etc. as MCP tools — this is `duho`'s own
  opt-in trigger, and pytruenas does not opt out of it. See the "MCP" section
  of the CLI guide.

## [0.5.2] - 2026-09-25

### Added

- **`pytruenas help <method>`** — CLI-style help for any middleware method,
  read from the appliance's own API definition: every field with its type,
  whether it is required, its default, the values an enum allows, and whether
  the method is a job. Also `help <namespace>` to list a namespace's methods and
  `help all` for the index of namespaces; `--json` emits the definition slice
  for tooling.

  It asks the API per namespace (`core.get_services` and
  `core.get_methods(<service>)`), which requires **no roles and no command
  access** — so it works for an API-key account with no shell, no SSH and no web
  shell. `--dump` reads the full `middlewared --dump-api` definition instead,
  which needs command access and is only necessary for `--api-version` (the live
  API cannot describe an older version).
- **`call` takes fields instead of hand-written JSON.** After a literal `--`,
  `--field=value` and bare `field=value` are interchangeable and typed from the
  method's schema:

  ```sh
  pytruenas call user.create nas1 -- --username=svc --full_name='Svc' --group_create=true
  ```

  Booleans, integers, nullable fields, arrays (a comma list or a repeated flag)
  and nested objects (`--options.acl=true`) are coerced; `--name:json=...` and
  `--name=@file` are the escape hatches. An unknown field name or a bad enum
  value is an error naming the alternatives, raised before anything is called.
  `--no-schema` skips the definition, `--refresh-api` re-fetches it.
- `examples/provision/` — a dry-run-by-default provisioning flow (users, DNS,
  datasets and encryption, shares and services), plus `examples/README.md`
  indexing every example.
- `$PYTRUENAS_CACHE` — where the fetched API definition is cached (default: the
  platform user cache directory), keyed by host and API version, with
  per-namespace answers in their own small files.

### Fixed

- **`dump_api()` could not work on a host with no SSH leg.** It captured
  `middlewared --dump-api` from `run()`'s stdout, and that output is
  24,103,000 bytes on 26.0 — enough to lose the web shell's connection every
  time, i.e. exactly the host the web shell exists for. The dump is now built
  and gzipped on the target (2,025,240 bytes, 11.9x) and fetched over SFTP when
  there is an SSH leg, otherwise in 256 KiB chunks through the command channel,
  with the transfer checked against the target's own sha256. The `filesystem.get`
  HTTP side channel is deliberately not used: it truncated both the 23 MB file
  and the 2 MB one.
- `dump_api()` caches its result per host and API version, so a second call (or
  a second `help`) does not spend ~75 s rebuilding it. `cache=False` and
  `refresh=True` control that.

### Changed

- `query -f` and the new `call` fields share one `NAME=VALUE` parser
  (`utils.cmd.split_assignment`), so a malformed one is reported the same way
  everywhere.

## [0.5.1] - 2026-09-23

### Changed

- **Tokens for the web shell and the HTTP side channels are now origin-bound
  and single-use.** pytruenas passed `match_origin=False` where the server's
  own default is `True`, so a leaked token was usable from anywhere; both
  flags are on now. A setup whose HTTP request leaves from a different IP than
  its websocket (multi-homed, or proxied) would be refused where it used to
  work.
- Credentials sent over plaintext `ws://` to a non-loopback host log one
  warning per host. Not a refusal: `ws://` is legitimate for a loopback target
  or an already-private link.
- Dependency: `hostctl>=0.3.2,<0.4` (and the `ssh` extra). 0.3.2's `redact_uri`
  leaves a well-formed URI alone, which this package's redaction and its
  "does this target parse?" check both rely on.
- **`call`/`query`/`dump-api` attribute their output when there is more than
  one target**: each line becomes `{"target": "<host>", "result": <result>}`
  (credentials removed). A single target still prints the bare result, so
  existing one-host scripts are unaffected. Interleaved unattributed lines
  could not be matched to a host at all.
- A command module's `args` is a per-target copy carrying `args.target`, and a
  client the CLI built is closed when the command finishes. A client returned
  by an `init` hook is left alone — it belongs to the hook.
- **A config file found rather than asked for no longer supplies
  `commandspath`.** An implicit `./pytruenas.yaml` belongs to whatever
  directory the CLI runs in, and that key names code to import. Pass
  `--config` (or set `$PYTRUENAS_CONFIG`) to load commands from a config file;
  every other key of an implicit file is read as before.
- **A keyword argument to a middleware call now raises `TypeError`.** Those
  methods take positional parameters; a keyword was swallowed and logged at
  debug level, so `client.api.user.query(filters=[["uid", "=", 0]])` sent no
  filters and returned **every** row — which then drove an update. Pass
  parameters in order (`query([["uid", "=", 0]])`) or use the `_query`/`_get`
  helpers, which take keywords by design. `timeout` and the
  upstream-compatibility names (`job`, `background`, …) are still accepted.

### Fixed

- **A deployed copy could not report its own version.** A zipapp carries no
  installed metadata, so `importlib.metadata` raised `PackageNotFoundError`:
  `__version__` read `0.0.0.dev0` and `pytruenas --version` answered with a
  usage error (exit 2) instead of a version. A bundle now carries a minimal
  `.dist-info` for every distribution in it — the real `METADATA` where it can
  be read — so `--version` works in both layouts and the versions of everything
  bundled are visible on the target. `--source repo` carries none: there is no
  installed metadata to copy, and inventing a version would be a lie.
- **A unix socket path was mangled by the URI layer.** `_target` interpolated it
  raw, so `/run/a?b/x.sock` rendered as `/run/a`; a `unix://` URI's path is
  percent-decoded now, as a URI path must be (`unix:///run/a%3Fb/x.sock`
  names `/run/a?b/x.sock`, where the literal `%3F` spelling would open a
  different file).
- **A client dropped without `close()` leaked its websocket and reader thread**
  for the life of the process; it is closed when the client is collected.
  `close()` (or a `with` block) is still the right way — the finalizer is a
  safety net, not a substitute.
- **The SFTP leg built a fresh backend on every call**, and pathlib_next keys
  its connection cache on the backend object — so nothing ever hit that cache:
  five `readlink()` calls opened five concurrent SSH sessions and closed none
  (measured). One backend per client now, keyed on the SSH settings so
  `install_sshcreds()` cannot leave one authenticating with old credentials.
- `install_sshcreds()` swapped the provider selectors one at a time without the
  lifecycle lock and never closed the transports it replaced, leaking the old
  SSH connection.
- **An OTP written the documented way was mis-parsed.** `"root:pw\notp:123456"`
  produced the token `"otp:123456"`; the raw credential string is now split by
  the same `hostctl.host.parse_credentials` the URI path already used, so both
  spellings mean the same thing. A bare token on its own line still works.
- **Generated stubs describe `enum`/`const` and maps.** Both rendered as
  `JsonValue` while the appliance's dump uses them 6413 and 6420 times; they
  are `Literal[...]` now (with `None` as a union member), and an object whose
  `additionalProperties` carries a schema is `Mapping[str, T]` rather than
  "some object". On TrueNAS 26.0 that is 1275 `Literal` annotations where there
  were none.
- **A middleware method whose name is also a `Namespace` method is no longer
  emitted.** `core.subscribe` redefined the real `Namespace.subscribe`, so a
  checker accepted `ns.subscribe(event)` — which at runtime calls the real
  method with a positional callback — and rejected the correct `ns.subscribe()`.
  Reach the middleware one as `ns(_method="subscribe", ...)`, as the runtime
  documents; generation logs which methods it skipped.
- **Generated signatures offered the call options positionally.**
  `_method`, `_ioerror` and `_filetransfer` appeared as ordinary parameters
  while the runtime takes middleware parameters positionally and now rejects
  stray keywords — following the stub shifted a real parameter. They are
  keyword-only (after a `*`), and `_timeout`/`_tries`, which were missing
  entirely, are included.
- **Generation crashed on valid schemas.** A list `type`
  (`{"type": ["string", "null"]}`) raised `NotImplementedError` and
  `{"items": true}` a `TypeError`, each aborting the whole run; they render as
  a union and as a list of anything. An unknown type name degrades to
  `JsonValue` instead of failing.
- **A docstring ending in `"""` produced a stub that would not parse.** Every
  double quote is escaped now, not just an interior run or a single trailing one.
- **Names from the dump became invalid identifiers.** Only `.`, `_` and `-`
  were treated as word boundaries, so `acl(nfs4)`, `smb:share`, `bracket[x]`
  and a leading digit went straight into a class name.
- **Two different shapes could take the same TypedDict name**, and the later
  definition silently replaced the earlier — so every reference to the first
  pointed at the wrong shape. The second gets a numbered name.
- **A string default changed type.** It was parsed with `literal_eval` and used
  verbatim when that succeeded, so a schema default of `"0"` became the integer
  `0` and `"true"`/`"None"` changed meaning. Only this package's own synthetic
  defaults are Python source now (`codegen.Source`).
- **`JsonValue`/`JsonObject`/`JsonArray` were plain strings**, so every stub
  annotation naming them resolved to a `str` variable rather than a type.
- `generate()` renamed the methods of the **caller's** dump and overwrote its
  return titles, so generating twice from one dump gave different output.
- `get_instance` without an `id` parameter raised `UnboundLocalError` (or
  reused the previous namespace's id type).
- A name from the dump could write **outside the output directory**; such a
  path now raises `codegen.BadApiName`.
- **The stub template could not be read from a zipapp** — the shape
  `deploy --mode pyz` installs — because it was loaded by filesystem path.
- The `codegen` extra pins `jinja2>=3.0,<4`, per the project's own convention.
- **A deployed bundle was missing `uritools`.** The dependency closure dropped
  a requirement's own extras, and pytruenas depends on `pathlib_next[uri]`,
  whose extra requires it. The appliance does not ship it (measured on
  26.0.0-BETA.1, 386 distributions), so `pathlib_next.uri` — which every
  remote path is built on — could not import on the target. A requirement's
  extras are followed now, and the root's extras are no longer applied to
  every distribution in the closure.
- **Environment markers were evaluated against the machine running `deploy`**,
  not the target, so a platform- or version-gated dependency was decided by the
  wrong environment. The probe reports the target's marker environment
  (`bundle.parse_probe` reads it; an older probe that prints names only still
  works) and the closure is resolved with it.
- **`deploy --source repo` shipped things a clone would not.** `.git` was
  matched only as the first path component, so a nested checkout's history was
  included; a nested `.gitignore` was ignored entirely (git applies one per
  directory); and a symlink or junction pointing outside the repo was followed,
  shipping whatever it pointed at.
- **A missing `--ignore-file` silently disabled all filtering** — the fastest
  way to ship a gitignored secret. A file the caller names and that is not
  there is now an error; the defaults stay forgiving.
- An unparseable line in a `requirements.txt` aborted the whole deploy, though
  that list is only printed as a heads-up; it is skipped with a warning.
  Backslash continuations and inline comments are read correctly.
- **Arguments after `--` were parsed twice.** pytruenas split `argv` itself
  and carried the tail in a module global, duplicating duho's own
  `_passthrough_` capture; `deploy` reads it off the parsed instance now.
  A tail that no command reads, or a target placed *after* the separator
  (where it becomes part of the remote command and the run silently falls back
  to `localhost`), is reported instead of dropped.
- A RunPath step whose third parameter has a default — or which takes `*args`
  — was mistaken for the 3-argument module-command shape and had its
  arguments swapped by the adapter. Only *required* positionals count now.
- Command discovery read global options off the default app root, so a derived
  tool's own options were invisible to it, and the RunPath base registration
  was skipped for the default args — leaving a derived tool's base registered
  process-wide for whatever ran next.
- **Concurrent targets shared one `args` object.** Per-target state a command
  wrote on it (and `args.target`, which did not exist at all) belonged to
  whichever target ran last; `init` hooks had no way to know which target they
  were building a client for.
- **Per-target clients were never closed**, so every target leaked its
  websocket and reader thread for the life of the process — under `--parallel`,
  all of them at once.
- **`--logto` files missed the records they exist for.** The handler was
  attached to the command's logger only, so a transport fallback warning or a
  connection error from the library never reached the per-target file.
- **Concurrent result lines interleaved mid-line** (`print()` is two writes),
  so neither line parsed as JSON. Results are written through one lock.
- A set in a result serialized as its Python repr (`"{1, 2}"`), and a datetime
  as whatever `str()` produced; they are a sorted list and an ISO timestamp.
- `generate-typings` with an unknown `--api-version` raised `SystemExit` inside
  a fan-out worker, aborting the whole run and discarding the other targets'
  exit codes; it fails that target with exit code 2.
- A discovered command module with no `run(client, args, logger)` was offered
  in `--help` and failed on every target; it is skipped with a warning.
- **Target expansion split passwords.** Commas and `[A-Z]`/`[0-9]` ranges were
  expanded over the whole target, so `wss://root:pw,with,commas@nas` became
  three targets (two of them nonsense) and `root:secret@nas1,nas2` gave the
  second host no credentials at all. Only the host part is expanded now, and
  credentials are carried to every expanded target.
- A config file was read with the console's encoding, so a UTF-8 file with a
  non-ASCII value raised `UnicodeDecodeError` on Windows; a config whose top
  level is not a mapping is now ignored with a warning instead of crashing.
- A string `commandspath` in a config file was iterated per character, turning
  `mycmds` into six one-letter sources. A relative entry that exists beside the
  config file now resolves against it rather than against the process's
  working directory.
- A command source that is neither a directory nor an importable name crashed
  the CLI; it is skipped with a warning, as a bad command already was.
- **A timestamp came back late by its own milliseconds**: the sub-second part
  was added twice, so `…T03:42:00.600Z` decoded as `…T03:42:01.200Z`. Negative
  timestamps (before 1970) decode correctly now too.
- **A response that could not be decoded was dropped**, leaving its caller to
  wait out the whole timeout (or forever, with `timeout=None`) for a reply that
  had already arrived. It fails that one call with `ClientException`
  (`errno=EPROTO`); the connection stays usable.
- **`_update`/`_upsert` on an id with no record** raised
  `AttributeError: 'NoneType' object has no attribute 'get'`, naming neither
  the record nor the collection; it raises `FileNotFoundError` naming both.
- **A `True`/`False` result was treated as a job id** (`bool` is an `int`), so
  the client waited on "job 1" and returned that job's result instead of the
  answer.
- **A no-op update rewrote middleware properties forever.** `pool.dataset`
  reports a property as `{"value": "10G", "parsed": 10737418240, …}` while a
  caller sets `"10G"`, so the field looked changed on every call and `_upsert`
  reported a change that never happened. A partial dict is now compared on its
  own keys only.
- `utils.query.MISSING` is an instance, matching `EXCLUDE`; the untested,
  unused `utils.query.merge()` is gone.

## [0.5.0] - 2026-09-23

### Added

- `client.wait(job_id, callback=None, timeout=None)` returns a middleware job's
  result once it has finished and raises `JobFailed` (with the job record and
  errno) when it failed; `callback(job)` receives every change of state and
  progress. `client.job_updates(job_id)` yields the same updates as a
  generator. `upload()`, `download()` and `_create`/`_update`/`_upsert` accept
  a callable `wait=` for progress.
- `TrueNASClient(..., verify=False)` — one switch that turns off every check the
  client makes: TLS certificate verification (websocket, HTTP side channels,
  web shell) and SSH host-key verification (commands and SFTP). `sslverify=`
  and `known_hosts=` override it individually.
- `sslverify=` accepts a CA bundle path (a PEM file or a hashed directory),
  trusted instead of the OS store. With `sslverify=True`, `$SSL_CERT_FILE`,
  `$REQUESTS_CA_BUNDLE`, `$CURL_CA_BUNDLE` or `$WEBSOCKET_CLIENT_CA_BUNDLE`
  (first one set) does the same.
- `TrueNASClient(..., known_hosts=...)` — the host-key policy for the SSH leg
  built from `shell=` or by `install_sshcreds()`: `()` (default) checks
  `~/.ssh/known_hosts`, `None` skips the check, a path or list names the
  file(s). An explicit `ssh=SshConfig(...)` keeps its own setting.
- `run()` logs a warning, once per host, when it falls back from its first
  transport (e.g. SSH unreachable or its host key untrusted) to the next.

### Changed

- **The CLI verifies TLS certificates by default.** `pytruenas <cmd> ... nas`
  sent its credentials over a connection whose certificate it never checked
  (`sslverify` defaulted to `False`, the opposite of the library). Turn it off
  per run with `-k`/`--insecure` or `--no-sslverify`, or set `sslverify` in
  the config file or `$PYTRUENAS_SSLVERIFY` (`false`, or a CA bundle path).
  **A self-signed NAS now fails until one of those is given.**
- **The CLI takes credentials from `$TN_CREDS` or the config file** when the
  target string carries none — before, a remote target with no userinfo
  connected unauthenticated and every call failed with `ENOTAUTHENTICATED`.
  A config file may set `credentials:` to a connection string or a mapping.
- **The SFTP leg now verifies the server's host key**, as the SSH command leg
  already did. A NAS missing from `~/.ssh/known_hosts` is no longer silently
  trusted: add it (`ssh-keyscan nas >> ~/.ssh/known_hosts`) or pass
  `known_hosts=None`. Without either, `client.path()` operations are served by
  the websocket leg instead of SFTP.
- `env=` in `run()` now adds to the target's environment on a local target too,
  instead of replacing it (`env={"A": "1"}` keeps `PATH`).
- Dependencies: `hostctl>=0.3.1,<0.4`, `netimps>=0.3.0,<0.4`,
  `pathlib_next[uri]>=0.9.10,<0.10`, `requests>=2.0,<3`,
  `websocket-client>=1.0,<2`; the `ssh` extra is now `hostctl[ssh]>=0.3.1,<0.4`.

### Fixed

- **`--config` crashed on every use.** The field was typed `dict`, so it got
  duho's `KEY=VALUE` action and argparse raised before any command ran
  (`'WindowsPath' object is not iterable`).
- **`python -m pytruenas` always exited 0**, discarding `main()`'s exit code,
  so no shell or CI step could tell a failed run from a successful one.
- **`query -f` values were always strings**, so a filter on a numeric or
  boolean field silently matched nothing (`-f uid=0`). They are decoded as
  JSON with a string fallback, the same as `call -p`; a filter that is not
  `KEY=VALUE` is now an error instead of a filter on `""`.
- **`--logto` could not create its file on Windows**: both `{isodate}` and a
  `{target}` with a port carry colons. The substituted values are sanitized
  (the template's own separators are left alone).
- A command's `success` hook ran even when it returned a non-zero exit code.
- **Generated stubs made every property required.** A schema with no
  `required` list requires nothing (JSON Schema), so update payloads,
  query-options and `_get` filters all demanded every field. They also used
  `typing.NotRequired`/`Unpack`, which do not exist before 3.11 — the stubs now
  import them from `typing_extensions` below that — and the root module exports
  `Current`, so the documented `TrueNASClient[Current]` resolves.
- **`deploy`'s "already current" skip never fired.** Both payloads carried
  per-build timestamps (the tar from the files `export()` had just copied), so
  the digest changed on every build and every deploy re-uploaded everything.
  Archive entries now use a fixed timestamp and mode.
- **`packaging` is a declared dependency.** It was imported with a fallback
  that could not work — it fed a whole requirement line to
  `importlib.metadata.distribution()` — so without it `deploy` silently
  shipped a payload missing duho, hostctl and netimps.
- **Keyword credentials produced local-socket auth.** `Credentials(api_key=…)`,
  `(token=…)` and `(username=…, password=…)` all returned `LocalAuth`, so the
  client connected without authenticating and every call failed with
  `ENOTAUTHENTICATED`. The factory now dispatches on the keyword names;
  an unknown name still raises (with the values masked).
- `upload()` never checked the HTTP status: a refused upload surfaced as a
  `KeyError` naming neither the status nor the reason. It raises for the
  status, and a response with no job id raises `ClientException` quoting it.
- **A retry could run a call twice.** After a dropped connection, the default
  one retry replayed the request — including `create`, `delete` and job
  starts — even when it had already been sent and the server may have run it.
  Only a call that never reached the socket is repeated now; the rest raise
  `ConnectionClosed` with `sent=True`. The retry also closes the connection it
  drops instead of leaking its socket and reader thread.
- **One malformed message wedged the connection.** A notification whose
  `params` was not a dict killed the reader thread outside its cleanup, so the
  connection was never marked closed, never reconnected, and every later call
  waited out its timeout (measured). The reader now logs and drops such a
  message, and always runs its cleanup.
- **A connection the server closed kept its socket.** `close()` returned early
  once the reader had noticed, leaking the file descriptor for the life of the
  process; the socket is now shut down in both paths, once.
- Opening a connection had no timeout, so an unresponsive host blocked the
  caller indefinitely (`connect_timeout`, default 30 s, on
  `TrueNASWSConnection`). The reader is unaffected: an idle connection stays
  open.
- A call registered just as the reader failed the outstanding calls could wait
  forever (with `timeout=None`); the check and registration are now atomic.
- A parameter JSON cannot encode raised `ClientException(ECONNABORTED)` —
  reported as a dropped connection, and so retried on a new one — instead of
  `TypeError`.
- A blocking call made from a subscription callback deadlocked the reader
  until the call timed out; it now raises `RuntimeError` naming the fix.
- **A wrong password or API key logged in "successfully".** The legacy
  `auth.login`/`login_with_api_key`/`login_with_token` answer a refusal with
  `False` (measured on 26.0), which was ignored: every later call failed with
  `ENOTAUTHENTICATED` far from the cause. `login()` — and so the first call
  under `autologin` — now raises `AuthenticationError` and closes the
  connection.
- **A reconnect did not log in the way the session had.** After a dropped
  connection, `conn` used the config's credentials under `autologin`, or none
  at all without it, so a session opened with `login(other_creds)` or
  `login_ex=True` came back as someone else or unauthenticated. It now
  repeats the last successful `login()` call.
- Concurrent first use of a client opened one connection per thread and
  leaked all but one; opening the connection is now locked.
- **Secrets reached logs and messages.** The per-call TRACE record printed raw
  arguments, so `auth.login` passwords, API keys and the private key
  `install_sshcreds()` uploads were written to any log at TRACE; arguments to
  `auth.*` are now reduced to type names and secret-looking dict keys masked
  at any depth (and nothing is formatted unless TRACE is on). `redact()` —
  behind the CLI's per-target label and `--logto` file name — returned a
  scheme-less `root:pw@nas` whole. A `Credentials(...)` error masked only a
  fixed list of names (not `otp_token`, `private_key`); every value but the
  user name is masked now.
- **A connection string that does not parse as a URI is refused**, with a
  message that does not quote the credentials it just rejected (an unencoded
  `/`, `?` or `#` in a password ends the authority early, so `user:secret` is
  read as host:port). A URI that *does* parse is taken at face value: an `@`
  in a path is a path, and nothing can distinguish it from a password someone
  forgot to encode — the same contract hostctl states for `ConnectionString`
  and `redact_uri`.
- **The TLS legs trusted different certificates.** The API websocket verified
  against the OS trust store and the HTTP side channels (upload, download, file
  reads over the websocket leg) against `requests`' certifi bundle, so a
  certificate trusted by the OS — a private CA — connected the API and failed
  every download with `SSLError` (measured). All legs now share one context:
  the OS store, or the CA bundle above; certifi is no longer consulted.
- A non-default API port (`wss://nas:8443`) was dropped for every HTTP side
  channel — uploads, downloads, file reads over the websocket leg and the web
  shell went to port 443, with their auth tokens. On the NAS itself those URLs
  had no host at all; they now use middlewared's `http://127.0.0.1:6000`.
- An IPv6 literal target (`https://[fe80::1]:8443`) failed on first connect; a
  custom unix socket path (`unix:///run/x.sock`) was ignored in favour of the
  default socket.
- **Every `wait=True` returned before the job finished.** `core.job_wait` is
  itself a job, so calling it returned a new job id at once (0.4 s, measured on
  26.0.0-BETA.1); `upload()`, `download(buffered=True)` and the
  `_create`/`_update`/`_upsert` helpers therefore returned early, a failed job
  went unreported, and a helper whose call ran as a job returned the waiter's
  job id instead of the record. They now wait on the job's state.
- **Web shell (`run()` without SSH) rewritten; measured against TrueNAS
  26.0.0-BETA.1's zsh before and after.**
  - A captured `stdout` contained the terminal's echo of the wrapped command and
    the completion marker (`run("echo hi")` returned 242 bytes); output with no
    trailing newline was dropped; the first command on a new session could
    capture the login banner. Captured output is now exactly the program's
    bytes.
  - A `^C` inside `input=` ended the here-document and ran the rest of the
    payload as a root command, and `stdin=` bytes the program did not read were
    executed by the shell. The command and its input are now sent
    base64-encoded and input is delivered through a temporary file; nothing
    typed is interpreted by the terminal.
  - `input=` combined with the default stderr capture never ended and hung until
    the timeout; stderr lines could be lost under bash or leak into the next
    command.
  - Output handling was quadratic: 64 KiB took over 240 s. 1 MiB now takes about
    2–5 s.
  - `timeout=None` meant 120 s; it now waits indefinitely. A timeout raised
    `SubprocessError` or took up to twice as long; it now interrupts the command
    and raises `TimeoutExpired` (with `orphaned`) on time.
  - `stderr=` sent to a file while stdout was captured was dropped, and
    `capture_output="stderr"` wrote stderr into the stdout target.
  - `CompletedProcess.args` and `CalledProcessError` carried the `input=`
    payload; they now carry the command only.
  - `bytearray`/`memoryview` input arrived as its `repr`.
  - Opening the session had no timeout.

### Changed

- Web shell: `stdin=` is read to EOF and delivered like `input=` instead of
  being pumped into the terminal while the command runs; with no input, stdin
  is `/dev/null` (a prompting command gets EOF instead of hanging), and
  `stdin=subprocess.DEVNULL` is accepted. stderr is captured in any POSIX login
  shell (no longer only bash/zsh/ksh) but a separate stderr target receives it
  when the command finishes; `stderr=subprocess.STDOUT` merges live.

### Fixed (continued)

- `patch` `FileTarget(baseline=True)`: the snapshot of an existing file was
  created with the default mode, so a copy of a `0640` `/etc/shadow` sat beside
  it at `0644`; `revert()` of a deleted target recreated it at `0644` too. Both
  now keep the original's mode, and a new file written with `mode=` is chmod'ed
  before its content is written rather than after.
- `patch` `FileTarget(baseline=True)` on a file that did not exist yet: the
  second write snapshotted the target's own first output as the "original", so
  a layering template duplicated its additions on every apply and `revert()`
  restored patched content. The first write now records that the original was
  absent (a `.absent` marker); `read()` then raises `FileNotFoundError` for
  that file, as it did before the first write.
- `TruenasPath.rename()` ignored the destination's host:
  `fs.path(nasA, x).move(fs.path(nasB, y))` renamed the file on nasA under `y`
  and reported success, and with `overwrite=True` also deleted nasB's copy.
  `rename()` now refuses a destination on another host, so `move()` copies and
  deletes. `rename()` returns the new `TruenasPath` (it returned the SFTP
  leg's own path object).
- Moving or copying a remote file onto a separately built path for the same
  file (`fs.path(c, x).move(fs.path(c, x), overwrite=True)`) deleted it; a
  recursive copy into its own subtree recursed until `RecursionError`. Such
  paths are now recognised as the same file.
- `mkdir()` on the websocket leg created world-writable (`0o777`) directories,
  because the middleware applies the requested mode without a umask; the
  default is now `0o755`. `mkdir(parents=True)` failed with `ClientException
  [Errno 2]` instead of creating the parents: a middleware error of the form
  `[Errno N] ...` is now mapped to the matching `OSError` subclass.
- `deploy --mode dir` replaced whatever directory `--path` named: an existing
  directory that was not a previous deploy was moved aside and deleted, and
  the run reported "Deployed". A `--path` without a previous deploy's digest
  marker is now refused (`FileExistsError`) in both modes, `--force` included.
- A `dir` deploy interrupted between its two renames left the last good tree
  only at `<path>.old`, which the next deploy deleted first. It is now restored.
- `deploy --mode pyz` overwrote the live zipapp in place; it is now written
  beside it and renamed over it. A `--path` with a trailing slash no longer
  stages inside the target.
- `generate-typings` (`Codegen().generate()`) deleted the whole `--path`
  directory before rendering — including a `.git` or any other files — and a
  render error or a missing `jinja2` then left it empty. It now renders into a
  temporary directory and swaps it in on success, and refuses a directory that
  holds anything but stubs (`FileExistsError`). A missing `jinja2` raises an
  `ImportError` naming `pytruenas[codegen]`.
- `_upsert()`/`_update()` with a selector made only of `!`-prefixed names
  (`("!uid",)`) queried the whole collection and updated its first record
  (`_upsert(("!uid",), username="bob", uid=1001)` renamed root). It now raises
  `ValueError`.
- `_update()`/`_upsert()` silently dropped any field set to `None`, so a
  nullable field could not be cleared (`_update(2, email=None)` sent nothing).
- The README and guide `_upsert("username", ...)` example passed the field name
  as a bare string, which is read as a record id and raises; the examples now
  use `("username",)`.
- With SSH unreachable or its host key untrusted, `client.path()` operations
  raised the connection error instead of falling back to the websocket leg, and
  every `run()` re-dialled SSH before falling back (~9 s per call).
- `copy()`/`move()` between two NAS hosts were refused as "Source and target are
  the same file" when the same path existed on both (the dependency set 0.4.6
  resolved to on a fresh install).
- A `rename()`/`symlink_to()` destination containing `?`, `#` or `%` landed on a
  truncated or re-decoded name (`rn?b.txt` → `rn`) on the SFTP leg.
- `p / "name"` read the name as URI syntax, so `p / "cache?v=2"` named `cache`,
  and a recursive `rm()` could delete the wrong file for such names.

## Earlier releases

0.0.0 to 0.4.6 are in [CHANGELOG-0.x.md](https://github.com/jose-pr/pytruenas/blob/main/CHANGELOG-0.x.md).

[Unreleased]: https://github.com/jose-pr/pytruenas/compare/v0.7.0...HEAD
[0.7.0]: https://github.com/jose-pr/pytruenas/compare/v0.6.1...v0.7.0
[0.6.1]: https://github.com/jose-pr/pytruenas/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/jose-pr/pytruenas/compare/v0.5.4...v0.6.0
[0.5.4]: https://github.com/jose-pr/pytruenas/compare/v0.5.3...v0.5.4
[0.5.3]: https://github.com/jose-pr/pytruenas/compare/v0.5.2...v0.5.3
[0.5.2]: https://github.com/jose-pr/pytruenas/compare/v0.5.1...v0.5.2
[0.5.1]: https://github.com/jose-pr/pytruenas/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/jose-pr/pytruenas/compare/v0.4.6...v0.5.0
[hostctl]: https://github.com/jose-pr/hostctl
