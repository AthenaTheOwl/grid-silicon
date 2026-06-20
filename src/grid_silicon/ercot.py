"""ERCOT fixture parser and live-fetch boundary."""

from __future__ import annotations

import csv
from pathlib import Path

from .models import EnergizationObservation, EvidenceItem, QueueProject

REQUIRED_QUEUE_COLUMNS = {
    "project_id_raw",
    "project_name",
    "county",
    "mw_requested",
    "requested_in_service",
    "status_code",
    "last_updated",
}

REQUIRED_OBSERVATION_COLUMNS = {
    "project_id_raw",
    "observed_energized_mw",
    "approval_status",
    "observed_on",
}

REQUIRED_EVIDENCE_COLUMNS = {
    "evidence_id",
    "project_id_raw",
    "category",
    "label",
    "source_url",
    "extracted_on",
    "weight",
}


class LiveFetchBlocked(RuntimeError):
    """Raised when a caller requests live ERCOT fetch in v0.1."""


def default_fixture_dir(root: Path | None = None, month: str = "2026-05") -> Path:
    base = root or Path.cwd()
    return base / "data" / "fixtures" / "ercot" / month


def _read_csv(path: Path, required: set[str]) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = sorted(required - columns)
        if missing:
            raise ValueError(f"{path} missing required columns: {', '.join(missing)}")
        return [dict(row) for row in reader]


def load_queue(path: Path) -> list[QueueProject]:
    rows = _read_csv(path, REQUIRED_QUEUE_COLUMNS)
    projects: list[QueueProject] = []
    for row in rows:
        projects.append(
            QueueProject(
                project_id_raw=row["project_id_raw"].strip(),
                project_name=row["project_name"].strip(),
                county=row["county"].strip(),
                mw_requested=float(row["mw_requested"]),
                requested_in_service=row["requested_in_service"].strip(),
                status_code=row["status_code"].strip(),
                last_updated=row["last_updated"].strip(),
            )
        )
    return projects


def load_observations(path: Path) -> dict[str, EnergizationObservation]:
    rows = _read_csv(path, REQUIRED_OBSERVATION_COLUMNS)
    out: dict[str, EnergizationObservation] = {}
    for row in rows:
        obs = EnergizationObservation(
            project_id_raw=row["project_id_raw"].strip(),
            observed_energized_mw=float(row["observed_energized_mw"]),
            approval_status=row["approval_status"].strip(),
            observed_on=row["observed_on"].strip(),
        )
        out[obs.project_id_raw] = obs
    return out


def load_evidence(path: Path) -> dict[str, list[EvidenceItem]]:
    rows = _read_csv(path, REQUIRED_EVIDENCE_COLUMNS)
    grouped: dict[str, list[EvidenceItem]] = {}
    for row in rows:
        item = EvidenceItem(
            evidence_id=row["evidence_id"].strip(),
            project_id_raw=row["project_id_raw"].strip(),
            category=row["category"].strip(),
            label=row["label"].strip(),
            source_url=row["source_url"].strip(),
            extracted_on=row["extracted_on"].strip(),
            weight=int(row["weight"]),
        )
        grouped.setdefault(item.project_id_raw, []).append(item)
    return grouped


def explain_live_fetch_boundary(user_agent: str | None = None) -> str:
    agent = user_agent or "grid-silicon/0.1 contact: public repo issue"
    return (
        "live ERCOT fetch is not enabled in v0.1. ERCOT's public data portal "
        "requires terms acceptance and API registration. Use --dry-run to run "
        f"the committed fixture. Intended User-Agent for a future live adapter: {agent}"
    )


def require_live_fetch_allowed(user_agent: str | None = None) -> None:
    raise LiveFetchBlocked(explain_live_fetch_boundary(user_agent=user_agent))
