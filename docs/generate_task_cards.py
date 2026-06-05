"""Generate one Markdown task card per sub-phase into docs/tasks/.

Data comes from the single source of truth ``project_plan.py``. Edit the plan
there, then run this (or Sync.bat) to regenerate all cards + the index.

    python docs/generate_task_cards.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from project_plan import (DONE, EMOJI, NEXT, PHASES, STATUS_LABEL, TODO,  # noqa: E402
                          counts, overall_progress, phase_progress)


def write_progress(here):
    """Regenerate docs/PROGRESS.md from the plan (single source of truth)."""
    c = counts()
    L = ["# ✅ GuitarMo — Progress Tracker", "",
         "> Auto-generated from `project_plan.py` (via `Sync.bat`). "
         "Edit the plan, not this file.", "",
         f"**Overall: {round(overall_progress() * 100)}%** · "
         f"✅ {c[DONE]} done · 🔜 {c[NEXT]} next · ⬜ {c[TODO]} planned", "",
         "| Phase | Status | Progress |", "|------:|--------|----------|"]
    for ph in PHASES:
        pct = round(phase_progress(ph) * 100)
        blocks = round(pct / 10)
        bar = "▓" * blocks + "░" * (10 - blocks)
        L.append(f"| {ph['num']} — {ph['title']} | {EMOJI[ph['status']]} "
                 f"{STATUS_LABEL[ph['status']]} | {bar} {pct}% |")
    L.append("")
    for ph in PHASES:
        L.append(f"## Phase {ph['num']} — {ph['title']} {EMOJI[ph['status']]}")
        L.append(f"*{ph['goal']}*\n")
        for t in ph["tasks"]:
            box = "x" if t["status"] == DONE else " "
            dod = "; ".join(t["dod"])
            L.append(f"- [{box}] **{t['id']}** {t['title']} "
                     f"{EMOJI[t['status']]} — *DoD:* {dod}")
        L.append("")
    L.append("---\nSee [CHANGELOG.md](../CHANGELOG.md) for the dated history.")
    with open(os.path.join(here, "PROGRESS.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))


def slug(title):
    s = "".join(c.lower() if c.isalnum() else "_" for c in title)
    while "__" in s:
        s = s.replace("__", "_")
    return s.strip("_")


def card(phase, task):
    box = "x" if task["status"] == DONE else " "
    lines = [
        f"# Task {task['id']} — {task['title']}", "",
        f"**Phase:** {phase['title']} · **Status:** "
        f"{EMOJI[task['status']]} {STATUS_LABEL[task['status']]}", "",
        "## Objective", task["objective"], "", "## Steps",
    ]
    lines += [f"- [{box}] {s}" for s in task["steps"]]
    lines += ["", "## Definition of Done"]
    lines += [f"- [{box}] {d}" for d in task["dod"]]
    lines += ["", "## Links",
              f"- Phase: [../phases/{phase['file']}](../phases/{phase['file']})",
              "- Progress: [../PROGRESS.md](../PROGRESS.md)",
              "- Roadmap: [../ROADMAP.md](../ROADMAP.md)", ""]
    return "\n".join(lines)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "tasks")
    os.makedirs(out, exist_ok=True)
    index = ["# 🗃️ Task cards", "",
             "One card per sub-phase. Generated from `project_plan.py`.", ""]
    n = 0
    for ph in PHASES:
        index.append(f"## Phase {ph['num']} — {ph['title']}")
        for task in ph["tasks"]:
            fname = f"T{task['id'].replace('.', '_')}_{slug(task['title'])}.md"
            with open(os.path.join(out, fname), "w", encoding="utf-8") as f:
                f.write(card(ph, task))
            index.append(f"- {EMOJI[task['status']]} [{task['id']} {task['title']}]({fname})")
            n += 1
        index.append("")
    with open(os.path.join(out, "INDEX.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(index))
    write_progress(here)
    print(f"generated {n} task cards + INDEX.md + PROGRESS.md in {here}")


if __name__ == "__main__":
    main()
