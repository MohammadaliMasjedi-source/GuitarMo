"""Regenerate the GuitarMo note in the Obsidian (Synotic) vault from the plan.

Single source of truth = project_plan.py. Writes META['obsidian_note'];
skips gracefully if the vault is not present on this machine.

    python tools/update_obsidian.py
"""
from __future__ import annotations

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from project_plan import (DONE, EMOJI, META, NEXT, PHASES, TODO,  # noqa: E402
                          counts, overall_progress, phase_progress)

# German "Wort des Tages" footer (Deutsch-A1 habit: a word + etymology).
GERMAN_FOOTER = """---
### 🇩🇪 Wort des Tages
**der Akkord** — *the chord*.
🔎 **Linguistik:** entlehnt aus französisch *accord* (Übereinstimmung), aus \
altfranzösisch *acorder*, aus vulgärlateinisch \\*_accordāre_ („in Einklang \
bringen"), zu lateinisch *ad-* („zu") + *cor / cordis* („Herz") — wörtlich \
„Herzen zusammenbringen". Verwandt mit englisch *accord* / *concord*.
Merksatz: *Ein **Akkord** bringt die Töne — und die Herzen — in Einklang.*"""


def next_actions():
    out = []
    for ph in PHASES:
        for t in ph["tasks"]:
            if t["status"] in (NEXT,) or (ph["status"] == NEXT and t["status"] != DONE):
                out.append(f"- [ ] **{t['id']}** {t['title']} — {t['objective']}")
        if len(out) >= 4:
            break
    return out[:5]


def build_note():
    c = counts()
    pct = round(overall_progress() * 100)
    done_phases = sum(1 for ph in PHASES if ph["status"] == DONE)
    rows = "\n".join(
        f"| {ph['num']} | {ph['title']} | {EMOJI[ph['status']]} | "
        f"{round(phase_progress(ph) * 100)}% |" for ph in PHASES)
    note = f"""---
title: {META['name']}
type: project
status: active
overall_progress: {pct}%
phase: "{done_phases} phases done · Phase 2 next"
updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
repo: {META['repo_url']}
tags: [project, music, ml, audio, mir, python, guitar]
---

# {META['emoji']} {META['name']}

> **{META['tagline']}**
> Hum/sing into a laptop, pick a **style** + **difficulty tier**, and it
> transcribes the pitch, finds the key, harmonizes it, and plays it back on a
> synthesized nylon-string guitar — with **tab**, **MIDI** and **sheet music**.

**Repo:** {META['repo_url']}
**Local:** `{META['local_path']}` · package/brand `guitarmo`
**Dashboard:** run `Dashboard.bat` in the repo for the live view.

## 📊 Status — {pct}% overall
✅ {c[DONE]} done · 🔜 {c[NEXT]} next · ⬜ {c[TODO]} planned

| # | Phase | Status | Progress |
|--:|-------|:------:|:--------:|
{rows}

## ▶️ Next actions
{os.linesep.join(next_actions())}

## 🧠 Why it matters
- Fun, demoable, paper-worthy → fits the **[[CellSight commercial demo]]**
  barbell (demo → consulting → productize) and a portfolio piece on
  [[Website repo|the Mo · MassJedi site]].
- The Phase-3 **training** reuses ML + GPU muscle from the
  [[Thesis dashboard|battery thesis]] on the [[ISSE GPU access|ISSE RTX-3090]].
- See `docs/VISION_AND_QUALITY.md` in the repo for the paper/presentation/career plan.

## 🔗 References
- [[Synotic vault]] · [[Deutsch A1 goal]]
- Repo docs: `ROADMAP.md`, `PROGRESS.md`, `RESEARCH.md`, `docs/tasks/`

{GERMAN_FOOTER}

<!-- Auto-generated from project_plan.py by tools/update_obsidian.py. Edit the plan, not this note. -->
"""
    return note


def main():
    path = META["obsidian_note"]
    parent = os.path.dirname(path)
    if not os.path.isdir(parent):
        print(f"[skip] Obsidian vault not found at {parent}")
        return 1
    with open(path, "w", encoding="utf-8") as f:
        f.write(build_note())
    print(f"updated Obsidian note -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
