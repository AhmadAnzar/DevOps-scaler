Name: Anzar, 24bcs10289

### Understanding Soft and Hard Links
A hard link is an additional name for the same inode, so the data remains accessible through the hard link even after the original filename is deleted. A symbolic link stores the path to its target, which means it becomes invalid if the target is removed. Symbolic links can also reference directories and targets on other filesystems.

```
# 1. Create a file
ubuntu@ip-172-31-38-20:~$ echo "Hello World" > target.txt

# 2. Create links


ubuntu@ip-172-31-38-20:~$ ln target.txt hard-link.txt
ubuntu@ip-172-31-38-20:~$ ln -s target.txt soft-link.txt

# 3. Verify inodes (notice target.txt and hard-link.txt share the same inode number)
ubuntu@ip-172-31-38-20:~$ ls -li

# 4. Delete the original and see what happens (soft link breaks, hard link survives)
ubuntu@ip-172-31-38-20:~$ rm target.txt
ubuntu@ip-172-31-38-20:~$ cat hard-link.txt  # Succeeds
ubuntu@ip-172-31-38-20:~$ cat soft-link.txt  # Fails: No such file or directory
```

### User Management: `adduser` vs `useradd`
On Ubuntu, `useradd` is the lower-level utility and requires options for settings such as the home directory and login shell. `adduser` provides an interactive interface and normally creates the user's home-directory setup automatically.

```
# Create a test user interactively on Ubuntu
ubuntu@ip-172-31-38-20:~$ sudo adduser testuser

# Verify the user was created successfully
ubuntu@ip-172-31-38-20:~$ id testuser
uid=1001(testuser) gid=1001(testuser) groups=1001(testuser)
```

### Viewing Logs with `journalctl`
I used `journalctl` to inspect the logs collected by `systemd-journald`.

```
# View all logs from the current boot
ubuntu@ip-172-31-38-20:~$ journalctl -b

# View logs for a specific service (e.g., SSH)
ubuntu@ip-172-31-38-20:~$ journalctl -u ssh

# Follow/tail logs live for a service (like 'tail -f')
ubuntu@ip-172-31-38-20:~$ journalctl -u ssh -f

# View logs from a specific time frame
ubuntu@ip-172-31-38-20:~$ journalctl --since "1 hour ago"
```
