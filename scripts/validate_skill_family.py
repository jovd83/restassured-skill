#!/usr/bin/env python3
"""Validate the local Rest Assured skill family for publish readiness."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
NAME_RE = re.compile(r"^name:\s*(.+)$", re.MULTILINE)
DESCRIPTION_RE = re.compile(r"^description:\s*(.+)$", re.MULTILINE)


def frontmatter(path: Path) -> tuple[str | None, str | None]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, None
    block = match.group(1)
    name_match = NAME_RE.search(block)
    desc_match = DESCRIPTION_RE.search(block)
    name = name_match.group(1).strip() if name_match else None
    desc = desc_match.group(1).strip() if desc_match else None
    return name, desc


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the local Rest Assured skill family.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent.parent), help="Root skill directory")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    skill_files = sorted(root.rglob("SKILL.md"))
    errors: list[str] = []
    seen_names: dict[str, Path] = {}

    for skill_file in skill_files:
        skill_dir = skill_file.parent
        name, description = frontmatter(skill_file)
        if not name or not description:
            errors.append(f"Missing or invalid frontmatter: {skill_file}")
        elif name in seen_names:
            errors.append(f"Duplicate skill name `{name}` in {skill_file} and {seen_names[name]}")
        else:
            seen_names[name] = skill_file
        metadata = skill_dir / "agents" / "openai.yaml"
        if not metadata.exists():
            errors.append(f"Missing agents/openai.yaml: {skill_dir}")

    if errors:
        print(f"Validated {len(skill_files)} skills under {root}")
        print("Errors:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(skill_files)} skills under {root}")
    print("All skills have SKILL frontmatter and agents/openai.yaml metadata.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
