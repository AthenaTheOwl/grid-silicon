"""Realness score v0.1."""

from __future__ import annotations

from .models import EnergizationObservation, EvidenceItem, QueueProject, RealnessRow

STATUS_POINTS = {
    "no_studies_submitted": 10,
    "under_ercot_review": 25,
    "planning_studies_approved": 45,
    "approved_to_energize_not_operational": 70,
    "observed_energized": 90,
}


def stable_project_id(raw_id: str) -> str:
    suffix = "".join(ch.lower() if ch.isalnum() else "-" for ch in raw_id).strip("-")
    return f"grds-ercot-{suffix}"


def compute_realness_score(
    project: QueueProject, observation: EnergizationObservation | None, evidence: list[EvidenceItem]
) -> int:
    status_points = STATUS_POINTS.get(project.status_code, 0)
    observed_mw = observation.observed_energized_mw if observation else 0.0
    ratio = 0.0 if project.mw_requested <= 0 else min(1.0, observed_mw / project.mw_requested)
    ratio_points = round(ratio * 20)
    category_points = min(10, len({item.category for item in evidence}) * 2)
    raw = status_points + ratio_points + category_points
    return max(0, min(100, int(raw)))


def build_report_rows(
    *,
    month: str,
    projects: list[QueueProject],
    observations: dict[str, EnergizationObservation],
    evidence_by_project: dict[str, list[EvidenceItem]],
    source_mode: str,
) -> list[RealnessRow]:
    rows: list[RealnessRow] = []
    for project in projects:
        observation = observations.get(project.project_id_raw)
        evidence = evidence_by_project.get(project.project_id_raw, [])
        observed_mw = observation.observed_energized_mw if observation else 0.0
        score = compute_realness_score(project, observation, evidence)
        evidence_payload = [
            {
                "evidence_id": item.evidence_id,
                "category": item.category,
                "label": item.label,
                "source_url": item.source_url,
                "extracted_on": item.extracted_on,
                "weight": item.weight,
            }
            for item in evidence
        ]
        rows.append(
            RealnessRow(
                month=month,
                iso="ercot",
                project_id=stable_project_id(project.project_id_raw),
                project_name=project.project_name,
                county=project.county,
                mw_announced=project.mw_requested,
                mw_observed_energized=observed_mw,
                phantom_mw=max(0.0, project.mw_requested - observed_mw),
                realness_score=score,
                status_code=project.status_code,
                source_mode=source_mode,
                evidence_ids=[item.evidence_id for item in evidence],
                evidence=evidence_payload,
                notes=(
                    "fixture-first v0.1 row. Live ERCOT portal fetch is deferred "
                    "until API registration and terms acceptance are handled by a human."
                ),
            )
        )
    return rows
