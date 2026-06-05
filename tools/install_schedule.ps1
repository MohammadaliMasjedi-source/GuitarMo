# Register a per-user Windows Scheduled Task (no admin needed) that runs
# Sync.bat every 4 hours while you are logged on. Sync only commits/pushes when
# something actually changed, so this is a no-op until you edit project_plan.py.
#
#   Install :  powershell -ExecutionPolicy Bypass -File tools\install_schedule.ps1
#   Remove  :  schtasks /Delete /TN "GuitarMo Sync" /F
#
# Notes:
# - Uses `cmd /c` with doubled quotes so paths with spaces are handled correctly
#   (PowerShell's native-arg quoting mangles schtasks otherwise).
# - An at-logon trigger (/SC ONLOGON) needs an elevated shell; the 4-hourly
#   trigger below works without admin and is enough to keep things in sync.

$repo = Split-Path -Parent $PSScriptRoot
$bat  = Join-Path $repo "Sync.bat"
if (-not (Test-Path $bat)) { throw "Sync.bat not found at $bat" }

cmd /c "schtasks /Create /TN ""GuitarMo Sync"" /TR ""$bat"" /SC HOURLY /MO 4 /F"

Write-Output ""
Write-Output "Installed scheduled task 'GuitarMo Sync' (every 4 hours)."
Write-Output "Remove with:  schtasks /Delete /TN ""GuitarMo Sync"" /F"
