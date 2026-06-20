"""Small validators for v0.1 schemas without a runtime dependency."""

from __future__ import annotations

from pathlib import Path

from .report import read_jsonl

REQUIRED_REPORT_FIELDS = {
    "month": str,
    "iso": str,
    "project_id": str,
    "project_name": str,
    "county": str,
    "mw_announced": (int, float),
    "mw_observed_energized": (int, float),
    "phantom_mw": (int, float),
    "realness_score": int,
    "status_code": str,
    "source_mode": str,
    "evidence_ids": list,
    "evidence": list,
    "notes": str,
}


def validate_report_row(row: dict[str, object]) -> list[str]:
    errors: list[str] = []
    for field, expected in REQUIRED_REPORT_FIELDS.items():
        if field not in row:
            errors.append(f"missing field {field}")
            continue
        if not isinstance(row[field], expected):
            errors.append(f"{field} has wrong type")
    score = row.get("realness_score")
    if isinstance(score, int) and not 0 <= score <= 100:
        errors.append("realness_score must be 0..100")
    ids = row.get("evidence_ids")
    evidence = row.get("evidence")
    if isinstance(ids, list) and len(ids) < 5:
        errors.append("evidence_ids must contain at least five entries")
    if isinstance(evidence, list):
        for idx, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(f"evidence[{idx}] must be an object")
                continue
            if not item.get("source_url"):
                errors.append(f"evidence[{idx}] missing source_url")
    return errors


def validate_report_file(path: Path) -> list[str]:
    errors: list[str] = []
    for row_idx, row in enumerate(read_jsonl(path), start=1):
        for error in validate_report_row(row):
            errors.append(f"{path}:{row_idx}: {error}")
    return errors


def validate_reports(root: Path) -> list[str]:
    reports_dir = root / "reports"
    if not reports_dir.exists():
        return ["reports directory is missing"]
    errors: list[str] = []
    for path in sorted(reports_dir.glob("*.jsonl")):
        errors.extend(validate_report_file(path))
    if not list(reports_dir.glob("*.jsonl")):
        errors.append("no reports/*.jsonl files found")
    return errors
