# requirements 0002-design

## scope

Spec 0002 narrows GridSilicon v0.1 to one ERCOT fixture-backed report row for
May 2026. The purpose is to turn the scaffold into runnable code and one
reviewable artifact, not to ship the full multi-source project graph.

## requirements

- R-GRDS2-001: `python -m grid_silicon ingest --iso ercot --month 2026-05 --dry-run` writes `reports/2026-05.jsonl`.
- R-GRDS2-002: The report contains exactly one ERCOT project row in v0.1.
- R-GRDS2-003: The row contains announced MW, observed energized MW, phantom MW, status code, and score.
- R-GRDS2-004: The row carries at least five evidence items, each with `source_url`.
- R-GRDS2-005: Live ERCOT fetching is refused unless a future registered adapter is added.
- R-GRDS2-006: The fixture parser validates required input columns and fails closed on missing columns.
- R-GRDS2-007: `realness_score` is deterministic and bounded between 0 and 100.
- R-GRDS2-008: `scripts/validate_schemas.py` validates report rows and schema metadata.
- R-GRDS2-009: `scripts/traceability.py` enforces the five-evidence-item rule.
- R-GRDS2-010: README documents the fixture-first boundary and the exact run command.

## non-goals

- Non-ERCOT ISOs.
- Full ERCOT Data Access Portal integration.
- Satellite, permit, or equipment-order live ingest.
- A web app.
- Calibrated probability claims.
