#!/usr/bin/env python3
"""Generate HTML reports from traceability and contract-mismatch markdown."""

from __future__ import annotations

import argparse
import html
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.report_theme import load_report_theme_css


SUMMARY_RE = re.compile(r"^- ([^:]+):\s*(.*)$")
MISMATCH_RE = re.compile(r"^###\s+(Mismatch\s+\d+)\s*$")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
CODE_RE = re.compile(r"`([^`]+)`")
TABLE_DIVIDER_RE = re.compile(r"^\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?$")
API_PREFIX_RE = re.compile(r"^/api/v\d+")

OPTIONAL_REPORTS = (
    {
        "stem": "coverage-gap-report",
        "title": "Coverage Gap Report",
        "description": "Focus planning on uncovered, partial, and drift-only operations.",
        "metrics": (("Not covered", "Not covered"), ("Partial", "Partial"), ("Contract drift", "Contract drift")),
    },
    {
        "stem": "openapi-change-impact-report",
        "title": "OpenAPI Change Impact Report",
        "description": "Compare baseline and current contracts and show impacted tests before drift becomes surprise work.",
        "metrics": (("Added operations", "Added"), ("Removed operations", "Removed"), ("Breaking changes", "Breaking")),
    },
    {
        "stem": "assertion-strength-report",
        "title": "Assertion Strength Report",
        "description": "Expose weak and transport-only tests so shallow checks are easy to strengthen.",
        "metrics": (("Weak", "Weak"), ("Moderate", "Moderate"), ("Strong", "Strong")),
    },
)


def slug(text: str) -> str:
    text = plain(text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "item"


def plain(text: str) -> str:
    text = LINK_RE.sub(lambda m: m.group(1), text)
    text = CODE_RE.sub(lambda m: m.group(1), text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" ,")


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
        tokens[token] = f'<a class="report-link" href="{html.escape(to_href(match.group(2)))}">{html.escape(match.group(1))}</a>'
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
    return out.replace("\n", "<br>")


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


def parse_traceability(path: Path) -> dict[str, object]:
    lines = path.read_text(encoding="utf-8").splitlines()
    data: dict[str, object] = {"summary": {}, "endpoint_mapping": [], "reverse_by_test": [], "reverse_by_docs": [], "gaps": []}
    idx = 0
    while idx < len(lines):
        line = lines[idx].rstrip()
        if line == "## Summary":
            data["summary"], idx = parse_summary(lines, idx + 1)
            continue
        if line == "## Endpoint Mapping":
            data["endpoint_mapping"], idx = parse_table(lines, idx + 1)
            continue
        if line == "## Reverse Mapping By Test Class":
            data["reverse_by_test"], idx = parse_table(lines, idx + 1)
            continue
        if line == "## Reverse Mapping By Documentation Artifact":
            data["reverse_by_docs"], idx = parse_table(lines, idx + 1)
            continue
        if line == "## Reverse Mapping By BDD Feature":
            data["reverse_by_docs"], idx = parse_table(lines, idx + 1)
            continue
        if line == "## Gaps":
            data["gaps"], idx = parse_list(lines, idx + 1)
            continue
        idx += 1
    return data


def parse_mismatches(path: Path) -> dict[str, object]:
    lines = path.read_text(encoding="utf-8").splitlines()
    summary: dict[str, str] = {}
    mismatches: list[dict[str, str]] = []
    idx = 0
    while idx < len(lines):
        line = lines[idx].rstrip()
        if line == "## Summary":
            summary, idx = parse_summary(lines, idx + 1)
            continue
        match = MISMATCH_RE.match(line)
        if match:
            item: dict[str, str] = {"Title": match.group(1)}
            idx += 1
            while idx < len(lines):
                cur = lines[idx].rstrip()
                if not cur:
                    idx += 1
                    continue
                if cur.startswith("### ") or cur.startswith("## "):
                    break
                bullet = SUMMARY_RE.match(cur)
                if bullet:
                    item[bullet.group(1).strip()] = bullet.group(2).strip()
                idx += 1
            mismatches.append(item)
            continue
        idx += 1
    return {"summary": summary, "mismatches": mismatches}


def parse_generic_summary(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    idx = 0
    while idx < len(lines):
        if lines[idx].rstrip() == "## Summary":
            summary, _ = parse_summary(lines, idx + 1)
            return summary
        idx += 1
    return {}


def collect_optional_reports(report_dir: Path, outdir: Path) -> list[dict[str, object]]:
    reports: list[dict[str, object]] = []
    for spec in OPTIONAL_REPORTS:
        stem = spec["stem"]
        md_path = report_dir / f"{stem}.md"
        html_path = outdir / f"{stem}.html"
        if not md_path.exists() or not html_path.exists():
            continue
        reports.append(
            {
                **spec,
                "md_path": md_path,
                "html_path": html_path,
                "summary": parse_generic_summary(md_path),
            }
        )
    return reports


def resource_name(path_text: str) -> str:
    path = API_PREFIX_RE.sub("", plain(path_text))
    if path.endswith("openapi.json") or path.endswith("swagger.json"):
        return "support"
    parts = [part for part in path.split("/") if part]
    return parts[0] if parts else "support"


def item_count(text: str) -> int:
    links = LINK_RE.findall(text)
    if links:
        return len(links)
    return len([item.strip() for item in plain(text).split(",") if item.strip()])


def split_items(text: str) -> list[str]:
    return [item.strip() for item in text.split(",") if item.strip()]


def distribute_items(items: list[str], row_count: int) -> list[list[str]]:
    buckets = [[] for _ in range(max(row_count, 1))]
    if not items:
        return buckets
    if row_count <= 1:
        buckets[0] = items[:]
        return buckets
    if len(items) == row_count:
        for index, item in enumerate(items):
            buckets[index].append(item)
        return buckets
    if len(items) < row_count:
        for index, item in enumerate(items):
            buckets[index].append(item)
        return buckets
    for index, item in enumerate(items):
        target = index if index < row_count - 1 else row_count - 1
        buckets[target].append(item)
    return buckets


def chip(label: str) -> str:
    return f'<span class="chip chip-{slug(label)}">{html.escape(label)}</span>'


def method_badge(method: str) -> str:
    return f'<span class="method-badge method-{slug(method)}">{html.escape(method)}</span>'


def detail(title: str, value: str) -> str:
    if not value:
        return ""
    return detail_html(title, f"<p>{render_inline(value)}</p>")


def detail_html(title: str, body_html: str, wide: bool = False) -> str:
    wide_class = " detail-wide" if wide else ""
    return f'<div class="detail-card{wide_class}"><strong>{html.escape(title)}</strong>{body_html}</div>'


def render_item_stack(items: list[str]) -> str:
    if not items:
        return '<span class="empty-cell">-</span>'
    return "".join(f'<div class="coverage-cell-item">{render_inline(item)}</div>' for item in items)


def documentation_refs(row: dict[str, str]) -> str:
    return row.get("Documentation References", row.get("BDD References", ""))


def documentation_reverse_title(rows: list[dict[str, str]]) -> str:
    if rows and "BDD Feature" in rows[0]:
        return "BDD Feature"
    return "Documentation Artifact"


def documentation_reverse_heading(rows: list[dict[str, str]]) -> str:
    if rows and "BDD Feature" in rows[0]:
        return "Reverse Mapping By BDD Feature"
    return "Reverse Mapping By Documentation Artifact"


def documentation_reverse_note(rows: list[dict[str, str]]) -> str:
    if rows and "BDD Feature" in rows[0]:
        return "Start from the Gherkin layer and walk back to endpoints and test methods."
    return "Start from the narrative documentation layer and walk back to endpoints and test methods."


def documentation_reverse_blocks(rows: list[dict[str, str]]) -> list[tuple[str, str]]:
    if rows and "BDD Feature" in rows[0]:
        return [("Scenarios", "Scenarios"), ("Endpoints", "Endpoints And Methods"), ("Tests", "Test References")]
    if rows and "Scenario Or Case References" in rows[0]:
        return [
            ("Type", "Documentation Type"),
            ("Cases", "Scenario Or Case References"),
            ("Endpoints", "Endpoints And Methods"),
            ("Tests", "Test References"),
        ]
    return [
        ("Type", "Documentation Type"),
        ("Cases", "Scenario Or Case References"),
        ("Endpoints", "Endpoints And Methods"),
        ("Tests", "Test References"),
    ]


def coverage_matrix(coverage: str, tests: str, docs: str) -> str:
    coverage_items = split_items(coverage)
    test_items = split_items(tests)
    doc_items = split_items(docs)
    row_count = len(test_items) if test_items else max(len(coverage_items), len(doc_items), 1)
    coverage_groups = distribute_items(coverage_items, row_count)
    test_groups = distribute_items(test_items, row_count)
    doc_groups = distribute_items(doc_items, row_count)
    rows = []
    for index in range(row_count):
        rows.append(
            '<div class="coverage-entry">'
            f'<div>{render_item_stack(coverage_groups[index])}</div>'
            f'<div>{render_item_stack(test_groups[index])}</div>'
            f'<div>{render_item_stack(doc_groups[index])}</div>'
            '</div>'
        )
    return (
        '<div class="coverage-table">'
        '<div class="coverage-head"><div>Coverage Row</div><div>Test Reference</div><div>Documentation Reference</div></div>'
        f'{"".join(rows)}'
        '</div>'
    )


def cards(items: list[tuple[str, str, str]]) -> str:
    html_cards = []
    for label, value, meta in items:
        meta_html = f'<div class="meta">{render_inline(meta)}</div>' if meta else ""
        html_cards.append(f'<div class="summary-card"><div class="label">{html.escape(label)}</div><div class="value">{render_inline(value)}</div>{meta_html}</div>')
    return f'<div class="card-grid">{"".join(html_cards)}</div>'


def portal_card(title: str, description: str, href: str, metrics: str = "", meta: str = "") -> str:
    meta_html = f'<div class="portal-meta metric-row">{metrics}</div>' if metrics else ""
    note_html = f'<p>{html.escape(meta)}</p>' if meta else ""
    return f'<a class="portal-card" href="{html.escape(href)}"><h3>{html.escape(title)}</h3><p>{html.escape(description)}</p>{meta_html}{note_html}</a>'


def source_card(title: str, description: str, href: str, meta: str = "") -> str:
    meta_html = f'<div class="portal-meta metric-row"><span class="metric-pill">{html.escape(meta)}</span></div>' if meta else ""
    return f'<a class="portal-card" href="{html.escape(href)}"><h3>{html.escape(title)}</h3><p>{html.escape(description)}</p>{meta_html}</a>'


def metric_pills(summary: dict[str, str], specs: tuple[tuple[str, str], ...]) -> str:
    pills = []
    for key, label in specs:
        value = summary.get(key)
        if value:
            pills.append(f'<span class="metric-pill">{html.escape(label)} {render_inline(value)}</span>')
    return "".join(pills)


def css() -> str:
    return load_report_theme_css()


def js() -> str:
    return """
document.querySelectorAll('[data-filter-root]').forEach((root)=>{const items=[...root.querySelectorAll('[data-filter-item]')];const groups=[...root.querySelectorAll('[data-filter-group]')];const pills=[...root.querySelectorAll('[data-filter-pill]')];const input=root.querySelector('[data-filter-input]');const count=root.querySelector('[data-filter-count]');const apply=()=>{const active={};pills.forEach((pill)=>{if(pill.classList.contains('active')) active[pill.dataset.filterName||'status']=pill.dataset.filterValue||'all';});const q=(input?.value||'').trim().toLowerCase();let visible=0;items.forEach((item)=>{let ok=!q||(item.dataset.filterText||'').toLowerCase().includes(q);Object.entries(active).forEach(([name,value])=>{if(!ok||value==='all') return;ok=ok&&((item.dataset[name]||'').toLowerCase()===value);});item.hidden=!ok;if(ok) visible+=1;});groups.forEach((group)=>{group.hidden=!Array.from(group.querySelectorAll('[data-filter-item]')).some((item)=>!item.hidden);});if(count) count.textContent=`${visible} visible`;};pills.forEach((pill)=>pill.addEventListener('click',()=>{const name=pill.dataset.filterName||'status';pills.forEach((candidate)=>{if((candidate.dataset.filterName||'status')===name) candidate.classList.remove('active');});pill.classList.add('active');apply();}));if(input) input.addEventListener('input',apply);root.querySelectorAll('[data-toggle-open]').forEach((button)=>button.addEventListener('click',()=>{const shouldOpen=button.dataset.toggleOpen==='true';root.querySelectorAll('details.operation-card').forEach((detail)=>{detail.open=shouldOpen;});}));apply();});
"""


def shell(title: str, page: str, brand: str, side_title: str, side_text: str, sections: list[tuple[str, str]], meta: list[tuple[str, str]], body: str) -> str:
    nav = [("Portal", "index.html", page == "index"), ("Traceability", "test-mapping-report.html", page == "trace"), ("Contract Drift", "contract-mismatches.html", page == "mismatch")]
    portal = "".join(f'<a class="{"active" if active else ""}" href="{html.escape(href)}">{html.escape(label)}</a>' for label, href, active in nav)
    side = "".join(f'<a href="#{html.escape(anchor)}">{html.escape(label)}</a>' for anchor, label in sections)
    meta_html = "".join(f'<div class="meta-item"><strong>{html.escape(label)}</strong>{render_inline(value)}</div>' for label, value in meta if value)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(title)}</title><style>{css()}</style></head>
<body><div class="layout"><aside class="sidebar"><div class="brand-mark">{html.escape(brand)}</div><h1>{html.escape(side_title)}</h1><p>{html.escape(side_text)}</p><div class="nav-title">Portal</div><div class="side-links">{portal}</div><div class="nav-title">Sections</div><div class="side-links">{side}</div><div class="nav-title">Report Meta</div><div class="meta-list">{meta_html}</div></aside><main class="content"><nav class="portal-nav">{portal}</nav>{body}<div class="report-footer">Generated deterministically from the canonical markdown artifacts.</div></main></div><script>{js()}</script></body></html>"""


def resource_cards(rows: list[dict[str, str]]) -> str:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[resource_name(row.get("Path", ""))].append(row)
    out = []
    for name, items in sorted(groups.items()):
        covered = sum(1 for row in items if plain(row.get("Status", "")) == "Covered")
        drift = sum(1 for row in items if plain(row.get("Status", "")) == "Contract drift")
        out.append(f'<article class="resource-card"><h4>{html.escape(name.title())}</h4><div class="pill-row"><span class="metric-pill">{len(items)} operations</span>{chip(f"{covered} covered")}{chip(f"{drift} drift")}</div><p>Grouped exactly the way the operation explorer renders this resource.</p></article>')
    return f'<div class="resource-grid">{"".join(out)}</div>'


def filter_pills(name: str, options: list[tuple[str, str]], active: str = "all") -> str:
    return "".join(
        f'<button type="button" class="filter-pill{" active" if value == active else ""}" data-filter-pill data-filter-name="{html.escape(name)}" data-filter-value="{html.escape(value)}">{html.escape(label)}</button>'
        for label, value in options
    )


def operation_card(row: dict[str, str], open_default: bool) -> str:
    method = plain(row.get("Method", ""))
    path = plain(row.get("Path", ""))
    operation_id = plain(row.get("Operation ID", ""))
    status = plain(row.get("Status", ""))
    coverage = row.get("Coverage Rows", "")
    tests = row.get("Test References", "")
    docs = documentation_refs(row)
    notes = row.get("Notes", "")
    resource = resource_name(path)
    metrics = f'<span class="metric-pill">Coverage {item_count(coverage)}</span><span class="metric-pill">Tests {item_count(tests)}</span><span class="metric-pill">Docs {item_count(docs)}</span>'
    details = "".join(
        [
            detail_html("Executable Coverage", coverage_matrix(coverage, tests, docs), wide=True),
            detail("Notes", notes),
        ]
    )
    data = " ".join([path, operation_id, plain(coverage), plain(tests), plain(docs), plain(notes), resource, status])
    return f'<details class="operation-card" data-filter-item data-status="{html.escape(slug(status))}" data-resource="{html.escape(slug(resource))}" data-filter-text="{html.escape(data)}"{" open" if open_default else ""}><summary class="operation-summary"><div class="operation-main">{method_badge(method)}<div><div class="operation-path">{html.escape(path)}</div><div class="operation-subtitle"><code>{html.escape(operation_id)}</code> in {html.escape(resource.title())}</div></div></div><div class="operation-side">{chip(status)}{metrics}</div></summary><div class="operation-details">{details}</div></details>'


def operations(rows: list[dict[str, str]]) -> str:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[resource_name(row.get("Path", ""))].append(row)
    resource_options = [("All resources", "all")] + [(name.title(), slug(name)) for name in sorted(groups)]
    sections = []
    for name, items in sorted(groups.items()):
        covered = sum(1 for row in items if plain(row.get("Status", "")) == "Covered")
        drift = sum(1 for row in items if plain(row.get("Status", "")) == "Contract drift")
        cards_html = "".join(operation_card(row, index == 0) for index, row in enumerate(items))
        sections.append(f'<section class="resource-section" data-filter-group id="resource-{html.escape(slug(name))}"><div class="resource-heading"><h4>{html.escape(name.title())}</h4><div class="pill-row"><span class="metric-pill">{len(items)} operations</span>{chip(f"{covered} covered")}{chip(f"{drift} drift")}</div></div><div class="operation-stack">{cards_html}</div></section>')
    return f'<div data-filter-root><div class="toolbar"><div class="search-box"><input data-filter-input type="search" placeholder="Search endpoint, operation id, tests, docs, or notes"></div><div class="filters">{filter_pills("status",[("All statuses","all"),("Covered","covered"),("Contract drift","contract-drift"),("Partial","partial"),("Not covered","not-covered")])}</div></div><div class="toolbar"><div class="filters">{filter_pills("resource", resource_options)}</div><div class="action-strip"><button type="button" data-toggle-open="true">Expand all</button><button type="button" data-toggle-open="false">Collapse all</button></div><div class="toolbar-note" data-filter-count></div></div>{"".join(sections)}</div>'


def mapping_cards(rows: list[dict[str, str]], title_key: str, blocks: list[tuple[str, str]]) -> str:
    if not rows:
        return '<p class="empty-state">No rows available.</p>'
    out = []
    for row in rows:
        metrics = "".join(f'<span class="metric-pill">{html.escape(label)} {item_count(row.get(key, ""))}</span>' for label, key in blocks)
        details = "".join(detail(label, row.get(key, "")) for label, key in blocks)
        out.append(f'<article class="mapping-card"><h4>{render_inline(row.get(title_key, ""))}</h4><div class="metric-row">{metrics}</div><div class="operation-details" style="padding:14px 0 0;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))">{details}</div></article>')
    return f'<div class="mapping-grid">{"".join(out)}</div>'


def gap_cards(items: list[str]) -> str:
    if not items:
        return '<p class="empty-state">No gaps reported.</p>'
    return f'<div class="mapping-grid">{"".join(detail("Gap", item) for item in items)}</div>'


def traceability_html(data: dict[str, object], out: Path) -> None:
    summary = data["summary"]
    rows = data["endpoint_mapping"]
    reverse_docs = data["reverse_by_docs"]
    body = f"""
<section id="summary" class="hero"><h2>Traceability Portal</h2><p>Review contract coverage in a grouped operation explorer, then trace each endpoint back to executable Rest Assured tests and narrative documentation references.</p><div class="hero-actions"><a class="hero-action" href="contract-mismatches.html">Open contract drift report</a><a class="hero-action" href="{html.escape(out.name)}">Refresh current page</a></div>{cards([("Total Operations", summary.get("Total operations", str(len(rows))), summary.get("Service", "")),("Covered", summary.get("Covered", "0"), "Fully executable coverage"),("Contract Drift", summary.get("Contract drift", "0"), "Runtime-aligned drift coverage"),("Not Covered", summary.get("Not covered", "0"), "Explicitly missing operations")])}</section>
<section id="resources" class="section"><h3>Resource Overview</h3><p class="section-note">Coverage is grouped by resource so humans can navigate the same way Swagger UI groups operations.</p>{resource_cards(rows)}</section>
<section id="operations" class="section"><h3>Operations Explorer</h3><p class="section-note">Search, filter, and expand operation cards. Each card links the contract operation to tests, documentation, and coverage rows.</p>{operations(rows)}</section>
<section id="reverse-tests" class="section"><h3>Reverse Mapping By Test Class</h3><p class="section-note">Start from the code layer and see which endpoints each test class touches.</p>{mapping_cards(data["reverse_by_test"],"Test Class",[("Test Methods","Test Methods"),("Endpoints","Endpoints And Methods")])}</section>
<section id="reverse-docs" class="section"><h3>{documentation_reverse_heading(reverse_docs)}</h3><p class="section-note">{documentation_reverse_note(reverse_docs)}</p>{mapping_cards(reverse_docs,documentation_reverse_title(reverse_docs),documentation_reverse_blocks(reverse_docs))}</section>
<section id="gaps" class="section"><h3>Coverage Gaps And Risks</h3><p class="section-note">Keep the remaining holes and runtime compromises visible instead of burying them in a footer note.</p>{gap_cards(data["gaps"])}</section>"""
    doc = shell(
        "Traceability Report",
        "trace",
        "Traceability",
        "Endpoint Coverage Map",
        "Grouped operation cards and reverse navigation across contract, tests, and documentation artifacts.",
        [("summary", "Summary"), ("resources", "Resource Overview"), ("operations", "Operations Explorer"), ("reverse-tests", "Reverse By Test"), ("reverse-docs", "Reverse By Docs"), ("gaps", "Gaps")],
        [("Service", summary.get("Service", "")), ("Contract", summary.get("Contract source", "")), ("Updated", summary.get("Last updated", "")), ("Test module", summary.get("Test module", ""))],
        body,
    )
    out.write_text(doc, encoding="utf-8")


def mismatch_card(item: dict[str, str]) -> str:
    title = item.get("Title", "Mismatch")
    endpoint = plain(item.get("Endpoint", ""))
    method = plain(item.get("Method", ""))
    op = plain(item.get("Operation ID", ""))
    status = plain(item.get("Status", "Unknown"))
    classification = plain(item.get("Classification", ""))
    resource = resource_name(endpoint)
    data = " ".join(plain(value) for value in item.values())
    sections = "".join([
        detail("Contract expectation", item.get("Contract expectation", "")),
        detail("Observed runtime behavior", item.get("Observed runtime behavior", "")),
        detail("Decision for executable tests", item.get("Decision for executable tests", "")),
        detail("Evidence", item.get("Evidence", "")),
        detail("Affected tests", item.get("Affected tests", "")),
        detail("Affected coverage rows", item.get("Affected coverage rows", "")),
        detail("Next action", item.get("Next action", "")),
        detail("Owner", item.get("Owner", "")),
        detail("Verification needed", item.get("Verification needed", "")),
    ])
    return f'<article class="mismatch-card" id="{html.escape(slug(title))}" data-filter-item data-status="{html.escape(slug(status))}" data-resource="{html.escape(slug(resource))}" data-filter-text="{html.escape(data)}"><div class="mismatch-head"><div><h4>{html.escape(title)}</h4><p>{method_badge(method)} <span class="operation-path">{html.escape(endpoint)}</span><br><code>{html.escape(op)}</code> in {html.escape(resource.title())}</p></div><div class="pill-row">{chip(status)}{chip(classification) if classification else ""}</div></div><div class="mismatch-body">{sections}</div></article>'


def spotlight_cards(mismatches: list[dict[str, str]]) -> str:
    top = sorted(mismatches, key=lambda item: (plain(item.get("Status", "")) != "Potential defect", plain(item.get("Title", ""))))[:4]
    if not top:
        return '<p class="empty-state">No mismatches recorded.</p>'
    out = []
    for item in top:
        title = item.get("Title", "Mismatch")
        out.append(f'<article class="spotlight-card"><h4><a class="report-link" href="contract-mismatches.html#{html.escape(slug(title))}">{html.escape(title)}</a></h4><div class="pill-row">{chip(item.get("Status", "Unknown"))}</div><p><code>{html.escape(plain(item.get("Endpoint", "")))}</code></p><p>{render_inline(item.get("Next action", ""))}</p></article>')
    return f'<div class="spotlight-grid">{"".join(out)}</div>'


def mismatch_html(data: dict[str, object], out: Path) -> None:
    summary = data["summary"]
    mismatches = data["mismatches"]
    status_counts: dict[str, int] = defaultdict(int)
    resource_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for item in mismatches:
        status_counts[plain(item.get("Status", "Unknown"))] += 1
        resource_groups[resource_name(item.get("Endpoint", ""))].append(item)
    resource_options = [("All resources", "all")] + [(name.title(), slug(name)) for name in sorted(resource_groups)]
    sections = []
    for name, items in sorted(resource_groups.items()):
        sections.append(f'<section class="resource-section" data-filter-group id="resource-{html.escape(slug(name))}"><div class="resource-heading"><h4>{html.escape(name.title())}</h4><div class="pill-row"><span class="metric-pill">{len(items)} mismatch records</span></div></div><div class="mismatch-grid">{"".join(mismatch_card(item) for item in items)}</div></section>')
    body = f"""
<section id="summary" class="hero"><h2>Contract Drift Portal</h2><p>Review runtime deviations as first-class report records, not buried notes. Each card shows the contract expectation, live behavior, impacted tests, and next action.</p><div class="hero-actions"><a class="hero-action" href="test-mapping-report.html">Open traceability report</a><a class="hero-action" href="{html.escape(out.name)}">Refresh current page</a></div>{cards([("Known Drift", str(status_counts.get("Known drift", 0)), "Stable runtime deviation"),("Potential Defect", str(status_counts.get("Potential defect", 0)), "Likely escalation candidates"),("Needs Decision", str(status_counts.get("Needs product decision", 0)), "Blocked by product clarification"),("Total Mismatches", str(len(mismatches)), summary.get("Environment", ""))])}</section>
<section id="spotlights" class="section"><h3>Drift Spotlights</h3><p class="section-note">Start with the highest-risk or highest-noise mismatches before reading the full list.</p>{spotlight_cards(mismatches)}</section>
<section id="mismatches" class="section"><h3>Mismatch Explorer</h3><p class="section-note">Search by endpoint, operation id, or evidence. Filter by status and resource to isolate the exact drift bucket.</p><div data-filter-root><div class="toolbar"><div class="search-box"><input data-filter-input type="search" placeholder="Search endpoint, operation id, evidence, or next action"></div><div class="filters">{filter_pills("status",[("All statuses","all"),("Known drift","known-drift"),("Potential defect","potential-defect"),("Needs decision","needs-product-decision")])}</div></div><div class="toolbar"><div class="filters">{filter_pills("resource", resource_options)}</div><div class="toolbar-note" data-filter-count></div></div>{"".join(sections)}</div></section>"""
    doc = shell(
        "Contract Mismatches",
        "mismatch",
        "Drift",
        "Contract Mismatches",
        "Swagger-like endpoint grouping plus evidence cards for runtime drift.",
        [("summary", "Summary"), ("spotlights", "Spotlights"), ("mismatches", "Mismatch Explorer")],
        [("Service", summary.get("Service", "")), ("Environment", summary.get("Environment", "")), ("Contract source", summary.get("Contract source", "")), ("Updated", summary.get("Last updated", ""))],
        body,
    )
    out.write_text(doc, encoding="utf-8")


def index_html(
    trace: dict[str, object],
    mismatch: dict[str, object],
    optional_reports: list[dict[str, object]],
    trace_html_file: Path,
    mismatch_html_file: Path,
    mapping_md: Path,
    mismatch_md: Path,
    out: Path,
) -> None:
    summary = trace["summary"]
    mismatches = mismatch["mismatches"]
    report_cards = [
        portal_card(
            "Traceability Portal",
            "Grouped operations, filters, reverse mapping, and coverage gaps in one page.",
            trace_html_file.name,
            f'<span class="metric-pill">{summary.get("Covered", "0")} covered</span><span class="metric-pill">{summary.get("Contract drift", "0")} drift</span>',
        ),
        portal_card(
            "Contract Drift Portal",
            "Mismatch spotlights, evidence cards, and escalation-ready next actions.",
            mismatch_html_file.name,
            f'<span class="metric-pill">{len(mismatches)} records</span><span class="metric-pill">{sum(1 for item in mismatches if plain(item.get("Status", "")) == "Potential defect")} potential defects</span>',
        ),
    ]
    source_cards = [
        source_card(
            "Traceability Markdown",
            "Canonical machine-friendly source used to generate the HTML explorer.",
            to_href(str(mapping_md)),
            "Markdown source",
        ),
        source_card(
            "Mismatch Markdown",
            "Canonical machine-friendly source used to generate the drift portal.",
            to_href(str(mismatch_md)),
            "Markdown source",
        ),
    ]
    for report in optional_reports:
        report_cards.append(
            portal_card(
                str(report["title"]),
                str(report["description"]),
                Path(str(report["html_path"])).name,
                metric_pills(report["summary"], report["metrics"]),
                plain(report["summary"].get("Last updated", "")),
            )
        )
        source_cards.append(
            source_card(
                f'{report["title"]} Markdown',
                f'Canonical markdown source for the {str(report["title"]).lower()}.',
                to_href(str(report["md_path"])),
                "Markdown source",
            )
        )
    body = f"""
<section id="summary" class="hero"><h2>Report Portal</h2><p>Use this landing page when humans need readable coverage, drift, planning, change impact, and assertion-quality views instead of raw markdown. The markdown artifacts remain canonical, and the HTML layers a grouped explorer on top.</p><div class="hero-actions"><a class="hero-action" href="{html.escape(trace_html_file.name)}">Open traceability portal</a><a class="hero-action" href="{html.escape(mismatch_html_file.name)}">Open contract drift portal</a><a class="hero-action" href="{html.escape(to_href(str(mapping_md)))}">Open traceability markdown</a><a class="hero-action" href="{html.escape(to_href(str(mismatch_md)))}">Open mismatch markdown</a></div>{cards([("Operations", summary.get("Total operations", str(len(trace["endpoint_mapping"]))), summary.get("Service", "")),("Covered", summary.get("Covered", "0"), "Executable happy-path and negative coverage"),("Contract Drift", summary.get("Contract drift", "0"), "Operations only covered via runtime drift"),("Mismatch Records", str(len(mismatches)), mismatch["summary"].get("Environment", ""))])}</section>
<section id="reports" class="section"><h3>Report Surfaces</h3><p class="section-note">Jump into the representation that fits the task: endpoint traceability, contract drift, gap planning, contract diffing, or assertion hardening.</p><div class="portal-card-grid">{"".join(report_cards)}</div></section>
<section id="sources" class="section"><h3>Canonical Sources</h3><p class="section-note">Open the source markdown when you need the deterministic artifact that the HTML portal was built from.</p><div class="portal-card-grid">{"".join(source_cards)}</div></section>
<section id="resources" class="section"><h3>Coverage By Resource</h3><p class="section-note">The same resource split appears inside the traceability portal.</p>{resource_cards(trace["endpoint_mapping"])}</section>
<section id="spotlights" class="section"><h3>Drift Spotlights</h3><p class="section-note">Start here when the current task is defect review or contract hardening.</p>{spotlight_cards(mismatches)}</section>"""
    doc = shell(
        "Test Report Portal",
        "index",
        "Portal",
        "Report Portal",
        "One landing page for human-friendly coverage, drift, and markdown source navigation.",
        [("summary", "Summary"), ("reports", "Reports"), ("sources", "Sources"), ("resources", "Resources"), ("spotlights", "Spotlights")],
        [("Service", summary.get("Service", "")), ("Contract source", summary.get("Contract source", "")), ("Updated", summary.get("Last updated", "")), ("Environment", mismatch["summary"].get("Environment", ""))],
        body,
    )
    out.write_text(doc, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate HTML reports from traceability and mismatch markdown.")
    parser.add_argument("--mapping", required=True, help="Path to the markdown traceability report.")
    parser.add_argument("--mismatches", required=True, help="Path to the markdown contract mismatch report.")
    parser.add_argument("--outdir", required=True, help="Directory where HTML files should be written.")
    args = parser.parse_args()

    mapping = Path(args.mapping).resolve()
    mismatches = Path(args.mismatches).resolve()
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    trace = parse_traceability(mapping)
    mismatch = parse_mismatches(mismatches)
    optional_reports = collect_optional_reports(mapping.parent, outdir)

    trace_html_file = outdir / "test-mapping-report.html"
    mismatch_html_file = outdir / "contract-mismatches.html"
    index_file = outdir / "index.html"

    traceability_html(trace, trace_html_file)
    mismatch_html(mismatch, mismatch_html_file)
    index_html(trace, mismatch, optional_reports, trace_html_file, mismatch_html_file, mapping, mismatches, index_file)

    print(trace_html_file)
    print(mismatch_html_file)
    print(index_file)


if __name__ == "__main__":
    main()
