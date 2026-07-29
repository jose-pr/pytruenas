# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-07-29

Run pytruenas *on* the appliance, and patch things the API does not expose.

`pytruenas.ops` is now `pytruenas.patch`, restructured into subpackages, with
`ops.host` and `ops.main` removed (see "Removed"). Renaming it is why this is
0.3.0 rather than 0.2.3 — though in practice there was nothing to break: the
subpackage was experimental, unexercised, and most of its paths simply did not
work. `MiddlewareFiles` referenced an attribute that never existed, `systemctl`
calls ran four commands instead of one, and creating a file with a baseline
raised. Those are all fixed below; the rename is the part worth noticing.

### Added

- **`pytruenas deploy <target>`** — installs pytruenas onto a host that cannot
  install for itself. TrueNAS has a read-only root and no `pip`, so this probes
  what the target already has, bundles only the difference, and copies that
  over. In practice five pure-Python packages under a megabyte: the appliance
  already ships `requests`, `websocket-client`, `pyyaml`, `asyncssh` and
  `jinja2`, and *which* it ships varies by release, so it is asked rather than
  assumed.
  - `--mode pyz` (default) writes one executable zipapp; `--mode dir` an
    unpacked `bin/` + `lib/` tree, swapped into place via a staging directory
    so an interrupted transfer never leaves a half-written tree.
  - Everything after `--` runs on the target once installed:
    `pytruenas deploy nas1 -- call system.info`.
  - Defaults to `/var/db/system`, which is a dataset on a *data* pool and
    survives an update — unlike `/var/db` itself, `/root` or `/data`, which
    live in the boot environment and are replaced by one. Verified on a live
    appliance rather than assumed.
  - A digest is recorded beside the payload, so a redeploy verifies instead of
    re-copying; `--force` overrides.
  - `--pkg-root`/`--pkg-name` (or `PYTRUENAS_PKG_ROOT`/`PYTRUENAS_PKG_NAME`)
    deploy *your* distribution with pytruenas bundled underneath, for when
    pytruenas is a dependency rather than the deliverable.
- **`pytruenas.utils.bundle`** — the machinery behind it, deliberately generic:
  it knows nothing about pytruenas or TrueNAS and could be lifted out. Resolves
  a transitive closure from installed *distribution metadata* (not an import
  scan — `import yaml` does not name `pyyaml`), and refuses a distribution
  carrying a compiled extension or resolving to data files only, both of which
  would build cleanly and fail to import on the target.
- **`pytruenas.patch.zfs`** — `writable(client, path)` clears `readonly` on the
  backing dataset and restores it **however the block exits**. Required for
  anything under `/usr`. `dataset_for` walks up to an existing ancestor,
  because `findmnt --target` fails on a path that does not exist yet.
- **Undo, for the patch system that promised it.** `FileTarget.revert()`
  restores the baseline and clears the snapshot; `is_patched()` reports whether
  a file currently differs from its baseline; `would_change(content)` is the
  dry run. A file the patch *created* is deliberately left alone — with no
  baseline there is nothing proving it was ours to delete.
- **`SystemFile(..., writable=True, mode=...)`** — patch a read-only mount
  without remembering the ZFS dance, and set the mode for a file the patch
  creates.

### Fixed

- **A rewrite no longer widens a file's permissions.** Rewriting reset the mode
  to whatever the umask gave, so patching `/etc/shadow` (`0640 root:shadow` on
  a real box) would silently have made it `0644`. The existing mode is now
  captured before the write and restored after.
- **`systemctl` was invoked as four separate commands.** `run(*cmds)` treats
  each positional as its own command, so `run("systemctl", "disable", "--now",
  name)` ran four — with the unit name hand-quoted on top, which argv does not
  want. Every call now builds one argv list.
- **`is-active`/`is-enabled` could raise on the non-zero exit that *is* their
  answer**, so asking "is this running?" about a stopped service threw.
- **`services="nfs"` iterated into three per-character reloads.**
- **`mkdir(755, ...)` passed decimal 755** — `0o1363`, setuid plus wrong bits —
  on every directory it created.
- **`baseline=True` on a file that does not exist yet raised
  `FileNotFoundError`** from inside `write()`: it tried to snapshot a missing
  original. That is the ordinary "create this config if absent" case.
- **`baseline()` called `resolve()`**, which hostctl's `CompositePosixPath` does
  not have, so any baseline against a real client path crashed.
- **`BaseTemplate.render` returned `None`** for a subclass that forgot to
  override it, and that `None` flowed into `write()` as the file's content. It
  now raises, and `write()` refuses `None` outright.
- **`MiddlewareFiles` used a `client.middlewared_path` that never existed.**
  Replaced with a lazy lookup that asks the host's own interpreter — no API
  method reports it (checked against 26.0's 781 methods).
- **`find_template` defaulted to taking a baseline** beside a template on a
  **read-only mount**, which cannot work; it failed with a bare `OSError` on
  first read.
- **`apply_template(**kwargs)`** raised `TypeError` for an already-built
  template and silently dropped the kwargs elsewhere.

### Changed

- **`PYTRUENAS_*` settings are read through one `duho.env` accessor.** The app
  had grown three names for two settings (`PYTRUENAS_CFG`, `PYTRUENAS_CONFIG`,
  `PYTRUENAS_PATH`); `PYTRUENAS_CONFIG` is now canonical with `CFG` still
  accepted, and the set is enumerable rather than grep-discoverable.
- **`pytruenas.ops` → `pytruenas.patch`**, split into `templates/`, `systemd/`,
  `middleware.py`, `zfs.py`. The old name described neither what the code does
  nor what it costs: it modifies a host beyond what the middleware API
  supports, which is unsupported by definition and discarded by a boot
  environment swap on update.
  - `ops.midclt` → `patch.systemd` (`midclt` is TrueNAS's own CLI binary, which
    nothing in the module invokes). `TruenasSystemFile` → `SystemFile`,
    `SystemdUnit` → `Unit`, `SystemdServiceUnit` → `ServiceUnit`,
    `MiddlewareCode` → `MiddlewareFiles`.
  - Unit `enable`/`start` are now three-valued: `None` means "not mine to
    manage", which a bool could not express.

### Removed

- **`pytruenas.ops.host`** — its packaging half became
  `patch.templates`/`utils.bundle`; the remaining network helpers
  (`is_localhost`, `is_local_ip`, `find_adapter_in_network`) were thin wrappers
  over `netimps` and `ipaddress` that nothing in the package imported. Call
  `netimps.interface_for`/`get_interfaces` and `ipaddress` directly.
- **`pytruenas.ops.main.init`** — imported by nothing, duplicated the CLI's own
  config loading, and documented a `pytruenas.client` module deleted in 0.2.0.
  Now `examples/simple_client_from_yaml.py`, as a worked example.

### Dependencies

- **`hostctl>=0.1.2`** — for `uri_hostname()`, which returns a URI's host as
  written rather than case-folded.

## [0.2.2] - 2026-07-28

Log records now identify the host they came from, and no longer carry the
connection string that used to be the only identification.

Released as a patch: the public surface only gains (`client.name`,
`config.name`, `TrueNASWSConnection(logger=...)`). The one output change is to
`pytruenas.utils.target`'s `redact`/`Target.redacted`, an internal utility
module — not exported from the package root, not in the docs, and reached only
by explicit deep import.

### Changed

- **Log records identify the host by name, not by connection string.** Every
  record carried the full URI — scheme, port, API path and any userinfo — which
  was unreadable at fan-out width and put the password on every line. Records
  are now prefixed with the machine's short name (`[nas1]`, `[nas1:8443]`,
  `localhost` for the unix socket), available as `client.name` /
  `config.name`. Because the prefix always names the target, the per-target
  `Started:`/`Finished:` messages no longer repeat it.
- **Attribution no longer depends on the CLI.** `client.logger` is now bound to
  the host's name, so a *library* caller with several clients open gets
  attributed records with no fan-out involved — previously only the CLI's
  `duho.fanout` added a prefix, and a bare "Websocket connection was closed"
  did not say which host closed. `TrueNASWSConnection` accepts `logger=` and
  the host passes its own, so transport-layer records are attributed too.
- **Redaction removes the password instead of masking it.**
  `pytruenas.utils.target.redact` and `Target.redacted` rendered
  `wss://root:***@nas`; they now render `wss://root@nas`. A `***` placeholder
  is not a real password and would reparse into a *wrong* credential if the
  rendered form were ever fed back in, whereas what comes out now is a valid,
  reusable URI. `redact` delegates to `hostctl.host.redact_uri`, so pytruenas
  and hostctl render a target identically. Note this is only for rendering a
  *raw* connection string: credentials are extracted at parse time, so
  `config.connection_uri` was already credential-free.
- **`--logto` filenames use the short name.** `{target}` now expands to `nas1`
  rather than a full URI, which is both credential-free and a legal filename —
  a URI is neither.

### Fixed

- **A hostname's typed casing is preserved in its label.** `urlsplit` folds
  case, so a fan-out over `nasA`/`nasB` logged `[nasa]`/`[nasb]`. Correct for
  resolution, wrong for a label an operator greps for.
- **The same host renders the same way with or without a password.** A target
  whose URI carried a credential logged as `[nasa]` while the identical host
  without one logged as `[nasA]`, because hostctl rebuilt the authority from
  the case-folded hostname when stripping the password. Filed upstream and
  fixed across hostctl 0.1.1/0.1.2.

### Dependencies

- **`hostctl>=0.1.2`** (was `>=0.1.0`) — for `uri_hostname()`, which returns a
  URI's host as written instead of as `urlsplit` case-folded it.
  `TrueNASConfig` stores that, since the value is rendered back out through
  `name` and `connection_uri`. Both hostctl releases came from a finding filed
  from this repo. **Note the trade-off inherited with it:** `config.host` is
  now the spelling the caller typed rather than a canonical one, so two
  spellings of one machine are not equal configs — casefold explicitly if you
  key on a host. Routing is unaffected.

## [0.2.1] - 2026-07-27

Documentation and one error-message fix. No API changes.

### Fixed

- **An unknown constructor argument now raises a useful error.** A typo like
  `TrueNASClient("wss://nas", passwrd="s3cret")` fell through to hostctl's
  `SystemHost.__init__` and raised `TypeError: SystemHost.__init__() got an
  unexpected keyword argument 'passwrd'` — accurate, but naming an internal
  class rather than the thing the caller got wrong. It now raises
  `ValueError: unknown credential argument: 'passwrd'` and lists the accepted
  configuration options. Found by testing the documented examples.

### Documentation

- **README** rewritten for 0.2.0: it still advertised a `pytruenas[host]` extra
  that no longer exists, said "once published to PyPI", and used a venv layout
  the project no longer follows. Adds the transport table and a
  commands/files section.
- **New [Recipes](https://jose-pr.github.io/pytruenas/guide/recipes/) guide** —
  worked examples for connecting, querying, idempotent upserts, subscriptions,
  running commands, upload/download, several hosts at once, and provisioning
  SSH. Every example was run against a live TrueNAS 26.0.0-BETA.1 host.
- **Filesystem guide** expanded with real path examples and a table of which
  operations need SFTP (`rename`, `symlink_to`, `readlink`, `resolve` have no
  `filesystem.*` equivalent and raise rather than failing quietly).
- `docs/index.md` extras list corrected; both CI workflows dropped a stale
  `host` extra that pip had been silently warning about.

## [0.2.0] - 2026-07-27

Rebases pytruenas' generic host machinery onto [hostctl], keeping only the
TrueNAS-specific parts here: the middleware websocket, the `api` namespace,
login/2FA, subscriptions, and the upload/download side channels. Everything
else — shell quoting, transport selection, the asyncssh lifecycle, path
backends — is now inherited.

**Requires `hostctl>=0.1.0,<0.2`.**

### Changed

- **BREAKING: `TrueNASClient.shell` is gone.** `.shell` now means what it means
  throughout hostctl — the *bound shell object* (`client.shell.run(...)`). The
  SSH connection target lives on the configuration as `client.config.ssh`, an
  `SshConfig`. The constructor argument is still spelled `shell=` and still
  takes a connection string (`shell="ssh://root@nas"`).
- **`.run()` and `.path()` now select a transport rather than branching.**
  Which one serves a call is chosen from the available providers, and
  `.last_selection` records what was tried and why — with credentials redacted.
  Previously `.run()` hard-coded a local-vs-SSH branch and `TruenasPath`
  hand-rolled its own SFTP→websocket fallback.
- **A remote target with no SSH can now run commands over the web shell.** The
  TrueNAS JSON-RPC API exposes no remote command execution (verified against
  26.0.0-BETA.1: of 781 methods only `core.resize_shell` and
  `user.shell_choices` are shell-adjacent, and the former only resizes an
  already-open session) — so such a host previously had no `run()` at all.
  `/websocket/shell`, the PTY the web UI's Shell page drives, is a real command
  channel on the same port. Pass `executor=["ssh"]` to require SSH instead.
- **The scheme/API-path probe moved from construction to first connect.**
  `TrueNASClient("bad-host")` now constructs successfully and raises on first
  use. Configs are therefore buildable offline, which is what `HostConfig`
  requires.

### Added

- **`pytruenas.host`** — `TrueNASConfig` (a `hostctl.host.HostConfig`) and
  `TrueNASHost` (a `PosixHost`). `HostConfig("truenas+wss://nas")` resolves
  through hostctl's registry; every connection string `TrueNASClient` accepts
  still works, normalized to a `truenas+*` scheme.
- **`TrueNASClient` and `TrueNASHost` are now one class.** They were briefly
  two objects that forwarded halves of their surface to each other —
  `client.run()` called `client.host.run()` while `host.api` called
  `host.client.api`, each holding a reference to the other. `TrueNASClient` is
  an alias for `TrueNASHost`, so every existing import and call keeps working,
  and `client.host` / `host.client` both return the object itself.
  `TrueNASHost("wss://nas")` also takes a connection string directly, with the
  same options as `TrueNASConfig.from_target`.
- **`pytruenas.providers`** — `TnasWsPathProvider` (the `filesystem.*`
  websocket leg) and `local_providers()`, which returns hostctl's stock local
  executor and path providers unchanged. A local target runs plain
  `subprocess` and uses plain local paths; there is nothing TrueNAS-specific to
  add, so pytruenas defines no provider class for it.
- **`pytruenas.webshell`** — `WebShellExecutorProvider`, command execution over
  `/websocket/shell`. Ordered after SSH; declares its limits rather than hiding
  them (stdout and stderr are one stream, no piped input, single-line commands
  only — pipes and here-strings work, being ordinary shell syntax).
- **`executor=` / `path=` on `TrueNASConfig`** — name the providers to use, in
  preference order, as a single name or a sequence: `executor=["ssh"]`,
  `path=["local", "tnasws"]`, `executor=[]` for no command channel at all.
  Unknown names, and `ssh`/`sftp` without an `SshConfig`, raise rather than
  composing a host that would fail later. Matches hostctl's own
  `SystemConfig(executor=..., path=...)` spelling.
- **`Credentials.from_host_credentials()`** — maps hostctl's already-parsed
  credential mapping (including a URI-supplied OTP) onto a `Credentials`
  subclass, with no second round of string parsing.
- **Inherited from hostctl**: `.capabilities` (so a host that genuinely cannot
  run commands says so up front rather than failing mid-call),
  `.last_selection`, `.info()`, `.spawn()`, `.connect()`/`.close()`, and
  context-manager support.
- `black` in the `dev` extra, pinned to the 3.9 floor.

### Removed

- **BREAKING: `pytruenas.jsonrpc` is now `pytruenas.connection`**, and its
  `Client` class is `TrueNASWSConnection`. `Client` was doubly wrong: the class
  is not generic JSON-RPC (it knows `core.subscribe`, TrueNAS error codes, and
  the middleware unix socket), and the name collided with `TrueNASClient`.
  `client.conn` is the connection, with `.websocket` kept as an alias.
- **BREAKING: `pytruenas.client` and `pytruenas._conn` are gone.**
  `from pytruenas import TrueNASClient` is unaffected. `_conn` was a re-export
  shim for swapping the client implementation, which never happened; `client`
  had been reduced to an alias by the host/client merge.
- ~190 lines of generic host machinery: shell quoting, the local-vs-SSH branch
  in `run()`, the asyncssh connection, and `_shellquote`.

### Known limitations

- **A local unix-socket client cannot use `download()`.** The HTTP side channel
  resolves to `https://localhost` and trips the appliance's self-signed
  certificate. This is pre-existing and unrelated to the migration — the URL
  construction is byte-identical to 0.1.1.
- **The web shell merges stdout and stderr** (a PTY is one stream), takes no
  piped `input=`, and requires single-line commands. Pipes and here-strings
  work, being ordinary shell syntax. It is ordered after SSH for these reasons.

[hostctl]: https://github.com/jose-pr/hostctl

## [0.1.1] - 2026-07-24

### Changed
- **`call`/`query`/`generate-typings` declare fewer field options.** Their
  `Args` classes no longer pass `NS(type=...)` for a plain `str`/`Path` field
  (duho already derives `type=` from the annotation) or `NS(action='append',
  nargs=...)` for a `list[str]` option (duho >=0.5.0 already defaults a
  list-typed option to `action="append"`, `nargs=None` — one value per
  occurrence). Only `NS(metavar=...)` remains where the display name isn't
  inferable. No CLI-surface change.
- **An option placed between a command's own positional and the trailing
  targets now parses**, e.g. `pytruenas call method -p '{"a":1}' nas1` — no
  longer only before the first positional or after the last. Was argparse's
  own greedy positional-run matching (bpo-15112); fixed by duho >=0.5.1's
  flag-between-positionals reorder, extended in 0.5.1 to a module command's
  subparser (this project's entire command set — 0.5.0 alone only covered
  duho's own declarative subcommand tree).
- **Dependency floor `duho>=0.4.1` → `duho>=0.5.1`**, required for both
  changes above.

## [0.1.0] - 2026-07-24

First published release with real content. `0.0.0` was a placeholder; everything
below accumulated since and is new to PyPI.

### Added
- **Modern `auth.login_ex` login with 2FA.** `client.login(login_ex=True)` uses
  the middleware's `auth.login_ex` mechanism (`PASSWORD_PLAIN`/`API_KEY_PLAIN`/
  `TOKEN_PLAIN`) instead of the legacy `auth.login`/`login_with_*`. It handles an
  `OTP_REQUIRED` challenge by continuing with `auth.login_ex_continue` — the OTP
  comes from the credential's `otp_token` or an `otp_provider` callback — and
  raises `auth.AuthenticationError` on `AUTH_ERR`/`DENIED`/etc. `login_options`
  overrides the server defaults. The legacy path remains the default and
  unchanged; a credential with no login_ex form (local-socket auth) falls back
  automatically. Validated live against TrueNAS 26.0.
- **Client convenience wrappers** `client.me()` (`auth.me`), `client.logout()`
  (`auth.logout`), and `client.ping()` (`core.ping`).
- **Event subscriptions.** Subscribe to middleware collection events over the
  existing websocket: `client.subscribe("alert.list")` (or
  `client.api.alert.list.subscribe()`) returns a `Subscription`. Consume events
  by iterating `sub.events(timeout=...)` — a bounded queue drained on the
  caller's thread, so backpressure is visible; a full queue drops the oldest
  event and counts it in `sub.dropped` rather than blocking. An optional
  `callback` is invoked inline on the reader thread (keep it fast; a raising
  callback is logged and contained). Each event is an `Event(collection, msg,
  fields, id)`. Close with `sub.unsubscribe()` or a `with` block; closing the
  client ends every `events()` iterator cleanly. A subscription is bound to the
  current connection and does **not** survive a reconnect — the `events()`
  iterator ending is the signal to re-subscribe. Validated live against
  TrueNAS 26.0.
- **RunPath step directories.** Adopt `duho.runpath` (requires `duho>=0.4.0`),
  wired into the per-target fan-out: a directory of numbered `NN-name.py` steps
  (no `__init__.py`), placed among the command sources (`PYTRUENAS_PATH` /
  `--cmdspath` / config `commandspath`, or nested one level inside a source
  directory), becomes a subcommand that runs the whole step sequence **once per
  target**, each target getting its own connected `TrueNASClient` — restoring
  the private predecessor's per-target `RunPathCmd` behavior the current
  duho-based `pytruenas` never had. A directory's optional `__main__.py`
  `init(cmd, logger)` builds the per-target client (reuse
  `pytruenas.utils.runpath.default_init`); steps are `main(cmd, ctx)` /
  `main(cmd)`; `-O/--rcopts` and filename `!`/`!strict`/`!enable` tokens select
  steps. The step signature is `duho`'s native `main(cmd, ctx)` rather than the
  predecessor's `run(client, args, logger)` (the logger travels on `cmd`, the
  client is `ctx`) — capability parity, not signature parity. The
  filename-modifier / `--rcopts` grammar follows the predecessor's intent with
  two of its original bugs fixed (the `:!enable`/`.enabled` attribute mismatch,
  and the `Extend()` nested-list double-collection), not reproduced.

### Changed
- **Local network-adapter discovery uses `netimps` instead of `ifaddr`.**
  `pytruenas.ops.host.is_local_ip` / `find_adapter_in_network` now delegate to
  `netimps` (a core dependency), so the optional **`host` extra is removed** —
  those helpers work out of the box, no `pip install pytruenas[host]` needed.
  `find_adapter_in_network` now returns a `netimps.Interface` (was an `ifaddr`
  adapter). Requires `netimps>=0.0.2`, which also supplies the `ws`/`wss` default
  ports built-in, so `utils/target.py` no longer registers them at import.
- **The trailing `TARGET...` positionals are registered centrally.** Every
  command's `register` hook previously had to call
  `pytruenas.utils.cmd.register_targets(parser)` **last** or silently lose the
  target grammar. `pytruenas.main` now wraps each command's hook and adds the
  positional after it, so targets stay trailing whatever positionals a command
  adds — including for a command with no `register` hook at all, and for
  third-party commands supplied via `--cmdspath`/`PYTRUENAS_PATH`, which now get
  the `<command> [args...] [TARGET ...]` grammar for free.
- **Commands declare their CLI fields via an `Args` class.** `call`, `query` and
  `generate-typings` declare arguments on their `Args` class rather than adding
  them imperatively in `register()` (which they no longer define). Previously the
  `Args` class was inert — duho ignored it, `register()` did the real work, and
  the two were hand-synced. `register()` remains supported as the escape hatch
  for what declarations can't express. The CLI surface is unchanged.
- **Dependency floor `duho>=0.4.0` → `duho>=0.4.1`** for the two behaviors the
  above depends on: a module command may declare its own `Args` class (added to
  the subparser before `register` runs), and the `register` hook is gated and
  introspected on the object actually called, so wrapping it app-wide works even
  for a command that defines no hook of its own.
- **Dependency floor `duho>=0.3.2` → `duho>=0.4.0`.** 0.4.0 carries the RunPath
  `register(base=...)` shared-root method inheritance, the `__main__.py`
  lifecycle, the corrected `enable`/`!enable` token spelling, and the `Extend()`
  nested-list fix that now flattens `--cmdspath a:b` to `['a', 'b']` (previously
  silently mis-collected as `[['a', 'b']]` for multi-value input).

### Security
- **Passwords in a target connection string are redacted from logs.** A target
  like `wss://root:secret@nas` passed as a positional was logged verbatim
  (`Started: …`/`Finished: …`, at INFO) and, worse, embedded in the `--logto`
  filename on disk. The password is now masked (`wss://root:***@nas`) at every
  such point via `pytruenas.utils.target.redact` — the username is kept, the
  real target still builds the client. The `auth.Credentials` "not supported"
  `ValueError` no longer carries the raw `password`/`token`/`api_key` kwargs
  (which an `exc_info=True` log would have surfaced). Command text logged by
  `client.run` is unchanged: that logging is intentional, opt-in via `loglevel`
  (default `TRACE`, off unless enabled), and suppressible with `loglevel=0`.

### Fixed
- **Connection-string reassembly preserves reserved characters.** `Target.uri`
  now percent-encodes userinfo and path, so a credential or path containing
  `@ : / #` round-trips instead of reassembling into a URL that reparses to a
  different host/port/path.
- **`ops` reads files as UTF-8**, and narrower exception handling in `auth`
  (`ValueError`/`TypeError` rather than bare `except Exception`) so a genuine
  error surfaces instead of being swallowed behind a generic message.

## [0.0.0] - 2026-07-22

Initial release.

Earlier version numbers appear in this project's git history but were never
tagged or published, so there is no upgrade path to describe -- everything
below is simply what the package contains.

### Fixed
- **`ws://` and `wss://` URLs no longer parse as port 0.** No system services
  database has an entry for the websocket schemes, so `getservbyname("wss")`
  failed -- and those are the schemes this client uses most. Port resolution now
  goes through `netimps`, whose scheme table is consulted before the system
  database.

### Added
- **`pytruenas call <method>` command.** Invoke any middleware method by its
  dotted name (`system.info`, `core.ping`, `pool.dataset.details`) — not just
  the queryable `<namespace>.query` methods `query` covers. Parameters are JSON
  values via `-p/--param` (repeatable).

### Changed
- **CLI targets are now trailing positional arguments, not `-t/--target`.**
  A command's own positionals come first, then the target host(s):
  `pytruenas query user nas1 nas2`, `pytruenas dump-api nas1,nas2`. Comma lists
  and `[A-Z]`/`[0-9]` range patterns still expand; no target means `localhost`.
  The `-t`/`--target` flag has been removed.

- Dependency floors raised to the validated versions: `duho>=0.3.2` (CLI parser
  fixes — a global option before a subcommand is no longer shadowed; a literal
  `%` in a `Cmd` docstring no longer breaks parser build) and the `ssh` extra's
  `pathlib_next[sftp-async]>=0.8.3` (SFTP default concurrency raised 8→16).

### Fixed
- **API calls no longer silently return `None` on a dropped connection.** The
  namespace call retry loop fell through and returned `None` after a single
  `ECONNABORTED` — which `_get` read as "record missing", turning an `_upsert`
  into a spurious create (possible duplicate rows). It now retries then raises,
  and never returns `None` on a connection error.
- **Long-running jobs no longer spuriously time out.** `core.job_wait` (waited
  on after uploads/downloads and mutating `_upsert`/`_update` calls) is now
  issued with no client-side timeout, so a job lasting longer than the 60s
  default no longer raises `CallTimeout` while it is still running server-side.
  `Client.call(timeout=None)` now means "wait indefinitely".
- `client.run()` with a `str` `input` together with a text `encoding`/`errors`
  no longer crashes. It used to pre-encode the string to bytes *and* hand the
  encoding to `subprocess.run`, which then tried to `.encode()` the already-bytes
  input (`AttributeError`). Now text mode keeps `str` input as-is (and decodes
  `bytes` input), binary mode encodes. Found by live testing on TrueNAS 26.0.

- `ops.template.TemplateTarget.apply_template` no longer crashes on a plain
  string template (`issubclass()` was called on a non-type); a `str` is now
  treated as literal template content and a path-like is read as file content.
- `namespace.ioerror` only maps a middleware error to `OSError` when the
  bracketed prefix names a real POSIX errno; previously an unrecognised prefix
  produced `IOError(None, msg)`, discarding the original exception type.

### Internal
- `jsonrpc.Client.call` narrows the compatibility kwargs it ignores and logs any
  other unexpected keyword at debug level instead of silently swallowing it;
  `_ioerror` is no longer forwarded into the upload/download paths.
- `Namespace` child lookups use a per-instance dict instead of `functools.cache`
  on the methods, so namespaces are garbage-collected with their client instead
  of being pinned for the process lifetime (relevant to long-lived embeddings).
- The `pytruenas.ops` subpackage (systemd/midclt host-config helpers) is
  **experimental** and exercised only by unit tests, not against a live host.

### Added
- Packaged as `pytruenas` (src layout, hatchling, `pytruenas` console script,
  `py.typed`). Python 3.9+.
- Lean in-house JSON-RPC 2.0 client (`pytruenas.jsonrpc`) speaking the middleware
  protocol over `wss://`/`ws://` and the local `ws+unix://` socket, with
  extended-JSON (datetime/date/time/set/IP) round-tripping and
  `ClientException`/`ValidationErrors` mapping. Verified against a live host.
- Attribute-style API namespace (`client.api.<namespace>.<method>(...)`) with
  `_get`/`_query`/`_create`/`_update`/`_upsert` convenience helpers.
- Filesystem paths on `pathlib_next`: `client.path()` returns a `LocalPath`
  (local) or `TruenasPath` (remote — SFTP-preferred via pathlib_next's `SftpPath`,
  falling back to the middleware `filesystem.*` websocket API for
  delete/rename/symlink).
- Typings generator (`generate-typings`): produces `.pyi` stubs for the whole
  API, validated to parse across every version of a real v26 dump (780 methods).
- CLI (`dump-api`, `query`, `generate-typings`) on `duho` with multi-target
  fan-out (`-t/--target`, `--parallel`) and optional YAML config.
- Optional extras: `ssh`, `config`, `codegen`, `host`.
- Test suite green on Python 3.9 and 3.13/3.14.

### Notes
- Runtime CLI/logging/qualname/text come from `duho` (>=0.3.0); path types from
  `pathlib_next` (>=0.8.2). Both are on PyPI.
- Remote shell command execution (`client.run` over SSH) uses `asyncssh` (the
  `ssh` extra); the middleware API has no command-exec method. SFTP is handled by
  `pathlib_next`.

[Unreleased]: https://github.com/jose-pr/pytruenas/compare/v0.1.1...HEAD
[0.2.1]: https://github.com/jose-pr/pytruenas/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/jose-pr/pytruenas/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/jose-pr/pytruenas/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/jose-pr/pytruenas/compare/v0.0.0...v0.1.0
[0.0.0]: https://github.com/jose-pr/pytruenas/releases/tag/v0.0.0
