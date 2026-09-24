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

### `help` — what does this method take?

```bash
pytruenas help user.create nas.example.com    # one method, in full
pytruenas help user nas.example.com           # a namespace's methods
pytruenas help all nas.example.com            # every namespace
```

Prints every field with its type, whether it is required, its default, the
values an enum allows, and whether the method is a **job** (a job returns an id,
not a result) — read from the appliance's own API definition, so it matches the
version in front of you rather than the docs. `--json` emits the definition slice
instead of prose.

`NAME` is required and comes first, like `query`'s namespace — hence `all` for
the index, rather than omitting it. (Omitting it cannot work: argparse would
claim the only remaining word, leaving no target.)

The schema is fetched from the API one namespace at a time, which needs **no
shell access and no special role** — it works with a plain API key on an account
that cannot run commands at all. Answers are cached per host, version and
namespace. `--refresh-api` re-fetches, needed only after upgrading an appliance
in place.

`--dump` instead reads the whole `middlewared --dump-api` definition. That needs
command access and weighs ~24 MB, so use it only for `--api-version`, to
describe a version older than the one running.

### `call` — invoke any method

```bash
pytruenas call system.info nas.example.com
pytruenas call core.ping nas.example.com
```

`call` invokes any middleware method by its dotted name (unlike `query`, which
only covers `<namespace>.query`). Parameters are JSON values via `-p/--param`
(repeatable), in any position relative to the method and the targets.

For anything that **writes**, pass fields after a literal `--` instead of
hand-written JSON:

```bash
pytruenas call user.create nas.example.com -- \
    --username=svc --full_name='Svc account' --group_create=true

pytruenas call user.update -p 1 nas.example.com -- --full_name='New name'
```

`--field=value` and bare `field=value` are the same thing there, and each value
is typed from the method's schema: booleans, integers, `null` for a nullable
field, arrays from a comma list *or* a repeated flag, and nested objects from
dotted names (`--options.acl=true`). Two escape hatches: `--name:json=<json>`
for a literal JSON value, and `--name=@path` to read one from a file — which is
what you want for a key or a certificate.

An unknown field name or a bad enum value is an error that names the
alternatives, raised **before** anything is called, so a typo cannot reach the
appliance as a half-filled payload.

!!! note
    The `--` separator is required rather than decorative: the valid field names
    are only known once the method name is parsed, so bare top-level `--flags`
    would collide with the global options — a middleware field named `config` or
    `parallel` would be unreachable. Targets go **before** the separator, as
    they do for `deploy`.

    `--no-schema` skips the definition entirely (values are typed the way `-p`
    types them, and no name is checked).

See [Provisioning](provisioning.md) for worked examples.

### `dump-api` — dump the API definition

```bash
pytruenas dump-api nas.example.com > api.json
```

The dump is built and compressed on the target, then fetched over SFTP when the
host has an SSH leg and in verified chunks through the command channel
otherwise. It is ~24 MB on 26.0 and takes about 75 s to produce, so it is cached
per host and API version under `$PYTRUENAS_CACHE` and shared with `help` and
`generate-typings`.

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
