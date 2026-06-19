# Acceptance — 0001-foundation (grid-silicon)

v0 is done when the following commands all succeed on a clean clone.

## Commands

```powershell
uv sync
uv run python -m gridsilicon ingest ercot --snapshot 2026-06-15
uv run python -m gridsilicon resolve --out data/projects.parquet
uv run python -m gridsilicon score --iso ercot --quarter 2026q2
uv run python -m gridsilicon render report --iso ercot --month 2026-07
uv run python eval/brier_backtest.py
uv run pytest
uv run python scripts/voice_lint.py
uv run python scripts/validate_schemas.py
uv run python scripts/traceability.py
```

## Gates that must pass

- All tests pass under `pytest`.
- `validate_schemas.py` exits 0 against `data/scores/ercot/2026q2.parquet`.
- `traceability.py` exits 0: every score row in the published report has
  at least five evidence items.
- `voice_lint.py` exits 0 against `reports/2026-07-ercot.md`.
- `brier_backtest.py` prints a Brier score strictly lower than the
  announced-as-COD baseline. The baseline is printed in the same run.

## Artifacts produced

- `data/scores/ercot/2026q2.parquet` validates against the realness-score schema.
- `reports/2026-07-ercot.md` exists and lints clean.
- `reports/2026-07-ercot.cytoscape.json` validates as Cytoscape JSON.
- `decisions/DEC-GRDS-001-realness-score-schema.md` is present and links from the report.

## What v0 explicitly does not promise

- Coverage of any ISO other than ERCOT.
- A web interface beyond a static Cytoscape viewer.
- Real-time or weekly refresh — the first cadence is monthly.
- Calibrated probabilities beyond the v0 rubric — calibration is the
  job of `interconnect-alpha` once it lands.
