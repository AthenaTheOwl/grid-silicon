from __future__ import annotations

from pathlib import Path

import pytest

from grid_silicon.ercot import load_evidence, load_observations, load_queue
from grid_silicon.models import EnergizationObservation, QueueProject
from grid_silicon.scoring import build_report_rows, compute_realness_score

FIXTURE = Path("data/fixtures/ercot/2026-05")


def _project(status_code: str, mw_requested: float = 1200.0) -> QueueProject:
    return QueueProject(
        project_id_raw="LL-2026-999",
        project_name="Synthetic",
        county="Test",
        mw_requested=mw_requested,
        requested_in_service="2026-12",
        status_code=status_code,
        last_updated="2026-05-01",
    )


def _observation(observed_mw: float) -> EnergizationObservation:
    return EnergizationObservation(
        project_id_raw="LL-2026-999",
        observed_energized_mw=observed_mw,
        approval_status="approved",
        observed_on="2026-05-01",
    )


def test_ratio_points_cap_when_observed_exceeds_announced() -> None:
    # observed (1500) > announced (1200) still clamps ratio to 1.0 -> 20 points, never more
    project = _project("no_studies_submitted", mw_requested=1200.0)
    observation = _observation(1500.0)
    # status 10 + ratio cap 20 + no evidence 0 == 30
    assert compute_realness_score(project, observation, evidence=[]) == 30


@pytest.mark.parametrize(
    ("status_code", "expected"),
    [
        ("no_studies_submitted", 10),
        ("under_ercot_review", 25),
        ("planning_studies_approved", 45),
        ("approved_to_energize_not_operational", 70),
        ("observed_energized", 90),
        ("unknown_status_code", 0),
    ],
)
def test_status_points_contribution(status_code: str, expected: int) -> None:
    # no observation and no evidence isolate the status contribution
    project = _project(status_code)
    assert compute_realness_score(project, observation=None, evidence=[]) == expected


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
