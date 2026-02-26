#!/usr/bin/env python3
"""Lightweight markdown link checker for docs/."""

from __future__ import annotations

import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def is_relative_link(target: str) -> bool:
    if not target:
        return False
    if target.startswith("#"):
        return False
    if "://" in target:
        return False
    if target.startswith("mailto:"):
        return False
    if target.startswith("/"):
        return False
    return True


def normalize_target(raw: str) -> str:
    target = raw.strip().strip("<>").strip()
    target = target.split("#", 1)[0]
    target = target.split("?", 1)[0]
    return target


def main() -> int:
    root = Path.cwd()
    docs_dir = root / "docs"
    files = sorted(docs_dir.rglob("*.md"))
    broken: list[str] = []

    for md_file in files:
        text = md_file.read_text(encoding="utf-8")
        for idx, line in enumerate(text.splitlines(), start=1):
            for match in LINK_RE.finditer(line):
                raw_target = normalize_target(match.group(1))
                if not is_relative_link(raw_target):
                    continue
                target_path = (md_file.parent / raw_target).resolve()
                if not target_path.exists():
                    rel_source = md_file.relative_to(root)
                    broken.append(f"{rel_source}:{idx} -> missing target: {match.group(1)}")

    if broken:
        print("[doc_check] error: broken relative markdown links found:", file=sys.stderr)
        for item in broken:
            print(f"  - {item}", file=sys.stderr)
        return 1

    print(f"[doc_check] markdown links ok ({len(files)} files scanned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
