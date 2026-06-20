from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    from grid_silicon.report import read_jsonl

    reports = sorted((ROOT / "reports").glob("*.jsonl"))
    if not reports:
        print("ERROR: no reports/*.jsonl files found")
        return 1
    failures: list[str] = []
    for report in reports:
        for idx, row in enumerate(read_jsonl(report), start=1):
            evidence = row.get("evidence", [])
            if not isinstance(evidence, list) or len(evidence) < 5:
                failures.append(f"{report}:{idx}: fewer than five evidence items")
                continue
            for item in evidence:
                if not isinstance(item, dict) or not item.get("source_url"):
                    failures.append(f"{report}:{idx}: evidence item missing source_url")
    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        return 1
    print("traceability OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
