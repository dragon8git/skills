#!/usr/bin/env python3
"""Read-only UniApp X cross-subpackage runtime-import scanner."""
from __future__ import annotations

import re
import sys
from pathlib import Path


IMPORT = re.compile(r"^\s*import(?!\s+type\b).*?from\s+['\"]@/pages/wbd/([^/'\"]+)(/[^'\"]*)?['\"]", re.M)
ROOT = re.compile(r'"root"\s*:\s*"pages/wbd/([^"/]+)')


def package_for(path: Path, app: Path, roots: set[str]) -> str | None:
    relative = path.relative_to(app).as_posix()
    match = re.match(r"pages/wbd/([^/]+)/", relative)
    if match and match.group(1) in roots:
        return match.group(1)
    return None


def main() -> int:
    app = Path(sys.argv[1] if len(sys.argv) > 1 else "app").resolve()
    pages = app / "pages.json"
    if not pages.is_file():
        print(f"ERROR: pages.json not found under {app}")
        return 2
    roots = set(ROOT.findall(pages.read_text(encoding="utf-8")))
    findings: list[tuple[str, str, str, str]] = []
    for suffix in ("*.uvue", "*.uts"):
        for file in app.rglob(suffix):
            owner = package_for(file, app, roots)
            if owner is None:
                continue
            text = file.read_text(encoding="utf-8", errors="replace")
            for match in IMPORT.finditer(text):
                imported = match.group(1)
                if imported != owner and imported in roots:
                    line = text.count("\n", 0, match.start()) + 1
                    findings.append((owner, imported, file.relative_to(app).as_posix(), str(line)))
    print("Subpackages: " + ", ".join(sorted(roots)))
    if not findings:
        print("No cross-subpackage runtime imports found.")
        return 0
    print("Cross-subpackage runtime imports:")
    for owner, imported, file, line in sorted(findings):
        print(f"HIGH | {owner} -> {imported} | {file}:{line}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
