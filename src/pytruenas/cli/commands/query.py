"""Query a TrueNAS namespace and print the matching records as JSON."""

from __future__ import annotations

from logging import Logger

from duho import Arg, Meta

from pytruenas import TrueNASClient
from pytruenas.cli._args import PyTrueNASArgs, emit_json, json_value, split_assignment


class Args(PyTrueNASArgs):
    """Declared CLI fields for ``query`` (added ahead of the trailing targets)."""

    namespace: str
    "API namespace, e.g. user or pool.dataset"
    ("namespace",)  # type: ignore

    # NOTE: not -q -- duho's LoggingArgs owns -q (quiet), and duho.app builds each
    # subcommand parser with parents=[root], so global short flags are inherited
    # and would collide.
    # duho 0.5.0+ already defaults a list-typed OPTION to action="append",
    # nargs=None (one value per occurrence, `-f a -f b`) -- no explicit
    # Meta(action=..., nargs=...) needed here.
    query: "Arg[list[str], Meta(metavar='KEY=VALUE')]" = []
    "Filter on a field (repeatable), e.g. -f username=root"
    ("--filter", "-f")  # type: ignore


def run(client: TrueNASClient, args: Args, logger: Logger):
    filter = {}
    for entry in args.query or []:
        if not entry:
            continue
        try:
            key, value = split_assignment(entry)
        except ValueError as exc:
            logger.error("%s", exc)
            return 2
        # Typed like `call -p`: a filter value was always a string, so
        # `-f uid=0` or `-f locked=true` matched nothing at all.
        filter[key] = json_value(value)

    logger.info("Querying %s with %s", args.namespace, filter or "no filter")
    result = client.api[args.namespace]._query(**filter)
    emit_json(result, args)
