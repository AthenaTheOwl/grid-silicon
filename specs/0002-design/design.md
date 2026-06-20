# design 0002-design

## blocks

### fixture ingest

`src/grid_silicon/ercot.py` reads three committed fixture CSV files:

- `queue.csv`
- `energization.csv`
- `evidence.csv`

The parser checks required columns before producing typed dataclass rows.

### scoring

`src/grid_silicon/scoring.py` joins a queue row to an energization observation
and evidence items. It emits one `RealnessRow` with a deterministic score.

### report writer

`src/grid_silicon/report.py` writes JSONL rows to `reports/<month>.jsonl`.
The CLI uses this writer for the pilot artifact.

### validation

`src/grid_silicon/validation.py`, `scripts/validate_schemas.py`, and
`scripts/traceability.py` validate the checked-in report. The validators use
the standard library so a fresh clone can run them without extra services.

### cli

`src/grid_silicon/cli.py` owns the command surface. `--dry-run` means "use
committed fixture data." Without `--dry-run`, the command refuses live fetch
and explains the ERCOT registration boundary.

## data flow

```text
data/fixtures/ercot/2026-05/*.csv
  -> parser
  -> scorer
  -> reports/2026-05.jsonl
  -> validators
```

## review findings applied

Architecture lens: split parser, scorer, report writer, validation, and CLI so
the live ERCOT adapter can be added later without changing the scoring code.

Security lens: no live fetch, no credentials, no scraped hidden endpoints. The
CLI fails closed when fixture mode is not requested.
