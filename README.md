# grid-silicon

A datacenter is announced as 1,200 megawatts. One hundred twenty are actually
energized. The other 1,080 live on a form. grid-silicon scores the difference.

## What it does

Half the gigawatts in the headlines do not exist yet. SemiAnalysis figures 311 of
the 410 GW sitting in the ERCOT large-load queue are phantom — names in a database,
not load on a wire. PJM's December 2025 capacity auction still cleared 6.6 GW short.
Transformers run four to five years out. The interesting number in infrastructure
right now is the gap between what got announced and what got built, and the public
signals that would close it — satellite, permits, queue status, equipment orders —
sit in separate places where nobody has added them up.

grid-silicon adds them up. It takes a published large-load project, scores it 0 to
100 on how real it is, and shows the five sourced pieces of evidence behind the
score. v0.1 ships one ERCOT month as a checked-in report. The model and the scorer
are the point; the data adapter is deliberately small.

It refuses to fetch the live ERCOT portal, by the way. The portal wants terms
acceptance and API registration, which is a human's signature, not a script's. So
the tool waits for the form to be signed instead of pretending it already was.

## Try it

One command, no setup, no keys. It reads the committed report and prints the result:

```powershell
python -m grid_silicon show
```

```
grid-silicon — datacenter-load realness, 2026-05 (ERCOT)
1 project(s), ranked by phantom MW (announced minus observed-energized)

project                      county      announced  energized   phantom  realness  status
-----------------------------------------------------------------------------------------
Lone Star Compute Campus     Ellis          1200MW      120MW    1080MW       37/100  under_ercot_review

biggest gap: Lone Star Compute Campus in Ellis county — 1080MW announced but not
yet energized (5 sourced evidence rows). realness 37/100.
```

Ranked by phantom MW, worst offender first. A project at the top of that list is an
announcement; a project at the bottom is a build.

## Live demo

`streamlit_app.py` is the same result as a page you can poke: the realness table,
the announced/energized/phantom split, the evidence per project, and a scorer you
can drive yourself — move the observed megawatts, advance the interconnection
status, watch the score climb from "mostly form" to "mostly real." It reads the
committed report. No network, no secrets.

```powershell
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

Live: deploy on [Streamlit Community Cloud](https://share.streamlit.io) — new app,
repo `AthenaTheOwl/grid-silicon`, branch `main`, main file `streamlit_app.py`.

<!-- once deployed: [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://<your-app>.streamlit.app) -->

## How it connects

grid-silicon is the data floor under the energy line. The others build on the same
project graph:

- [interconnect-alpha](https://github.com/AthenaTheOwl/interconnect-alpha) — the
  survival model: probability a queued project ever reaches commercial operation.
- [site-atlas](https://github.com/AthenaTheOwl/site-atlas) — the civic-data front
  end over the same queue.
- [ratepayer-exposure](https://github.com/AthenaTheOwl/ratepayer-exposure) — what
  the buildout does to one household's power bill.
- [chip-supply-chain-map](https://github.com/AthenaTheOwl/chip-supply-chain-map) /
  [fab-risk-radar](https://github.com/AthenaTheOwl/fab-risk-radar) — the silicon
  side of the same demand curve.

## Run it in full

```powershell
python -m grid_silicon ingest --iso ercot --month 2026-05 --dry-run   # writes reports/2026-05.jsonl
python -m grid_silicon validate
python -m pytest tests/ -q
```

`--dry-run` means "use the committed fixture." It still writes the output artifact.

## Layout

```
src/grid_silicon/     parser, scorer, cli, validators
data/fixtures/ercot/  the committed ERCOT-shaped fixture
reports/2026-05.jsonl the one phantom-vs-real row v0.1 ships
schemas/  scripts/  tests/  specs/  decisions/
```

## License

MIT. See [LICENSE](LICENSE).
