# Design — 0001-foundation (grid-silicon)

## Shape

A small monthly batch pipeline. Public sources land as raw files under
`data/raw/<source>/<date>/`. An entity-resolution pass joins them into
one project graph keyed by a `gridsilicon_project_id`. A scoring pass
emits one `realness_score` row per project with the supporting evidence
rows attached. A render pass produces the markdown report and the
Cytoscape JSON.

## Components

### Ingest (`src/fusion/`)

- `ercot_queue.py` — reads the ERCOT large-load interconnection queue
  CSV/XLS export, normalizes column names, writes
  `data/raw/ercot/<snapshot_date>/queue.parquet`.
- `permits.py` — reads county-level building and electrical permit
  filings for ERCOT counties. v0 supports a small set; the schema
  carries an extensible `jurisdiction` field.
- `equipment_orders.py` — reads disclosed transformer and switchgear
  backlogs from public-filing extracts. Cross-references against the
  shared `chip-supply-chain-map` export when relevant.
- `entity_resolution.py` — joins the above into a single project graph.
  Uses deterministic blocking on (state, county, ~10-km grid cell) plus
  string similarity on project names. Outputs `data/projects.parquet`.

### Scoring (`src/scoring/`)

- `realness_score.py` — takes `data/projects.parquet` plus the per-source
  evidence parquets and emits a per-project 0–100 score. The rubric
  starts as a documented weighted sum across five evidence categories
  (queue maturity, permit progression, equipment commitments, site
  imagery, counterparty disclosure). The rubric is owned by
  `DEC-GRDS-001`.

### Render (`src/render/`)

- `cytoscape_export.py` — emits a Cytoscape JSON graph of projects,
  evidence items, and counterparties.
- `report.py` — emits `reports/YYYY-MM-<iso>.md` from the scored
  parquet plus a Jinja template under `src/render/templates/`.

### Eval (`eval/`)

- `brier_backtest.py` — replays the scorer against the 2018–2023 ERCOT
  cohort and prints a Brier score against actual energization outcomes.
  Compared against an announced-as-COD baseline.

## Data flow

```
raw filings -> per-source parquet -> entity_resolution
                                         |
                                         v
                                  data/projects.parquet
                                         |
                                         v
                                 realness_score.py
                                         |
                                         v
                            data/scores/ercot/2026q2.parquet
                                         |
                          +--------------+---------------+
                          v                              v
                   cytoscape_export                  report.py
                          |                              |
                          v                              v
                  reports/.../graph.json        reports/2026-07-ercot.md
```

## Out-of-scope for 0001

- A live web frontend. The Cytoscape graph ships as a checked-in JSON
  plus a static HTML viewer; no server.
- Non-ERCOT ISOs.
- A REST API. Consumers read parquet and JSON directly.
