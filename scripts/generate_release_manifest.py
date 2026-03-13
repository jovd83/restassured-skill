#!/usr/bin/env python3
"""Generate a release manifest for the local Rest Assured skill family."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
NAME_RE = re.compile(r"^name:\s*(.+)$", re.MULTILINE)
DESCRIPTION_RE = re.compile(r"^description:\s*(.+)$", re.MULTILINE)
DISPLAY_RE = re.compile(r'^\s*display_name:\s*"(.*)"\s*$', re.MULTILINE)
SHORT_RE = re.compile(r'^\s*short_description:\s*"(.*)"\s*$', re.MULTILINE)


def parse_skill(skill_file: Path) -> dict[str, str]:
    text = skill_file.read_text(encoding="utf-8")
    frontmatter = FRONTMATTER_RE.match(text)
    body = frontmatter.group(1) if frontmatter else ""
    name_match = NAME_RE.search(body)
    description_match = DESCRIPTION_RE.search(body)
    metadata_path = skill_file.parent / "agents" / "openai.yaml"
    metadata_text = metadata_path.read_text(encoding="utf-8") if metadata_path.exists() else ""
    display_match = DISPLAY_RE.search(metadata_text)
    short_match = SHORT_RE.search(metadata_text)
    return {
        "path": str(skill_file.parent),
        "name": name_match.group(1).strip() if name_match else "",
        "description": description_match.group(1).strip() if description_match else "",
        "display_name": display_match.group(1).strip() if display_match else "",
        "short_description": short_match.group(1).strip() if short_match else "",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a release manifest for the local skill family.")
    parser.add_argument("--root", required=True, help="Root skill directory")
    parser.add_argument("--output", required=True, help="Markdown output path")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    skills = [parse_skill(path) for path in sorted(root.rglob("SKILL.md"))]
    lines = [
        "# Release Manifest",
        "",
        "## Summary",
        "",
        f"- Root: `{root}`",
        f"- Skills: {len(skills)}",
        "",
        "## Skills",
        "",
        "| Skill Name | Display Name | Path | Short Description |",
        "|---|---|---|---|",
    ]
    for skill in skills:
        lines.append(
            f"| `{skill['name']}` | {skill['display_name'] or '-'} | `{skill['path']}` | {skill['short_description'] or skill['description'] or '-'} |"
        )
    lines.append("")
    Path(args.output).resolve().write_text("\n".join(lines), encoding="utf-8")
    print(Path(args.output).resolve())
    print(f"skills={len(skills)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
