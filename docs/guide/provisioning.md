# Provisioning

Creating users, setting DNS, making datasets, unlocking encryption, publishing
shares — the write side of the API, and the shapes that surprise people.

Everything here works from the CLI with no script at all, because `call` types
its fields from the method's own schema. Start by asking the appliance what a
method takes:

```sh
pytruenas help user.create nas1
```

```text
pytruenas call user.create <target> -- --field=value ...

Create a new user.

Fields (after --):
  --username=<string>                   (required)
  --full_name=<string>                  (required)
  --uid=<integer|null>                  (default null)
      Leave unset to allocate one.
  --shell=<string>                      (default "/usr/bin/zsh")
      one of: '/usr/bin/zsh', '/usr/bin/bash', '/usr/sbin/nologin'
  ...
Returns: integer
```

`pytruenas help user` lists a namespace; `pytruenas help all` lists every
namespace. The schema comes from the API itself and needs no shell access — see
[Where the schema comes from](#where-the-schema-comes-from).

## Users and groups

```sh
pytruenas call group.create nas1 -- --name=svc-backup --smb=false
pytruenas call user.create nas1 -- \
    --username=svc-backup --full_name='Backup service' \
    --group_create=true --home=/var/empty --shell=/usr/sbin/nologin \
    --password_disabled=true --sshpubkey=@~/.ssh/id_ed25519.pub
```

`=@path` reads the value from a file, which is what you want for a key or a
certificate. Booleans are real JSON booleans — `--smb=false` sends `false`, not
`"false"`.

In Python, `_upsert` makes the same thing idempotent: it matches on the selector
fields, creates when there is no match, and otherwise diffs the record first so
a second run sends nothing.

```python
nas.api.user._upsert(
    ("username",),
    username="svc-backup",
    full_name="Backup service",
    group_create=True,
    home="/var/empty",
)
```

## Network and DNS

`network.configuration` is a **singleton**: one record, read with `config()` and
written with `update(payload)`. There is nothing to query and no id.

```python
config = nas.api.network.configuration.config()
nas.api.network.configuration.update({"nameserver2": "10.0.0.53"})
```

Three things to know:

- The resolvers are **three scalar fields** — `nameserver1`, `nameserver2`,
  `nameserver3` — not a list.
- `domain` is this host's own DNS domain; `domains` is the **search list**. Easy
  to swap.
- `state` is read-only and reports what the host is *actually* using, which is
  where a DHCP-supplied resolver appears even though the configured field is
  empty.

!!! warning
    Changing DNS or an address on the host you are talking to is how a
    provisioning run locks itself out. An interface change is staged behind
    `interface.commit` with a checkin window that **rolls it back** if you never
    confirm — use it:

    ```python
    nas.api.interface.update("ens18", {"ipv4_dhcp": False, "aliases": [...]})
    nas.api.interface.commit({"checkin_timeout": 60})
    nas.api.interface.checkin()      # only if you can still reach it
    ```

## Datasets and encryption

A dataset's **id is its path** (`tank/backups`), so `_get("tank/backups")` is
the lookup:

```python
dataset = nas.api.pool.dataset._get("tank/backups")
```

A ZFS **property is not a scalar**. `quota` reads back as a dict while you set
a plain number:

```python
{"value": "10G", "parsed": 10737418240, "rawvalue": "10737418240", "source": "LOCAL"}
```

`_update` compares either half against the scalar you pass, so a property that
already matches is left alone. Without that, every run would rewrite the field
and report a change that never happened.

To unlock, unlock the **encryption root** — a child inherits its parent's key,
so the dataset you must act on is `encryption_root`, not necessarily the one you
asked about. `encryption_summary` says what each dataset in the tree needs, and
`unlock` is a **job**: it returns a job id, so wait on it.

```python
for row in nas.api.pool.dataset.encryption_summary("tank"):
    print(row["name"], row.get("unlock_successful"), row.get("unlock_error"))

jobid = nas.api.pool.dataset.unlock("tank", {"recursive": True, "datasets": []})
nas.wait(jobid, callback=lambda job: print(job["progress"]))
```

A passphrase-encrypted dataset needs the passphrase supplied per dataset in
`datasets`; a key-encrypted one unlocks from the stored key alone.

## Shares

The two types are not symmetric. SMB is keyed by `name` and carries a `purpose`
preset plus an `options` sub-object; NFS is keyed by `path`, has no name, and
controls access with `networks`/`hosts`, `ro`, and the `maproot_*`/`mapall_*`
mapping.

```sh
pytruenas call sharing.smb.create nas1 -- \
    --name=media --path=/mnt/tank/media --enabled=true --browsable=true

pytruenas call sharing.nfs.create nas1 -- \
    --path=/mnt/tank/media --ro=true --networks=10.0.0.0/24
```

`locked` on either means the share's dataset is encrypted and not unlocked: the
share looks fine and serves nothing.

**A share does nothing until its service runs** — a separate API, and the step
people forget. `enable` is start-on-boot; `state` is now.

```python
for service in nas.api.service.query([["service", "in", ["cifs", "nfs"]]]):
    print(service["service"], service["state"], service["enable"])

nas.api.service.update("cifs", {"enable": True})
nas.api.service.start("cifs")
```

## A whole flow

[`examples/provision/`](https://github.com/jose-pr/pytruenas/tree/main/examples/provision)
is all of the above as a RunPath flow — **dry-run by default**, idempotent, and
fanned out per target:

```sh
pytruenas --cmdspath examples provision nas1              # plan only
pytruenas --cmdspath examples provision nas1 -- --apply   # make the changes
```

## Where the schema comes from

`help` and `call`'s field typing ask the API for **one namespace at a time**
(`core.get_services`, then `core.get_methods(<service>)`). Both middleware
methods declare no roles and need no command access, so this works for an
API-key account with **no shell, no SSH and no web shell** — and one namespace is
a small answer (13 methods, ~100 KB for `user` on 26.0). Answers are cached under
`$PYTRUENAS_CACHE`, per host, version and namespace.

`--refresh-api` re-fetches, which you need only after upgrading an appliance in
place. `--no-schema` (on `call`) skips the schema entirely and types fields the
way `-p` does.

`help --dump` reads the full `middlewared --dump-api` definition instead. That
needs command access on the target and is ~24 MB taking about 75 s to build, so
it is only worth it for `--api-version` — describing an API version older than
the one running, which the live API cannot report. It is also what
`generate-typings` consumes.
