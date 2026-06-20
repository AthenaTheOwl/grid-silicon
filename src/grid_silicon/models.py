"""Typed rows for the ERCOT v0.1 pilot."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QueueProject:
    project_id_raw: str
    project_name: str
    county: str
    mw_requested: float
    requested_in_service: str
    status_code: str
    last_updated: str


@dataclass(frozen=True)
class EnergizationObservation:
    project_id_raw: str
    observed_energized_mw: float
    approval_status: str
    observed_on: str


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    project_id_raw: str
    category: str
    label: str
    source_url: str
    extracted_on: str
    weight: int


@dataclass(frozen=True)
class RealnessRow:
    month: str
    iso: str
    project_id: str
    project_name: str
    county: str
    mw_announced: float
    mw_observed_energized: float
    phantom_mw: float
    realness_score: int
    status_code: str
    source_mode: str
    evidence_ids: list[str]
    evidence: list[dict[str, object]]
    notes: str

    def to_json_dict(self) -> dict[str, object]:
        return {
            "month": self.month,
            "iso": self.iso,
            "project_id": self.project_id,
            "project_name": self.project_name,
            "county": self.county,
            "mw_announced": self.mw_announced,
            "mw_observed_energized": self.mw_observed_energized,
            "phantom_mw": self.phantom_mw,
            "realness_score": self.realness_score,
            "status_code": self.status_code,
            "source_mode": self.source_mode,
            "evidence_ids": self.evidence_ids,
            "evidence": self.evidence,
            "notes": self.notes,
        }
