# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- **`TruenasPath`'s SFTP leg never engaged.** `_sftp()` looked the SSH target
  up on `client.ssh_config` (removed when `TrueNASClient` merged into
  `TrueNASHost`) and then `client.shell` (hostctl's bound `Shell`, which has
  no `host`), so it returned `None` for every real host: the documented
  SFTP-first behaviour of `unlink`/`rmdir`/`rename`/`readlink`/`symlink_to`/
  `resolve` was unreachable, and `rename`/`readlink`/`symlink_to` raised
  `NotImplementedError` no matter how the host was configured. It now reads
  `client.config.ssh` — the `hostctl.host.SshConfig` the host actually
  carries. (Host-level `client.path(...)` work was mostly unaffected: hostctl's
  composite path routes symlink-ish operations to its own `sftp` provider.)
- **`TruenasPath.symlink_to(force=True)` deleted the existing target and then
  failed** on a host with no SFTP leg: the force-removal ran first, and only
  afterwards did the call discover there was no way to create the link. The
  creating leg is now resolved before anything is removed, so the call raises
  `NotImplementedError` with the target untouched. (Consequence of the
  ordering: on a host with no SFTP leg, a `force=` conflict now raises
  `NotImplementedError` rather than `FileExistsError` — neither call could
  ever have succeeded.)
- **`Credentials(...)` printed the secret when called with both positional and
  keyword arguments.** That branch raised `AttributeError(args, kwargs)` with
  the raw values — and an exception's args are exactly what a traceback or log
  handler renders, so a call-shape mistake leaked the credential. It now
  raises `ValueError` (matching the sibling "Credentials not supported"
  branch) with the keyword secrets masked as `***` and the positional
  credential reduced to its type name.

### Changed

- Declare Python 3.14 support (classifier), and test it in CI — it is the
  routine development interpreter, so a 3.14-only breakage should not have to
  wait for a manual check.

### Documentation

- The shipped API header (`pytruenas/AGENTS.md`) documents 0.4.2's whole repo
  mode: every `deploy --source repo` flag, and `utils.bundle`'s `collect_repo`
  / `repo_requirements` / `DEFAULT_IGNORE_FILES` / `contents=`. The `repo`
  extra is listed there and in the README.
- The changelog's reference links stopped at `[0.3.4]`, so every `## [0.4.x]`
  heading rendered as a dead reference. Added the missing definitions
  (`0.2.2`, `0.3.0`, `0.3.1`, `0.4.0`, `0.4.1`, `0.4.2`) and repointed
  `[Unreleased]` at `v0.4.2...HEAD`.

## [0.4.2] - 2026-08-06

### Fixed

- **The web shell's stderr split could misattribute stdout as stderr.**
  `wrap_stderr` bracketed stderr with its start/end markers around the whole
  `2> >(...)` process substitution's *lifetime*, not each individual write —
  so the subshell's own scheduling decided when the markers actually fired,
  and stdout written while that bracket happened to still be open came back
  labelled as stderr. Switched to a per-line read loop that closes the
  bracket after each line, so a write can only be misattributed if it lands
  mid-line.
- **`clean_output()` left stray escape bytes behind for one OSC form.** It
  only recognized a BEL-terminated OSC sequence (`ESC ] ... BEL`); the
  equally common ST-terminated form (`ESC ] ... ESC \`) — including its own
  stray `ESC \` — passed through into what was supposed to be cleaned output.

### Added

- **`pytruenas deploy --source repo`: ship a repo working tree as-is,** rather
  than the installed dependency closure. Copies files filtered by whichever of
  `.gitignore`/`.ignore`/`.bundleignore` exist (`--ignore-file` narrows the
  selection; `--ignore-pattern` adds patterns on the command line), and reads
  declared dependencies straight from `pyproject.toml`/`requirements.txt` —
  no import, nothing installed required — logging them as a heads-up via the
  new `bundle.repo_requirements()` (`--include`/`--exclude` accept a bare
  dependency name or a bracketed `[extra]`; an exclude always wins).

  This does **not** vendor the repo's own dependencies alongside it — that
  needs a resolved transitive closure, which requires those dependencies
  installed here, the exact thing repo mode exists to avoid needing. It is
  for the read-only-root workflow of shipping source to be read, edited, or
  run by an interpreter that already has (or can reach) what the repo
  declares; `--source installed` (the default, unchanged) is still what
  builds a fully self-contained bundle.

  Only `--mode dir` supports it: a zipapp needs its package importable at the
  archive root, which a `src/`-layout repo copy does not have. `--mode dir`'s
  launcher instead puts every directory an importable package was found under
  (`src/`, `lib/`, `vendor/`, or the repo root itself — auto-detected, or
  named explicitly with `--pythonpath`) on `PYTHONPATH`.

  New public `pytruenas.utils.bundle` functions: `collect_repo()` (the
  gitignore-filtered tree walk, via the new optional `pathspec` dependency —
  the `repo` extra) and `repo_requirements()` (the static dependency reader,
  using `tomllib`/the optional `tomli` fallback below Python 3.11). `build()`
  and `export()` gained a `contents=` parameter accepting either function's
  output directly, so the zipapp/tree-writing code is identical regardless of
  where the file list came from.

## [0.4.1] - 2026-08-06

### Fixed

- **Wrapper objects reach the API as the scalars it expects.** Holding a value
  as `IPv4Address`, a MAC type, or a `PurePath` is the natural thing to do in
  Python, and it broke twice: serializing raised
  `TypeError: not JSON serializable`, and `diff()` compared the wrapper against
  the plain string the API had reported. Those are never equal, so the field
  looked changed on *every* call — an upsert rewrote it forever and reported a
  change that never happened.

  A type may define `__json__()` to choose its own form (the only hook that can
  produce something other than a string); otherwise a type carrying its own
  `__str__` is stringified. Anything else — JSON natives, containers, and
  objects with the *default* `__str__` — is left alone, so an opaque object
  still raises `TypeError` rather than being sent as
  `"<module.Thing object at 0x...>"`.

  The middleware's extended types (`datetime`, `set`, IP *interfaces*) keep
  their `{"$date": ...}`-style envelopes: the reduction runs only after those
  are handled. `diff()` normalizes for the comparison only — the value sent is
  the caller's original.

### Changed

- **Requires `hostctl>=0.2.5`** (was `>=0.2.3`). The web-shell executor
  imported `write_output` from `hostctl.executor._common` because it was not
  exported; 0.2.5 makes the stream helpers public, so the import moves to
  `hostctl.executor`. No private `hostctl` imports remain.

## [0.4.0] - 2026-08-05

### Added

- **The web shell separates stdout from stderr.** A PTY has one stream, so the
  command is wrapped to fence its stderr in terminal escape markers and the
  reader splits them back out into `CompletedProcess.stderr`.

  This needs a shell with process substitution (bash/zsh/ksh). The login shell
  is read from `auth.me()`, and output stays **merged** under anything else
  (`sh`, `dash`) with `.stderr` as `None` — always correct, just less
  informative. The wrapper is applied only when the caller asks for the
  distinction, so an ordinary `capture_output=True` costs nothing.

  Reading the shell from the API rather than by running a command is
  deliberate: probing by driving the terminal would hang in exactly the case
  the probe exists to detect.

- **The web shell accepts input.** `input=` rides along as a here-document —
  no timing, no second channel — and is the reliable form. `stdin=` takes a
  readable object and pumps it on a background thread for a stream still being
  produced; it races the terminal's echo of the command line and is mitigated
  by a short delay rather than cured. A file *descriptor* is rejected: there is
  no PTY fd to attach one to.

- **Web-shell output that is not captured is streamed as it arrives**, in raw
  bytes, to `stdout` (default `sys.stdout.buffer`). A long-running command
  reports progress instead of going silent until it exits, and colour and other
  escape sequences survive. Captured `.stdout` remains cleaned text.

### Fixed

- **A patched file could lose its only undo path.** `read()` created the
  baseline snapshot, which made *reading* a write — and that fails outright on
  the read-only mount the middlewared package ships on. `find_template` worked
  around it by defaulting `baseline=False`, trading away the safety net to
  dodge the bug.

  Reading no longer snapshots (`write()` already did, which is the correct
  moment: the mount must be writable by then anyway). With that fixed,
  `find_template` defaults `baseline=True` like everything else in the package,
  and skipping the snapshot is opt-in. Overwriting a stock template with
  nothing beside it has no way back — the original ships inside the middlewared
  package, so recovering it means reinstalling.

- **A shell prompt could end up inside a filesystem path.** The web shell's
  prompt stripping missed zsh's trailing prompt when its line redraw and the
  prompt merged onto one line, so `middlewared_path()` returned
  `/usr/.../middlewared\n#   root@HOST[~]#` and every path built from it was
  wrong.

### Changed

- **The web shell no longer rejects `stdout=`/`stderr=`.** `capture_output` and
  `stdout` resolve through `hostctl.executor.capture_streams`, the same helper
  the SSH executor uses, so the option surface matches whichever provider a
  host selects. `stdin=` as a file descriptor is still rejected.
- `WebShellSession.run_script()` returns `(text, raw_bytes, returncode)` and
  takes `sink=`, `errsink=`, `heredoc=`, and `stdin=`. The extra return element
  is the raw byte stream.

### Added

- **A derived tool can supply its own shared args root.** `main(args=...)`, or
  `_ARGS_` on a `PyTrueNAS` subclass, sets the class every command inherits —
  so a tool built on pytruenas can add global options:

  ```python
  class MyApp(PyTrueNAS):
      _ARGS_ = MyArgs        # a PyTrueNASArgs subclass

  main("mytool", root=MyApp)
  ```

  The value reaches **both** the app root and `duho.runpath`'s base, which is
  the whole point: a global flag that worked on `pytruenas call` but vanished
  on a RunPath directory would be the obvious way to get this wrong. A plain
  `PyTrueNASArgs` subclass is combined with `PyTrueNASRunPathArgs` for the
  RunPath base, so a derived tool keeps its trailing `TARGET` positional.

  This does **not** add per-directory arguments: the base is app-wide, and a
  step directory still cannot declare its own flags.

## [0.3.4] - 2026-08-04

### Fixed

- **`client.path()` raised `ModuleNotFoundError: asyncssh`** whenever an SSH
  configuration existed but the optional `ssh` extra did not — even though the
  websocket backend could serve the call. The sequel to 0.3.3: provisioning
  worked without the extra, and the next path call died. Provider *names* were
  chosen from "is SSH configured", never "is it importable"; they are now gated
  on an import check before any provider is built.

  Only **defaults** degrade. A caller who names `executor=["ssh"]` or
  `path=["sftp"]` explicitly still gets it, and still fails loudly — silently
  serving a transport the caller did not ask for is its own bug.
- **A download link's query string was percent-encoded into the path**
  (`/_download/12345%3Fauth_token%3Dabc`), so the middleware 404'd. Split in
  `_http_target()`, the one choke point every HTTP side channel uses. This also
  fixed `Target.uri`, which parsed a `query` but never rendered it — so the
  split alone would have dropped the query silently instead.
- **`repr()` on any namespace raised `AttributeError`**, reading a `_client._api`
  attribute that no longer exists. `repr` is what a traceback frame renders, so
  it failed while something else was already going wrong. Now renders the host's
  short, credential-free `name`.
- The same stale attribute made `fs.path()` unreachable through the path
  provider entirely; resolved via `fs._settings()`, which accepts either
  spelling.

### Changed

- **The websocket path provider returns a `TruenasPath`**, not a `TnasWsPath`.
  Both ride the same backend, so the transport is unchanged — but `TruenasPath`
  carries the documented `symlink_to(force=, onremove=)` and the
  SFTP→websocket fallback. Pinning the narrower type was silently dropping a
  documented API.

  With `pathlib_next>=0.9.1` and `hostctl>=0.2.3`, `force=` now survives the
  whole chain: `client.path(...).symlink_to(target, force=True)` reaches the
  backend instead of raising `TypeError` at the composition boundary.

### Dependencies

Both floors rise for the same reason, and both came from findings filed here:
the provider hands back a `TruenasPath` so its documented
`symlink_to(force=, onremove=)` is available, and below these versions that
kwarg is stripped before it reaches the backend — the API would be advertised
and not deliverable.

- **`pathlib_next[uri]>=0.9.1,<0.10`** (from `>=0.9.0`) — `symlink_to(force=)`
  as a generic `Path` extension over a `_symlink_to()` backend primitive.
- **`hostctl>=0.2.3,<0.3`** (from `>=0.1.2`) — signature-aware keyword
  forwarding through composite path dispatch. This is the first time the
  hostctl floor has moved past 0.1.2.

## [0.3.3] - 2026-08-03

### Fixed

- **`install_sshcreds` no longer requires the `ssh` extra.** It provisions a
  keypair over the middleware API and opens no SSH connection, but imported
  `asyncssh` unconditionally to derive the public key from the private one — so
  the extra was required for work that never used it. The middleware already
  returns both halves on the paths that generate or store a keypair, so the
  public key is now carried through when known and derived only when genuinely
  absent (a caller-supplied `private_key=` for a key the host does not have).
- **The root user was selected by id rather than by field name.**
  `_upsert("username", ...)` passes a bare `str`, which `DbAction.execute`
  reads as a record *id*; `("username",)` is the sequence form meaning "match
  on this field".

### Added

- **RunPath steps may use the module command signature** — `(client, args,
  logger)`, the same shape `cmd/` modules use — with no decorator in the step
  file. Requires duho 0.5.2's `register(step_adapter=...)`. Only unambiguous
  3-argument steps are adapted automatically; a shorter `(client, args)` is
  indistinguishable from duho's own `(cmd, ctx)` and still needs `@step`.
  duho-native steps are unaffected.
- **`examples/runpath/`** — a runnable three-step flow showing all three step
  shapes side by side, with a README covering the arguments and the per-target
  `init` hook.

### Changed

- **Public-key derivation prefers `cryptography` over `asyncssh`.** `asyncssh`
  depends on `cryptography`, so the `ssh` extra already brings it, and it is
  far lighter than an SSH protocol stack for pure key math. `asyncssh` remains
  the fallback. Both OpenSSH and PEM/PKCS#8 encodings are handled.

### Dependencies

- **`duho>=0.5.2`** (from `>=0.5.1`) for `runpath.register(step_adapter=...)`.
  Not optional: the keyword is passed at import, so 0.5.1 raises `TypeError` on
  startup.

### CI

- Actions updated to current majors (`checkout@v7`, `setup-python@v7`,
  `upload-artifact@v7`, `download-artifact@v8`, and the Pages actions), ahead
  of the Node 20 runtime deprecation.

## [0.3.2] - 2026-08-03

### Fixed

- **`sslverify` never reached the web shell.** `WebShellSession.connect()`
  read `client.sslverify`, but the flag lives on `TrueNASConfig` and
  `TrueNASHost` exposed no such attribute — so every `wss://` web shell connect
  raised `AttributeError` rather than falling back to verifying.
  `TrueNASHost.sslverify` now delegates to the config, so the JSON-RPC, REST,
  and web shell legs all answer from the one value the caller set.

### Added

- **`patch.zfs` can get and set arbitrary dataset properties.**
  `get_property`/`set_property`, the batched `get_properties`/`set_properties`
  (one round trip instead of one per property), and `inherit_property` to clear
  one — ZFS has no `zfs unset`. Native properties and user properties
  (`com.example:role`) are both supported; an unset user property reads as
  absent rather than as the literal `-` ZFS prints, and booleans render as
  `on`/`off`. `is_readonly`/`set_readonly` are now thin wrappers over this API.
- **`utils.runpath.step`** — a decorator letting a RunPath step use the module
  command signature `(client, args, logger)` instead of duho's `main(cmd,
  ctx)`, so the same body works in either command kind. Steps declaring fewer
  parameters are handed only those; undecorated duho-native steps are
  unaffected.

### Changed

- **`utils.runpath.default_init` reads `cmd.sslverify` directly.** The previous
  `getattr(cmd, "sslverify", False)` would have turned a missing field into
  silently disabled TLS verification; every RunPath command inherits the field
  from `PyTrueNASRunPathArgs`.

## [0.3.1] - 2026-07-29

### Fixed

- **`hostctl<0.2` made the dependency set unresolvable.** `pathlib_next`
  0.9.0's `uri` extra requires `netimps>=0.2.0`, and `hostctl` widened its own
  ranges to admit that in 0.2.2 — so pinning `hostctl<0.2` left no solution for
  a `pip install pytruenas` that also pulled `pathlib_next[uri]`.
- **`os.fspath()` on a `TruenasPath`/`TnasWsPath` raised
  `NotImplementedError`.** Both now set `_host_filesystem_path`, so `fspath`
  returns the host-local path (`/usr/lib/x`, not
  `truenas://root@nas/usr/lib/x`). Requires `pathlib_next>=0.9.0`.

### Changed

- **`patch.zfs.host_path` uses `os.fspath()` only.** It previously fell back to
  `.path`, then `as_posix()`, then `str()`, for `pathlib_next<0.9` where
  `fspath` raised for every non-`file` scheme. A URI scheme with no host-local
  path now raises rather than yielding a string that is not a path.

### Dependencies

- **`hostctl>=0.1.2,<0.3`** (from `<0.2`). Nothing pytruenas imports changed;
  the floor stays at 0.1.2 because no 0.2 API is used here. Validated on 0.2.2.
- **`pathlib_next[uri]>=0.9.0,<0.10`** (from `>=0.8.2`, uncapped) — for
  `UriPath.__fspath__` on host-filesystem schemes, and for
  `Source.__str__`/`__repr__` no longer emitting the password. The `ssh`
  extra's `pathlib_next[sftp-async]` moves to `>=0.9.0,<0.10` alongside it.
- **`netimps>=0.0.2,<0.3`** — ceiling added; 0.2.0 reworked `resolve()` and
  made `dnspython` optional, neither of which touches `get_default_port`, the
  only function used here. Validated on 0.2.0.

## [0.3.0] - 2026-07-29

### Added

- **`deploy` command** — installs pytruenas onto a target that has no `pip` and
  a read-only root. Queries the target's installed distributions, bundles only
  those it lacks, and transfers the result. On TrueNAS 26.0.0-BETA.1 that is 5
  packages / ~600 KB (`duho`, `hostctl`, `netimps`, `pathlib-next`,
  `pytruenas`); the appliance already provides `requests`, `websocket-client`,
  `pyyaml`, `asyncssh`, `jinja2`, `certifi`, `urllib3`, `idna`,
  `charset-normalizer` and `dnspython`.
  - `--mode pyz` (default): a single executable zipapp. `--mode dir`: a
    `bin/` + `lib/` tree, unpacked to a staging directory and swapped into
    place.
  - Arguments after `--` are executed on the target after installation:
    `pytruenas deploy nas1 -- call system.info`.
  - Default path `/var/db/system`, the mountpoint of `<pool>/.system` on a data
    pool. `/var/db`, `/root` and `/data` are datasets under
    `boot-pool/ROOT/<version>/` and are replaced by a boot-environment swap on
    update.
  - A SHA-256 digest is stored beside the payload; a redeploy with a matching
    digest transfers nothing. `--force` overrides.
  - `--pkg-root` / `--pkg-name`, or `PYTRUENAS_PKG_ROOT` / `PYTRUENAS_PKG_NAME`:
    bundle a different distribution as the root, with pytruenas as a dependency
    of it.
- **`pytruenas.utils.bundle`** — dependency-closure resolution and bundle
  construction. Reads installed distribution metadata (`importlib.metadata`)
  rather than scanning imports. Raises `BundleError` for a distribution
  containing a compiled extension, or one resolving to data files with no
  importable module.
- **`pytruenas.patch.zfs`** — `writable(client, path)` context manager: clears
  `readonly` on the ZFS dataset backing `path` and restores the previous value
  on exit, including when the block raises. `dataset_for` walks to the nearest
  existing ancestor, as `findmnt --target` exits non-zero for a path that does
  not exist. Also `is_readonly`, `set_readonly`, `host_path`.
- **`FileTarget.revert(remove_baseline=True)`** — restores the baseline
  snapshot and removes it. Returns `False` when no baseline exists.
- **`FileTarget.is_patched()`** — whether the file differs from its baseline.
- **`FileTarget.would_change(content)`** — whether a write would modify the
  file. No side effects.
- **`FileTarget(..., mode=)` and `SystemFile(..., writable=, mode=)`** — mode
  for a newly created file; `writable=True` wraps writes in `patch.zfs.writable`.

### Fixed

- **File permissions are preserved across a rewrite.** The mode was previously
  reset to the umask default. On TrueNAS 26.0, `/etc/shadow` is `0640
  root:shadow`; patching it produced `0644`.
- **`systemctl` invocations ran as separate commands.** `Host.run(*cmds)`
  treats each positional argument as its own command, so
  `run("systemctl", "disable", "--now", name)` executed four commands. Unit
  names were also shell-quoted while being passed as argv. Each invocation now
  builds a single argv list.
- **`is-active` / `is-enabled` raised on a non-zero exit**, which is their
  result value for "no".
- **`services="nfs"` was iterated character-wise**, producing three service
  reloads.
- **`mkdir(755, ...)` passed decimal `755`** (`0o1363`: setuid, setgid, sticky
  and `rwx-wx-wx`) as the mode for created directories. Now `0o755`.
- **`baseline=True` raised `FileNotFoundError` for a file that does not exist**,
  from `read_bytes()` on the absent original inside `write()`.
- **`FileTarget.baseline()` called `resolve()`**, absent from
  `hostctl.host.CompositePosixPath`.
- **`BaseTemplate.render` returned `None`** when not overridden; the value
  reached `write()` as file content. Now raises `NotImplementedError`, and
  `write()` rejects `None`.
- **`MiddlewareFiles` read `client.middlewared_path`**, which does not exist.
  Replaced by `middlewared_path(client)`, which runs `import middlewared` on
  the host. No API method reports the path (checked against all 781 methods on
  26.0.0-BETA.1).
- **`MiddlewareFiles.find_template` defaulted to `baseline=True`.** The
  middlewared package is on a read-only mount
  (`boot-pool/ROOT/<version>/usr`), so the snapshot write failed with `OSError`
  on first read. Now defaults to `False`.
- **`apply_template(**kwargs)` raised `TypeError`** for an already-constructed
  template, and discarded the arguments in other branches.
- **`pytruenas/cmd/` had no `__init__.py`.** `zipimport` does not support
  namespace packages, so a zipapp built from the package exposed no commands.
- **`pytruenas/utils/io.py` called `Path(__file__).stat()` at import** to build
  an unused `STAT_FIELDS` constant, raising `NotADirectoryError` when imported
  from a zipapp. Removed.

### Changed

- **`PYTRUENAS_*` variables are read through a single `duho.env.Env`
  accessor** (`pytruenas.utils.cmd.ENV`). `PYTRUENAS_CONFIG` is the documented
  name; `PYTRUENAS_CFG` remains accepted. `PYTRUENAS_PATH` is split with
  `os.pathsep` and yields `[]` when unset (previously `[""]`, which resolved to
  the working directory).
- **`pytruenas.ops` is now `pytruenas.patch`**, split into `templates/`
  (`base.py`, `targets.py`), `systemd/` (`unitfile.py`, `files.py`, `units.py`),
  `middleware.py` and `zfs.py`.
  - `ops.midclt` → `patch.systemd`. `TruenasSystemFile` → `SystemFile`,
    `SystemdUnit` → `Unit`, `SystemdServiceUnit` → `ServiceUnit`,
    `SystemdMountUnit` → `MountUnit`, `SystemdAutoMountUnit` → `AutomountUnit`,
    `MiddlewareCode` → `MiddlewareFiles`.
  - `ops.template` → `patch.templates`.
  - `Unit.enable` and `Unit.start` accept `None`, meaning the current state is
    left unchanged. Previously `bool` only.
  - `MountUnit` omits `Options` and `Type` when empty.
  - `FileTarget` accepts any object providing `exists`, `read_bytes`,
    `write_bytes` and `with_name`, rather than requiring
    `pathlib_next.Path`.

### Removed

- **`pytruenas.ops.host`** — `package`/`package_digest`/`PathPatterns` are now
  `pytruenas.utils.bundle.tar_tree`/`tar_digest`. `is_localhost`, `is_local_ip`
  and `find_adapter_in_network` are removed with no replacement; they wrapped
  `netimps.interface_for` / `netimps.get_interfaces` and `ipaddress`.
- **`pytruenas.ops.main`** — moved to `examples/simple_client_from_yaml.py`.

### Dependencies

- **`hostctl>=0.1.2`** (from `>=0.1.0`) — for `uri_hostname()`.

### Dependencies

- **`hostctl>=0.1.2`** — for `uri_hostname()`, which returns a URI's host as
  written rather than case-folded.

## [0.2.2] - 2026-07-28

### Added

- **`client.name` / `config.name`** — the host's short label: hostname, plus
  the port when it is not the scheme default; `localhost` for the unix socket.
- **`TrueNASWSConnection(logger=)`** — the connection emits through the host's
  logger when one is supplied.

### Changed

- **Log records are prefixed with the host name** (`[nas1]`, `[nas1:8443]`)
  instead of the full connection string, which included the scheme, port, API
  path and userinfo. `client.logger` is bound to the name, so records are
  attributed without the CLI's `duho.fanout` prefix filter. The per-target
  `Started:` / `Finished:` messages no longer repeat the target.
- **`utils.target.redact` and `Target.redacted` remove the password** rather
  than masking it: `wss://root:secret@nas` renders as `wss://root@nas`, not
  `wss://root:***@nas`. The result reparses to an equivalent target;
  `***` reparsed as a literal password. `redact` now delegates to
  `hostctl.host.redact_uri`. This affects only the rendering of a raw
  connection string — credentials are extracted during parsing, so
  `config.connection_uri` contained none.
- **`--logto` `{target}` expands to the host name** rather than the connection
  string. The name is also a valid filename component.

### Fixed

- **Hostname case is preserved in the log label.** `urlsplit` case-folds
  `hostname`, so `nasA` / `nasB` were logged as `[nasa]` / `[nasb]`.
- **A host renders identically with and without a credential.** With a password
  in the URI the label was `[nasa]`; without one, `[nasA]`. `hostctl.redact_uri`
  rebuilt the authority from the case-folded hostname (fixed in hostctl 0.1.1,
  completed by `uri_hostname()` in 0.1.2).

### Dependencies

- **`hostctl>=0.1.2`** (from `>=0.1.0`) — for `uri_hostname()`. Note the
  behaviour it brings: `config.host` holds the spelling as given, not a
  canonical one, so two spellings of one host are not equal configs. Routing
  case-folds before comparing and is unaffected.

## [0.2.1] - 2026-07-27

### Fixed

- **An unknown constructor keyword raises `ValueError` naming it.**
  `TrueNASClient("wss://nas", passwrd="s3cret")` reached
  `hostctl.host.SystemHost.__init__` and raised `TypeError:
  SystemHost.__init__() got an unexpected keyword argument 'passwrd'`. It now
  raises `ValueError: unknown credential argument: 'passwrd'`, listing the
  accepted configuration options.

### Documentation

- **README** updated for 0.2.0: removed the `pytruenas[host]` extra (dropped in
  0.2.0) and a pre-publication note; corrected the venv layout; added the
  transport table and a commands/files section.
- **Added the [Recipes](https://jose-pr.github.io/pytruenas/guide/recipes/)
  guide** — 13 examples covering connections, queries, upserts, subscriptions,
  commands, transfers, multi-host fan-out and SSH provisioning. All executed
  against TrueNAS 26.0.0-BETA.1.
- **Filesystem guide** — added path examples and a table of operations
  requiring SFTP: `rename`, `symlink_to`, `readlink` and `resolve` have no
  `filesystem.*` equivalent.
- `docs/index.md` extras list corrected. Both CI workflows referenced the
  removed `host` extra.

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

[Unreleased]: https://github.com/jose-pr/pytruenas/compare/v0.4.2...HEAD
[0.4.2]: https://github.com/jose-pr/pytruenas/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/jose-pr/pytruenas/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/jose-pr/pytruenas/compare/v0.3.4...v0.4.0
[0.3.4]: https://github.com/jose-pr/pytruenas/compare/v0.3.3...v0.3.4
[0.3.3]: https://github.com/jose-pr/pytruenas/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/jose-pr/pytruenas/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/jose-pr/pytruenas/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/jose-pr/pytruenas/compare/v0.2.2...v0.3.0
[0.2.2]: https://github.com/jose-pr/pytruenas/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/jose-pr/pytruenas/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/jose-pr/pytruenas/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/jose-pr/pytruenas/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/jose-pr/pytruenas/compare/v0.0.0...v0.1.0
[0.0.0]: https://github.com/jose-pr/pytruenas/releases/tag/v0.0.0
