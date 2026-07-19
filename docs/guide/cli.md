# CLI

The `pytruenas` console script (built on [duho](https://pypi.org/project/duho/))
runs a command against one or more targets.

```bash
pytruenas --help
pytruenas <command> [command-options] [command-positionals] [TARGET ...]
```

Targets are the **trailing positional arguments** of the command — a
command's own positionals (like `query`'s namespace) come first, and any hosts
after them are the targets.

## Targets

Each target may be comma-separated and supports `[A-Z]`/`[0-9]` range expansion.
With no target given, the command runs against `localhost` (the local
middleware socket).

```bash
pytruenas query user 'nas[1-3].example.com'
pytruenas query user nas1 nas2 --parallel 2
pytruenas query user nas1,nas2
```

`--parallel N` runs several targets concurrently, each with its own connected
client and its own log prefix.

## Commands

### `query` — read a namespace

```bash
pytruenas query user nas.example.com
pytruenas query user -f username=root nas.example.com     # -f/--filter, repeatable
pytruenas query pool.dataset nas.example.com
```

`query` issues `<namespace>.query`, so it works on queryable namespaces
(`user`, `pool.dataset`, …), not on plain methods like `system.info`.

### `dump-api` — dump the API definition

```bash
pytruenas dump-api nas.example.com > api.json
```

### `generate-typings` — build `.pyi` stubs

See [Generating typings](typings.md).

## Config file

With the `config` extra, `--config file.yaml` (`-c`) supplies targets and
defaults so you don't repeat the target hosts every invocation.
