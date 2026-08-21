#!/usr/bin/env python3
"""Initialize, audit, and map a local Web of Belief knowledge base."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FOLDERS = ("nodes", "claims", "evidence", "cases", "questions")
ALLOWED_RELATIONS = {
    "enables", "constrains", "influences", "depends_on", "governs",
    "legitimizes", "filters", "transmits", "incentivizes", "competes_with", "serves",
}
SKELETONS = {
    "INDEX.md": "# 信念之网\n\n## 当前焦点\n\n## 最近更新\n\n## 待复盘\n",
    "INBOX.md": "# 收件箱\n\n未处理的原始输入放在这里；它们不是已验证的事实或关系。\n",
    "RELATIONS.md": "# 关系登记册\n\n| From | Relation | To | Confidence | Support | Notes |\n| --- | --- | --- | --- | --- | --- |\n",
    "MAP.md": "# 信念之网地图\n\n```mermaid\ngraph LR\n```\n",
}


def init(path: Path) -> int:
    if path.exists() and any(path.iterdir()):
        print(f"Refusing to initialize non-empty directory: {path}", file=sys.stderr)
        return 1
    path.mkdir(parents=True, exist_ok=True)
    for folder in FOLDERS:
        (path / folder).mkdir(exist_ok=True)
    for name, content in SKELETONS.items():
        (path / name).write_text(content, encoding="utf-8")
    print(f"Initialized Web of Belief at {path}")
    return 0


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}
    result = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def relation_rows(path: Path) -> list[list[str]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        separator = all(set(cell) <= {"-", ":", " "} for cell in cells)
        if len(cells) != 6 or cells[0] == "From" or separator:
            continue
        rows.append(cells)
    return rows


def audit(path: Path) -> int:
    issues: list[str] = []
    for folder in FOLDERS:
        directory = path / folder
        if not directory.exists():
            issues.append(f"missing directory: {folder}/")
            continue
        for note in directory.glob("*.md"):
            meta = frontmatter(note)
            if not meta:
                issues.append(f"missing frontmatter: {note.relative_to(path)}")
                continue
            expected = "case" if folder == "cases" else folder.rstrip("s")
            if meta.get("type") != expected:
                issues.append(f"type mismatch: {note.relative_to(path)}")
            if meta.get("type") == "claim":
                for required in ("status", "confidence", "scope"):
                    if not meta.get(required):
                        issues.append(f"claim missing {required}: {note.relative_to(path)}")
    for source, relation, target, confidence, support, _ in relation_rows(path / "RELATIONS.md"):
        if relation not in ALLOWED_RELATIONS:
            issues.append(f"unknown relation '{relation}': {source} -> {target}")
        if confidence not in {"low", "medium", "high"}:
            issues.append(f"invalid relation confidence: {source} -> {target}")
        if confidence == "high" and not support:
            issues.append(f"high-confidence relation lacks support: {source} -> {target}")
    if issues:
        print("Audit found issues:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Audit passed: structure and registered relations are internally consistent.")
    return 0


def clean_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_\u4e00-\u9fff]", "_", value).strip("_") or "node"


def sync(path: Path) -> int:
    relations = relation_rows(path / "RELATIONS.md")
    ids: dict[str, str] = {}
    used: set[str] = set()
    for source, _, target, _, _, _ in relations:
        for name in (source, target):
            if name not in ids:
                candidate = clean_id(name)
                suffix = 2
                base = candidate
                while candidate in used:
                    candidate = f"{base}_{suffix}"
                    suffix += 1
                ids[name] = candidate
                used.add(candidate)
    lines = ["# 信念之网地图", "", "由 `RELATIONS.md` 生成；请修改登记册后重新运行 `sync`。", "", "```mermaid", "graph LR"]
    for name, node_id in ids.items():
        lines.append(f'  {node_id}["{name}"]')
    for source, relation, target, confidence, _, _ in relations:
        lines.append(f"  {ids[source]} -->|{relation} ({confidence})| {ids[target]}")
    lines.extend(["```", ""])
    (path / "MAP.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Synced {len(relations)} relation(s) into {path / 'MAP.md'}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("init", "audit", "sync"):
        subparsers.add_parser(command).add_argument("path", type=Path)
    args = parser.parse_args()
    path = args.path.expanduser().resolve()
    if args.command == "init":
        return init(path)
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1
    if args.command == "audit":
        return audit(path)
    return sync(path)


if __name__ == "__main__":
    raise SystemExit(main())
