#!/usr/bin/env python3
"""Generate a bundled Rest Assured report set from canonical markdown and tests."""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import date
from pathlib import Path


def script_path(root: Path, *parts: str) -> Path:
    return root.joinpath(*parts).resolve()


def run_script(script: Path, *args: str) -> None:
    subprocess.run([sys.executable, str(script), *args], check=True)


def write_manifest(
    output: Path,
    mapping: Path,
    mismatches: Path,
    tests_root: Path,
    html_dir: Path,
    documentation_mode: str,
    include_change_impact: bool,
    report_dir: Path,
) -> None:
    lines = [
        "# Report Bundle Manifest",
        "",
        "## Summary",
        "",
        f"- Generated at: {date.today().isoformat()}",
        f"- Mapping source: `{mapping}`",
        f"- Mismatch source: `{mismatches}`",
        f"- Tests root: `{tests_root}`",
        f"- HTML directory: `{html_dir}`",
        f"- Documentation mode: `{documentation_mode}`",
        f"- Change-impact included: `{str(include_change_impact).lower()}`",
        "",
        "## Artifacts",
        "",
        f"- Traceability HTML: `{html_dir / 'test-mapping-report.html'}`",
        f"- Contract mismatches HTML: `{html_dir / 'contract-mismatches.html'}`",
        f"- Coverage gap markdown: `{report_dir / 'coverage-gap-report.md'}`",
        f"- Coverage gap HTML: `{html_dir / 'coverage-gap-report.html'}`",
        f"- Assertion strength markdown: `{report_dir / 'assertion-strength-report.md'}`",
        f"- Assertion strength HTML: `{html_dir / 'assertion-strength-report.html'}`",
        f"- OpenAPI change impact markdown: `{report_dir / 'openapi-change-impact-report.md' if include_change_impact else 'Skipped'}`",
        f"- OpenAPI change impact HTML: `{html_dir / 'openapi-change-impact-report.html' if include_change_impact else 'Skipped'}`",
        "",
        "## Notes",
        "",
        "- Treat the mapping and mismatch markdown files as canonical inputs.",
        "- Treat the sibling markdown analytics reports and HTML portal as deterministic projections.",
        "- Documentation references may come from BDD, TDD, plain-text, mixed, or absent narrative documentation.",
        "",
    ]
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a bundled Rest Assured report set.")
    parser.add_argument("--mapping", required=True, help="Path to docs/testing/test-mapping-report.md")
    parser.add_argument("--mismatches", required=True, help="Path to docs/testing/contract-mismatches.md")
    parser.add_argument("--tests-root", required=True, help="Root folder containing Java test classes")
    parser.add_argument("--html-dir", required=True, help="Directory for HTML output")
    parser.add_argument("--baseline", help="Baseline OpenAPI source for change-impact reporting")
    parser.add_argument("--current", help="Current OpenAPI source for change-impact reporting")
    parser.add_argument("--documentation-mode", default="auto", help="Narrative documentation mode: auto, mixed, bdd, tdd, plain-text, or none")
    parser.add_argument("--output-manifest", help="Optional markdown manifest path")
    args = parser.parse_args()

    mapping = Path(args.mapping).resolve()
    mismatches = Path(args.mismatches).resolve()
    tests_root = Path(args.tests_root).resolve()
    html_dir = Path(args.html_dir).resolve()
    report_dir = mapping.parent.resolve()
    html_dir.mkdir(parents=True, exist_ok=True)

    root = Path(__file__).resolve().parents[3]
    coverage_gap_script = script_path(root, "documentation", "coverage-gap-report", "scripts", "generate_coverage_gap_report.py")
    assertion_script = script_path(root, "documentation", "assertion-strength-report", "scripts", "generate_assertion_strength_report.py")
    change_impact_script = script_path(root, "documentation", "openapi-change-impact-report", "scripts", "generate_openapi_change_impact_report.py")
    html_portal_script = script_path(root, "documentation", "traceability-report", "scripts", "generate_html_reports.py")

    run_script(
        coverage_gap_script,
        "--mapping",
        str(mapping),
        "--output-md",
        str(report_dir / "coverage-gap-report.md"),
        "--output-html",
        str(html_dir / "coverage-gap-report.html"),
    )
    run_script(
        assertion_script,
        "--tests-root",
        str(tests_root),
        "--mapping",
        str(mapping),
        "--output-md",
        str(report_dir / "assertion-strength-report.md"),
        "--output-html",
        str(html_dir / "assertion-strength-report.html"),
    )

    include_change_impact = bool(args.baseline and args.current)
    if include_change_impact:
        run_script(
            change_impact_script,
            "--baseline",
            str(args.baseline),
            "--current",
            str(args.current),
            "--mapping",
            str(mapping),
            "--output-md",
            str(report_dir / "openapi-change-impact-report.md"),
            "--output-html",
            str(html_dir / "openapi-change-impact-report.html"),
        )

    run_script(
        html_portal_script,
        "--mapping",
        str(mapping),
        "--mismatches",
        str(mismatches),
        "--outdir",
        str(html_dir),
    )

    if args.output_manifest:
        write_manifest(
            Path(args.output_manifest).resolve(),
            mapping,
            mismatches,
            tests_root,
            html_dir,
            args.documentation_mode,
            include_change_impact,
            report_dir,
        )
        print(Path(args.output_manifest).resolve())

    print(report_dir / "coverage-gap-report.md")
    print(report_dir / "assertion-strength-report.md")
    if include_change_impact:
        print(report_dir / "openapi-change-impact-report.md")
    print(html_dir / "index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
