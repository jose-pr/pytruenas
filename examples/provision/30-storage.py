"""Step 3 -- verify or create a dataset, and unlock an encrypted one.

Three things here are specific to TrueNAS and catch people out:

**A dataset id is its path.** ``pool.dataset`` is keyed by ``tank/backups``, not
by a number, so ``_get("tank/backups")`` is the lookup and there is no separate
id to remember.

**A ZFS property is not a scalar.** ``quota`` comes back as
``{"value": ..., "parsed": ..., "rawvalue": "0", "source": "DEFAULT"}`` while a
caller sets the plain value. ``_update`` compares either half against the scalar
you pass, so a property that already matches is left alone -- without that, every
run would rewrite the field and report a change that never happened.

**Unlocking needs the encryption root.** A child inherits its parent's key, so
the dataset you must unlock is ``encryption_root``, not necessarily the one you
asked about. ``encryption_summary`` says what each dataset in the tree needs, and
``unlock`` is a **job**: it returns a job id, so wait on it.
"""

from __future__ import annotations

POOL = "data"
DATASET = f"{POOL}/provision-example"

#: 10 GiB, as a byte count. ZFS takes bytes; the human string is what it
#: reports back.
QUOTA = 10 * 1024**3


def main(client, args, logger):
    plan = args.plan

    pools = [p["name"] for p in client.api.pool.query()]
    if POOL not in pools:
        logger.error("pool %r not found (have: %s); skipping storage", POOL, pools)
        return

    # -- verify or create --------------------------------------------------
    dataset = client.api.pool.dataset._get(DATASET)
    if dataset is None:
        plan.change(
            f"create dataset {DATASET} (quota {QUOTA})",
            lambda: client.api.pool.dataset._create(
                name=DATASET,
                type="FILESYSTEM",
                compression="LZ4",
                atime="OFF",
                quota=QUOTA,
            ),
        )
    else:
        logger.info(
            "dataset %s exists: %s used, quota %s",
            DATASET,
            dataset.get("used", {}).get("value"),
            (dataset.get("quota") or {}).get("value") or "none",
        )
        # Pass the scalar; `_update` reads the property shape on the other side
        # and sends nothing when it already agrees.
        current = (dataset.get("quota") or {}).get("parsed")
        if current != QUOTA:
            plan.change(
                f"set quota on {DATASET} to {QUOTA}",
                lambda: client.api.pool.dataset._update(DATASET, quota=QUOTA),
            )
        else:
            plan.ok(f"quota on {DATASET} already {QUOTA}")

    # -- encryption --------------------------------------------------------
    for entry in client.api.pool.dataset.query([["pool", "=", POOL]]):
        if not entry.get("encrypted"):
            continue
        root = entry.get("encryption_root") or entry["name"]
        if not entry.get("locked"):
            logger.info(
                "%s is encrypted and unlocked (key %s, root %s)",
                entry["name"],
                entry.get("key_format", {}).get("value"),
                root,
            )
            continue

        # What does this tree need to unlock? The summary answers per dataset,
        # which matters when only some children are locked.
        summary = client.api.pool.dataset.encryption_summary(root)
        needs = [
            row["name"] for row in summary if row.get("unlock_successful") is False
        ]
        logger.info("%s is LOCKED; unlock would affect %s", root, needs or [root])

        def unlock(root=root):
            # `unlock` is a job: it returns an id rather than a result, so the
            # caller has to wait for it. `_upsert`/`_update` do this for you;
            # a direct call does not.
            jobid = client.api.pool.dataset.unlock(
                root,
                {"recursive": True, "datasets": []},
            )
            return client.wait(
                jobid,
                callback=lambda job: logger.debug(
                    "unlock %s: %s", job.get("state"), job.get("progress", {})
                ),
            )

        # Passphrase-encrypted datasets need the passphrase supplied in
        # `datasets`; a key-encrypted one unlocks from the stored key alone.
        plan.change(f"unlock {root}", unlock)

    # -- a snapshot is a cheap, reversible checkpoint ----------------------
    if client.api.pool.dataset._get(DATASET) is not None:
        name = f"{DATASET}@provision-example"
        if client.api.pool.snapshot._get(name) is None:
            plan.change(
                f"snapshot {name}",
                lambda: client.api.pool.snapshot._create(
                    dataset=DATASET, name="provision-example"
                ),
            )
        else:
            plan.ok(f"snapshot {name} exists")
