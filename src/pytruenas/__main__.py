"""``python -m pytruenas`` -- the same entry point as the console script."""

from duho.logging import init_stderr_logging

from .main import main

if __name__ == "__main__":
    # Logging is set up here, not at import: importing `pytruenas.__main__`
    # (a test, a wrapper) must not reconfigure the importer's logging.
    init_stderr_logging()
    # `raise SystemExit(...)`, not a bare call: main()'s exit code was
    # discarded, so `python -m pytruenas call nope host` exited 0 and every
    # shell and CI step read a failed run as a success.
    raise SystemExit(main("pytruenas"))
