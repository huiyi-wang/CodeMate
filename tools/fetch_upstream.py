#!/usr/bin/env python3
"""Clone upstream repository at a pinned ref for secondary-dev diff.

Usage:
  python tools/fetch_upstream.py --repo sunny2109/SAFMN --ref main --out SAFMN/.distill/_upstream/SAFMN

Output: prints JSON line with clone path and resolved commit.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def repo_to_url(repo: str) -> str:
    repo = repo.strip().rstrip("/")
    if repo.startswith("git@") or repo.startswith("http://") or repo.startswith("https://"):
        return repo
    if "/" not in repo:
        raise ValueError(f"invalid repo slug: {repo}")
    return f"https://github.com/{repo}.git"


def run(cmd: list[str], cwd: Path | None = None) -> str:
    proc = subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
    return proc.stdout.strip()


def is_commit(ref: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-fA-F]{7,40}", ref))


def clone_at_ref(url: str, ref: str, out_dir: Path) -> str:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.parent.mkdir(parents=True, exist_ok=True)

    if is_commit(ref):
        run(["git", "clone", "--no-checkout", url, str(out_dir)])
        run(["git", "fetch", "--depth", "1", "origin", ref], cwd=out_dir)
        run(["git", "checkout", "FETCH_HEAD"], cwd=out_dir)
    else:
        run(["git", "clone", "--depth", "1", "--branch", ref, url, str(out_dir)])

    return run(["git", "rev-parse", "HEAD"], cwd=out_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch upstream repo at ref for 码伴 CodeMate diff")
    parser.add_argument("--repo", required=True, help="owner/name or git URL")
    parser.add_argument("--ref", required=True, help="tag, branch, or commit")
    parser.add_argument("--out", required=True, help="output directory for clone")
    args = parser.parse_args()

    out_dir = Path(args.out).resolve()
    url = repo_to_url(args.repo)
    try:
        commit = clone_at_ref(url, args.ref, out_dir)
    except subprocess.CalledProcessError as exc:
        print(json.dumps({"ok": False, "error": exc.stderr or str(exc)}), file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "ok": True,
                "repo": args.repo,
                "ref": args.ref,
                "commit": commit,
                "path": str(out_dir),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
