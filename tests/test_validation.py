from __future__ import annotations

from pathlib import Path

from grid_silicon.validation import validate_report_file


def test_checked_in_report_validates() -> None:
    errors = validate_report_file(Path("reports/2026-05.jsonl"))
    assert errors == []
