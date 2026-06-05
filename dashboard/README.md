# GuitarMo Dashboard

A live, single-file dashboard for the whole project: phases, progress rings,
Definition-of-Done, the full task board, and **local + online git activity**.

## Use
- **Double-click `Dashboard.bat`** (repo root) → builds and opens the dashboard.
- Or: `python dashboard/build_dashboard.py` then open `dashboard/dashboard.html`.

## How "realtime" works
- **Local** (plan, progress, recent commits, branch, dirty state) is **baked**
  into the HTML each time you build it — rebuild via `Dashboard.bat` or let
  `Sync.bat` do it on a schedule.
- **Online** (GitHub stars, last push, open issues, latest commits) is fetched
  **live in the browser** from the GitHub API and **auto-refreshes every 5 min**
  (no rebuild needed). If you're offline it falls back to the baked local data.

## Data source
Everything derives from **`project_plan.py`** (the single source of truth) plus
`git`. Change the plan there and the dashboard, task cards, `PROGRESS.md` and the
Obsidian note all update together via `Sync.bat`.

`dashboard.html` is git-ignored (a local build artifact); the builder is tracked.
