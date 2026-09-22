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

## Credentials and TLS

Credentials come from the target string (`wss://root:pw@nas`,
`wss://nas` with `1-<api-key>` as the password). A target that carries none
falls back to `$TN_CREDS`, then to `credentials:` in the config file — either
a connection string or a mapping of keyword arguments:

```bash
export TN_CREDS='1-<64-char-api-key>'
pytruenas call system.version nas.example.com
```

TLS certificates are verified, against the same trust store the library uses.
A lab box with a self-signed certificate needs an explicit opt-out, or a CA
bundle:

```bash
pytruenas call -k system.version nas            # or --insecure / --no-sslverify
PYTRUENAS_SSLVERIFY=/etc/pki/lab-ca.pem pytruenas call system.version nas
```

The config file's `sslverify` (`false`, or a bundle path) sets the default for
a whole site; a flag on the command line still wins.

## Commands

### `query` — read a namespace

```bash
pytruenas query user nas.example.com
pytruenas query user -f username=root nas.example.com     # -f/--filter, repeatable
pytruenas query pool.dataset nas.example.com
```

`query` issues `<namespace>.query`, so it works on queryable namespaces
(`user`, `pool.dataset`, …), not on plain methods like `system.info`.

### `call` — invoke any method

```bash
pytruenas call system.info nas.example.com
pytruenas call core.ping nas.example.com
pytruenas call -p '{"username": "svc"}' user.create nas.example.com
```

`call` invokes any middleware method by its dotted name (unlike `query`, which
only covers `<namespace>.query`). Parameters are JSON values via `-p/--param`
(repeatable), in any position relative to the method and the targets.

### `dump-api` — dump the API definition

```bash
pytruenas dump-api nas.example.com > api.json
```

### `generate-typings` — build `.pyi` stubs

See [Generating typings](typings.md).

## Config file

With the `config` extra, `--config file.yaml` (`-c`) supplies targets and
defaults so you don't repeat the target hosts every invocation. It also
carries `credentials:` and `sslverify:` for the hosts it names:

```yaml
credentials: 1-<64-char-api-key>   # or a mapping: {username: root, password: ...}
sslverify: /etc/pki/lab-ca.pem     # or false
```
