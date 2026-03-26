# Ubuntu Basic Commands Cheat Sheet

## System Information

* `uname -a` — Shows system kernel and architecture info.
* `hostnamectl` — Displays system hostname and OS details.
* `uptime` — Shows how long the system has been running.

## File & Directory Management

* `ls` — Lists files and directories.
* `ls -la` — Lists all files with details including hidden ones.
* `cd <dir>` — Changes the current directory.
* `pwd` — Prints current directory path.
* `mkdir <name>` — Creates a new directory.
* `rm <file>` — Deletes a file.
* `rm -r <dir>` — Deletes a directory recursively.
* `cp <src> <dest>` — Copies files or directories.
* `mv <src> <dest>` — Moves or renames files.

## File Viewing & Editing

* `cat <file>` — Displays file contents.
* `less <file>` — Views file page by page.
* `nano <file>` — Opens file in nano editor.
* `head <file>` — Shows first lines of a file.
* `tail <file>` — Shows last lines of a file.

## Permissions & Ownership

* `chmod <mode> <file>` — Changes file permissions.
* `chown <user>:<group> <file>` — Changes file ownership.

## Package Management (APT)

* `sudo apt update` — Updates package list.
* `sudo apt upgrade` — Upgrades installed packages.
* `sudo apt install <pkg>` — Installs a package.
* `sudo apt remove <pkg>` — Removes a package.
* `sudo apt autoremove` — Removes unused packages.

## User & Account Administration

* `sudo adduser <name>` — Creates a new user.
* `sudo deluser <name>` — Deletes a user.
* `passwd` — Changes current user password.
* `sudo passwd <user>` — Changes another user's password.
* `whoami` — Shows current logged-in user.
* `id` — Displays user and group IDs.

## Group Management

* `sudo addgroup <name>` — Creates a new group.
* `sudo usermod -aG <group> <user>` — Adds user to a group.
* `groups <user>` — Shows groups of a user.

## Process Management

* `ps aux` — Lists running processes.
* `top` — Shows real-time process usage.
* `kill <PID>` — Terminates a process by ID.
* `killall <name>` — Terminates processes by name.

## Disk & Storage

* `df -h` — Shows disk space usage.
* `du -sh <dir>` — Shows directory size.
* `lsblk` — Lists block devices.
* `mount` — Mounts a filesystem.
* `umount` — Unmounts a filesystem.

## Networking

* `ip a` — Shows network interfaces.
* `ping <host>` — Tests network connectivity.
* `curl <url>` — Fetches data from a URL.
* `wget <url>` — Downloads files from internet.
* `ss -tuln` — Lists open ports.

## System Control

* `sudo reboot` — Reboots the system.
* `sudo shutdown now` — Shuts down immediately.
* `sudo shutdown -h +10` — Shuts down after 10 minutes.

## Time & Timezone

* `timedatectl` — Shows current time and timezone settings.
* `sudo timedatectl set-timezone <zone>` — Sets system timezone.
* `sudo timedatectl set-ntp true` — Enables automatic time sync.

## Environment & Variables

* `env` — Lists environment variables.
* `echo $VAR` — Displays a variable value.
* `export VAR=value` — Sets an environment variable.

## Searching

* `find <path> -name <name>` — Searches for files by name.
* `grep <pattern> <file>` — Searches text in files.

## Archives & Compression

* `tar -cvf file.tar <dir>` — Creates tar archive.
* `tar -xvf file.tar` — Extracts tar archive.
* `zip -r file.zip <dir>` — Compresses to zip.
* `unzip file.zip` — Extracts zip archive.

## Service Management (systemd)

* `systemctl status <service>` — Shows service status.
* `sudo systemctl start <service>` — Starts a service.
* `sudo systemctl stop <service>` — Stops a service.
* `sudo systemctl enable <service>` — Enables service on boot.
* `sudo systemctl disable <service>` — Disables service on boot.

## Logs

* `journalctl` — Views system logs.
* `journalctl -u <service>` — Shows logs for a service.

## Hardware Info

* `lscpu` — Shows CPU information.
* `lsusb` — Lists USB devices.
* `lspci` — Lists PCI devices.

## Miscellaneous

* `history` — Shows command history.
* `clear` — Clears terminal screen.
* `alias` — Creates command shortcuts.
