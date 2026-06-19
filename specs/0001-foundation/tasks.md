# Tasks — 0001-foundation (grid-silicon)

Ordered for the first two to three PRs after this scaffold lands.

## PR 1 — schema and ERCOT ingest

- [ ] Add `pyproject.toml` with `polars`, `pyarrow`, `pydantic`, `jsonschema`, `pytest`, `ruff`.
- [ ] Add `schemas/realness-score.schema.json` with the v0 score row shape.
- [ ] Add `schemas/evidence-item.schema.json` for the per-score evidence rows.
- [ ] Add `src/fusion/ercot_queue.py` with a parser for the public ERCOT large-load queue export.
- [ ] Add `data/raw/ercot/2026-06-15/queue.csv.example` (small fixture, not full snapshot).
- [ ] Add `tests/test_ercot_queue.py` exercising the parser on the fixture.
- [ ] Add `scripts/validate_schemas.py` and wire it as a local gate.

## PR 2 — entity resolution and first score

- [ ] Add `src/fusion/entity_resolution.py` with deterministic blocking plus name-similarity match.
- [ ] Add `src/scoring/realness_score.py` implementing the documented v0 rubric.
- [ ] Add `decisions/DEC-GRDS-001-realness-score-schema.md` naming the five evidence categories and weights.
- [ ] Add `tests/test_entity_resolution.py` with a hand-built five-project fixture.
- [ ] Add `tests/test_realness_score.py` covering boundary cases (0, 100, missing-evidence).

## PR 3 — render and eval

- [ ] Add `src/render/cytoscape_export.py`.
- [ ] Add `src/render/report.py` plus `src/render/templates/monthly_iso.md.j2`.
- [ ] Add `reports/2026-07-ercot.md` as the first checked-in report.
- [ ] Add `eval/brier_backtest.py` plus the 2018–2023 cohort parquet fixture.
- [ ] Add `scripts/voice_lint.py` and wire as gate on `reports/`.
- [ ] Add `scripts/traceability.py` enforcing the five-evidence-items rule.
