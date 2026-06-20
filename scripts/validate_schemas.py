from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    from grid_silicon.validation import validate_reports

    for path in sorted((ROOT / "schemas").glob("*.schema.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if "$schema" not in data or "$id" not in data:
            print(f"ERROR: {path} missing $schema or $id")
            return 1
    errors = validate_reports(ROOT)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("validate_schemas OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
