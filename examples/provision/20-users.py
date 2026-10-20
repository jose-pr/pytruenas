"""Step 2 -- a group, a service account, and an SSH key for it.

Shows the ``_upsert`` helper doing the work a hand-written script gets wrong:
it looks for a match on the selector fields, creates when there is none,
and otherwise **diffs** the record first so a second run sends nothing.

The field names here are real: ``user.create`` takes ``username``,
``full_name``, ``group``/``group_create``, ``home``, ``shell``, ``sshpubkey``,
``password_disabled``, ``smb``, ``sudo_commands_nopasswd``. Ask the appliance
itself for the full list with ``pytruenas help user.create <target>``.
"""

from __future__ import annotations

GROUP = "svc-backup"
USER = "svc-backup"

#: Where the account's home is created: the dataset step 1 made. TrueNAS
#: refuses an SSH key for a user whose home is not on a data pool.
HOME_PARENT = "/mnt/data/provision-example"

#: A real deployment reads this from wherever it keeps public keys; the CLI's
#: `--sshpubkey=@path` does the same thing for a one-off.
PUBKEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAExampleKeyForTheExample"


def main(client, args, logger):
    plan = args.plan

    # -- the group ---------------------------------------------------------
    # A service account gets its own group, so its files are not readable by
    # everything else that happens to share a shared group.
    group = client.api.group._get(group=GROUP)
    if group is None:
        gid = plan.change(
            f"create group {GROUP}",
            lambda: client.api.group._create(name=GROUP, smb=False),
        )
    else:
        gid = group["id"]
        plan.ok(f"group {GROUP} exists (gid {group['gid']})")

    # -- the user ----------------------------------------------------------
    existing = client.api.user._get(username=USER)
    desired = dict(
        full_name="Backup service account",
        home=f"{HOME_PARENT}/{USER}",
        shell="/usr/sbin/nologin",
        # A service account authenticates by key, never by password.
        password_disabled=True,
        sshpubkey=PUBKEY,
        smb=False,
    )

    if existing is None:
        plan.change(
            f"create user {USER}",
            # `home` names the parent; `home_create` makes `<home>/<username>`,
            # which is the home the record then reports.
            lambda: client.api.user._create(
                username=USER,
                group=gid,
                **{**desired, "home": HOME_PARENT, "home_create": True},
            ),
        )
    else:
        # `_update` diffs against the current record, so passing the whole
        # desired state is safe and idempotent -- it sends only what differs.
        from pytruenas.query import diff

        pending = diff(existing, desired)
        if pending:
            plan.change(
                f"update user {USER}: {', '.join(sorted(pending))}",
                lambda: client.api.user._update(existing["id"], **desired),
            )
        else:
            plan.ok(f"user {USER} matches the desired state")

    # -- what the account can do ------------------------------------------
    # Roles and privileges live on a separate API; listing them is enough to
    # show where to look.
    logger.debug(
        "account currently has roles: %s",
        (client.api.user._get(username=USER) or {}).get("roles"),
    )
