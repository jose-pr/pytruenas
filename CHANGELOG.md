# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
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

[Unreleased]: https://github.com/jose-pr/pytruenas/compare/v0.0.0...HEAD
[0.0.0]: https://github.com/jose-pr/pytruenas/releases/tag/v0.0.0
