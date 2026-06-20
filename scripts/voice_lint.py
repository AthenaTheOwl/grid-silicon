from __future__ import annotations

import sys
from pathlib import Path

BANNED_FAIL = (
    "leverage",
    "demonstrates",
    "comprehensive",
    "synergy",
    "robust",
    "best-in-class",
    "seamless",
    "cutting-edge",
)


def iter_files(paths: list[str]) -> list[Path]:
    if not paths:
        paths = ["README.md", "specs", "decisions", "reports", "docs"]
    out: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            out.extend(sorted(path.rglob("*.md")))
        elif path.exists() and path.suffix.lower() == ".md":
            out.append(path)
    return out


def main(argv: list[str] | None = None) -> int:
    failures: list[str] = []
    for path in iter_files(list(argv or sys.argv[1:])):
        text = path.read_text(encoding="utf-8").lower()
        for word in BANNED_FAIL:
            if word in text:
                failures.append(f"{path}: banned word {word}")
    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        return 1
    print("voice_lint: clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
