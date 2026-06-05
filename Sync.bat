@echo off
REM Regenerate plan docs + Obsidian note + dashboard, then commit & push if changed.
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  set "PY=.venv\Scripts\python.exe"
) else (
  set "PY=python"
)
%PY% tools\sync.py %*
