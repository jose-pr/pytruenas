# CLI

The `pytruenas` console script (built on [duho](https://pypi.org/project/duho/))
runs a command against one or more targets.

```bash
pytruenas --help
pytruenas <command> -t <target> [options]
```

!!! important
    The subcommand comes **first**, then `-t/--target`. Because `-t` accepts a
    variable number of hosts, putting it before the subcommand
    (`pytruenas -t host query`) lets the target list swallow the command name.

## Targets

`-t/--target` may be repeated or comma-separated and supports `[A-Z]`/`[0-9]`
range expansion:

```bash
pytruenas query user -t 'nas[1-3].example.com'
pytruenas query user -t nas1 -t nas2 --parallel 2
```

`--parallel N` runs several targets concurrently, each with its own connected
client and its own log prefix.

## Commands

### `query` — read a namespace

```bash
pytruenas query user -t nas.example.com
pytruenas query user -t nas.example.com -f username=root      # -f/--filter, repeatable
pytruenas query pool.dataset -t nas.example.com
```

`query` issues `<namespace>.query`, so it works on queryable namespaces
(`user`, `pool.dataset`, …), not on plain methods like `system.info`.

### `dump-api` — dump the API definition

```bash
pytruenas dump-api -t nas.example.com > api.json
```

### `generate-typings` — build `.pyi` stubs

See [Generating typings](typings.md).

## Config file

With the `config` extra, `--config file.yaml` (`-c`) supplies targets and
defaults so you don't repeat `-t` every invocation.
