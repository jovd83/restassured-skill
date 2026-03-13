#!/usr/bin/env python3
"""Generate an assertion-strength report from Rest Assured Java tests."""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.report_theme import load_report_theme_css


TEST_ANNOTATION_RE = re.compile(r"@(?:Test|ParameterizedTest|RepeatedTest)\b")
METHOD_SIGNATURE_RE = re.compile(r"(?:public|protected|private)?\s+void\s+([A-Za-z0-9_]+)\s*\(")
STATUS_RE = re.compile(r"\bstatusCode\s*\(")
CONTENT_RE = re.compile(r"\bcontentType\s*\(")
HEADER_RE = re.compile(r"\bheaders?\s*\(")
BODY_RE = re.compile(r"\bbody\s*\(|\bjsonPath\s*\(|\bxmlPath\s*\(")
SCHEMA_RE = re.compile(r"\bmatchesJsonSchema|\bmatchesXsd")
HTTP_CALL_RE = re.compile(r"\bgiven\s*\(|\bwhen\s*\(")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
CODE_RE = re.compile(r"`([^`]+)`")
TABLE_DIVIDER_RE = re.compile(r"^\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?$")


def split_link(target: str) -> tuple[str, str]:
    if "#" in target:
        path_part, anchor = target.split("#", 1)
        return path_part, f"#{anchor}"
    return target, ""


def to_href(target: str) -> str:
    path_part, anchor = split_link(target)
    if re.match(r"^[A-Za-z]:[\\/]", path_part):
        return f"{Path(path_part).resolve().as_uri()}{anchor}"
    if path_part.startswith(("http://", "https://", "file://")):
        return target
    return f"{quote(path_part)}{anchor}"


def render_inline(text: str) -> str:
    tokens: dict[str, str] = {}

    def repl_link(match: re.Match[str]) -> str:
        token = f"__L{len(tokens)}__"
        tokens[token] = f'<a href="{html.escape(to_href(match.group(2)))}">{html.escape(match.group(1))}</a>'
        return token

    def repl_code(match: re.Match[str]) -> str:
        token = f"__C{len(tokens)}__"
        tokens[token] = f"<code>{html.escape(match.group(1))}</code>"
        return token

    work = LINK_RE.sub(repl_link, text)
    work = CODE_RE.sub(repl_code, work)
    out = html.escape(work)
    for token, replacement in tokens.items():
        out = out.replace(html.escape(token), replacement)
    return out


def plain(text: str) -> str:
    text = LINK_RE.sub(lambda match: match.group(1), text)
    text = CODE_RE.sub(lambda match: match.group(1), text)
    return re.sub(r"\s+", " ", text).strip(" ,")


def split_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def skip_blanks(lines: list[str], idx: int) -> int:
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    return idx


def parse_reverse_mapping(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    idx = 0
    mapping: dict[str, str] = {}
    while idx < len(lines):
        if lines[idx].rstrip() != "## Reverse Mapping By Test Class":
            idx += 1
            continue
        idx = skip_blanks(lines, idx + 1)
        headers = split_cells(lines[idx])
        idx += 1
        idx = skip_blanks(lines, idx)
        if idx < len(lines) and TABLE_DIVIDER_RE.match(lines[idx].strip()):
            idx += 1
        while idx < len(lines):
            line = lines[idx].rstrip()
            if not line or line.startswith("## "):
                break
            values = split_cells(line)
            row = {headers[i]: values[i] if i < len(values) else "" for i in range(len(headers))}
            label = row.get("Test Class", "")
            class_name = LINK_RE.sub(lambda match: Path(match.group(2)).stem, label)
            mapping[class_name] = row.get("Endpoints And Methods", "")
            idx += 1
        break
    return mapping


def extract_methods(content: str) -> list[tuple[str, int, str]]:
    lines = content.splitlines()
    line_starts = []
    cursor = 0
    for line in lines:
        line_starts.append(cursor)
        cursor += len(line) + 1
    methods: list[tuple[str, int, str]] = []
    annotation_positions = list(TEST_ANNOTATION_RE.finditer(content))
    for annotation in annotation_positions:
        signature = METHOD_SIGNATURE_RE.search(content, annotation.end())
        if not signature:
            continue
        brace_start = content.find("{", signature.end())
        if brace_start == -1:
            continue
        depth = 1
        idx = brace_start + 1
        while idx < len(content) and depth:
            char = content[idx]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
            idx += 1
        method_name = signature.group(1)
        start_offset = annotation.start()
        line_number = 1 + sum(1 for start in line_starts if start < start_offset)
        methods.append((method_name, line_number, content[brace_start:idx]))
    return methods


def classify(body: str) -> tuple[str, list[str], list[str]]:
    status = bool(STATUS_RE.search(body))
    content = bool(CONTENT_RE.search(body))
    header = bool(HEADER_RE.search(body))
    body_assert = bool(BODY_RE.search(body))
    schema = bool(SCHEMA_RE.search(body))
    http_calls = len(HTTP_CALL_RE.findall(body))
    workflow = http_calls > 2
    signals = []
    weaknesses = []
    score = 0
    if status:
        signals.append("status")
        score += 1
    if content:
        signals.append("content-type")
        score += 1
    if header:
        signals.append("headers")
        score += 1
    if body_assert:
        signals.append("body")
        score += 2
    if schema:
        signals.append("schema")
        score += 2
    if workflow:
        signals.append("workflow")
        score += 1
    if status and not (body_assert or schema or header):
        weaknesses.append("Transport-level assertions dominate")
    if not body_assert and not schema:
        weaknesses.append("No semantic payload validation")
    if http_calls <= 1:
        weaknesses.append("Single-call verification only")
    if score <= 1:
        return "Weak", signals, weaknesses
    if score <= 3:
        return "Moderate", signals, weaknesses
    return "Strong", signals, weaknesses


def recommend(strength: str, weaknesses: list[str]) -> str:
    if strength == "Weak":
        return "Add body assertions or workflow-level follow-up checks."
    if strength == "Moderate":
        return "Add stronger semantic assertions on key fields or side effects."
    return "Keep the current strength and watch for helper-based hidden assertions."


def write_markdown(results: list[dict[str, str]], output: Path) -> None:
    weak = sum(1 for row in results if row["Strength"] == "Weak")
    moderate = sum(1 for row in results if row["Strength"] == "Moderate")
    strong = sum(1 for row in results if row["Strength"] == "Strong")
    transport_only = sum(1 for row in results if "Transport-level assertions dominate" in row["Weaknesses"])
    lines = [
        "# Assertion Strength Report",
        "",
        "## Summary",
        "",
        f"- Tests analyzed: {len(results)}",
        "- Last updated: 2026-03-12",
        f"- Weak: {weak}",
        f"- Moderate: {moderate}",
        f"- Strong: {strong}",
        f"- Transport-only: {transport_only}",
        "",
        "## Test Strength",
        "",
        "| Test Class | Test Method | Strength | Signals Found | Weaknesses | Recommended Improvement |",
        "|---|---|---|---|---|---|",
    ]
    for row in results:
        lines.append(
            f"| {row['Test Class']} | {row['Test Method']} | {row['Strength']} | {row['Signals Found']} | {row['Weaknesses']} | {row['Recommended Improvement']} |"
        )
    weak_rows = [row for row in results if row["Strength"] == "Weak"]
    lines.extend(["", "## Priority Fixes", ""])
    if weak_rows:
        for row in weak_rows[:10]:
            lines.append(f"- Strengthen `{row['Test Class']}::{row['Test Method']}` by adding semantic assertions.")
    else:
        lines.append("- None")
    lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")


def write_html(results: list[dict[str, str]], output: Path) -> None:
    weak = sum(1 for row in results if row["Strength"] == "Weak")
    moderate = sum(1 for row in results if row["Strength"] == "Moderate")
    strong = sum(1 for row in results if row["Strength"] == "Strong")
    transport_only = sum(1 for row in results if "Transport-level assertions dominate" in row["Weaknesses"])
    rows_html = "".join(
        f"<tr><td>{render_inline(row['Test Class'])}</td><td>{render_inline(row['Test Method'])}</td>"
        f"<td><span class='chip chip-{row['Strength'].lower()}'>{html.escape(row['Strength'])}</span></td>"
        f"<td>{render_inline(row['Signals Found'])}</td><td>{render_inline(row['Weaknesses'])}</td><td>{render_inline(row['Recommended Improvement'])}</td></tr>"
        for row in results
    )
    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Assertion Strength Report</title>
<style>{load_report_theme_css()}</style></head>
<body><main>
<section class="hero"><h1>Assertion Strength Report</h1><p>Score the current Rest Assured test methods and isolate weak assertions before false confidence spreads across the suite.</p>
<div class="cards">
<div class="card"><div class="label">Weak</div><div class="value">{weak}</div></div>
<div class="card"><div class="label">Moderate</div><div class="value">{moderate}</div></div>
<div class="card"><div class="label">Strong</div><div class="value">{strong}</div></div>
<div class="card"><div class="label">Transport-only</div><div class="value">{transport_only}</div></div>
</div></section>
<section class="panel"><h2>Test Strength</h2><div class="table-shell"><table><thead><tr><th>Test Class</th><th>Test Method</th><th>Strength</th><th>Signals Found</th><th>Weaknesses</th><th>Recommended Improvement</th></tr></thead><tbody>{rows_html}</tbody></table></div></section>
</main></body></html>"""
    output.write_text(doc, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an assertion-strength report for Rest Assured Java tests.")
    parser.add_argument("--tests-root", required=True, help="Root folder containing Java test classes")
    parser.add_argument("--mapping", required=True, help="Path to docs/testing/test-mapping-report.md")
    parser.add_argument("--output-md", required=True, help="Markdown output path")
    parser.add_argument("--output-html", required=True, help="HTML output path")
    args = parser.parse_args()

    endpoint_map = parse_reverse_mapping(Path(args.mapping))
    results: list[dict[str, str]] = []
    for path in sorted(Path(args.tests_root).rglob("*.java")):
        content = path.read_text(encoding="utf-8")
        class_name = path.stem
        endpoints = endpoint_map.get(class_name, "")
        for method_name, line_number, body in extract_methods(content):
            strength, signals, weaknesses = classify(body)
            if endpoints:
                signals.append(f"endpoints: {plain(endpoints)}")
            results.append(
                {
                    "Test Class": f"[{class_name}.java#L{line_number}]({path.resolve()}#L{line_number})",
                    "Test Method": f"`{method_name}`",
                    "Strength": strength,
                    "Signals Found": ", ".join(f"`{item}`" for item in signals) if signals else "-",
                    "Weaknesses": ", ".join(f"`{item}`" for item in weaknesses) if weaknesses else "-",
                    "Recommended Improvement": recommend(strength, weaknesses),
                }
            )

    write_markdown(results, Path(args.output_md))
    write_html(results, Path(args.output_html))
    print(Path(args.output_md).resolve())
    print(Path(args.output_html).resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
