"""Step 2 -- ``@step`` with a shorter signature.

A decorated step may declare fewer parameters and is handed only those, so a
step that never logs does not have to name a ``logger`` it ignores. The order
is fixed: ``client``, then ``args``, then ``logger``.
"""

from __future__ import annotations

from pytruenas.utils.runpath import step


@step
def main(client, args):
    for pool in client.api.pool.query():
        if pool["healthy"]:
            continue
        # No logger parameter here -- record it for the reporting step instead.
        args.findings.append(("pool", f"{pool['name']} is {pool['status']}"))
