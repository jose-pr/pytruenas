"""Step 4 -- view, create and update SMB and NFS shares, and start the service.

A share does nothing until its service runs, which is a separate API
(``service.query`` / ``service.update`` / ``service.start``) and the step people
forget: the share exists, the client cannot see it.

The two share types have genuinely different shapes, so this reads both rather
than pretending they are symmetric:

* ``sharing.smb`` is keyed by ``name`` (the share name a client connects to),
  and 26.0 carries a ``purpose`` preset (``DEFAULT_SHARE``, ...) plus an
  ``options`` sub-object, rather than the long flat list of booleans it used to
  have. ``pytruenas help sharing.smb.create <target>`` prints the current set.
* ``sharing.nfs`` is keyed by ``path`` and has no name at all; access is
  ``networks``/``hosts`` (allow lists), ``ro``, and the ``maproot_*``/``mapall_*``
  identity mapping.

``locked`` on either means the share's dataset is encrypted and not unlocked --
worth reporting, because the share looks fine and still serves nothing.
"""

from __future__ import annotations

POOL = "data"
DATASET = f"{POOL}/provision-example"
PATH = f"/mnt/{DATASET}"

SMB_NAME = "provision-example"
#: Who may mount the NFS export. An empty list means "anyone who can reach it",
#: which is not a default to ship.
NFS_NETWORKS = ["192.0.2.0/24"]


def main(client, args, logger):
    plan = args.plan

    # -- what exists today -------------------------------------------------
    for share in client.api.sharing.smb.query():
        logger.info(
            "SMB %-20s %-28s enabled=%s purpose=%s%s",
            share["name"],
            share["path"],
            share["enabled"],
            share.get("purpose"),
            " LOCKED" if share.get("locked") else "",
        )
    for share in client.api.sharing.nfs.query():
        logger.info(
            "NFS %-28s enabled=%s ro=%s networks=%s%s",
            share["path"],
            share["enabled"],
            share.get("ro"),
            share.get("networks") or "any",
            " LOCKED" if share.get("locked") else "",
        )

    if client.api.pool.dataset._get(DATASET) is None and plan.apply:
        logger.warning("dataset %s does not exist; skipping shares", DATASET)
        return

    # -- SMB ---------------------------------------------------------------
    smb = client.api.sharing.smb._get(name=SMB_NAME)
    if smb is None:
        plan.change(
            f"create SMB share {SMB_NAME} -> {PATH}",
            lambda: client.api.sharing.smb._create(
                name=SMB_NAME,
                path=PATH,
                comment="Created by the pytruenas provisioning example",
                enabled=True,
                readonly=False,
                browsable=True,
            ),
        )
    else:
        # `_upsert` would do this lookup-then-branch for us; spelled out here so
        # the two halves are visible. It diffs, so a matching share is untouched.
        plan.change(
            f"ensure SMB share {SMB_NAME} points at {PATH} and is enabled",
            lambda: client.api.sharing.smb._upsert(
                ("name",),
                name=SMB_NAME,
                path=PATH,
                enabled=True,
            ),
        )

    # -- NFS ---------------------------------------------------------------
    nfs = client.api.sharing.nfs._get(path=PATH)
    if nfs is None:
        plan.change(
            f"create NFS export {PATH} for {NFS_NETWORKS}",
            lambda: client.api.sharing.nfs._create(
                path=PATH,
                comment="Created by the pytruenas provisioning example",
                enabled=True,
                ro=True,
                networks=NFS_NETWORKS,
            ),
        )
    elif sorted(nfs.get("networks") or []) != sorted(NFS_NETWORKS):
        plan.change(
            f"restrict NFS export {PATH} to {NFS_NETWORKS}",
            lambda: client.api.sharing.nfs._update(nfs["id"], networks=NFS_NETWORKS),
        )
    else:
        plan.ok(f"NFS export {PATH} already restricted to {NFS_NETWORKS}")

    # -- the services ------------------------------------------------------
    # A share with a stopped service is the classic "it exists but nothing can
    # mount it". `enable` is start-on-boot; `state` is now.
    services = {s["service"]: s for s in client.api.service.query()}
    for name, label in (("cifs", "SMB"), ("nfs", "NFS")):
        service = services.get(name)
        if service is None:
            logger.warning("no %s service on this host", label)
            continue
        if not service["enable"]:
            plan.change(
                f"enable {label} at boot",
                lambda name=name: client.api.service.update(name, {"enable": True}),
            )
        if service["state"] != "RUNNING":
            plan.change(
                f"start {label}",
                lambda name=name: client.api.service.start(name),
            )
        else:
            plan.ok(f"{label} service running (enable={service['enable']})")
