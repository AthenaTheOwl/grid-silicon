from __future__ import annotations

from pathlib import Path

from grid_silicon.validation import validate_report_file, validate_report_row


def _good_row() -> dict[str, object]:
    return {
        "month": "2026-05",
        "iso": "ercot",
        "project_id": "grds-ercot-ll-2026-001",
        "project_name": "Sample",
        "county": "Ellis",
        "mw_announced": 1200.0,
        "mw_observed_energized": 120.0,
        "phantom_mw": 1080.0,
        "realness_score": 37,
        "status_code": "under_ercot_review",
        "source_mode": "fixture",
        "evidence_ids": ["a", "b", "c", "d", "e"],
        "evidence": [
            {"source_url": "https://example.test/1"},
            {"source_url": "https://example.test/2"},
            {"source_url": "https://example.test/3"},
            {"source_url": "https://example.test/4"},
            {"source_url": "https://example.test/5"},
        ],
        "notes": "ok",
    }


def test_checked_in_report_validates() -> None:
    errors = validate_report_file(Path("reports/2026-05.jsonl"))
    assert errors == []


def test_good_row_has_no_errors() -> None:
    assert validate_report_row(_good_row()) == []


def test_wrong_field_type_error() -> None:
    row = _good_row()
    row["month"] = 5  # expected str
    assert "month has wrong type" in validate_report_row(row)


def test_realness_score_out_of_range_error() -> None:
    row = _good_row()
    row["realness_score"] = 101
    assert "realness_score must be 0..100" in validate_report_row(row)


def test_too_few_evidence_ids_error() -> None:
    row = _good_row()
    row["evidence_ids"] = ["a", "b", "c", "d"]
    assert "evidence_ids must contain at least five entries" in validate_report_row(row)


def test_evidence_item_missing_source_url_error() -> None:
    row = _good_row()
    row["evidence"][2] = {"category": "permit"}  # no source_url
    assert "evidence[2] missing source_url" in validate_report_row(row)
