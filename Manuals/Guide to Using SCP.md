# Guide to Using SCP: Securely Sending and Downloading Files

SCP (Secure Copy Protocol) is a command-line tool for securely transferring files and directories between a local machine and a remote host (or between two remote hosts) using SSH for encryption. It's simple, fast, and widely available on Unix-like systems (Linux, macOS) and can be installed on Windows via tools like OpenSSH or Git Bash.

## Prerequisites
- **SSH Access**: You need SSH credentials (username/password or SSH key) to the remote server.
- **Installation**:
  - Linux/macOS: Usually pre-installed. Check with `scp --version`.
  - Windows: Install OpenSSH via Settings > Apps > Optional Features, or use PuTTY's `pscp`.
- Run commands in a terminal (e.g., Terminal on macOS/Linux, Command Prompt/PowerShell on Windows).

**Note**: SCP uses the same authentication as SSH, so ensure your SSH key is set up if using key-based auth (`~/.ssh/id_rsa` by default).

## Basic Syntax
```
scp [options] source destination
```
- **Source**: Local or remote file/directory path.
- **Destination**: Remote or local path.
- Paths can include `user@host:/path` for remote.

**Key Options**:
- `-r`: Recursive (for directories).
- `-P port`: Specify SSH port (default: 22).
- `-i keyfile`: Use a specific SSH private key.
- `-v`: Verbose mode for debugging.
- `-C`: Compress data during transfer.

## Common Examples

### 1. Upload a Single File to Remote Server
Copy a local file to a remote directory.

**Command**:
```bash
scp /path/to/local/file.txt username@remote_host:/remote/path/
```

**Example**:
```bash
scp ~/Documents/report.pdf user@example.com:/home/user/uploads/
```
- Transfers `report.pdf` from your local `~/Documents/` to `/home/user/uploads/` on the remote server.

### 2. Download a Single File from Remote Server
Copy a remote file to your local machine.

**Command**:
```bash
scp username@remote_host:/remote/path/file.txt /local/path/
```

**Example**:
```bash
scp user@example.com:/var/www/html/index.html ~/Downloads/
```
- Downloads `index.html` from the remote server to your local `~/Downloads/` directory.

### 3. Upload a Directory Recursively
Copy an entire local directory to the remote server.

**Command**:
```bash
scp -r /local/directory/ username@remote_host:/remote/path/
```

**Example**:
```bash
scp -r ~/projects/myapp/ dev@server.com:/opt/apps/
```
- Uploads the `myapp` directory and all its contents to `/opt/apps/` on the remote server. (Note the trailing `/` on source to copy contents, not the folder itself.)

### 4. Download a Directory Recursively
Copy an entire remote directory to your local machine.

**Command**:
```bash
scp -r username@remote_host:/remote/path/directory/ /local/path/
```

**Example**:
```bash
scp -r backup@backup-server.com:/backups/2023/ ~/Archives/
```
- Downloads the `2023` directory and subcontents to your local `~/Archives/`.

### 5. Transfer Between Two Remote Servers
Copy files directly from one remote host to another (via your local machine as proxy).

**Command**:
```bash
scp username1@host1:/path/file.txt username2@host2:/path/
```

**Example**:
```bash
scp alice@serverA:/data/logs/error.log bob@serverB:/logs/
```
- Transfers `error.log` from `serverA` to `serverB`. You'll authenticate to both servers.

### 6. Using a Non-Standard SSH Port
If the remote SSH server uses a custom port (e.g., 2222).

**Command**:
```bash
scp -P 2222 /local/file.txt username@remote_host:/remote/path/
```

**Example**:
```bash
scp -P 2222 ~/notes.md user@securehost.com:/docs/
```

### 7. Using a Specific SSH Key
For key-based authentication with a custom key file.

**Command**:
```bash
scp -i ~/.ssh/mykey.pem /local/file.txt username@remote_host:/remote/path/
```

**Example**:
```bash
scp -i ~/id_ed25519 /etc/hosts admin@ec2-instance:/tmp/
```
- Uses the `id_ed25519` key for AWS EC2 transfer.

### 8. Verbose Transfer with Compression
Monitor progress and compress large files.

**Command**:
```bash
scp -v -C /largefile.zip username@remote_host:/remote/path/
```

**Example**:
```bash
scp -v -C ~/backups/bigdb.tar.gz user@dbserver.com:/var/backups/
```
- `-v` shows transfer details; `-C` reduces bandwidth usage.

## Tips and Troubleshooting
- **Progress Indicator**: SCP doesn't show progress by default. Pipe to `pv` (install if needed: `sudo apt install pv` on Debian-based) like `scp file user@host:/path/ | pv`.
- **Permissions**: Ensure you have read/write access on both ends. Use `ls -la` to check.
- **Overwriting Files**: SCP prompts before overwriting; use `-f` (force) sparingly.
- **Errors**:
  - "Permission denied": Check credentials/keys (`ssh user@host` first).
  - "No such file": Verify paths.
  - "Connection refused": Ensure SSH is running on the remote host/port.
- **Alternatives**: For more features (resumable transfers, GUI), consider `rsync` over SSH (`rsync -avz -e ssh source/ dest/`).
- **Security**: Always use SCP over untrusted networks; avoid passwords in scripts—use keys.
