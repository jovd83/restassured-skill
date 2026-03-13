#!/usr/bin/env python3
"""Audit narrative documentation drift against the canonical traceability report."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
TABLE_DIVIDER_RE = re.compile(r"^\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?$")


def split_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def skip_blanks(lines: list[str], idx: int) -> int:
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    return idx


def parse_mapping(path: Path) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    idx = 0
    rows: list[dict[str, str]] = []
    while idx < len(lines):
        if lines[idx].rstrip() != "## Endpoint Mapping":
            idx += 1
            continue
        idx = skip_blanks(lines, idx + 1)
        if idx >= len(lines):
            return rows
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
            rows.append({headers[i]: values[i] if i < len(values) else "" for i in range(len(headers))})
            idx += 1
        break
    return rows


def split_ref_items(cell: str) -> list[str]:
    items = []
    for raw in cell.split(","):
        item = raw.strip()
        if not item or item in {"-", "`-`"}:
            continue
        items.append(item)
    return items


def split_target(target: str) -> tuple[str, str]:
    if "#" in target:
        path_part, anchor = target.split("#", 1)
        return path_part, f"#{anchor}"
    return target, ""


def resolve_target(item: str, base_dir: Path) -> tuple[str, Path | None]:
    match = LINK_RE.search(item)
    target = match.group(2) if match else item
    path_part, _ = split_target(target)
    if path_part.startswith("file:///"):
        resolved = Path(path_part.replace("file:///", "", 1))
        return target, resolved
    if re.match(r"^[A-Za-z]:[\\/]", path_part):
        return target, Path(path_part)
    if path_part.startswith(("http://", "https://")):
        return target, None
    return target, (base_dir / path_part).resolve()


def documentation_type(path: Path) -> str:
    text = str(path).lower().replace("\\", "/")
    if path.suffix.lower() == ".feature":
        return "BDD"
    if "/tdd/" in text or "tdd" in path.stem.lower():
        return "TDD"
    if path.suffix.lower() == ".md":
        try:
            content = path.read_text(encoding="utf-8")
        except OSError:
            content = ""
        if "test_suite:" in content and "Covered requirement:" in content and "Test script:" in content:
            return "TDD"
        if "Title:" in content and "Purpose:" in content and "Covered requirement:" in content and "Test script:" in content:
            return "Plain text"
    if "/plain" in text or path.suffix.lower() == ".txt":
        return "Plain text"
    if path.suffix.lower() == ".md":
        return "Markdown"
    if path.suffix.lower() == ".adoc":
        return "AsciiDoc"
    return path.suffix.lower().lstrip(".") or "Unknown"


def candidate_files(root: Path) -> list[Path]:
    exts = {".feature", ".md", ".txt", ".adoc"}
    files = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in exts:
            continue
        lower = str(path).lower().replace("\\", "/")
        if "/html/" in lower:
            continue
        files.append(path.resolve())
    return files


def default_docs_roots(mapping_path: Path) -> list[Path]:
    docs_dir = mapping_path.parent.parent
    candidates = [
        docs_dir / "tests",
        docs_dir / "features",
        docs_dir / "tests" / "features",
    ]
    return [path.resolve() for path in candidates if path.exists()]


def collapse_roots(roots: set[Path]) -> list[Path]:
    ordered = sorted(path.resolve() for path in roots)
    collapsed: list[Path] = []
    for path in ordered:
        if any(parent == path or parent in path.parents for parent in collapsed):
            continue
        collapsed.append(path)
    return collapsed


def write_report(
    mapping_path: Path,
    docs_roots: list[Path],
    referenced: list[Path],
    missing: list[tuple[str, str]],
    orphaned: list[Path],
    output: Path,
) -> None:
    modes = sorted({documentation_type(path) for path in referenced + orphaned})
    lines = [
        "# Documentation Sync Report",
        "",
        "## Summary",
        "",
        f"- Mapping source: `{mapping_path}`",
        f"- Documentation roots audited: {', '.join(f'`{path}`' for path in docs_roots) if docs_roots else 'None detected'}",
        "- Last updated: 2026-03-12",
        f"- Referenced documentation files: {len(referenced)}",
        f"- Missing documentation references: {len(missing)}",
        f"- Orphan documentation files: {len(orphaned)}",
        f"- Documentation modes: {', '.join(modes) if modes else 'None detected'}",
        "",
        "## Missing References",
        "",
        "| Reference | Problem | Suggested Fix |",
        "|---|---|---|",
    ]
    if missing:
        for item, problem in missing:
            lines.append(f"| `{item}` | {problem} | Repair the traceability link or recreate the missing documentation file. |")
    else:
        lines.append("| - | None | Keep the current references stable. |")
    lines.extend(["", "## Orphan Documentation", "", "| File | Documentation Type | Suggested Action |", "|---|---|---|"])
    if orphaned:
        for path in orphaned:
            lines.append(f"| `{path}` | {documentation_type(path)} | Link this file from the traceability report or archive it if it is obsolete. |")
    else:
        lines.append("| - | None | No orphan narrative documentation was detected. |")
    lines.extend(["", "## Notes", ""])
    if missing or orphaned:
        lines.append("- Repair the traceability report first, then update the narrative docs only where the executable scenarios changed.")
    else:
        lines.append("- Narrative documentation and traceability are currently aligned.")
    lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit narrative documentation drift against the traceability report.")
    parser.add_argument("--mapping", required=True, help="Path to docs/testing/test-mapping-report.md")
    parser.add_argument("--docs-root", action="append", default=[], help="Narrative documentation root. Repeat as needed.")
    parser.add_argument("--output", required=True, help="Output markdown path")
    args = parser.parse_args()

    mapping_path = Path(args.mapping).resolve()
    rows = parse_mapping(mapping_path)
    base_dir = mapping_path.parent
    ref_column_names = ("Documentation References", "BDD References")

    referenced_existing: list[Path] = []
    missing: list[tuple[str, str]] = []
    inferred_roots: set[Path] = set()

    for row in rows:
        cell = ""
        for column in ref_column_names:
            if row.get(column):
                cell = row[column]
                break
        for item in split_ref_items(cell):
            target, resolved = resolve_target(item, base_dir)
            if resolved is None:
                missing.append((target, "Non-file or remote documentation reference cannot be audited locally"))
                continue
            resolved = resolved.resolve()
            if resolved.exists():
                referenced_existing.append(resolved)
                inferred_roots.add(resolved.parent)
            else:
                missing.append((target, "Referenced documentation file does not exist"))

    explicit_docs_roots = {Path(path).resolve() for path in args.docs_root}
    docs_roots = set(explicit_docs_roots or inferred_roots)
    if not explicit_docs_roots:
        docs_roots.update(default_docs_roots(mapping_path))
    docs_root_list = collapse_roots(docs_roots)
    orphan_pool: set[Path] = set()
    for root in docs_root_list:
        if root.exists():
            orphan_pool.update(candidate_files(root))
    referenced_set = set(referenced_existing)
    orphaned = sorted(path for path in orphan_pool if path not in referenced_set and path != Path(args.output).resolve())

    write_report(
        mapping_path,
        docs_root_list,
        sorted(referenced_set),
        missing,
        orphaned,
        Path(args.output).resolve(),
    )
    print(Path(args.output).resolve())
    summary = Counter()
    summary["referenced"] = len(referenced_set)
    summary["missing"] = len(missing)
    summary["orphaned"] = len(orphaned)
    print(f"referenced={summary['referenced']} missing={summary['missing']} orphaned={summary['orphaned']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
