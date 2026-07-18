# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
