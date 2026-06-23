"""grid-silicon — live demo (Streamlit Community Cloud).

Reads the committed report under reports/*.jsonl and shows datacenter-load
"realness": how much announced ERCOT large-load capacity is actually energized
versus still phantom (named in a queue but not built). No network, no secrets —
runs entirely off the committed fixture report.

Deploy: Streamlit Community Cloud -> New app -> repo AthenaTheOwl/grid-silicon,
branch main, main file streamlit_app.py.
"""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

REPO = Path(__file__).resolve().parent
REPORTS = REPO / "reports"


def load_rows() -> tuple[list[dict], str]:
    files = sorted(REPORTS.glob("*.jsonl"))
    if not files:
        return [], ""
    latest = files[-1]
    rows = [json.loads(line) for line in latest.read_text(encoding="utf-8").splitlines() if line.strip()]
    return rows, latest.stem


st.set_page_config(page_title="grid-silicon — datacenter-load realness", layout="wide")
st.title("grid-silicon")
st.caption(
    "which announced ERCOT datacenter loads are real, and which are phantom — "
    "named in an interconnection queue but not yet energized."
)

rows, month = load_rows()
if not rows:
    st.warning("no report found under reports/*.jsonl")
    st.stop()

iso = rows[0].get("iso", "?").upper()
st.subheader(f"{iso} large-load realness — {month}")

total_announced = sum(r.get("mw_announced", 0) for r in rows)
total_energized = sum(r.get("mw_observed_energized", 0) for r in rows)
total_phantom = sum(r.get("phantom_mw", 0) for r in rows)

c1, c2, c3 = st.columns(3)
c1.metric("announced", f"{total_announced:,.0f} MW")
c2.metric("energized", f"{total_energized:,.0f} MW")
c3.metric("phantom", f"{total_phantom:,.0f} MW", help="announced minus observed-energized")

min_phantom = st.slider("minimum phantom MW", 0, int(max(r.get("phantom_mw", 0) for r in rows)) or 1, 0)
shown = sorted(
    [r for r in rows if r.get("phantom_mw", 0) >= min_phantom],
    key=lambda r: r.get("phantom_mw", 0),
    reverse=True,
)

st.dataframe(
    [
        {
            "project": r.get("project_name", r["project_id"]),
            "county": r.get("county"),
            "announced MW": r.get("mw_announced"),
            "energized MW": r.get("mw_observed_energized"),
            "phantom MW": r.get("phantom_mw"),
            "realness /100": r.get("realness_score"),
            "status": r.get("status_code"),
        }
        for r in shown
    ],
    use_container_width=True,
    hide_index=True,
)

if shown:
    worst = shown[0]
    st.info(
        f"**biggest gap:** {worst.get('project_name', worst['project_id'])} in "
        f"{worst.get('county')} county — {worst.get('phantom_mw', 0):,.0f} MW announced "
        f"but not yet energized ({len(worst.get('evidence_ids', []))} sourced evidence rows). "
        f"realness {worst.get('realness_score')}/100."
    )
    with st.expander("evidence for the selected project"):
        for ev in worst.get("evidence", []):
            st.markdown(
                f"- **{ev.get('category')}** (weight {ev.get('weight')}): {ev.get('label')}  \n"
                f"  source: {ev.get('source_url')}"
            )

st.caption(
    "v0.1 ships one ERCOT fixture month. the model + scoring live in `src/grid_silicon/`; "
    "this page reads the committed `reports/*.jsonl`. repo: github.com/AthenaTheOwl/grid-silicon"
)
