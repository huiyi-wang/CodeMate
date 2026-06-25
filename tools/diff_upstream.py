#!/usr/bin/env python3
"""List file-level diff between upstream clone and local project tree.

Usage:
  python tools/diff_upstream.py \\
    --upstream SAFMN/.distill/_upstream/SAFMN \\
    --local SAFMN \\
    --include basicsr,local_inference,local_convert \\
    --exclude node_modules,.git,__pycache__,TensorRT-8.6.1.6 \\
    --out SAFMN/.distill/_file_inventory.json

Prints JSON with three change types (aliases for MD §改动文件清单):
  - added / only_local     — 新增（本地有、上游无）
  - deleted / only_upstream — 删除（上游有、本地无）
  - modified               — 修改（同路径、内容不同）
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


DEFAULT_EXCLUDE = {
    ".git",
    "__pycache__",
    ".venv",
    "node_modules",
    "experiments",
    "results",
    "models",
    "weights",
    ".distill/_upstream",
}


def iter_files(root: Path, excludes: set[str]) -> set[str]:
    out: set[str] = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in excludes]
        rel_dir = Path(dirpath).relative_to(root)
        for name in filenames:
            rel = (rel_dir / name).as_posix()
            if rel.startswith("./"):
                rel = rel[2:]
            skip = False
            for part in rel.split("/"):
                if part in excludes:
                    skip = True
                    break
            if not skip:
                out.add(rel)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", required=True, help="cloned upstream root")
    parser.add_argument("--local", required=True, help="local project root")
    parser.add_argument("--include", default="", help="comma prefixes to keep (empty=all)")
    parser.add_argument("--exclude", default="", help="extra comma excludes")
    parser.add_argument("--out", default="", help="write JSON to this path")
    args = parser.parse_args()

    up = Path(args.upstream).resolve()
    local = Path(args.local).resolve()
    excludes = set(DEFAULT_EXCLUDE)
    excludes.update(x.strip() for x in args.exclude.split(",") if x.strip())
    includes = [x.strip() for x in args.include.split(",") if x.strip()]

    up_files = iter_files(up, excludes)
    local_files = iter_files(local, excludes)

    if includes:
        def keep(p: str) -> bool:
            return any(p == pref or p.startswith(pref + "/") for pref in includes)

        up_files = {p for p in up_files if keep(p)}
        local_files = {p for p in local_files if keep(p)}

    only_up = sorted(up_files - local_files)
    only_local = sorted(local_files - up_files)
    common = sorted(up_files & local_files)

    modified = []
    for rel in common:
        up_path = up / rel
        loc_path = local / rel
        if up_path.read_bytes() != loc_path.read_bytes():
            modified.append(rel)

    result = {
        "added": only_local,
        "deleted": only_up,
        "modified": modified,
        "only_local": only_local,
        "only_upstream": only_up,
        "unchanged_count": len(common) - len(modified),
        "counts": {
            "added": len(only_local),
            "deleted": len(only_up),
            "modified": len(modified),
            "unchanged": len(common) - len(modified),
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
