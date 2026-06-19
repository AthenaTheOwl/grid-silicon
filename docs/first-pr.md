# First PR — grid-silicon

The literal first PR after the scaffold. Scope kept narrow so review
is fast and gates are real on day one.

## Title

`feat(GRDS): ERCOT queue ingest plus realness-score schema (PR 1)`

## Goal

Land the parser for the ERCOT large-load interconnection queue, the
two JSON Schemas that constrain every downstream artifact, and the
first gate that enforces them.

## Files added

- `pyproject.toml` — project metadata; deps: `polars`, `pyarrow`,
  `pydantic`, `jsonschema`, `pytest`, `ruff`.
- `src/gridsilicon/__init__.py` — package marker; exposes `__version__`.
- `src/gridsilicon/fusion/__init__.py`
- `src/gridsilicon/fusion/ercot_queue.py` — pure parser. Inputs the
  ERCOT public CSV; outputs a `polars.DataFrame` with the normalized
  columns `project_id_raw`, `project_name`, `county`, `mw_requested`,
  `requested_in_service`, `status_code`, `last_updated`.
- `schemas/realness-score.schema.json` — v0 score row shape with
  `project_id`, `iso`, `quarter`, `realness_score`, `evidence_ids`.
- `schemas/evidence-item.schema.json` — `evidence_id`, `project_id`,
  `source`, `source_url`, `extracted_on`, `category`, `weight`.
- `data/raw/ercot/2026-06-15/queue.csv.example` — small fixture, six
  rows, hand-curated for tests; not the full snapshot.
- `tests/test_ercot_queue.py` — parses the fixture, asserts column
  set, types, and that no row drops out silently.
- `scripts/validate_schemas.py` — walks `schemas/` and any
  `data/scores/**/*.parquet` and validates against the registered
  schemas; exits 1 on any mismatch.
- `.github/.gitkeep` — placeholder so the directory exists before CI
  lands in a later PR.

## Files not in this PR

- Entity resolution. That is PR 2.
- The scorer itself. PR 2.
- The first report. PR 3.
- Any GitHub Actions workflow. Lands separately under its own spec.

## Verification

Reviewer runs:

```powershell
uv sync
uv run pytest
uv run python scripts/validate_schemas.py
```

Expected: all tests pass; `validate_schemas.py` exits 0.

## Review checklist

- [ ] No row in the parser drops without an explicit log line.
- [ ] Both schemas declare `$id` and `$schema` and validate themselves
      against the JSON Schema 2020-12 meta-schema.
- [ ] The fixture is small and synthetic; no scraped data is checked in.
- [ ] `pyproject.toml` pins a lower bound on every dep; no `*` versions.
- [ ] No marketing words in any added markdown.

## After merge

PR 2 adds `entity_resolution.py` and the scorer. PR 3 ships the first
real report and wires `voice_lint` plus `traceability` as gates.
