"""One-command sync: plan -> docs + Obsidian + dashboard -> GitHub.

Regenerates everything from project_plan.py, then commits & pushes **only if
something actually changed** (so scheduled runs never create empty/noisy
commits). Run manually or on a schedule (see tools/install_schedule.ps1).

    python tools/sync.py                 # regenerate, commit changed, push
    python tools/sync.py --no-push       # local only
    python tools/sync.py --message "..." # custom commit message
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable

try:                                  # console may be cp1252 (Windows)
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def run(rel, *, required=True):
    path = os.path.join(ROOT, rel)
    print(f"-> {rel}")
    r = subprocess.run([PY, path], cwd=ROOT)
    if r.returncode != 0 and required:
        print(f"  ! {rel} exited {r.returncode}")
    return r.returncode


def git(*args, capture=False):
    r = subprocess.run(["git", "-C", ROOT, *args],
                       capture_output=capture, text=True)
    return r.stdout.strip() if capture else r.returncode


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--no-push", action="store_true")
    p.add_argument("--message", default=None)
    args = p.parse_args(argv)

    print("=== GuitarMo sync ===")
    run("docs/generate_task_cards.py")    # task cards + PROGRESS.md
    run("tools/update_obsidian.py", required=False)   # vault may be absent
    run("dashboard/build_dashboard.py")   # local dashboard (gitignored)

    # commit only repo-tracked changes that actually differ
    git("add", "-A")
    changed = git("status", "--porcelain", capture=True)
    if not changed:
        print("[ok] nothing changed -- repo already in sync.")
        return 0

    msg = args.message or (
        "chore(sync): regenerate plan docs / progress / dashboard "
        f"({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    git("commit", "-m", msg)
    print("[ok] committed changes.")

    if args.no_push:
        print("(--no-push) staying local.")
        return 0
    rc = git("push", "origin", "HEAD")
    print("[ok] pushed to GitHub." if rc == 0 else
          "[!] push failed (auth/offline?) -- commit is saved locally.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
