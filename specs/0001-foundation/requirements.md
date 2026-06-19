# Requirements — 0001-foundation (grid-silicon)

Brand prefix: `GRDS`.

## Scope

The foundation spec names what v0 must produce: the schema, the ingest
shape, the first scored report, and the gates that hold the rest of the
portfolio's discipline.

## Requirements

- R-GRDS-001: The repo publishes one monthly report under `reports/`
  named `YYYY-MM-<iso>.md`. The first issue is `2026-07-ercot.md`.
- R-GRDS-002: Every project that appears in a report has a `realness_score`
  in the integer range 0–100. Half-points are not allowed.
- R-GRDS-003: Every `realness_score` carries at least five evidence
  items. Each evidence item has a public URL, a filing ID, or an
  imagery date.
- R-GRDS-004: Project identity is resolved across ISO queue, county
  permit filings, and equipment-order signals before scoring. A single
  project that appears under three names in three sources is one row
  in the output, not three.
- R-GRDS-005: Score outputs are persisted as parquet under
  `data/scores/<iso>/<quarter>.parquet` with a checked-in schema at
  `schemas/realness-score.schema.json`.
- R-GRDS-006: The interactive Cytoscape export is generated from the
  same parquet, not from a parallel data model. Render code reads
  parquet, never markdown.
- R-GRDS-007: A `brier_backtest.py` runs against the 2018–2023 ERCOT
  cohort and prints a Brier score with two-decimal precision. The
  baseline (announced-as-COD) Brier is printed alongside.
- R-GRDS-008: A `voice_lint` pass runs against every checked-in report
  before merge. The banned set is owned by the script, not by this
  spec.
- R-GRDS-009: Every report ends with a `## Methodology` section that
  links to the score schema, the eval script, and the decision records
  that govern the current scoring rubric.
- R-GRDS-010: No source-tracked artifact under `data/` is larger than
  50 MB. Anything larger lives under `data/cache/` and is gitignored.
- R-GRDS-011: Decision records live under `decisions/DEC-GRDS-NNN.md`
  in append-only form. The first is `DEC-GRDS-001-realness-score-schema.md`.
- R-GRDS-012: This repo does not call into any private API or scraped
  source that violates a publisher's terms. ISO sources are public
  filings; satellite signals are licensed or open.
