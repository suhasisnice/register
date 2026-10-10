# Home server (deploy target only)

Develop on this PC. The server only runs what gets pushed to it. No editing or debugging on the server.

## Server
- Host `homelab`, user `suhasisnice`, passwordless SSH from this PC: `ssh suhasisnice@192.168.68.108`
- IP is reserved at .108 in the Deco app (Address Reservation). It used to float (was .110). If SSH times out, the server is off or missed the network, not an IP change.
- Ubuntu 26.04.1 LTS, kernel 7.0, x86_64, 2 vCPU, 3.3 GB RAM, 19 GB disk (41% used). Looks like a VM on the Proxmox host.
- Proxmox host: `192.168.68.200` (web UI https://192.168.68.200:8006). The VM must be started there after a host reboot unless "Start at boot" is on.
- `sudo` needs a password. Do not assume root.

## Network quirk
Router is a TP-Link Deco M5 mesh (192.168.68.1). If the server boots before the Deco is up it can miss the network. Power the Deco first, then the server.

Mitigation (installed 2026-10-11 on the Proxmox host, `ssh root@192.168.68.200`, key auth): `net-watchdog.timer` pings the router every minute. After 3 failures it runs `ifreload -a`, after 5 it bounces `nic0` (Realtek r8169). Never reboots. Logs: `journalctl -t net-watchdog`. Script: `/usr/local/bin/net-watchdog.sh`.

## Installed (as of 2026-10-11)
- python3 3.14.4, git 2.53.0
- Not installed: node, npm, docker, nginx, caddy, pm2, go, java, php

## Running
- Only sshd (port 22) and system services (chrony, fwupd, upower). No app listening on any port.

## Folder layout
- Fresh install: `/srv`, `/opt`, `/var/www` are empty. No git repos, no cron jobs. Home dir has only dotfiles.
- No deploy location chosen yet.

## How to deploy
Not set up yet. Decide per project, then record it here:
1. Pick a target folder on the server (suggest `/srv/<app>`, needs sudo to create).
2. Copy from this PC: `rsync -av --exclude .git ./app/ suhasisnice@192.168.68.108:/srv/<app>/` (or scp / git pull).
3. Install any runtime the app needs (needs sudo password, ask the user).
4. Run it as a systemd service so it survives reboots.
