#!/usr/bin/env python3
"""Evaluate report-driven quality gates for a Rest Assured suite."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


SUMMARY_RE = re.compile(r"^- ([^:]+):\s*(.*)$")
MISMATCH_RE = re.compile(r"^###\s+Mismatch\s+\d+\s*$")
STATUS_RE = re.compile(r"^- Status:\s*(.*)$")
INT_RE = re.compile(r"-?\d+")
CODE_RE = re.compile(r"`([^`]+)`")


def parse_summary(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    summary: dict[str, str] = {}
    in_summary = False
    for line in lines:
        if line.rstrip() == "## Summary":
            in_summary = True
            continue
        if in_summary and line.startswith("## "):
            break
        if in_summary:
            match = SUMMARY_RE.match(line.rstrip())
            if match:
                summary[match.group(1).strip()] = match.group(2).strip()
    return summary


def to_int(text: str | None) -> int:
    if not text:
        return 0
    match = INT_RE.search(text)
    return int(match.group(0)) if match else 0


def plain(text: str) -> str:
    text = CODE_RE.sub(lambda match: match.group(1), text)
    return re.sub(r"\s+", " ", text).strip()


def parse_mismatch_statuses(path: Path) -> Counter[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    statuses: Counter[str] = Counter()
    in_mismatch = False
    for line in lines:
        if MISMATCH_RE.match(line.rstrip()):
            in_mismatch = True
            continue
        if in_mismatch and line.startswith("### "):
            in_mismatch = False
        if in_mismatch:
            match = STATUS_RE.match(line.rstrip())
            if match:
                statuses[plain(match.group(1))] += 1
    return statuses


def evaluate(metric: str, actual: int, maximum: int | None, failures: list[str], report_lines: list[str]) -> None:
    if maximum is None:
        return
    report_lines.append(f"- {metric}: actual `{actual}`, allowed `{maximum}`")
    if actual > maximum:
        failures.append(f"{metric} exceeded: actual {actual}, allowed {maximum}")


def write_report(output: Path, report_lines: list[str], failures: list[str], passed: bool) -> None:
    lines = [
        "# Quality Gate Evaluation",
        "",
        "## Result",
        "",
        f"- Passed: `{'true' if passed else 'false'}`",
        "",
        "## Evaluated Metrics",
        "",
        *report_lines,
        "",
        "## Failures",
        "",
    ]
    if failures:
        for failure in failures:
            lines.append(f"- {failure}")
    else:
        lines.append("- None")
    lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate report-driven quality gates for a Rest Assured suite.")
    parser.add_argument("--coverage-gap", required=True, help="Path to coverage-gap-report.md")
    parser.add_argument("--assertion-strength", required=True, help="Path to assertion-strength-report.md")
    parser.add_argument("--contract-mismatches", help="Path to contract-mismatches.md")
    parser.add_argument("--change-impact", help="Path to openapi-change-impact-report.md")
    parser.add_argument("--max-not-covered", type=int)
    parser.add_argument("--max-partial", type=int)
    parser.add_argument("--max-contract-drift", type=int)
    parser.add_argument("--max-weak", type=int)
    parser.add_argument("--max-transport-only", type=int)
    parser.add_argument("--max-potential-defects", type=int)
    parser.add_argument("--max-known-drift", type=int)
    parser.add_argument("--max-needs-product-decision", type=int)
    parser.add_argument("--max-breaking-changes", type=int)
    parser.add_argument("--output-md", help="Optional markdown output path")
    args = parser.parse_args()

    failures: list[str] = []
    report_lines: list[str] = []

    coverage = parse_summary(Path(args.coverage_gap).resolve())
    strength = parse_summary(Path(args.assertion_strength).resolve())

    evaluate("Not covered", to_int(coverage.get("Not covered")), args.max_not_covered, failures, report_lines)
    evaluate("Partial", to_int(coverage.get("Partial")), args.max_partial, failures, report_lines)
    evaluate("Contract drift", to_int(coverage.get("Contract drift")), args.max_contract_drift, failures, report_lines)
    evaluate("Weak tests", to_int(strength.get("Weak")), args.max_weak, failures, report_lines)
    evaluate("Transport-only tests", to_int(strength.get("Transport-only")), args.max_transport_only, failures, report_lines)

    if args.contract_mismatches:
        statuses = parse_mismatch_statuses(Path(args.contract_mismatches).resolve())
        evaluate("Potential defects", statuses.get("Potential defect", 0), args.max_potential_defects, failures, report_lines)
        evaluate("Known drift", statuses.get("Known drift", 0), args.max_known_drift, failures, report_lines)
        evaluate(
            "Needs product decision",
            statuses.get("Needs product decision", 0),
            args.max_needs_product_decision,
            failures,
            report_lines,
        )

    if args.change_impact:
        impact = parse_summary(Path(args.change_impact).resolve())
        evaluate("Breaking changes", to_int(impact.get("Breaking changes")), args.max_breaking_changes, failures, report_lines)

    passed = not failures
    if args.output_md:
        write_report(Path(args.output_md).resolve(), report_lines, failures, passed)
        print(Path(args.output_md).resolve())

    for line in report_lines:
        print(line)
    if failures:
        print("Quality gates failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Quality gates passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
