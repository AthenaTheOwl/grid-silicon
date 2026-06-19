# GridSilicon

Phantom-vs-real capacity engine for announced US data-center gigawatts. Fuses
satellite, permit, interconnection-queue, and equipment-order signals into
one confidence score per project, refreshed monthly.

## What this is

SemiAnalysis estimates 311 of 410 GW in the ERCOT large-load queue is phantom.
PJM's Dec 2025 capacity auction cleared 6.6 GW short. Transformer lead times
run four to five years. The gap between announcement and energization is now
the most valuable number in infrastructure investing, and no one has fused
the public layers into a single score with the evidence behind it.

GridSilicon is the data layer. The first artifact is an ERCOT-only static
report — every large-load queue project ranked by a 0-100 "real" score, with
the five evidence items behind each score, shipped as a public PDF plus an
interactive Cytoscape graph, updated monthly.

Bucket: ai-infra. Category: ai-infra. Brand prefix: `GRDS`.

## Who this is for

- Long/short equity desks trading utility, REIT, and semis names.
- Infrastructure private-credit underwriters at Apollo, Blackstone, Brookfield.
- Hyperscaler corporate-development siting teams.
- ISO resource-planning groups.

## Status

v0 scaffold. No implementation yet. The first PR after this scaffold lands the
ERCOT queue ingest plus the realness-score schema; see `docs/first-pr.md`.

## How to run

Placeholder. Run commands will land in spec `0002-ercot-ingest`. The shape
will be:

```powershell
uv sync
uv run python -m gridsilicon ingest ercot --quarter 2026q2
uv run python -m gridsilicon score --queue data/ercot_queue_2026q2.parquet
uv run python -m gridsilicon render report --out reports/2026-07-ercot.md
```

## Layout

```
gridsilicon/
  AGENTS.md
  LICENSE
  README.md
  specs/
    0001-foundation/
      requirements.md
      design.md
      tasks.md
      acceptance.md
  docs/
    first-pr.md
  src/
    fusion/             # entity resolution across queue, permit, satellite
    scoring/            # realness_score.py
    render/             # cytoscape_export, report templates
  data/                 # parquet snapshots per ISO per quarter (gitignored cache)
  reports/              # checked-in monthly publications
  eval/                 # brier_backtest.py and calibration
  decisions/            # DEC-GRDS-* architectural choices
```

The directories named under `src/`, `data/`, `reports/`, `eval/`, and
`decisions/` are the targets the first real PR will create. The scaffold
does not create empty source folders.

## Compounds with

- InterconnectAlpha as the survival-model and capacity-curve analytics module.
- SiteAtlas as the civic-data frontend over the same project graph.
- RatepayerExposure as the bill-impact derivative.
- RobustSiting as the optimization input layer.
- FabRiskRADAR via the shared chip-supply-chain-map infrastructure.
- WaferToWatt as the silicon-side complement.

## License

MIT. See [LICENSE](LICENSE).
