#!/usr/bin/env python3
"""Generate an OpenAPI change-impact report and map changed operations back to tests."""

from __future__ import annotations

import argparse
import json
import html
import re
import sys
from pathlib import Path
from urllib.parse import quote, urlparse
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.report_theme import load_report_theme_css


HTTP_METHODS = {"get", "post", "put", "patch", "delete", "options", "head"}
SUMMARY_RE = re.compile(r"^- ([^:]+):\s*(.*)$")
TABLE_DIVIDER_RE = re.compile(r"^\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?$")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
CODE_RE = re.compile(r"`([^`]+)`")


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


def skip_blanks(lines: list[str], idx: int) -> int:
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    return idx


def split_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_mapping(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    idx = 0
    rows: dict[tuple[str, str], dict[str, str]] = {}
    while idx < len(lines):
        if lines[idx].rstrip() != "## Endpoint Mapping":
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
            rows[(plain(row.get("Method", "")), plain(row.get("Path", "")))] = row
            idx += 1
        break
    return rows


def documentation_refs(row: dict[str, str]) -> str:
    return row.get("Documentation References", row.get("BDD References", "-"))


def load_source(source: str) -> dict:
    parsed = urlparse(source)
    if parsed.scheme in {"http", "https"}:
        with urlopen(source, timeout=30) as response:  # nosec - caller chooses the source
            text = response.read().decode("utf-8")
    else:
        text = Path(source).read_text(encoding="utf-8")
    if source.lower().endswith(".json") or text.lstrip().startswith("{"):
        return json.loads(text)
    try:
        import yaml  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise SystemExit("PyYAML is required for YAML OpenAPI sources.") from exc
    return yaml.safe_load(text)


def join_paths(prefix: str, path: str) -> str:
    prefix_part = prefix.strip("/")
    path_part = path.strip("/")
    if prefix_part and path_part:
        return f"/{prefix_part}/{path_part}"
    if prefix_part:
        return f"/{prefix_part}"
    if path_part:
        return f"/{path_part}"
    return "/"


def api_prefix(document: dict) -> str:
    for server in document.get("servers") or []:
        if isinstance(server, dict):
            url = server.get("url", "")
        else:
            url = str(server)
        if not url:
            continue
        path = urlparse(url).path.rstrip("/")
        marker = path.rfind("/api")
        if marker != -1:
            return path[marker:]
    return ""


def normalized_api_path(document: dict, raw_path: str) -> str:
    prefix = api_prefix(document)
    if prefix and raw_path.startswith(prefix):
        return raw_path
    if prefix:
        return join_paths(prefix, raw_path)
    return raw_path


def resolve_ref(document: dict, ref: str) -> dict:
    if not ref.startswith("#/"):
        return {"ref": ref}
    node: object = document
    for token in ref[2:].split("/"):
        if not isinstance(node, dict):
            return {"ref": ref}
        node = node.get(token)
    return node if isinstance(node, dict) else {"ref": ref}


def summarize_schema(document: dict, schema: dict | None) -> dict:
    if not schema:
        return {}
    if "$ref" in schema:
        resolved = resolve_ref(document, schema["$ref"])
        return {"$ref": schema["$ref"], **summarize_schema(document, resolved if isinstance(resolved, dict) else {})}
    summary = {
        "type": schema.get("type"),
        "format": schema.get("format"),
        "required": schema.get("required") or [],
        "enum": schema.get("enum") or [],
    }
    properties = schema.get("properties") or {}
    if isinstance(properties, dict):
        summary["properties"] = sorted(properties.keys())
    items = schema.get("items")
    if isinstance(items, dict):
        summary["items"] = summarize_schema(document, items)
    return {key: value for key, value in summary.items() if value not in (None, [], {}, "")}


def normalize_operation(document: dict, path: str, method: str, operation: dict) -> dict:
    normalized_path = normalized_api_path(document, path)
    params = []
    for parameter in operation.get("parameters") or []:
        if not isinstance(parameter, dict):
            continue
        schema = parameter.get("schema") if isinstance(parameter.get("schema"), dict) else {}
        params.append(
            {
                "name": parameter.get("name"),
                "in": parameter.get("in"),
                "required": parameter.get("required", False),
                "type": schema.get("type"),
            }
        )
    request_body = operation.get("requestBody") if isinstance(operation.get("requestBody"), dict) else {}
    responses = {}
    for status, response in sorted((operation.get("responses") or {}).items()):
        if not isinstance(response, dict):
            continue
        media = {}
        for media_type, info in sorted((response.get("content") or {}).items()):
            schema = info.get("schema") if isinstance(info, dict) else {}
            media[media_type] = summarize_schema(document, schema if isinstance(schema, dict) else {})
        responses[status] = {"content": media, "description": response.get("description")}
    request_content = {}
    for media_type, info in sorted((request_body.get("content") or {}).items()):
        schema = info.get("schema") if isinstance(info, dict) else {}
        request_content[media_type] = summarize_schema(document, schema if isinstance(schema, dict) else {})
    return {
        "method": method.upper(),
        "path": normalized_path,
        "operationId": operation.get("operationId"),
        "summary": operation.get("summary"),
        "tags": operation.get("tags") or [],
        "parameters": sorted(params, key=lambda item: (item["in"] or "", item["name"] or "")),
        "requestBody": {"required": request_body.get("required", False), "content": request_content},
        "responses": responses,
        "security": operation.get("security", document.get("security", [])),
    }


def normalize_contract(document: dict) -> dict[tuple[str, str], dict]:
    operations: dict[tuple[str, str], dict] = {}
    for path, methods in (document.get("paths") or {}).items():
        if not isinstance(methods, dict):
            continue
        for method, operation in methods.items():
            if method.lower() not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            normalized = normalize_operation(document, path, method, operation)
            operations[(method.upper(), normalized["path"])] = normalized
    return operations


def diff_operations(baseline: dict[tuple[str, str], dict], current: dict[tuple[str, str], dict], mapping_rows: dict[tuple[str, str], dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    keys = sorted(set(baseline) | set(current))
    for key in keys:
        before = baseline.get(key)
        after = current.get(key)
        change_type = "No change"
        summary = "No contract delta detected."
        if before is None:
            change_type = "Added"
            summary = "Operation exists only in the current contract."
        elif after is None:
            change_type = "Removed"
            summary = "Operation exists only in the baseline contract."
        elif before != after:
            details: list[str] = []
            breaking = False
            if before.get("parameters") != after.get("parameters"):
                details.append("Parameters changed")
                before_required = {item["name"] for item in before.get("parameters", []) if item.get("required")}
                after_required = {item["name"] for item in after.get("parameters", []) if item.get("required")}
                if after_required - before_required:
                    breaking = True
            if before.get("requestBody") != after.get("requestBody"):
                details.append("Request body changed")
                if (before.get("requestBody") or {}).get("required") is False and (after.get("requestBody") or {}).get("required") is True:
                    breaking = True
            if before.get("responses") != after.get("responses"):
                details.append("Responses changed")
                if set((before.get("responses") or {}).keys()) - set((after.get("responses") or {}).keys()):
                    breaking = True
            if before.get("security") != after.get("security"):
                details.append("Security changed")
            if before.get("tags") != after.get("tags"):
                details.append("Tags changed")
            if before.get("summary") != after.get("summary"):
                details.append("Summary changed")
            change_type = "Breaking change" if breaking else "Non-breaking change"
            summary = ", ".join(details) if details else "Operation metadata changed."
        if change_type == "No change":
            continue
        mapping = mapping_rows.get(key, {})
        operation = after or before or {}
        rows.append(
            {
                "Method": key[0],
                "Path": key[1],
                "Operation ID": operation.get("operationId") or "",
                "Change Type": change_type,
                "Change Summary": summary,
                "Affected Tests": mapping.get("Test References", "-"),
                "Affected Documentation": documentation_refs(mapping),
                "Recommended Action": "Review and update the mapped tests before the next execution."
                if change_type != "Added"
                else "Add a new test slice for the new operation.",
            }
        )
    return rows


def recommendation(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "No contract delta was detected between the baseline and current sources."
    breaking = [row for row in rows if row["Change Type"] == "Breaking change"]
    if breaking:
        return f"Prioritize the {len(breaking)} breaking-change operation(s) before the next suite run."
    return f"Prioritize the {rows[0]['Method']} {rows[0]['Path']} change first because it already maps to existing coverage."


def write_markdown(rows: list[dict[str, str]], baseline_source: str, current_source: str, output: Path) -> None:
    counts = {
        "Added": sum(1 for row in rows if row["Change Type"] == "Added"),
        "Removed": sum(1 for row in rows if row["Change Type"] == "Removed"),
        "Breaking change": sum(1 for row in rows if row["Change Type"] == "Breaking change"),
        "Non-breaking change": sum(1 for row in rows if row["Change Type"] == "Non-breaking change"),
    }
    lines = [
        "# OpenAPI Change Impact Report",
        "",
        "## Summary",
        "",
        f"- Baseline source: `{baseline_source}`",
        f"- Current source: `{current_source}`",
        "- Last updated: 2026-03-12",
        f"- Added operations: {counts['Added']}",
        f"- Removed operations: {counts['Removed']}",
        f"- Breaking changes: {counts['Breaking change']}",
        f"- Non-breaking changes: {counts['Non-breaking change']}",
        f"- No-change operations: {0 if rows else 'All compared operations'}",
        "",
        "## Operation Impact",
        "",
        "| Method | Path | Operation ID | Change Type | Change Summary | Affected Tests | Affected Documentation | Recommended Action |",
        "|---|---|---|---|---|---|---|---|",
    ]
    if rows:
        for row in rows:
            lines.append(
                f"| {row['Method']} | {row['Path']} | {row['Operation ID']} | {row['Change Type']} | {row['Change Summary']} | {row['Affected Tests']} | {row['Affected Documentation']} | {row['Recommended Action']} |"
            )
    else:
        lines.append("| - | - | - | No change | No contract delta was detected between the compared sources. | - | - | Keep the current suite stable and monitor future contract updates. |")
    lines.extend(["", "## Recommendation", "", f"- {recommendation(rows)}", ""])
    output.write_text("\n".join(lines), encoding="utf-8")


def write_html(rows: list[dict[str, str]], baseline_source: str, current_source: str, output: Path) -> None:
    counts = {
        "Added": sum(1 for row in rows if row["Change Type"] == "Added"),
        "Removed": sum(1 for row in rows if row["Change Type"] == "Removed"),
        "Breaking change": sum(1 for row in rows if row["Change Type"] == "Breaking change"),
        "Non-breaking change": sum(1 for row in rows if row["Change Type"] == "Non-breaking change"),
    }
    body_rows = "".join(
        f"<tr><td>{render_inline(row['Method'])}</td><td>{render_inline(row['Path'])}</td><td>{render_inline(row['Operation ID'])}</td>"
        f"<td><span class='chip chip-{plain(row['Change Type']).lower().replace(' ', '-')}'>{html.escape(row['Change Type'])}</span></td>"
        f"<td>{render_inline(row['Change Summary'])}</td><td>{render_inline(row['Affected Tests'])}</td><td>{render_inline(row['Affected Documentation'])}</td><td>{render_inline(row['Recommended Action'])}</td></tr>"
        for row in rows
    ) or "<tr><td colspan='8'>No contract delta was detected between the compared sources.</td></tr>"
    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>OpenAPI Change Impact</title>
<style>{load_report_theme_css()}</style></head>
<body><main>
<section class="hero"><h1>OpenAPI Change Impact Report</h1><p>Compare two API contracts and map any changed operations back to the current executable suite.</p>
<p><strong>Baseline:</strong> {render_inline(f'`{baseline_source}`')}<br><strong>Current:</strong> {render_inline(f'`{current_source}`')}</p>
<div class="cards">
<div class="card"><div class="label">Added</div><div class="value">{counts['Added']}</div></div>
<div class="card"><div class="label">Removed</div><div class="value">{counts['Removed']}</div></div>
<div class="card"><div class="label">Breaking</div><div class="value">{counts['Breaking change']}</div></div>
<div class="card"><div class="label">Non-breaking</div><div class="value">{counts['Non-breaking change']}</div></div>
</div></section>
<section class="panel"><h2>Operation Impact</h2><div class="table-shell"><table><thead><tr><th>Method</th><th>Path</th><th>Operation ID</th><th>Change Type</th><th>Change Summary</th><th>Affected Tests</th><th>Affected Documentation</th><th>Recommended Action</th></tr></thead><tbody>{body_rows}</tbody></table></div></section>
<section class="panel"><h2>Recommendation</h2><p>{render_inline(recommendation(rows))}</p></section>
</main></body></html>"""
    output.write_text(doc, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an OpenAPI change-impact report.")
    parser.add_argument("--baseline", required=True, help="Baseline OpenAPI source")
    parser.add_argument("--current", required=True, help="Current OpenAPI source")
    parser.add_argument("--mapping", required=True, help="Path to docs/testing/test-mapping-report.md")
    parser.add_argument("--output-md", required=True, help="Markdown output path")
    parser.add_argument("--output-html", required=True, help="HTML output path")
    args = parser.parse_args()

    baseline = normalize_contract(load_source(args.baseline))
    current = normalize_contract(load_source(args.current))
    mapping_rows = parse_mapping(Path(args.mapping))
    rows = diff_operations(baseline, current, mapping_rows)

    write_markdown(rows, args.baseline, args.current, Path(args.output_md))
    write_html(rows, args.baseline, args.current, Path(args.output_html))
    print(Path(args.output_md).resolve())
    print(Path(args.output_html).resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
