"""Root shim so `python -m grid_silicon` works from a fresh checkout."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    src = Path(__file__).resolve().parent / "src"
    sys.path.insert(0, str(src))
    from grid_silicon.cli import main as cli_main

    return cli_main()


if __name__ == "__main__":
    raise SystemExit(main())
