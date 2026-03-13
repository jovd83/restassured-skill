#!/usr/bin/env python3
"""Generate a coverage gap report from the canonical traceability markdown."""

from __future__ import annotations

import argparse
import html
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.report_theme import load_report_theme_css


SUMMARY_RE = re.compile(r"^- ([^:]+):\s*(.*)$")
TABLE_DIVIDER_RE = re.compile(r"^\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?$")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
CODE_RE = re.compile(r"`([^`]+)`")
API_PREFIX_RE = re.compile(r"^/api/v\d+")


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


def resource_name(path_text: str) -> str:
    path = API_PREFIX_RE.sub("", plain(path_text))
    if path.endswith("openapi.json") or path.endswith("swagger.json"):
        return "support"
    parts = [part for part in path.split("/") if part]
    return parts[0] if parts else "support"


def skip_blanks(lines: list[str], idx: int) -> int:
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    return idx


def split_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_summary(lines: list[str], start: int) -> tuple[dict[str, str], int]:
    idx = skip_blanks(lines, start)
    data: dict[str, str] = {}
    while idx < len(lines):
        line = lines[idx].rstrip()
        if not line:
            idx += 1
            continue
        if line.startswith("## "):
            break
        match = SUMMARY_RE.match(line)
        if match:
            data[match.group(1).strip()] = match.group(2).strip()
        idx += 1
    return data, idx


def parse_table(lines: list[str], start: int) -> tuple[list[dict[str, str]], int]:
    idx = skip_blanks(lines, start)
    rows: list[dict[str, str]] = []
    if idx >= len(lines) or not lines[idx].lstrip().startswith("|"):
        return rows, idx
    headers = split_cells(lines[idx])
    idx += 1
    idx = skip_blanks(lines, idx)
    if idx < len(lines) and TABLE_DIVIDER_RE.match(lines[idx].strip()):
        idx += 1
    while idx < len(lines):
        line = lines[idx].rstrip()
        if not line or line.startswith("## ") or not line.lstrip().startswith("|"):
            break
        if TABLE_DIVIDER_RE.match(line.strip()):
            idx += 1
            continue
        values = split_cells(line)
        rows.append({headers[i]: values[i] if i < len(values) else "" for i in range(len(headers))})
        idx += 1
    return rows, idx


def parse_list(lines: list[str], start: int) -> tuple[list[str], int]:
    idx = skip_blanks(lines, start)
    items: list[str] = []
    while idx < len(lines):
        line = lines[idx].rstrip()
        if not line:
            idx += 1
            continue
        if line.startswith("## "):
            break
        if line.startswith("- "):
            items.append(line[2:].strip())
        idx += 1
    return items, idx


def parse_mapping(path: Path) -> tuple[dict[str, str], list[dict[str, str]], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    summary: dict[str, str] = {}
    rows: list[dict[str, str]] = []
    gaps: list[str] = []
    idx = 0
    while idx < len(lines):
        line = lines[idx].rstrip()
        if line == "## Summary":
            summary, idx = parse_summary(lines, idx + 1)
            continue
        if line == "## Endpoint Mapping":
            rows, idx = parse_table(lines, idx + 1)
            continue
        if line == "## Gaps":
            gaps, idx = parse_list(lines, idx + 1)
            continue
        idx += 1
    return summary, rows, gaps


def build_operation_gaps(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    gaps: list[dict[str, str]] = []
    for row in rows:
        status = plain(row.get("Status", ""))
        if status not in {"Not covered", "Partial", "Contract drift"}:
            continue
        reason = {
            "Not covered": "No executable coverage exists for this operation.",
            "Partial": "The operation is only partially proven by the current suite.",
            "Contract drift": "The operation is only proven through runtime-drift assertions.",
        }.get(status, "Coverage is incomplete.")
        gaps.append(
            {
                "Method": row.get("Method", ""),
                "Path": row.get("Path", ""),
                "Operation ID": row.get("Operation ID", ""),
                "Status": status,
                "Why It Is A Gap": reason,
                "Recommended Next Action": "Add or strengthen executable coverage for the happy path and critical negative cases."
                if status != "Not covered"
                else "Implement a focused Rest Assured slice for this operation.",
            }
        )
    return gaps


def recommend_next_slice(operation_gaps: list[dict[str, str]], gap_bullets: list[str]) -> str:
    if operation_gaps:
        counts = Counter(resource_name(row["Path"]) for row in operation_gaps)
        resource, count = counts.most_common(1)[0]
        return f"Prioritize the `{resource}` resource next because it contains {count} primary gap operation(s)."
    if gap_bullets:
        return f"Prioritize the explicit gap note: {gap_bullets[0]}"
    return "No primary gap slice is open. Use this report as a drift and hardening watchlist."


def write_markdown(summary: dict[str, str], operation_gaps: list[dict[str, str]], gap_bullets: list[str], output: Path) -> None:
    lines = [
        "# Coverage Gap Report",
        "",
        "## Summary",
        "",
        f"- Service: {summary.get('Service', '')}",
        f"- Contract source: {summary.get('Contract source', '')}",
        f"- Last updated: {summary.get('Last updated', '')}",
        f"- Total operations: {summary.get('Total operations', '')}",
        f"- Not covered: {summary.get('Not covered', '0')}",
        f"- Partial: {summary.get('Partial', '0')}",
        f"- Contract drift: {summary.get('Contract drift', '0')}",
        f"- Explicit gap bullets: {len(gap_bullets)}",
        "",
        "## Operation Gaps",
        "",
        "| Method | Path | Operation ID | Status | Why It Is A Gap | Recommended Next Action |",
        "|---|---|---|---|---|---|",
    ]
    if operation_gaps:
        for row in operation_gaps:
            lines.append(
                f"| {row['Method']} | {row['Path']} | {row['Operation ID']} | {row['Status']} | {row['Why It Is A Gap']} | {row['Recommended Next Action']} |"
            )
    else:
        lines.append("| - | - | - | No primary operation gaps | Use the explicit gap bullets and drift watchlist instead. | Monitor the current suite and add hardening where needed. |")
    lines.extend(["", "## Gap Bullets", ""])
    if gap_bullets:
        for gap in gap_bullets:
            lines.append(f"- {gap}")
    else:
        lines.append("- None")
    lines.extend(["", "## Recommended Next Slice", "", f"- {recommend_next_slice(operation_gaps, gap_bullets)}", ""])
    output.write_text("\n".join(lines), encoding="utf-8")


def write_html(summary: dict[str, str], operation_gaps: list[dict[str, str]], gap_bullets: list[str], output: Path) -> None:
    gap_rows = "".join(
        f"<tr><td>{render_inline(row['Method'])}</td><td>{render_inline(row['Path'])}</td><td>{render_inline(row['Operation ID'])}</td>"
        f"<td><span class='chip chip-{plain(row['Status']).lower().replace(' ', '-')}'>{html.escape(row['Status'])}</span></td>"
        f"<td>{render_inline(row['Why It Is A Gap'])}</td><td>{render_inline(row['Recommended Next Action'])}</td></tr>"
        for row in operation_gaps
    ) or "<tr><td colspan='6'>No primary operation gaps. The current focus is drift and hardening.</td></tr>"
    gap_cards = "".join(f"<li>{render_inline(item)}</li>" for item in gap_bullets) or "<li>None</li>"
    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Coverage Gap Report</title>
<style>{load_report_theme_css()}</style></head>
<body><main>
<section class="hero"><h1>Coverage Gap Report</h1><p>Use this view to focus on uncovered, partial, and drift-only coverage before reading the full traceability report.</p>
<div class="cards">
<div class="card"><div class="label">Not Covered</div><div class="value">{html.escape(summary.get('Not covered', '0'))}</div></div>
<div class="card"><div class="label">Partial</div><div class="value">{html.escape(summary.get('Partial', '0'))}</div></div>
<div class="card"><div class="label">Contract Drift</div><div class="value">{html.escape(summary.get('Contract drift', '0'))}</div></div>
<div class="card"><div class="label">Explicit Gaps</div><div class="value">{len(gap_bullets)}</div></div>
</div></section>
<section class="panel"><h2>Operation Gaps</h2><div class="table-shell"><table><thead><tr><th>Method</th><th>Path</th><th>Operation ID</th><th>Status</th><th>Why It Is A Gap</th><th>Recommended Next Action</th></tr></thead><tbody>{gap_rows}</tbody></table></div></section>
<section class="panel"><h2>Gap Bullets</h2><ul>{gap_cards}</ul></section>
<section class="panel"><h2>Recommended Next Slice</h2><p>{render_inline(recommend_next_slice(operation_gaps, gap_bullets))}</p></section>
</main></body></html>"""
    output.write_text(doc, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a coverage gap report from the traceability markdown.")
    parser.add_argument("--mapping", required=True, help="Path to docs/testing/test-mapping-report.md")
    parser.add_argument("--output-md", required=True, help="Markdown output path")
    parser.add_argument("--output-html", required=True, help="HTML output path")
    args = parser.parse_args()

    summary, rows, gap_bullets = parse_mapping(Path(args.mapping))
    operation_gaps = build_operation_gaps(rows)
    write_markdown(summary, operation_gaps, gap_bullets, Path(args.output_md))
    write_html(summary, operation_gaps, gap_bullets, Path(args.output_html))
    print(Path(args.output_md).resolve())
    print(Path(args.output_html).resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
