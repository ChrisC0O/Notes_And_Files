# Guide to Setting Up Caddy Web Server on Fedora

Caddy is a powerful, open-source web server that automatically enables HTTPS, serves static files, acts as a reverse proxy, and more. It's ideal for creating directory index pages (like the one in your screenshot) with built-in browsing features. This guide walks you through installing Caddy on a Fedora server (tested on Fedora 42+, but should work on recent versions), configuring it for a basic directory listing, and enabling automatic HTTPS. We'll use the official installation method from caddyserver.com.

**Prerequisites:**
- A Fedora server with root or sudo access.
- A domain name pointed to your server's IP (optional for local testing, but required for public HTTPS).
- Firewall configured to allow ports 80 (HTTP) and 443 (HTTPS). On Fedora, use `firewall-cmd`.
- Basic familiarity with the terminal.

## Step 1: Update Your System
Ensure your system is up to date to avoid package conflicts.

```
sudo dnf update -y
```

## Step 2: Install Prerequisites
Fedora uses `dnf` as the package manager. Install the DNF plugins for COPR (Cool Other Package Repo) support.

```
sudo dnf install dnf5-plugins -y
```

## Step 3: Enable the Official Caddy Repository
Caddy provides an official COPR repository for Fedora. Enable it with:

```
sudo dnf copr enable @caddy/caddy -y
```

This adds the repository maintained by the Caddy team.

## Step 4: Install Caddy
Install the Caddy package:

```
sudo dnf install caddy -y
```

This installs Caddy as a systemd service but doesn't start it automatically.

## Step 5: Configure Firewall (If Enabled)
Allow HTTP and HTTPS traffic:

```
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

## Step 6: Start and Enable Caddy Service
Start the service and enable it to run on boot:

```
sudo systemctl start caddy
sudo systemctl enable caddy
```

Check the status:

```
sudo systemctl status caddy
```

If it's running, you'll see output indicating the service is active.

## Step 7: Configure Caddy for a Directory Index Page
Caddy uses a configuration file called `Caddyfile` (by default at `/etc/caddy/Caddyfile`). We'll set it up to serve a directory with browsing enabled, similar to your screenshot. This enables an elegant file browser for directories without an index.html.

1. Create a directory to serve (e.g., `/var/www/downloads`) and add some subdirectories/files for testing:

   ```
   sudo mkdir -p /var/www/downloads/{captions,clearvision,documents,scripts,tracker,uploads,wallpapers}
   sudo chown -R $USER:$USER /var/www/downloads  # For easier editing; adjust permissions as needed
   ```

   Add some placeholder files if desired (e.g., `touch /var/www/downloads/captions/test.txt`).

2. Edit the Caddyfile:

   ```
   sudo nano /etc/caddy/Caddyfile
   ```

   Replace the contents with a basic configuration. Assuming you have a domain like `example.com` (replace with yours). For local testing, use `localhost`.

   ```
   example.com {
       root * /var/www/downloads
       file_server browse
       encode gzip zstd  # Optional: Enable compression
   }
   ```

   - `root * /var/www/downloads`: Sets the root directory to serve.
   - `file_server browse`: Enables the directory listing browser with features like file sizes, dates, and icons.
   - If using localhost for testing: Replace `example.com` with `localhost` or your server's IP.
   - For automatic HTTPS: Caddy will handle TLS certificates via Let's Encrypt if the domain is public and DNS is pointed correctly.

3. Reload Caddy to apply changes (Caddy supports graceful reloads without downtime):

   ```
   sudo systemctl reload caddy
   ```

## Step 8: Test the Setup
- Visit `http://example.com` (or `http://your-server-ip`) in a browser. Caddy will redirect to HTTPS automatically if configured.
- You should see a directory listing similar to your screenshot, showing folders like `captions/`, `clearvision/`, etc., with names, sizes (empty folders show `-`), and dates.
- For local testing: `http://localhost` or `https://localhost` (Caddy auto-installs a local CA for HTTPS on localhost).

If HTTPS doesn't work:
- Ensure your domain's DNS A/AAAA records point to the server's IP.
- Check logs: `journalctl -u caddy` for errors (e.g., certificate issuance issues).
- Allow time for DNS propagation.

## Step 9: Advanced Tips
- **Automatic HTTPS for Custom Domains**: As described in the Caddy docs, it uses On-Demand TLS. No extra config needed for public domains.
- **Security**: Set proper permissions (`chmod -R 755 /var/www/downloads`) and consider adding authentication if exposing sensitive files.
- **Updates**: Update Caddy with `sudo dnf update caddy` and reload the service.
- **Custom Builds**: If you need plugins (e.g., for PHP with FrankenPHP), download custom builds from caddyserver.com/download.
- **Troubleshooting**: View full docs at caddyserver.com/docs. Common issues include firewall blocks or SELinux (disable temporarily with `setenforce 0` if needed, but harden later).

This setup replicates a simple index download page using Caddy's built-in features. If you need to integrate with the caddyserver.com demo (e.g., pointing a subdomain to their IP for testing automagic HTTPS), follow the "Experience it" section in the provided document—no local changes needed beyond DNS updates. For more complex configs like reverse proxies or PHP, expand the Caddyfile as shown in the examples. Let me know if you encounter issues!
