#!/usr/bin/env python3
"""Validate an xlsx2prd Markdown delivery for structure and traceability."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FR_RE = re.compile(r"\bFR-[A-Z0-9]+-\d{3}\b")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    root = args.output_dir.resolve()
    prd = root / "PRD.md"
    todo_root = root / "todolist"
    todo_index = todo_root / "README.md"
    errors: list[str] = []

    for required in (prd, todo_root, todo_index):
        if not required.exists():
            errors.append(f"Missing required path: {required.relative_to(root)}")

    markdown_files = sorted(root.rglob("*.md")) if root.exists() else []
    broken_links = []
    all_ids: set[str] = set()
    prd_ids: list[str] = []
    todo_text_parts = []
    story_files = []
    epic_files = []
    todo_count = 0

    for file in markdown_files:
        text = file.read_text(encoding="utf-8")
        ids = FR_RE.findall(text)
        all_ids.update(ids)
        if file == prd:
            prd_ids = ids
        if todo_root in file.parents or file == todo_index:
            todo_text_parts.append(text)
            todo_count += len(re.findall(r"^- \[ \]", text, re.MULTILINE))
        if file.name.startswith("Story") and file.suffix == ".md":
            story_files.append(file)
        if file.name.startswith("Epic") and file.suffix == ".md":
            epic_files.append(file)
        for target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            clean_target = unquote(target.split("#", 1)[0])
            if clean_target and not (file.parent / clean_target).resolve().exists():
                broken_links.append(
                    {
                        "file": str(file.relative_to(root)),
                        "target": target,
                    }
                )

    duplicate_prd_ids = sorted(
        requirement_id
        for requirement_id in set(prd_ids)
        if prd_ids.count(requirement_id) > 1
    )
    todo_text = "\n".join(todo_text_parts)
    uncovered = sorted(set(prd_ids) - set(FR_RE.findall(todo_text)))

    for story in story_files:
        if story.name not in todo_text:
            errors.append(f"Story is not indexed: {story.relative_to(root)}")
    if broken_links:
        errors.append(f"Broken Markdown links: {len(broken_links)}")
    if duplicate_prd_ids:
        errors.append(f"Duplicate PRD requirement IDs: {duplicate_prd_ids}")
    if uncovered:
        errors.append(f"PRD requirements absent from todolist: {uncovered}")
    if prd.exists() and not prd_ids:
        errors.append("PRD contains no FR-* requirement IDs")

    result = {
        "root": str(root),
        "markdownFiles": len(markdown_files),
        "prdRequirementIds": len(set(prd_ids)),
        "allRequirementIds": len(all_ids),
        "epicFiles": len(epic_files),
        "storyFiles": len(story_files),
        "todoItems": todo_count,
        "brokenLinks": broken_links,
        "duplicatePrdRequirementIds": duplicate_prd_ids,
        "uncoveredRequirementIds": uncovered,
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
