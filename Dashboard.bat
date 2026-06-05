@echo off
REM Build the GuitarMo dashboard from the local repo + plan, then open it.
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  set "PY=.venv\Scripts\python.exe"
) else (
  set "PY=python"
)
%PY% dashboard\build_dashboard.py
start "" "%~dp0dashboard\dashboard.html"
