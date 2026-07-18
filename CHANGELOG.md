# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-17

First packaged release.

### Added
- Packaged as `pytruenas` (src layout, hatchling, `pytruenas` console script).
- Lean in-house JSON-RPC 2.0 client (`pytruenas.jsonrpc`) speaking the
  middleware protocol over `wss://`/`ws://` and the local `ws+unix://` socket,
  with extended-JSON (datetime/date/time/set/IP) round-tripping and
  `ClientException`/`ValidationErrors` mapping. Verified against a live host.
- Attribute-style API namespace with `_get`/`_query`/`_create`/`_update`/
  `_upsert` convenience helpers.
- Multi-backend remote filesystem `Path` (local / SFTP / TrueNAS filesystem API).
- Typings generator (`generate-typings`): produces `.pyi` stubs for the whole
  API, validated to parse across every version of a real dump.
- CLI (`dump-api`, `query`, `generate-typings`) with multi-target fan-out
  (`-t/--target`, `--parallel`) and optional YAML config.
- Optional extras: `ssh`, `config`, `codegen`, `host`.
- Test suite (auth, target, query, jsonrpc, codegen, fs) green on Python 3.9
  and 3.14.

### Changed
- Runtime CLI/logging/qualname/text now come from `duho`; path types align with
  `pathlib_next`.
- Python 3.9+ supported (was 3.10+-only in practice).

### Fixed
- Typings generator now emits valid Python for the full real API: sanitized
  namespace/class names (keywords, numeric version segments), escaped
  docstrings, correct default rendering, no `**kwargs` defaults, valid TypedDict
  names, resolved synthetic-helper return types, and correct
  optional-before-required parameter ordering.
- Unconditional `pwd` import (crashed on Windows); `client.path()` backend-kwarg
  precedence; `Path.read()` now returns its bytes.
