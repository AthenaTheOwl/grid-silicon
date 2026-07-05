from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_dry_run_cli_writes_report(tmp_path: Path) -> None:
    out = tmp_path / "2026-05.jsonl"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "grid_silicon",
            "ingest",
            "--iso",
            "ercot",
            "--month",
            "2026-05",
            "--dry-run",
            "--out",
            str(out),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "wrote 1 row" in result.stdout
    row = json.loads(out.read_text(encoding="utf-8").splitlines()[0])
    assert row["project_id"] == "grds-ercot-ll-2026-001"
    assert row["source_mode"] == "fixture"


def test_live_cli_blocks_without_fixture_mode() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "grid_silicon",
            "ingest",
            "--iso",
            "ercot",
            "--month",
            "2026-05",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "live ERCOT fetch is not enabled" in (result.stderr + result.stdout)


def _ingest(fixture_dir: Path, tmp_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "grid_silicon",
            "ingest",
            "--iso",
            "ercot",
            "--month",
            "2026-05",
            "--dry-run",
            "--fixture-dir",
            str(fixture_dir),
            "--out",
            str(tmp_path / "out.jsonl"),
        ],
        capture_output=True,
        text=True,
    )


def _show(report: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "grid_silicon", "show", "--report", str(report)],
        capture_output=True,
        text=True,
    )


def test_ingest_missing_fixture_dir_exits_clean(tmp_path: Path) -> None:
    result = _ingest(tmp_path / "does" / "not" / "exist", tmp_path)
    assert result.returncode != 0
    assert "Traceback" not in result.stderr
    assert "fixture not found" in result.stderr


def test_ingest_queue_path_is_directory_exits_clean(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "fixture"
    (fixture_dir / "queue.csv").mkdir(parents=True)  # a directory where a CSV is expected
    result = _ingest(fixture_dir, tmp_path)
    assert result.returncode != 0
    assert "Traceback" not in result.stderr


def test_ingest_non_numeric_value_exits_clean(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "fixture"
    fixture_dir.mkdir()
    (fixture_dir / "queue.csv").write_text(
        "project_id_raw,project_name,county,mw_requested,"
        "requested_in_service,status_code,last_updated\n"
        "LL-2026-002,Bad,Test,NOTANUMBER,2026-12,under_ercot_review,2026-05-01\n",
        encoding="utf-8",
    )
    result = _ingest(fixture_dir, tmp_path)
    assert result.returncode != 0
    assert "Traceback" not in result.stderr
    assert "mw_requested" in result.stderr


def test_show_empty_report_exits_clean(tmp_path: Path) -> None:
    report = tmp_path / "blank.jsonl"
    report.write_text("\n   \n\n", encoding="utf-8")
    result = _show(report)
    assert result.returncode != 0
    assert "Traceback" not in result.stderr
    assert "no report rows" in result.stderr


def test_show_malformed_report_exits_clean(tmp_path: Path) -> None:
    report = tmp_path / "bad.jsonl"
    report.write_text("this is not json\n", encoding="utf-8")
    result = _show(report)
    assert result.returncode != 0
    assert "Traceback" not in result.stderr
    assert "cannot read report" in result.stderr


def test_compare_reports_prints_derived_month_delta(tmp_path: Path) -> None:
    may = tmp_path / "2026-05.jsonl"
    june = tmp_path / "2026-06.jsonl"
    for month, out in [("2026-05", may), ("2026-06", june)]:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "grid_silicon",
                "ingest",
                "--iso",
                "ercot",
                "--month",
                month,
                "--dry-run",
                "--out",
                str(out),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    may_row = json.loads(may.read_text(encoding="utf-8").splitlines()[0])
    june_row = json.loads(june.read_text(encoding="utf-8").splitlines()[0])
    observed_delta = int(june_row["mw_observed_energized"] - may_row["mw_observed_energized"])
    phantom_delta = int(june_row["phantom_mw"] - may_row["phantom_mw"])

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "grid_silicon",
            "compare",
            "--before",
            str(may),
            "--after",
            str(june),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "month-over-month delta" in result.stdout
    assert f"{observed_delta:+d}MW" in result.stdout
    assert f"{phantom_delta:+d}MW" in result.stdout
    assert "less phantom" in result.stdout


def test_compare_without_overlap_exits_clean(tmp_path: Path) -> None:
    before = tmp_path / "before.jsonl"
    after = tmp_path / "after.jsonl"
    before.write_text('{"project_id":"a","month":"2026-05"}\n', encoding="utf-8")
    after.write_text('{"project_id":"b","month":"2026-06"}\n', encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "grid_silicon",
            "compare",
            "--before",
            str(before),
            "--after",
            str(after),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "Traceback" not in result.stderr
    assert "no overlapping project_id" in result.stderr
