import sys
from pathlib import Path

from .main import MODULE, main
from .utils.logging import init_stderr_logging

init_stderr_logging()

if __name__ == "__main__":
    main(name=MODULE)
