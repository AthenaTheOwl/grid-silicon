from __future__ import annotations

from pathlib import Path

import pytest

from grid_silicon.ercot import load_evidence, load_observations, load_queue

FIXTURE = Path("data/fixtures/ercot/2026-05")

QUEUE_HEADER = (
    "project_id_raw,project_name,county,mw_requested,"
    "requested_in_service,status_code,last_updated"
)
OBS_HEADER = "project_id_raw,observed_energized_mw,approval_status,observed_on"
EVIDENCE_HEADER = (
    "evidence_id,project_id_raw,category,label,source_url,extracted_on,weight"
)


def test_load_queue_fixture() -> None:
    projects = load_queue(FIXTURE / "queue.csv")
    assert len(projects) == 1
    assert projects[0].project_id_raw == "LL-2026-001"
    assert projects[0].mw_requested == 1200


def test_load_observations_fixture() -> None:
    observations = load_observations(FIXTURE / "energization.csv")
    assert observations["LL-2026-001"].observed_energized_mw == 120


def test_load_evidence_fixture_has_five_items() -> None:
    evidence = load_evidence(FIXTURE / "evidence.csv")
    assert len(evidence["LL-2026-001"]) == 5
    assert {item.category for item in evidence["LL-2026-001"]} >= {
        "queue_status",
        "energization",
        "permit",
        "equipment",
        "counterparty",
    }


@pytest.mark.parametrize(
    ("filename", "header", "dropped", "loader"),
    [
        ("queue.csv", QUEUE_HEADER, "mw_requested", load_queue),
        ("energization.csv", OBS_HEADER, "observed_energized_mw", load_observations),
        ("evidence.csv", EVIDENCE_HEADER, "weight", load_evidence),
    ],
)
def test_missing_required_column_raises(tmp_path, filename, header, dropped, loader) -> None:
    fields = header.split(",")
    short_fields = [f for f in fields if f != dropped]
    path = tmp_path / filename
    path.write_text(",".join(short_fields) + "\n", encoding="utf-8")
    with pytest.raises(ValueError) as excinfo:
        loader(path)
    assert dropped in str(excinfo.value)


def test_load_queue_non_numeric_mw_raises(tmp_path) -> None:
    path = tmp_path / "queue.csv"
    path.write_text(
        QUEUE_HEADER + "\n"
        "LL-2026-002,Bad,Test,NOTANUMBER,2026-12,under_ercot_review,2026-05-01\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError) as excinfo:
        load_queue(path)
    assert "mw_requested" in str(excinfo.value)
    assert "NOTANUMBER" in str(excinfo.value)
