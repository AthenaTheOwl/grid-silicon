# GridSilicon

Phantom-vs-real capacity engine for announced US data-center gigawatts. Fuses
satellite, permit, interconnection-queue, and equipment-order signals into
one confidence score per project, refreshed monthly.

## what this is

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

## who this is for

- Long/short equity desks trading utility, REIT, and semis names.
- Infrastructure private-credit underwriters at Apollo, Blackstone, Brookfield.
- Hyperscaler corporate-development siting teams.
- ISO resource-planning groups.

## status

v0.1 pilot. The repo now has a fixture-first ERCOT row pipeline:

- parser for a committed ERCOT-shaped fixture
- deterministic `realness_score`
- `reports/2026-05.jsonl` with one phantom-vs-real row
- schema, traceability, and voice checks
- tests for parser, scoring, CLI, and report validation

Live ERCOT portal fetch is deferred. The public data portal requires terms
acceptance and API registration. The command refuses live fetch unless a later
registered adapter is added.

## how to run

From a fresh checkout:

```powershell
python -m grid_silicon ingest --iso ercot --month 2026-05 --dry-run
python -m grid_silicon validate
python -m pytest tests/ -q
python scripts/validate_schemas.py
python scripts/traceability.py
python scripts/voice_lint.py
```

The first command writes `reports/2026-05.jsonl`. In v0.1, `--dry-run` means
"use committed fixture data." It still writes the local output artifact.

## layout

```
grid-silicon/
  AGENTS.md
  LICENSE
  README.md
  pyproject.toml
  grid_silicon.py       # root shim for python -m grid_silicon
  src/grid_silicon/     # parser, scorer, cli, validators
  data/fixtures/ercot/2026-05/
  reports/2026-05.jsonl
  schemas/
  scripts/
  tests/
  specs/
    0001-foundation/
    0002-design/
  decisions/DEC-GRDS-001-realness-score-schema.md
```

## compounds with

- InterconnectAlpha as the survival-model and capacity-curve analytics module.
- SiteAtlas as the civic-data frontend over the same project graph.
- RatepayerExposure as the bill-impact derivative.
- Siting optimization lab as the optimization input layer.
- FabRiskRADAR via the shared chip-supply-chain-map infrastructure.
- WaferToWatt as the silicon-side complement.

## license

MIT. See [LICENSE](LICENSE).
