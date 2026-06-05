# Register a Windows Scheduled Task that keeps GuitarMo's docs, Obsidian note
# and dashboard in sync and pushes plan changes to GitHub automatically.
#
# Runs Sync.bat at logon and every 4 hours. Sync only commits/pushes when
# something actually changed, so this is a no-op until you edit project_plan.py.
#
#   Install :  powershell -ExecutionPolicy Bypass -File tools\install_schedule.ps1
#   Remove  :  Unregister-ScheduledTask -TaskName "GuitarMo Sync" -Confirm:$false

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
$bat  = Join-Path $repo "Sync.bat"
$name = "GuitarMo Sync"

if (-not (Test-Path $bat)) { throw "Sync.bat not found at $bat" }

$action  = New-ScheduledTaskAction -Execute $bat -WorkingDirectory $repo
$atLogon = New-ScheduledTaskTrigger -AtLogOn
$daily   = New-ScheduledTaskTrigger -Once -At (Get-Date).Date.AddHours(9) `
           -RepetitionInterval (New-TimeSpan -Hours 4) `
           -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable `
            -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
            -ExecutionTimeLimit (New-TimeSpan -Minutes 15)

try { Unregister-ScheduledTask -TaskName $name -Confirm:$false } catch {}

Register-ScheduledTask -TaskName $name -Action $action `
  -Trigger @($atLogon, $daily) -Settings $settings `
  -Description "Keep GuitarMo docs/Obsidian/dashboard in sync and push plan changes." | Out-Null

Write-Output "Registered scheduled task '$name' (at logon + every 4h)."
Write-Output "Remove with: Unregister-ScheduledTask -TaskName '$name' -Confirm:`$false"
