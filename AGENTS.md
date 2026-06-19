# AGENTS.md — grid-silicon

Operating contract for AI agents (Claude, Codex, Cursor) working in this
repo. Conventions match the AthenaTheOwl portfolio so an agent already
trained on supplier-risk-rag-agent or chip-supply-chain-map recognizes
the shape.

## What this repo is

A monthly-cadence data publication that scores announced US data-center
projects on probability of actually energizing at announced nameplate.
The first issue covers the ERCOT large-load queue. Every score carries
five evidence items linked back to public sources (queue filings,
permits, satellite, equipment orders). The product is the report and
the underlying parquet snapshot, not a live dashboard.

## Voice constraints

- No marketing words. The banned set will live in
  `scripts/voice_lint.py::BANNED_FAIL` once the lint script lands in
  spec 0002. Examples that always fail: leverage, demonstrate, seamless,
  cutting-edge, best-in-class, synergy.
- No antithetical reversals as a structural device. The "X isn't Y — Z
  is the W" shape is the AI tell.
- Plain assertions. The fused data is the moat; the prose is scaffolding.
- Numbers carry citations. Every score in a report links to the queue
  filing, permit number, or imagery date that produced it.

## Gates

Will land in spec `0002-gates`. The intended chain:

- `voice_lint` on every report under `reports/`.
- `validate_schemas` on score outputs against `schemas/realness-score.schema.json`.
- `traceability` check: every score row must reference at least three
  evidence rows; every evidence row must reference a public URL or
  filing ID.
- `brier_backtest` against the historical ERCOT cohort must beat the
  naive "announced GW will energize on announced date" baseline.

## Out of scope

- Live data feeds. ISO queue snapshots are public and update on the
  ISO's own cadence; the report is monthly, not push.
- Channel checks with named utilities or hyperscalers under NDA. This
  repo only consumes public sources.
- Non-US ISOs in v0. PJM, MISO, CAISO, SPP arrive after ERCOT lands.
- A general data-center directory. The product is the realness score
  and its evidence — not a CRM of facilities.
