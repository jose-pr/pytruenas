# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

## [0.1.0] - 2026-07-18

First packaged release.

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

[Unreleased]: https://github.com/jose-pr/pytruenas/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/jose-pr/pytruenas/releases/tag/v0.1.0
