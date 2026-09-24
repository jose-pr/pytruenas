# Examples

Runnable scripts and flows. Each is complete enough to copy into your own tool
and adapt; none of them is imported by the package.

| | |
|---|---|
| [`simple_client_from_yaml.py`](simple_client_from_yaml.py) | Wire a small YAML file to a client by hand. The long way round — the CLI does config, targets, fan-out and logging for you. |
| [`runpath/health/`](runpath/health/) | A read-only flow: system info, pool health, a report. Shows the three step signatures a RunPath accepts. |
| [`provision/`](provision/) | Provisioning a system end to end — users, DNS, datasets and encryption, shares and their services. **Dry-run by default.** |

## Running the flows

A **RunPath** is a directory of numbered `NN-name.py` steps, run in order and
fanned out once per target — each target gets its own client and its own copy of
the command instance, so nothing leaks between them.

```sh
pytruenas --cmdspath examples provision nas1              # plan only, changes nothing
pytruenas --cmdspath examples provision nas1 -- --apply   # make the changes
pytruenas --cmdspath examples provision --parallel 4 'nas[1-3]'
```

`--rcopts` selects steps by name (`!` disables, a bare name re-enables), so you
can run one part of a flow:

```sh
pytruenas --cmdspath examples provision --rcopts '!*,shares' nas1
```

## What `provision/` covers

Every step is idempotent: run it twice and the second run reports no changes.
That is what `_upsert`/`_update` buy you — they diff against the current record
and send only what differs.

| step | what it shows |
|---|---|
| [`10-users.py`](provision/10-users.py) | A group and a key-only service account with `_upsert`/`_update` diffing. |
| [`20-network.py`](provision/20-network.py) | The `network.configuration` **singleton**: `config()`/`update()`, three scalar `nameserverN` slots rather than a list, `domain` vs the `domains` search list, and read-only `state` showing what DHCP actually supplied. Reads interfaces rather than writing them — an address change is staged behind `interface.commit` with a checkin window precisely because a bad one cuts off the connection you are using. |
| [`30-storage.py`](provision/30-storage.py) | A dataset keyed by its **path**, a ZFS **property** (`quota` comes back `{value, parsed, rawvalue, source}` while you set the scalar), `encryption_summary` and unlocking at the **`encryption_root`** — and `unlock` being a **job** you have to wait on. |
| [`40-shares.py`](provision/40-shares.py) | SMB (keyed by `name`, with a `purpose` preset and an `options` sub-object) and NFS (keyed by `path`, access via `networks`/`hosts`/`ro`/`maproot_*`), plus enabling and starting the service — the step people forget, where the share exists and still serves nothing. |

## Finding the field names yourself

The examples name real 26.0 fields, but the appliance is the authority and its
schema changes between versions. Ask it:

```sh
pytruenas help user.create nas1        # every field, with types, defaults, enums
pytruenas help sharing.smb nas1        # the methods of a namespace
pytruenas help nas1                    # every namespace
```

The same schema drives `call`, so a one-off change needs no script and no JSON:

```sh
pytruenas call user.create nas1 -- --username=svc --full_name='Svc' --group_create=true
```
