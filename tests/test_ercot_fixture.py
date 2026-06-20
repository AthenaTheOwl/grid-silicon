from __future__ import annotations

from pathlib import Path

from grid_silicon.ercot import load_evidence, load_observations, load_queue

FIXTURE = Path("data/fixtures/ercot/2026-05")


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
