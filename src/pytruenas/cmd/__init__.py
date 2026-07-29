"""Built-in ``pytruenas`` command modules.

Each module here is one subcommand, exposing ``run(client, args, logger)`` plus
the optional ``register``/``init``/``success``/``finally_`` hooks; see
:mod:`pytruenas.utils.cmd` for the full contract. They are discovered by name
rather than imported here, so adding a module is all it takes to add a command.

This file exists to make that discovery work when pytruenas is **zipped**. The
directory has no runtime need for an ``__init__.py`` -- an implicit namespace
package resolves fine from a filesystem -- but ``zipimport`` does not implement
namespace packages at all. Without this file the deployed zipapp imports
pytruenas successfully and then reports no commands whatsoever
(``No module named 'pytruenas.cmd'``, and a subcommand list of ``{}``), which
reads like a discovery bug rather than a packaging one.
"""
