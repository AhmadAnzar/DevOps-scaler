+# Linux Homework

Name: Anzar
Enrollment Number: 24BCS10289

This README documents the Linux homework exercises for soft links, hard links,
user management, system logs, and common Linux commands.

## 1. Soft Links and Hard Links

A hard link is another directory entry for the same inode as the original
file. It continues to work when the original filename is deleted.

A symbolic link, also called a soft link, stores the path to another file. It
has its own inode and becomes broken when its target is deleted.

### Commands used

```bash
mkdir -p ~/linux-session-1/links
cd ~/linux-session-1/links

echo "Hello from the original file" > original.txt
ln original.txt hard-link.txt
ln -s original.txt soft-link.txt

ls -li
cat original.txt
cat hard-link.txt
cat soft-link.txt
```

### Expected observation

`original.txt` and `hard-link.txt` should have the same inode number.
`soft-link.txt` should have a different inode number and point to
`original.txt`.

### Delete the original file

```bash
rm original.txt

echo "Hard link after deleting original:"
cat hard-link.txt

echo "Soft link after deleting original:"
cat soft-link.txt
```

### Expected observation

The hard link should still display the file contents. The soft link should
fail with a message similar to `No such file or directory`.

## 2. `adduser` versus `useradd`

`useradd` is a low-level, non-interactive utility. It normally requires
explicit options for settings such as the home directory, login shell, and
groups.

`adduser` is a higher-level interactive utility available on Debian and
Ubuntu systems. It guides the user through account creation and normally
creates the home-directory setup automatically.

For manually creating a user on Ubuntu, `adduser` is easier for beginners. For
repeatable automation scripts, `useradd` is useful because it is
non-interactive and provides precise options.

### Commands used

```bash
which adduser
which useradd

sudo adduser linux-test-user
id linux-test-user
getent passwd linux-test-user

sudo deluser --remove-home linux-test-user
```

## 3. Viewing Logs with `journalctl`

`journalctl` is used to view and filter logs collected by
`systemd-journald`. It can show logs for the current boot, kernel logs,
individual services, and specific time ranges.

### Commands used

```bash
systemctl is-active systemd-journald
journalctl -b -n 20 --no-pager
journalctl -k -n 20 --no-pager
```

To inspect a service, first find an available service:

```bash
systemctl list-units --type=service --all | grep -E 'ssh|cron|systemd'
```

Then use an available service name. For example:

```bash
sudo journalctl -u ssh -n 20 --no-pager
journalctl --since "1 hour ago" --no-pager
```

If the `ssh` service is not installed, use `cron` instead:

```bash
sudo journalctl -u cron -n 20 --no-pager
```

To follow new entries live:

```bash
sudo journalctl -u ssh -f
```

Press `Ctrl+C` to stop the live log view.

### Useful `journalctl` options

| Command | Purpose |
| --- | --- |
| `journalctl -b` | Shows logs from the current boot |
| `journalctl -k` | Shows kernel logs |
| `journalctl -u SERVICE` | Shows logs for a specific service |
| `journalctl -f` | Follows new log entries live |
| `journalctl --since "1 hour ago"` | Filters logs by time |
| `-n 20` | Shows only the latest 20 entries |
| `--no-pager` | Prints output directly in the terminal |

## 4. Linux Command Cheat Sheet

| Command | Purpose | Example |
| --- | --- | --- |
| `pwd` | Shows the current directory | `pwd` |
| `ls` | Lists files and directories | `ls -la` |
| `cd` | Changes directory | `cd /var/log` |
| `mkdir` | Creates a directory | `mkdir project` |
| `touch` | Creates an empty file | `touch notes.txt` |
| `cat` | Displays file contents | `cat notes.txt` |
| `cp` | Copies files | `cp a.txt b.txt` |
| `mv` | Moves or renames files | `mv old.txt new.txt` |
| `rm` | Removes files | `rm notes.txt` |
| `grep` | Searches text | `grep error app.log` |
| `find` | Finds files | `find . -name "*.log"` |
| `chmod` | Changes permissions | `chmod +x script.sh` |
| `ps` | Lists running processes | `ps aux` |
| `df` | Displays disk usage | `df -h` |
| `du` | Displays directory size | `du -sh .` |
| `free` | Displays memory usage | `free -h` |
| `whoami` | Displays the current user | `whoami` |
| `hostname` | Displays the system hostname | `hostname` |
| `date` | Displays the current date and time | `date` |
| `systemctl` | Manages system services | `systemctl status ssh` |
| `journalctl` | Reads systemd logs | `journalctl -b` |

### Practice commands

```bash
mkdir -p ~/linux-command-practice
cd ~/linux-command-practice
pwd
ls -la
touch notes.txt
echo "Linux practice" > notes.txt
cat notes.txt
cp notes.txt backup.txt
mv backup.txt renamed.txt
grep "Linux" notes.txt
find . -type f
df -h
du -sh .
free -h
whoami
hostname
date
```

## Conclusion

In this session, I learned the difference between hard links and symbolic
links, user creation with `adduser` and `useradd`, and system log inspection
using `journalctl`. I also practised common Linux commands used for file
management, permissions, processes, disk usage, and system troubleshooting.
