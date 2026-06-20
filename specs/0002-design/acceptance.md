# acceptance 0002-design

## commands

```powershell
python -m grid_silicon ingest --iso ercot --month 2026-05 --dry-run
python -m grid_silicon validate
python -m pytest tests/ -q
python scripts/validate_schemas.py
python scripts/traceability.py
python scripts/voice_lint.py
```

## expected results

- The ingest command writes one row to `reports/2026-05.jsonl`.
- The row has five evidence items.
- The row has `source_mode` set to `fixture`.
- Tests pass.
- Validators exit 0.
- Voice lint exits 0.

## pilot evidence

The useful artifact is `reports/2026-05.jsonl`: one phantom-vs-real row for the
ERCOT fixture project. The command is repeatable from a fresh checkout.
