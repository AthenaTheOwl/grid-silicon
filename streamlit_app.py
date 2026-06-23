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

# ---------------------------------------------------------------------------
# Run the real scoring engine live. This is not a viewer — the sliders below
# call grid_silicon.scoring.compute_realness_score, the same function that
# produced the committed report. Change the inputs, watch realness move.
# ---------------------------------------------------------------------------
st.divider()
st.subheader("score a project yourself")
st.caption("drive the actual realness engine — `grid_silicon.scoring.compute_realness_score` — with your own inputs.")

try:
    import sys
    sys.path.insert(0, str(REPO / "src"))
    from grid_silicon.models import EnergizationObservation, EvidenceItem, QueueProject
    from grid_silicon.scoring import STATUS_POINTS, compute_realness_score

    col_a, col_b = st.columns(2)
    with col_a:
        announced = st.number_input("announced MW", min_value=1.0, max_value=5000.0, value=1200.0, step=50.0)
        observed = st.slider("observed energized MW", 0.0, float(announced), min(120.0, float(announced)), step=10.0)
    with col_b:
        status = st.selectbox("ERCOT interconnection status", list(STATUS_POINTS), index=1)
        evidence_cats = st.multiselect(
            "evidence categories on file",
            ["queue_status", "energization", "permit", "equipment", "filing"],
            default=["queue_status", "energization"],
        )

    project = QueueProject(
        project_id_raw="user-input", project_name="your project", county="—",
        mw_requested=announced, requested_in_service="2027", status_code=status, last_updated="2026-06",
    )
    obs = EnergizationObservation(
        project_id_raw="user-input", observed_energized_mw=observed,
        approval_status=status, observed_on="2026-06",
    )
    ev_items = [
        EvidenceItem(evidence_id=f"EV-{i}", project_id_raw="user-input", category=c,
                     label=c, source_url="https://example", extracted_on="2026-06", weight=2)
        for i, c in enumerate(evidence_cats)
    ]
    score = compute_realness_score(project, obs, ev_items)
    phantom = max(0.0, announced - observed)

    m1, m2, m3 = st.columns(3)
    m1.metric("realness score", f"{score}/100")
    m2.metric("phantom MW", f"{phantom:,.0f} MW")
    m3.metric("status floor", f"{STATUS_POINTS[status]} pts")
    if score >= 70:
        st.success(f"realness {score}/100 — this reads as a real, energizing project.")
    elif score >= 40:
        st.warning(f"realness {score}/100 — partially real; meaningful announced capacity is still phantom.")
    else:
        st.error(f"realness {score}/100 — mostly phantom: announced but not backed by interconnection progress.")
    st.caption("move observed MW up, advance the status, or add evidence categories and watch the score recompute — it's the live engine, not a lookup.")
except Exception as exc:  # pragma: no cover - defensive for cloud import differences
    st.info(f"interactive scoring needs the package importable ({exc}). the committed report above still renders.")

st.caption(
    "v0.1 ships one ERCOT fixture month. the model + scoring live in `src/grid_silicon/`; "
    "the table reads the committed `reports/*.jsonl` and the scorer above is the real engine. "
    "repo: github.com/AthenaTheOwl/grid-silicon"
)
