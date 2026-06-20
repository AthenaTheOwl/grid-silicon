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
