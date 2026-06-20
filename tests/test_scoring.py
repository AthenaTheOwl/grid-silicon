from __future__ import annotations

from pathlib import Path

from grid_silicon.ercot import load_evidence, load_observations, load_queue
from grid_silicon.scoring import build_report_rows, compute_realness_score

FIXTURE = Path("data/fixtures/ercot/2026-05")


def test_realness_score_is_bounded() -> None:
    project = load_queue(FIXTURE / "queue.csv")[0]
    observation = load_observations(FIXTURE / "energization.csv")[project.project_id_raw]
    evidence = load_evidence(FIXTURE / "evidence.csv")[project.project_id_raw]
    score = compute_realness_score(project, observation, evidence)
    assert 0 <= score <= 100
    assert score == 37


def test_build_report_row() -> None:
    projects = load_queue(FIXTURE / "queue.csv")
    rows = build_report_rows(
        month="2026-05",
        projects=projects,
        observations=load_observations(FIXTURE / "energization.csv"),
        evidence_by_project=load_evidence(FIXTURE / "evidence.csv"),
        source_mode="fixture",
    )
    assert len(rows) == 1
    row = rows[0]
    assert row.project_id == "grds-ercot-ll-2026-001"
    assert row.phantom_mw == 1080
    assert len(row.evidence_ids) == 5
