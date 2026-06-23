"""Command-line interface for the grid-silicon v0.1 pilot."""

from __future__ import annotations

import argparse
from pathlib import Path

import json

from .ercot import (
    default_fixture_dir,
    load_evidence,
    load_observations,
    load_queue,
    require_live_fetch_allowed,
)
from .report import write_jsonl
from .scoring import build_report_rows
from .validation import validate_reports


def _repo_root() -> Path:
    return Path.cwd()


def _latest_report(root: Path) -> Path | None:
    reports = sorted((root / "reports").glob("*.jsonl"))
    return reports[-1] if reports else None


def _run_show(args: argparse.Namespace) -> int:
    """Print a readable, ranked view of a generated report (no args needed)."""
    root = _repo_root()
    path = Path(args.report) if args.report else _latest_report(root)
    if path is None or not path.is_file():
        raise SystemExit("no report found under reports/*.jsonl — run `ingest --month <m> --dry-run` first")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    rows.sort(key=lambda r: r.get("phantom_mw", 0), reverse=True)
    print(f"grid-silicon — datacenter-load realness, {path.stem} ({rows[0].get('iso', '?').upper()})")
    print(f"{len(rows)} project(s), ranked by phantom MW (announced minus observed-energized)\n")
    header = f"{'project':<28} {'county':<10} {'announced':>10} {'energized':>10} {'phantom':>9} {'realness':>9}  status"
    print(header)
    print("-" * len(header))
    for r in rows:
        print(
            f"{r.get('project_name', r['project_id'])[:28]:<28} "
            f"{r.get('county', '?')[:10]:<10} "
            f"{r.get('mw_announced', 0):>8.0f}MW "
            f"{r.get('mw_observed_energized', 0):>8.0f}MW "
            f"{r.get('phantom_mw', 0):>7.0f}MW "
            f"{r.get('realness_score', 0):>8}/100  "
            f"{r.get('status_code', '?')}"
        )
    worst = rows[0]
    print(
        f"\nbiggest gap: {worst.get('project_name', worst['project_id'])} in {worst.get('county')} county — "
        f"{worst.get('phantom_mw', 0):.0f}MW announced but not yet energized "
        f"({len(worst.get('evidence_ids', []))} sourced evidence rows). realness {worst.get('realness_score')}/100."
    )
    return 0


def _run_ingest(args: argparse.Namespace) -> int:
    root = _repo_root()
    if args.iso != "ercot":
        raise SystemExit("v0.1 supports --iso ercot only")
    if not args.dry_run:
        require_live_fetch_allowed(user_agent=args.user_agent)
    fixture_dir = Path(args.fixture_dir) if args.fixture_dir else default_fixture_dir(root, args.month)
    queue = load_queue(fixture_dir / "queue.csv")
    observations = load_observations(fixture_dir / "energization.csv")
    evidence = load_evidence(fixture_dir / "evidence.csv")
    rows = build_report_rows(
        month=args.month,
        projects=queue,
        observations=observations,
        evidence_by_project=evidence,
        source_mode="fixture" if args.dry_run else "live",
    )
    out = Path(args.out) if args.out else root / "reports" / f"{args.month}.jsonl"
    write_jsonl(rows, out)
    print(f"wrote {len(rows)} row(s) to {out}")
    for row in rows:
        print(
            f"{row.project_id}: score={row.realness_score} "
            f"announced={row.mw_announced:.0f}MW observed={row.mw_observed_energized:.0f}MW"
        )
    return 0


def _run_validate(_args: argparse.Namespace) -> int:
    errors = validate_reports(_repo_root())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("valid: reports")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="grid_silicon")
    sub = parser.add_subparsers(dest="command", required=True)
    ingest = sub.add_parser("ingest", help="ingest ERCOT fixture or future live source")
    ingest.add_argument("--iso", default="ercot")
    ingest.add_argument("--month", required=True)
    ingest.add_argument("--dry-run", action="store_true", help="use committed fixture data")
    ingest.add_argument("--fixture-dir", default=None)
    ingest.add_argument("--out", default=None)
    ingest.add_argument(
        "--user-agent",
        default="grid-silicon/0.1 contact: github.com/AthenaTheOwl/grid-silicon",
    )
    ingest.set_defaults(func=_run_ingest)
    validate = sub.add_parser("validate", help="validate generated reports")
    validate.set_defaults(func=_run_validate)
    show = sub.add_parser("show", help="print a readable ranked view of the latest report")
    show.add_argument("--report", default=None, help="path to a report jsonl (default: latest under reports/)")
    show.set_defaults(func=_run_show)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
