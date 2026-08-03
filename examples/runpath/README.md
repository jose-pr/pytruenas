# RunPath example — `health`

A **RunPath** is a directory of numbered `NN-name.py` step files that run in
order, fanned out once per target. Each target gets its own client, its own
logger prefix, and its own copy of the command instance, so per-target state
cannot bleed between them.

`health/` is a complete, runnable flow that reads system info, checks pool
health, and reports what it found.

## Running it

Point `--cmdspath` at this directory; the flow becomes a subcommand named after
its directory:

```sh
pytruenas --cmdspath examples/runpath health nas1 nas2
```

Targets are trailing positionals, so a range pattern and the global options work
as they do for any other command:

```sh
pytruenas --cmdspath examples/runpath health --sslverify -v 'nas[1-3]'
pytruenas --cmdspath examples/runpath health --parallel 4 nas1,nas2
```

`--rcopts` selects steps by name (`!` disables, and a bare name re-enables):

```sh
pytruenas --cmdspath examples/runpath health --rcopts '!*,system-info' nas1
```

## The step signature

A step may take the **module command signature**, `(client, args, logger)` —
the same one a command module's `run()` takes, so the same body works in either
kind. No decorator, no import:

```python
def main(client, args, logger):
    logger.info("%s", client.api.system.info()["hostname"])
```

| | |
|---|---|
| `client` | the per-target client `__main__.py`'s `init` returned |
| `args` | the parsed command for this target: options, `args.target`, stashed state |
| `logger` | already `[target]`-prefixed by the fan-out |

Three arguments is unambiguous — duho never calls a step with more than two —
so pytruenas adapts it automatically, via duho's `register(step_adapter=...)`
hook.

A **shorter** app-shaped signature is ambiguous: `(client, args)` and duho's own
`(cmd, ctx)` look identical, and guessing would silently swap them. Those need
an explicit decorator:

```python
from pytruenas.utils.runpath import step

@step
def main(client, args):
    ...
```

duho's native `main(cmd, ctx)` keeps working untouched. All three forms coexist
in one directory.

| file | shape |
|---|---|
| [`10-system-info.py`](health/10-system-info.py) | `(client, args, logger)`, adapted automatically |
| [`20-pools.py`](health/20-pools.py) | `@step` with a shorter signature |
| [`30-report.py`](health/30-report.py) | duho-native `main(cmd, ctx)` |

## Per-target setup

`health/__main__.py` defines `init(cmd, logger)`, which runs once per target
before any step and whose return value becomes each step's `client`. Re-exporting
`default_init` is enough for the common case:

```python
from pytruenas.utils.runpath import default_init as init
```

This example wraps it to also stash `cmd.findings`, which later steps read back.
`success(ctx, cmd, logger)` and `finally_(ctx, cmd, logger)` hooks are available
there too.
