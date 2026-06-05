# Contributing to GuitarMo

Thanks for your interest! GuitarMo is a phased project — see
[docs/ROADMAP.md](docs/ROADMAP.md) and the live
[docs/PROGRESS.md](docs/PROGRESS.md) for what's planned and in flight.

## Dev setup
```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .            # editable install (optional)
pytest -q                  # run the test suite
```

## Workflow
1. Pick a task from [docs/tasks/](docs/tasks/) or open an issue.
2. Branch: `git checkout -b phaseN/short-description`.
3. Keep the **rule-based path dependency-free** — new engines/models go behind
   the pluggable interfaces (see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)).
4. Add/extend tests; keep `pytest` green.
5. Update the task card's checklist and `docs/PROGRESS.md` (mark DoD items).
6. Open a PR describing which phase/sub-phase it advances.

## Definition of Done (every task)
- [ ] Code + docstrings.
- [ ] Tests cover the change and pass.
- [ ] The relevant task card and PROGRESS.md are updated.
- [ ] No new mandatory heavy dependency in the base install.

## Style
- Pure-Python, readable, small functions; NumPy for DSP.
- Music timing in **beats** upstream; seconds only at render time.
