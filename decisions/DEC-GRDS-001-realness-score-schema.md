# DEC-GRDS-001 realness-score schema

Date: 2026-06-20

Status: approved

## decision

GridSilicon v0.1 scores one ERCOT large-load project row with a bounded
`realness_score` from 0 to 100. The row carries announced MW, observed
energized MW, phantom MW, status code, source mode, and at least five evidence
items.

## rationale

The pilot needs one useful artifact before a larger queue model exists. A
single JSONL row is enough to test the core claim: announced load and observed
energization can be reconciled into a reviewable phantom-vs-real packet.

## scoring rubric

The v0.1 score is deterministic:

- ERCOT status contributes 0 to 90 points.
- Observed energized share contributes up to 20 points.
- Evidence category coverage contributes up to 10 points.
- The final score is clamped to 0 through 100.

This is not a calibrated probability. Calibration belongs in a later cohort
backtest once public queue snapshots and realized energization outcomes are
available.

## source boundary

Live ERCOT portal fetch is deferred. ERCOT's public data access path requires
terms acceptance and registration. The v0.1 command uses committed fixture rows
when `--dry-run` is set and refuses live fetch otherwise.

## rollback

Replace the rubric and schema in a later DEC after the first real registered
data pull and backtest.
