# Release Notes

Detailed notes per release: the narrative, the performance story, and the
validation evidence behind each version. `CHANGELOG.md` stays terse and
user-facing; this file is the durable record.

---

## [Unreleased]

Next performance target: still a CI benchmark baseline, so the following release
has a previous->current table. The ejson codec is the hot path worth watching
(`ejson.loads.plain` is the largest per-call cost); the `benchmark` job in
test.yml produces the numbers.

---

## [0.5.1] - 2026-09-23

### What changed

The medium- and low-severity items the 2026-09-22 review had deliberately
deferred, worked through in five passes. No documented API was removed or
renamed, so this is a patch; two behaviours did change on purpose, and both are
listed under Migration.

### Wrong answers, not wrong messages

The rpc layer returned or recorded the wrong value in six places. The one that
matters most: **a keyword argument to a middleware call was silently dropped**,
so `client.api.user.query(filters=[["uid", "=", 0]])` sent no filters and
returned *every* row — which then drove an update. Middleware methods take
positional parameters, and a stray keyword now raises `TypeError`; the
`_query`/`_get`/`_update` helpers still take keywords, by design.

Alongside it: a timestamp decoded late by its own milliseconds (`.600` came back
`1.200`); a response that failed to decode was dropped, leaving its caller to
wait out the whole timeout for a reply that had already arrived; `True`/`False`
was treated as a job id, because `bool` is an `int`; and a middleware *property*
(`{"value": "10G", "parsed": ...}`) was compared against the scalar a caller
sets, so `_upsert` rewrote the field forever and reported a change that never
happened.

### What actually reaches the appliance

**Every deployed bundle was missing `uritools`.** The dependency closure dropped
each requirement's own extras, and pytruenas depends on `pathlib_next[uri]`,
whose extra requires it — and the appliance does not ship it (measured: 386
distributions installed, `uritools` not among them). So `pathlib_next.uri`, the
base of every remote path type, could not import on the target. Environment
markers were also evaluated against the machine running `deploy` rather than the
target; the probe now reports the target's marker environment.

`--source repo` shipped things a clone would not: a nested checkout's `.git`, a
nested `.gitignore` ignored entirely, and anything a symlink pointed at outside
the repo. A missing `--ignore-file` silently disabled *all* filtering, which is
the fastest way to ship a gitignored secret; it is an error now.

A deployed copy can also answer `--version`, which it never could: a zipapp
carries no installed metadata, so the flag answered with a usage error. The
payload now carries a minimal `.dist-info` per bundled distribution.

### Stubs that disagreed with the runtime

Generation crashed outright on schema forms the middleware sends (a list `type`,
`items: true`) and produced files that would not parse (a docstring ending in
`"""`). Names from the dump became invalid identifiers, two different shapes
could claim one TypedDict name with the later silently replacing the earlier, and
a string default of `"0"` became the integer `0`.

The stubs are also more precise than before: `enum`/`const` render as
`Literal[...]` (6413 and 6420 occurrences in the 26.0 dump — 1275 `Literal`
annotations where there were none), a typed `additionalProperties` as
`Mapping[str, T]`, and the call options are keyword-only, matching the runtime.

### Scope

Side-channel tokens are now origin-bound and single-use: pytruenas had been
passing `match_origin=False` where the server's own default is `True`. A client
dropped without `close()` no longer leaks its websocket and reader thread. The
SFTP leg built a fresh backend per call, which defeated pathlib_next's
connection cache entirely — five `readlink()` calls opened five sessions and
closed none.

### The CLI's fan-out

Concurrent targets shared one `args` object, so per-target state belonged to
whichever target ran last; clients were never closed; `--logto` files missed the
library records they exist for; and concurrent result lines interleaved mid-line
so neither parsed as JSON. Target expansion also split passwords —
`root:secret@nas1,nas2` gave the second host no credentials at all.

### Migration

- **A keyword argument to a middleware call raises `TypeError`.** Pass
  parameters positionally (`query([["uid", "=", 0]])`) or use the `_query`/`_get`
  helpers. `timeout` and the upstream-compatibility names still work.
- **`call`/`query`/`dump-api` attribute their output when there is more than one
  target**: each line becomes `{"target": ..., "result": ...}`. A single target
  still prints the bare result.
- A config file found rather than named (`./pytruenas.yaml`) no longer supplies
  `commandspath`; pass `--config` to load commands from one.
- A setup whose HTTP request leaves from a different IP than its websocket will
  now be refused by the origin-bound token.
- Dependency floor: `hostctl>=0.3.2`.

### Performance

No CI benchmark numbers for this cycle either: the runner was repaired in 0.5.0
and its baseline is still the next release's job. The measurable change here is
the SFTP backend cache (five sessions per five `readlink()` calls, down to one
connection) — a resource fix rather than a throughput one.

### Validation

- Suite: 893 passed / 6 skipped on Python 3.14.7 and on the 3.9 floor, both
  native ARM64; 769 passed / 130 skipped with no optional extras.
- `mkdocs build --strict` and `black --check src tests benchmarks examples`
  clean; `pip check` clean on both venvs.
- Live against a TrueNAS 26.0.0-BETA.1 appliance throughout: the repaired
  payload imports `pathlib_next.uri` and answers `call system.version` from the
  target; `--version` works from a deployed pyz and a deployed dir launcher;
  origin-bound tokens work on the web shell, uploads and downloads; 129 typing
  stubs generated from the appliance's own dump parse on the 3.9 floor.
- Every fix has a test that fails on 0.5.0.

### Publication state

Released as 0.5.1 on the owner's instruction (patch: no documented API was
removed or renamed).

---

## [0.5.0] - 2026-09-23

### What changed

A review of the whole package, fixed in place. The themes: **verification is on
by default and means one thing everywhere**, **a command's output is exactly
what the command wrote**, **a dropped connection cannot silently repeat a
request**, and **destructive operations refuse ambiguous input**.

### Verification

`verify=True` is the default and now covers every check the client makes: TLS
for the API websocket, the HTTP side channels and the web shell, and SSH
host-key verification for commands and SFTP. `verify=False` turns all of them
off in one place. The three TLS legs previously disagreed -- the websocket
trusted the operating system's store, `requests` trusted its own certifi bundle
-- so against a NAS with a privately signed certificate the API connected and
every download failed with `SSLError`. They now share one context: the OS store,
or a CA bundle from `sslverify=` or `$SSL_CERT_FILE` / `$REQUESTS_CA_BUNDLE` /
`$CURL_CA_BUNDLE` / `$WEBSOCKET_CLIENT_CA_BUNDLE`.

The CLI verified nothing at all. It now matches the library, with `-k` /
`--insecure` / `--no-sslverify` as the opt-out. **This is the one deliberate
break in the cycle**: a self-signed appliance that worked yesterday fails until
one of those is given, or `sslverify` is set in the config file or
`$PYTRUENAS_SSLVERIFY`.

### The web shell

The `/websocket/shell` executor was rewritten. The old one built a shell command
by interpolation and read back whatever the terminal echoed, which meant the
echoed wrapper came back as output, leftover input could execute as root, and
16 KiB of output took 19 s while 64 KiB never finished. Commands and input are
now base64, output is framed by printed markers with `stty -opost` so the bytes
are exact, and parsing is linear. Measured on the appliance afterwards: 64 KiB
in 1.5 s, 1 MiB in 2-5 s, and output can be streamed to a callback as it
arrives rather than waited for.

### Jobs, logins and dropped connections

`core.job_wait` is itself a job, so it returned a *new job id* immediately
(0.4 s, measured) and every `wait=True` returned before the work finished, with
its failure lost. Waiting now polls `core.get_jobs`: `client.wait(job_id,
callback=...)` returns the result, raises `JobFailed`, and reports progress.

The legacy `auth.login*` methods answer wrong credentials with `False` rather
than an error; that was ignored, so a bad password produced a client whose every
later call failed with `ENOTAUTHENTICATED`. It raises `AuthenticationError` now.
A reconnect repeats the login that was actually used, rather than the configured
credentials or none.

A dropped call is only retried when the request never reached the socket
(`ConnectionClosed.sent`). Before, the default retry could replay a create, a
delete or a job start that the server may already have run.

### Migration

- A self-signed appliance needs `-k` (CLI) or `verify=False` / `sslverify=`
  (library). The SFTP leg also verifies host keys now: add the host to
  `~/.ssh/known_hosts`, or pass `known_hosts=None`.
- `client.wait_job(...)` is `client.wait(...)`.
- Catching `ClientException` with `errno == ECONNABORTED` still works;
  `ConnectionClosed` is a subclass and carries `.sent`.
- A URI password containing `/`, `?` or `#` must be percent-encoded.
- Generated typings: optional keys are now `NotRequired`, imported from
  `typing_extensions` below Python 3.11, and the root module exports `Current`.

### Performance

No CI benchmark numbers for this cycle yet: the benchmark runner had imported a
module removed in 0.2.0, so the suite -- and its CI job -- had been dead since
then. It runs again and reports the same six metrics, which makes the tracked
0.1.0 results comparable again. Numbers for the next release come from the
`benchmark` job (one fixed runner and interpreter per result), not a developer
machine; local runs on Windows ARM64 were used only to confirm the runner works.

The measured performance change in this cycle is the web shell above (64 KiB:
>240 s to 1.5 s), which is protocol work rather than a micro-benchmark metric.

### Validation

- Suite: 748 passed / 6 skipped on Python 3.14.7 and on the 3.9 floor, both
  native ARM64; 694 passed / 58 skipped with no optional extras installed (it
  used to error rather than skip). The skips are the POSIX-shell and
  extra-gated tests.
- `mkdocs build --strict` clean; `black --check src tests benchmarks examples`
  clean (89 files).
- Built artifacts checked as a pair: `AGENTS.md` ships in the sdist and the
  wheel, `AGENTS.local.md` in neither, `py.typed` present, and the metadata is
  PEP 639 (`License-Expression: MIT`).
- Live against a TrueNAS 26.0.0-BETA.1 appliance: TLS trust (default, a CA
  bundle, and an unrelated CA that correctly fails), refused logins, a dropped
  session reconnecting authenticated, `close()` in 0.31 s, an unresponsive host
  failing instead of hanging, the web shell's throughput and streaming, `mkdir`
  modes and parents, and the CLI authenticating from `$TN_CREDS`.
- Typings generated from that appliance: 129 stubs, all parsing on the 3.9
  floor.

### Publication state

Released as 0.5.0 on the owner's instruction. The full matrix ran green before
tagging: 9 test jobs (3.9, 3.13, 3.14 across Linux, Windows and macOS), both
benchmark jobs and the docs build. Two failures the matrix caught first, fixed
before the tag: the web shell decoded its input file with a positional argument
that BSD base64 (macOS) ignores, so input arrived empty there; and the deploy
tests had been reading pre-`packaging` metadata from a local editable install.

---

## [0.3.0] - 2026-07-29

### What changed

Two things: pytruenas can now install and run *on* an appliance, and the
subpackage for changing a host beyond the API — `ops`, now `patch` — was
rewritten from something that mostly did not work into something verified
against a live box.

### Running on the appliance

TrueNAS has a read-only root and no `pip`, so "install it there" has no answer.
`pytruenas deploy <target>` bootstraps instead: it asks the target what it
already has, bundles only the difference, and copies that over.

The probe is the point. TrueNAS 26.0 already ships `requests`,
`websocket-client`, `pyyaml`, `asyncssh`, `jinja2` and the whole `requests`
transitive set, so a vendored payload would be mostly redundant — and *which*
packages are present varies by release. In practice the bundle is five
pure-Python packages, ~600 KB.

It reads installed distribution metadata rather than walking imports. Declared
dependencies resolve transitively and already account for extras and markers,
where an import scan cannot tell that `import yaml` means `pyyaml`, and misses
anything imported inside a function body. That found `certifi`, `urllib3`,
`idna` and `dnspython` — none of which appear in pytruenas' own dependency
list.

The default destination, `/var/db/system`, was chosen by asking the appliance
rather than by picking a plausible path. `/var/db` itself is in the boot
environment (`boot-pool/ROOT/<version>/var`) and is replaced by an update, as
are `/root` and `/data`. `/var/db/system` is the mountpoint of `<pool>/.system`
on a *data* pool, so it survives.

### Five bugs that only a real box could find

Every one built cleanly and failed only after deployment:

- **`pytruenas/cmd/` had no `__init__.py`.** Fine on a filesystem, but
  `zipimport` does not implement namespace packages — so the deployed app
  imported cleanly and offered *zero* commands.
- **`utils/io.py` stat-ed its own `__file__`** at import to build a constant
  nothing used. Inside a zipapp that path is not a real file, so importing
  pytruenas raised `NotADirectoryError`.
- **`pathlib.Path` mangled remote POSIX paths** into `\var\db\system` on a
  Windows controller.
- **`write_text` wrote CRLF** into the launcher, making the shebang
  `#!/bin/sh\r` — "bad interpreter", naming a path that visibly exists.
- **A RECORD entry escaping site-packages** (`../../Scripts/foo.exe`) made a
  mypyc `.pyd` belonging to *black* look like part of hostctl.

Plus editable installs: their RECORD lists only a `.pth` shim, so `pytruenas`
first shipped as a lone `README.md`.

### The patch subpackage

`ops` said nothing about what the code does or what it costs. `patch` says
both, and the package docstring is explicit that this is unsupported territory:
the appliance owns its configuration, and a boot environment swap discards
anything outside the persistent datasets.

Verifying it as asked turned up seven bugs with no tests between them — the
sharpest being `mkdir(755, ...)`, which passes **decimal** 755, i.e. `0o1363`:
setuid plus wrong permission bits on every directory it created. Also
`baseline=True` on a file that did not exist yet raised from inside `write()`
(the ordinary "create this config if absent" case), `baseline()` called
`resolve()` which hostctl's path type does not have, and `MiddlewareFiles`
referenced a `client.middlewared_path` that never existed.

Then the gap that mattered most: the docstring promised "undoable" and there
was no way to undo. Baselines were snapshotted faithfully and nothing restored
from them. `revert()`, `is_patched()` and `would_change()` close that.

And one security bug, found by checking what modes real files carry rather than
assuming: `/etc/shadow` is `0640 root:shadow`, and rewriting a file resets its
mode to whatever the umask gives. Patching it would have silently widened it to
`0644`. The mode is now captured before the write and restored after.

`patch.zfs` restores capability lost in an earlier code transfer:
`writable(client, path)` clears `readonly` on the backing dataset and restores
it however the block exits — which is why it is a context manager and not two
functions.

### Validation

443 passed / 5 skipped on 3.14 and the 3.9 floor. Verified live against
TrueNAS 26.0.0-BETA.1: both deploy modes install and run against the local
middleware socket with the appliance's stock `python3`; a file on a read-only
mount is created, patched, reverted and its `0640` mode preserved throughout;
`readonly` restores even when the patch body raises.

**Not verified live:** the `systemctl` paths. `ServiceUnit.apply()` is covered
only by a test double, and that is exactly where the four-commands-instead-of-one
bug lived. Install a real unit before relying on it.

### Upstream

Two findings filed: `pathlib_next` (`os.fspath()` raises for remote schemes, so
code building a command line for a process running *on that host* has no
correct generic way to name the path) and `hostctl` (three implementations of
"parse a connection string" exist, differing in defaults rather than structure;
asks for a `ConnectionString` base).

---

## [0.2.2] - 2026-07-28

### What changed

Every log record used to carry the whole connection string:

```
[wss://root:hunter2@nas1.example.com:8443/api/current] Started: wss://root:...
```

That is unreadable at fan-out width, repeats the target twice, and puts the
password on every line. Records now carry the machine's short name:

```
[nas1.example.com:8443] Started
```

The name is `client.name` / `config.name` — the hostname, plus the port only
when it is non-default (`:8443` distinguishes; `:443` just repeats the scheme).
`--logto`'s `{target}` uses it too, which additionally makes it a *legal
filename*, where a raw URI is not.

### Attribution was missing outside the CLI

Investigating the prefix turned up a gap that had nothing to do with the URI.
The `[target]` tag came only from `duho.fanout`, which the CLI installs. A
library caller with three clients open got three interleaved streams with
nothing to tell them apart, and `connection.py` logged through a module-global
logger that could not know its host at all — so `Websocket connection was
closed` never said *which* host closed.

`client.logger` is now bound to the host's name via a `LoggerAdapter`, and
`TrueNASWSConnection` accepts `logger=` so the host can share its own. An
adapter rather than a filter: it needs no handler installation, so it works
with whatever logging the caller has already configured, including none.

### Redaction removes the password instead of masking it

`wss://root:***@nas` is now `wss://root@nas`. A `***` placeholder is not a real
password and would reparse into a *wrong* credential if the rendered form were
ever fed back in; removing it leaves a URI that is both safe to log and still
correct to reconnect with.

This turned out to be a duplicate worth deleting rather than a change worth
making: hostctl's `redact_uri` already did exactly this, with the same
reasoning in its docstring. `pytruenas.utils.target.redact` now delegates to
it, so a target rendered here and one rendered by hostctl read identically.

Worth being precise about the scope, because the old docstrings overstated it:
credentials are extracted at *parse* time, so `config.connection_uri` was
already credential-free and `repr(config)` was already safe. Redaction only
ever applied to rendering a *raw* connection string, which is now just the
`--logto` filename path.

### A test caught a design mistake

The fan-out target was first implemented as a `str` subclass whose `__str__`
returned the label. Tests failed with `ctx-nasA` becoming `ctx-nasa`: a RunPath
step doing `'ctx-%s' % cmd.target` silently got the label instead of the value.
Overriding `__str__` on a value that user code also formats is too surprising,
so the label moved to a separate attribute that only the logging path reads.

### Two upstream releases, from one finding

`urlsplit().hostname` case-folds unconditionally — right for resolution, wrong
for a label an operator greps for, so a `nasA`/`nasB` fan-out logged
`[nasa]`/`[nasb]`. Recovering the typed spelling locally fixed most of it, but
exposed a real hostctl bug: `redact_uri` folded the host, and *only* on the
branch that rebuilds an authority. So one machine rendered two ways depending
on whether a credential happened to be present:

```
redact_uri("wss://root:pw@nasA:8443")  ->  'wss://root@nasa:8443'
redact_uri("wss://root@nasA")          ->  'wss://root@nasA'
```

Filed upstream, and fixed in two steps that are worth distinguishing because
the intermediate state was misread once here. **0.1.1** fixed the rebuild,
which removed the inconsistency — but the local workaround was still
load-bearing for *every* target, since `_from_parsed_uri` reads
`parsed.hostname` and `urlsplit` folds that regardless of who produced the
`SplitResult`. **0.1.2** exported `uri_hostname()` so a config stores the
written spelling in the first place, which is what actually retired the
workaround. Verified both times by deleting the local helper and watching what
broke, rather than by reading the release note.

The floor is now `hostctl>=0.1.2`, and it carries a deliberate trade-off from
that release: `config.host` is the spelling the caller typed rather than a
canonical one, so **two spellings of one machine are not equal configs**.
Routing is unaffected — `_normalize_target` case-folds before the local-host
check and `is_local` keys off `socket_path` — and both facts are now pinned by
tests so neither is rediscovered the hard way.

### Validation

389 passed / 5 skipped on 3.14 and the 3.9 floor (23 new tests), against
hostctl 0.1.2 installed from PyPI rather than the sibling checkout. CLI
behavior checked end to end, including that no password reaches a log record
or a `--logto` filename.

---

## [0.2.1] - 2026-07-27

### What changed

Documentation, plus one error message that 0.2.0 got wrong.

The README had drifted: it advertised a `pytruenas[host]` extra removed when
`ops.host` moved to `netimps`, still said "once published to PyPI", and gave a
venv layout the project no longer uses. It also said nothing about the biggest
change in 0.2.0 — that commands and files now pick a transport.

A new **Recipes** guide covers what people actually do: connect and reuse,
query with the `_get`/`_upsert` helpers, subscribe to events, run commands,
upload and download, fan out across hosts, and provision SSH.

### Writing the docs found a bug

Every recipe was executed against the live 26.0.0-BETA.1 box rather than
written from memory, and two of thirteen failed on the first pass. One was the
example's own fault (`me()` returns `pw_name`; `api.user` records use
`username` — now called out in the guide, since it is an easy mix-up).

The other was real. This:

```python
TrueNASClient("wss://nas", passwrd="s3cret")
```

raised `TypeError: SystemHost.__init__() got an unexpected keyword argument
'passwrd'`. Accurate, but it names a hostctl-internal class rather than telling
the caller they misspelled `password`. 0.2.0 already rejected unknown
*credential* names inside the config, and unknown *provider* names in
`executor=`/`path=` — this was the one path where a typo escaped to a layer
that could only describe it in its own terms. It now raises
`ValueError: unknown credential argument: 'passwrd'` with the accepted options
listed.

That is the argument for running documentation examples rather than reviewing
them: the failure was in a message nobody would exercise deliberately, and it
only surfaced because a doc claimed a specific error and the claim was checked.

---

## [0.2.0] - 2026-07-27

### What changed

pytruenas stops maintaining its own generic host machinery and inherits it from
[hostctl](https://github.com/jose-pr/hostctl). What stays here is the part no
other host has: the middleware JSON-RPC websocket, the typed `api` namespace,
login/2FA, subscriptions, and the upload/download side channels. Roughly 190
lines of shell quoting, local-vs-SSH branching, asyncssh lifecycle and
path-backend selection are gone, replaced by `TrueNASHost(PosixHost)` composing
transports that hostctl selects between.

The user-facing shape is deliberately unchanged: `TrueNASClient("wss://nas")`
works exactly as before, and every connection string it ever accepted — bare
host, `host:port`, `ws`/`wss`, `http`/`https`, the unix socket, `None` — still
resolves. The breaks are `.shell` (now the bound shell object, with the SSH
target on `.config.ssh`) and the `jsonrpc` → `connection` module rename.

### Why the transports became providers

The old `run()` was a hard `if local: subprocess else: ssh` branch, and
`TruenasPath` hand-rolled its own "try SFTP, fall back to the websocket"
fallback. Both are now provider lists that hostctl's selector orders and fails
over, which bought three things the branch could not:

- **`.capabilities`** — a host that genuinely cannot run commands says so up
  front instead of raising halfway through a call.
- **`.last_selection`** — a redacted trace of what was tried and why.
- **A place to add a transport.** Which is what made the web shell possible.

### The web shell

Investigating "can a remote host without SSH run anything?" turned up a real
gap: the JSON-RPC API exposes **no** remote command execution. Of 781 methods
on 26.0.0-BETA.1, only `core.resize_shell` and `user.shell_choices` are
shell-adjacent, and the former merely resizes an already-open session. So a
host behind NAT, or a firewall allowing only 443, had no `run()` at all.

`middlewared` also serves `/websocket/shell` — the PTY the web UI's Shell page
drives — which is a real command channel on the same port. It is now a provider,
ordered after SSH because a PTY merges stdout and stderr and takes no piped
input. Verified live: correct exit codes, multi-line output, and stdin through
pipes and here-strings.

Two things about that endpoint cost real time and are recorded so nobody pays
twice:

- **It is `/websocket/shell`, not `/_shell`.** The latter is the internal path
  on middlewared's own port. Connecting to it on 443 does not fail cleanly —
  nginx serves the web UI there, returns 200 instead of a websocket 400,
  `websocket-client` follows the redirect, and rejects its own `https://`
  target with `ValueError: scheme https is invalid`.
- **Input must be sent as binary frames.** The server writes `msg.data`
  straight to the pty fd; a text frame delivers `str`, `os.write` raises on the
  worker thread, and the connection resets with no error message.

### Validation

Windows cannot verify `run()` — those tests are `skipif(not
_has_posix_shell())` and skip there. Everything touching command or path
dispatch was therefore checked against a live TrueNAS 26.0.0-BETA.1 box, which
caught three bugs the full Windows suite passed over: a provider missing the
`args` capability (so the whole invocation arrived as one literal filename), a
path provider that assumed it held a client rather than a host, and a local
target routed through the HTTP side channel it cannot reach.

358 tests pass on both 3.14 and the 3.9 floor.

### Upstream

Four findings were filed against hostctl during the migration and fixed there
before this release: a URI password's raw newline being silently swallowed
(taking an OTP with it), `run(input=<bytes>, encoding=...)` deadlocking rather
than raising, the SSH provider factories being unexported, and the URI helpers
for third-party configs being private.

---

## [0.1.1] - 2026-07-24

### What changed

`call`/`query`/`generate-typings` drop now-redundant `NS(...)` overrides on
their `Args` fields — `NS(type=...)` on a plain `str`/`Path` field (duho
already derives `type=` from the annotation) and `NS(action='append',
nargs=...)` on a `list[str]` option (duho ≥0.5.0 already defaults a list-typed
option to `action="append"`, `nargs=None`). Only `NS(metavar=...)` remains
where the display name isn't inferable. No CLI-surface or dependency-floor
change from 0.1.0 — the `duho>=0.4.1` floor is unchanged since this
simplification is purely cosmetic against an installed 0.4.1 (duho's own
default already matches what the explicit overrides asked for).

### Validation evidence

- Tests: **187 passed / 5 skipped** on Windows Python 3.9.13 (unchanged
  count/shape from 0.1.0 — this release touches only `Args` declarations, no
  behavior).
- Build: `python -m build` produces `pytruenas-0.1.1.tar.gz` and
  `pytruenas-0.1.1-py3-none-any.whl` cleanly.
- Not re-validated live against a real TrueNAS host for this release (0.1.0's
  live evidence below still describes the exercised code paths; this release
  doesn't touch client/namespace/jsonrpc).

### Publication state

Committed to `main` (`ff56cdb`). **Not tagged/published** — same as 0.1.0,
publishing a `v0.1.1` tag is user-gated.

---

## [0.1.0] - 2026-07-24

### What changed

- **`client.run()` text-mode input fix.** `str` input together with a text
  `encoding`/`errors` used to be pre-encoded to bytes *and* handed to
  `subprocess.run` with the encoding, which then tried to `.encode()` bytes and
  crashed. Text mode now keeps `str` as-is (and decodes `bytes` input); binary
  mode encodes. Found by live testing against a real TrueNAS 26.0 host — the
  unit tests mock `subprocess.run`, so only a real POSIX run exercised it.
- **`pytruenas.__version__`** now exposed (resolved from installed metadata).
- **Dependency floors** raised to the tested versions: `duho>=0.3.2` (CLI parser
  fixes) and the `ssh` extra's `pathlib_next[sftp-async]>=0.8.3` (SFTP
  concurrency 8→16).
- **Repo brought to standard:** benchmark suite (`benchmarks/run.py`), docs site
  (`mkdocs.yml` + `docs/`), `CONTRIBUTING.md`, and this file.
- **Everything else accumulated since `0.0.0`** (auth.login_ex/2FA login, client
  convenience wrappers, event subscriptions, netimps-based adapter discovery,
  password redaction in logs, RunPath support) is covered in `CHANGELOG.md`'s
  `[0.1.0]` section, not repeated here.
- **CLI: the trailing `targets` positional is registered centrally**, not by
  each command calling `register_targets(parser)` — `main._with_targets` wraps
  every module command's `register` hook (even a command with none of its own)
  and adds `targets` after it, so an external `--cmdspath` command gets the
  same `<command> [args...] [TARGET ...]` grammar for free.
- **Commands declare their CLI fields via `Args`** instead of an imperative
  `register()` that hand-synced against an otherwise-inert `Args` class (duho
  ≥0.4.1 adds a module command's declared `Args` fields before `register`
  runs). `register()` remains for what a declaration can't express. No
  CLI-surface change (`call method [TARGET ...]`, `query namespace [TARGET
  ...]`, repeatable `-f`/`-p`, `--api-version`/`--api-cache` unchanged).
- **Known gap, not fixed in this release:** an option placed between a
  command's own positional and the trailing targets still fails to parse
  (`query user -f x nas1` → `unrecognized arguments: nas1`) — argparse's own
  greedy positional-run matching. `call.py`'s docstring documents the
  workaround; filed upstream against duho (its own flag-reorder fix doesn't
  reach a module command's subparser).

### Performance

First benchmark baseline (see `benchmarks/results/`). These are **local**
numbers (Intel i7-1065G7 class, Windows) for regression-catching, not a CI
figure. The suite measures pure-CPU hot paths — no network.

| metric | py3.9 median (ms/call) | py3.14 median (ms/call) |
| --- | --- | --- |
| `ejson.dumps.plain` (20-row response) | 0.048 | 0.045 |
| `ejson.loads.plain` | 0.048 | 0.050 |
| `ejson.dumps.extended` | 0.020 | 0.021 |
| `ejson.loads.extended` | 0.020 | 0.020 |
| `namespace.methodname` | 0.004 | 0.004 |
| `query.filter_from_kwargs` | 0.003 | 0.002 |

**Hot-path analysis:** the ejson encode/decode paths dominate and are already
near stdlib-optimal. Two candidate micro-optimizations were measured and
**rejected** (each ~1.02x, within noise): swapping `json.dumps(cls=Encoder)` for
`default=func` (Python's `json` uses the pure-Python encoder whenever any custom
type handling is present, regardless), and a fast-path bail in `_object_hook`
(real response dicts are multi-key, already short-circuited). The client's cost
is I/O-bound; there is no pending CPU speedup. This baseline exists to catch a
future regression.

**Performance target for the next release:** no regression on the medians above
(compare same machine + interpreter).

### Validation evidence

- Tests (as of this file's earlier entries, predating the CLI/`Args` work
  above): **113 passed / 5 skipped** on Windows Python 3.9; **118 passed / 0
  skipped** on Python 3.13 on a real TrueNAS 26.0 host (the POSIX-shell-gated
  `run()` tests that skip on Windows run there).
- Live integration on TrueNAS 26.0.0-BETA.1 via the local middleware socket:
  `system.info`, `user.query`, `pool.dataset.query`, `_get`, fs `Path`
  exists/read, `client.run()` shell paths, and the `dump-api` / `query` /
  `generate-typings` CLI subcommands (129 valid `.pyi` stubs generated).
- Build: `python -m build` + `twine check` PASS; wheel carries `py.typed`, no
  agent-file leakage.
- Docs: `mkdocs build --strict` clean.
- Coverage: TOTAL 70% (client 62%, namespace 79%, jsonrpc 84%, main 80%).
- **Re-verified for the final `0.1.0` tree** (CLI centralization + `Args`
  declarations included): **187 passed / 5 skipped** on Windows Python 3.9.13
  (no environment with a live TrueNAS host or `twine`/`mkdocs` available in
  this pass — the sections above are the last live-host/docs-build evidence on
  record; only the automated-test count and `python -m build` were re-run).

### Publication state

Prepared and merged to `main`. **Not tagged/published** — a `v0.1.0` release is
user-gated and requires PyPI trusted-publishing + GitHub Pages setup by the repo
owner.

---
