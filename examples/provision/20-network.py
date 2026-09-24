"""Step 2 -- DNS and the global network configuration.

``network.configuration`` is a **singleton**: there is one record, read with
``config()`` and written with ``update(payload)``, so there is nothing to query
and no id to pass. The nameservers are three separate scalar fields
(``nameserver1``, ``nameserver2``, ``nameserver3``) rather than a list -- a
shape worth seeing before you go looking for an array that does not exist.

Two fields here are easy to confuse: ``domain`` is this host's own DNS domain,
and ``domains`` is the *search* list. ``state`` is read-only and reports what
the host is actually using, which is where a DHCP-supplied nameserver shows up
even though the configured field is empty.

This step is deliberately conservative: it only *adds* a nameserver when a slot
is free, and never removes one. Changing DNS on a host you are talking to over
the network is how a provisioning run locks itself out.
"""

from __future__ import annotations

#: Resolvers this flow wants present. Adjust for your own site.
WANTED = ["192.0.2.53"]

#: The DNS search list.
SEARCH = ["example.com"]

SLOTS = ("nameserver1", "nameserver2", "nameserver3")


def main(client, args, logger):
    plan = args.plan
    config = client.api.network.configuration.config()

    logger.info(
        "hostname %s.%s, gateway %s",
        config.get("hostname"),
        config.get("domain") or "(no domain)",
        config.get("ipv4gateway") or "(none)",
    )
    # `state` is what the host resolved to -- including anything DHCP handed it,
    # which never appears in the configured fields.
    state = config.get("state") or {}
    logger.info(
        "configured resolvers %s; in use %s",
        [config.get(s) for s in SLOTS if config.get(s)],
        [state.get(s) for s in SLOTS if state.get(s)],
    )

    current = [config.get(slot) or "" for slot in SLOTS]
    payload = {}
    for wanted in WANTED:
        if wanted in current:
            plan.ok(f"nameserver {wanted} already configured")
            continue
        try:
            free = current.index("")
        except ValueError:
            # Refusing beats silently overwriting a resolver someone chose.
            logger.warning(
                "no free nameserver slot for %s; all three are set (%s)",
                wanted,
                current,
            )
            continue
        current[free] = wanted
        payload[SLOTS[free]] = wanted

    configured_search = config.get("domains") or []
    missing = [d for d in SEARCH if d not in configured_search]
    if missing:
        payload["domains"] = [*configured_search, *missing]
    else:
        plan.ok(f"search domains already include {SEARCH}")

    if payload:
        plan.change(
            f"update network configuration: {', '.join(sorted(payload))}",
            lambda: client.api.network.configuration.update(payload),
        )

    # -- interfaces are a different shape ----------------------------------
    # Each interface carries its own `aliases` list, and a change to one is
    # staged until `interface.commit` -- with a checkin window that rolls it
    # back if you never confirm. That is exactly what you want when a bad
    # address would cut off the connection you are using, and it is why this
    # example reads interfaces rather than writing them.
    for interface in client.api.interface.query():
        addresses = [a.get("address") for a in interface.get("aliases") or []]
        logger.info(
            "interface %s (%s): dhcp=%s addresses=%s",
            interface["name"],
            interface["type"],
            interface.get("ipv4_dhcp"),
            addresses or "(none)",
        )
