# Pocket DevStation: open Git Bash and start Claude Code with Remote Control.
# Windows runs this by itself every time the laptop wakes from sleep.
$project = "$env:USERPROFILE\Desktop\projects"  # folder Claude opens in; change this to pick another project

# If a session started by this script is still open, do not start a second one.
$running = Get-CimInstance Win32_Process -Filter "Name = 'claude.exe'" |
    Where-Object { $_.CommandLine -like '*--remote-control*' }
if (-not $running) {
    Start-Process 'C:\Program Files\Git\git-bash.exe' -ArgumentList "--cd=`"$project`"", '-c', '"claude --remote-control DevStation"'
}
