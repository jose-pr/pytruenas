# pytruenas

[![Version](https://img.shields.io/pypi/v/pytruenas.svg)](https://pypi.org/project/pytruenas/)
[![Python versions](https://img.shields.io/pypi/pyversions/pytruenas.svg)](https://pypi.org/project/pytruenas/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/jose-pr/pytruenas/blob/main/LICENSE)
[![Docs](https://img.shields.io/badge/docs-latest-blue.svg)](https://jose-pr.github.io/pytruenas/)
[![CI](https://img.shields.io/github/actions/workflow/status/jose-pr/pytruenas/test.yml)](https://github.com/jose-pr/pytruenas/actions/workflows/test.yml)

A typed, Pythonic client and CLI for the [TrueNAS](https://www.truenas.com/)
middleware API. **Every middleware method, attribute-style, over the
middleware's own JSON-RPC 2.0 websocket — from a remote host or on the NAS
itself — with commands and files over whichever transport the target
actually offers.** Documentation: <https://jose-pr.github.io/pytruenas/>.

## Features

- **The whole API, attribute-style.** `client.api.pool.dataset.query(...)` is
  the middleware method `pool.dataset.query`; no per-endpoint wrappers.
- **Create-or-update helpers.** `_get`/`_query`/`_create`/`_update`/`_upsert`
  diff against the current record and send only what differs.
- **Local and remote.** `wss://`/`ws://` to a remote host with an API key,
  password or token, or the root-owned unix socket (`ws+unix://`) with no
  auth on the NAS itself.
- **Extended JSON.** `datetime`/`date`/`time`/`set`/IP-interface values
  round-trip through the middleware's wire format.
- **Commands and files.** `run()` and `path()` come from
  [hostctl](https://github.com/jose-pr/hostctl): plain `subprocess` on the NAS,
  SSH, or the web UI's own shell for a host reachable only on the API port;
  SFTP or the middleware `filesystem.*` API for files.
- **A CLI for many hosts.** `query`, `call`, `dump-api`, `deploy` and your own
  command modules, fanned out over host ranges such as `'nas[1-3]'`.
- **Typings on demand.** `generate-typings` writes `.pyi` stubs for a host's
  whole API, so editors and type checkers understand every call.

## Installation

```sh
pip install pytruenas
```

| Extra | Enables |
| ----- | ------- |
| `pytruenas[ssh]` | SSH commands + the SFTP filesystem leg (`asyncssh`) |
| `pytruenas[yaml]` | A CLI config file written in YAML (`#!yaml`, `.yaml`); TOML needs no extra (`anycfg[yaml]`) |
| `pytruenas[codegen]` | `generate-typings` command (`jinja2`) |
| `pytruenas[repo]` | `deploy --source repo`; included in the core install (`hostctl[deploy]`) |

## Quick start

```python
from pytruenas import TrueNASClient

# Remote host (api key, or "user:password", or a token)
client = TrueNASClient("nas.example.com", credentials="1-<64-char-api-key>", verify=False)

# Attribute-style access to any API namespace/method:
for user in client.api.user.query():
    print(user["username"])

# Convenience helpers for common DB patterns:
client.api.user._upsert(("username",), username="svc", full_name="Service", group_create=True)

# Running on the NAS itself talks to the local unix socket, no auth:
local = TrueNASClient()            # ws+unix:///var/run/middleware/middlewared.sock
print(local.api.system.info())
```

### Commands and files

`run()` and `path()` are inherited from `hostctl`, which selects a transport
rather than assuming one:

```python
client = TrueNASClient("nas.example.com", credentials=api_key, shell="ssh://root@nas.example.com")

client.run("zpool status", capture_output="stdout", encoding="utf-8").stdout
client.path("/mnt/tank/notes.txt").read_text()

client.capabilities      # {"run", "path", ...} -- what this target can actually do
client.last_selection    # which transport served the last run(), and why
```

| target | commands | files |
| --- | --- | --- |
| on the NAS | `local` (plain `subprocess`) | `local` |
| remote, SSH configured | `ssh`, then `webshell` | `sftp`, then `tnasws` |
| remote, no SSH | `webshell` | `tnasws` |

`webshell` runs commands over `/websocket/shell` — the same PTY the web UI's
Shell page uses — so a host reachable on the API port but **not** on 22 (NAT, a
firewall allowing only 443) can still run commands. Name providers explicitly
with `executor=` / `path=` to force or exclude one.

Output is exact: commands and input travel base64-encoded and output is
framed by markers the command prints, so the terminal's echo, prompt and banner
never reach your result. Uncaptured stdout streams live; stderr is captured
separately (delivered when the command ends); `input=`/`stdin=` are delivered
through a temporary file, never typed into the terminal.

### Credentials

`TrueNASClient(target, credentials=...)` accepts, as `credentials=` (a keyword):

- an **API key** string `"<id>-<64 chars>"`,
- `"user:password"` (optionally `"user:password\n<otp>"`),
- a **token** string,
- a `(user, password)` tuple,
- `None` / omitted → local socket auth.

`Credentials.from_env()` reads `TN_CREDS`. Credentials may also travel in the
target (`wss://root:secret@nas`). In a **URI** an OTP follows the password after
a newline as a keyed line — `otp:<token>`, with the newline percent-encoded:
`wss://root:secret%0Aotp:123456@nas`. In the plain credential string above the
token follows the newline on its own (`"user:password\n123456"`).

A password containing `/`, `?` or `#` must be percent-encoded (`%2F`, `%3F`,
`%23`); a raw one is refused, because the URL parser would otherwise read the
rest of it as a host, port and path.

## Command line

```sh
pytruenas --help
pytruenas query user -f username=root nas.example.com
pytruenas call system.info nas.example.com          # any method by dotted name
pytruenas dump-api nas.example.com > api.json
pytruenas generate-typings --api-version v26.0.0 nas.example.com
pytruenas deploy nas.example.com                    # install pytruenas ON the host
```

The target host(s) are the **trailing positional arguments** — a command's own
positionals (like `query`'s namespace) come first, then the hosts. Each target
may be comma-separated and supports `[A-Z]`/`[0-9]` range expansion (e.g.
`'nas[1-3].example.com'`); with no target the command runs against `localhost`.
`--parallel N` runs several targets concurrently. Filter `query` with
`-f/--filter KEY=VALUE` (repeatable).

## API overview

| Module | Purpose |
| --- | --- |
| `pytruenas` | `TrueNASClient`, `TrueNASConfig`, `Credentials`, `Namespace`, `Event`, `Subscription`, `__version__` |
| `pytruenas.host` | The client: connection and login, `client.api`, events, and hostctl's `run()` / `path()` |
| `pytruenas.namespace` | `Namespace`: middleware calls by attribute, and the `_get`/`_query`/`_create`/`_update`/`_upsert` helpers |
| `pytruenas.connection` | The JSON-RPC 2.0 websocket transport, the extended-JSON codec and the call exceptions |
| `pytruenas.auth` | Credentials: API key, user and password (with OTP), token, local socket |
| `pytruenas.fs` | Remote paths over the middleware `filesystem.*` API |
| `pytruenas.providers`, `pytruenas.webshell` | The transports behind `run()` and `path()`, the web shell among them |
| `pytruenas.main`, `pytruenas.cmd` | The CLI and its built-in commands |
| `pytruenas.utils.runpath` | `step` and `default_init` for RunPath flows (numbered step directories) |
| `pytruenas.patch` | Changing a host beyond what the API exposes: templates, systemd units, the middleware itself |
| `pytruenas.codegen`, `pytruenas.models` | The typings generator and the API-dump schemas it reads |

Every export, with its signature and contract, is in the API header that ships
inside the package,
[`pytruenas/AGENTS.md`](https://github.com/jose-pr/pytruenas/blob/main/src/pytruenas/AGENTS.md),
and in the [API reference](https://jose-pr.github.io/pytruenas/api/reference/).

## Running on the appliance

TrueNAS has a read-only root and no `pip`, so `deploy` bootstraps instead,
through [hostctl](https://pypi.org/project/hostctl/)'s `hostctl.deploy`: it
asks the target which distributions it already has, bundles only the
difference, and copies that over. The appliance already ships `requests`,
`websocket-client`, `pyyaml`, `asyncssh`, `jinja2` and `packaging`, so the
bundle is pytruenas and its pure-Python dependencies `duho`, `hostctl`,
`netimps`, `pathapi` and `pathapi-uri`, plus `pathspec` where the target lacks
it.

```sh
pytruenas deploy nas.example.com                 # a single executable .pyz
pytruenas deploy --mode dir nas.example.com      # an unpacked bin/ + lib/ tree
pytruenas deploy nas.example.com -- call system.info   # install, then run there
```

Everything after `--` runs on the target once it is installed. The default
destination is under `/var/db/system`, which is a dataset on a *data* pool and
so survives an update — unlike `/var/db` itself, `/root` or `/data`, which live
in the boot environment and are replaced by one. A digest is recorded beside
the payload, so redeploying verifies instead of re-copying; `--force` overrides.
An existing `--path` that a previous deploy did not create is refused rather
than replaced.

When pytruenas is a *dependency* of your own tool rather than the thing being
deployed, name yours as the root: `--pkg-root mytool` (or `PYTRUENAS_PKG_ROOT`),
and your package ships with pytruenas bundled underneath it.

`--source repo` ships a working tree as-is instead of an installed dependency
closure — the files a clone would have, filtered by whichever of `.gitignore`,
`.ignore` and `.bundleignore` are present, with nothing needing to be installed
locally first. It requires `--mode dir`: a zipapp
needs an importable package root, which a working tree does not have.

```sh
pytruenas deploy --source repo --mode dir --repo-root . nas.example.com
```

## Typings generator

`generate-typings` turns a host's API definition into a package of `.pyi` stubs
so editors and type checkers understand `client.api.<namespace>.<method>(...)`.
The test suite compiles the stubs it generates from a fixture dump and a set of
unusual schema shapes and type-checks them with pyright and mypy; it does not
run against a full live dump.

```sh
pytruenas generate-typings --path truenasapi_typings/current nas.example.com
```

## Development

```sh
git clone https://github.com/jose-pr/pytruenas.git
cd pytruenas
py -V:3.14-arm64 -m venv .venv/3.14-nt-arm64
.venv/3.14-nt-arm64/Scripts/python -m pip install --only-binary=cryptography -e ".[dev,docs]"
.venv/3.14-nt-arm64/Scripts/python -m pytest -q -rs
```

That is the recipe on Windows ARM64. A venv is named
`.venv/<python>-<os>-<arch>` after the interpreter it holds: on Linux, for
example, `python3.14 -m venv .venv/3.14-posix-x86_64`, with `bin/` where
Windows has `Scripts/`. `--only-binary=cryptography` stops pip from building
`cryptography` from source, which fails on Windows ARM64, where recent
releases ship no wheel; on a platform with a wheel it changes nothing.

`dev` carries every extra that has tests. A test whose extra is missing skips,
so a partial install still prints green: `-rs` lists what skipped. Some
`run()` tests need a POSIX shell and skip on Windows, so verify anything
touching command or path dispatch on a real target. Supports Python 3.9+; run
the suite on 3.9 as well before a release. Formatting, docs and benchmarks:
[CONTRIBUTING.md](https://github.com/jose-pr/pytruenas/blob/main/CONTRIBUTING.md).

### Releasing

1. Add the `## [x.y.z] - <date>` section to `CHANGELOG.md` and set `version`
   in `pyproject.toml` (PEP 440: `1.0.0rc1` for the tag `v1.0.0-rc.1`) in the
   same commit. The release notes are scraped from that section.
2. Run the suite on 3.9 and 3.14 and `mkdocs build --strict`; pushing a
   throwaway `ci-*` tag runs the whole test workflow.
3. Push the `vX.Y.Z` tag. The release workflow tests, tests at the dependency
   floors, builds, smoke-tests the wheel and gates on the docs build before it
   creates the GitHub release, uploads to PyPI and deploys the docs. A tag with
   a `-` (a pre-release) stops at the GitHub release.

Before 1.0, the minor version changes only when the documented API breaks;
additions and fixes are patch releases.

## License

MIT — see [LICENSE](https://github.com/jose-pr/pytruenas/blob/main/LICENSE).
