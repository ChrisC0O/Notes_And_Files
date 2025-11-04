# Guide: Setting Up Caddy to Host a Flask App on an Ubuntu Server with Request Logging

This guide walks you through deploying a simple Flask application on an Ubuntu server (tested on Ubuntu 24.04 LTS) using Caddy as a reverse proxy web server. Caddy is chosen for its simplicity, automatic HTTPS support, and built-in logging. We'll run the Flask app with Gunicorn (a production WSGI server) for reliability.

**Prerequisites:**
- A fresh Ubuntu server (e.g., 24.04 LTS) with sudo access.
- Basic familiarity with SSH and terminal commands.
- A domain name pointing to your server's IP (for HTTPS; optional for local testing).
- Firewall enabled (UFW recommended).

We'll assume you're deploying a basic "Hello World" Flask app for demonstration. Replace paths and details with your actual app as needed.

## Step 1: Update Your System
Start by updating packages to ensure everything is current.

```bash
sudo apt update && sudo apt upgrade -y
```

## Step 2: Install Python and Dependencies
Flask requires Python 3 (pre-installed on Ubuntu 24.04). Install pip and virtual environments for isolation.

```bash
sudo apt install python3 python3-pip python3-venv -y
```

## Step 3: Create and Set Up Your Flask App
Create a project directory and a simple Flask app.

```bash
mkdir ~/flask-app && cd ~/flask-app
python3 -m venv venv
source venv/bin/activate
pip install flask gunicorn
```

Create `app.py` with a basic Flask app:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Flask on Caddy!"

if __name__ == '__main__':
    app.run()
```

Test locally (in the virtual env):

```bash
python app.py
```

Visit `http://localhost:5000` in your browser (or `curl http://localhost:5000`). Stop with Ctrl+C.

Deactivate the venv for now: `deactivate`.

## Step 4: Install and Configure Gunicorn as a Service
Gunicorn runs your Flask app in production mode. We'll create a systemd service to manage it.

Install Gunicorn globally (or use the venv in the service file):

```bash
sudo apt install gunicorn -y
```

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/flask-app.service
```

Add the following (adjust paths if your app is elsewhere):

```
[Unit]
Description=Gunicorn instance for Flask app
After=network.target

[Service]
User=www-data  # Or your username
Group=www-data
WorkingDirectory=/home/yourusername/flask-app  # Replace with your path
Environment="PATH=/home/yourusername/flask-app/venv/bin"  # If using venv
ExecStart=/home/yourusername/flask-app/venv/bin/gunicorn --workers 3 --bind unix:/home/yourusername/flask-app/flask-app.sock app:app  # Unix socket for security

[Install]
WantedBy=multi-user.target
```

- Replace `yourusername` with your actual username.
- We're using a Unix socket (`flask-app.sock`) for Caddy to proxy to—more secure than TCP.
- If not using venv, use `/usr/bin/gunicorn` and remove the PATH environment.

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl start flask-app
sudo systemctl enable flask-app
```

Check status:

```bash
sudo systemctl status flask-app
```

Test: `curl http://localhost` should fail (no direct access), but the service should be running.

## Step 5: Install Caddy
Caddy is installed via its official APT repository for easy updates.

```bash
# Install dependencies
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https

# Add Caddy's GPG key
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg

# Add Caddy's repository
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list

# Update and install
sudo apt update
sudo apt install caddy -y
```

Caddy is now installed and running (initially serving a placeholder page).

## Step 6: Configure Caddy as a Reverse Proxy
Edit the Caddyfile to proxy requests to your Gunicorn socket and enable logging.

```bash
sudo nano /etc/caddy/Caddyfile
```

Replace contents with (use your domain; for local testing, use `:80`):

```
yourdomain.com {  # Replace with your domain or use :80 for port 80 only
    # Enable access logging to a file
    log {
        output file /var/log/caddy/access.log {
            roll_size 100mb  # Rotate logs at 100MB
            roll_keep 5      # Keep 5 old logs
            roll_keep_for 720h  # Keep for 30 days
        }
    }

    # Reverse proxy to Gunicorn socket
    reverse_proxy /home/yourusername/flask-app/flask-app.sock
}
```

- **Logging Explanation**: The `log` directive captures all HTTP requests (access logs) in JSON format by default. Customize format if needed (e.g., `format json` or `format console`).
- **Proxy**: Points to the Unix socket. For TCP (e.g., `127.0.0.1:8000`), change the ExecStart in Step 4 to `--bind 127.0.0.1:8000` and update here accordingly.
- Caddy automatically handles HTTPS if a domain is specified (via Let's Encrypt).

Validate and reload Caddy:

```bash
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

Check Caddy status:

```bash
sudo systemctl status caddy
```

## Step 7: Configure Firewall
Allow HTTP/HTTPS traffic (Caddy listens on ports 80/443).

```bash
sudo ufw allow 'Caddy'  # Or explicitly: sudo ufw allow 80/tcp && sudo ufw allow 443/tcp
sudo ufw reload
sudo ufw status
```

## Step 8: Test the Setup
- Visit `http://yourdomain.com` (or `http://your-server-ip` for IP-based testing). You should see "Hello from Flask on Caddy!".
- HTTPS will auto-provision on domain use: `https://yourdomain.com`.
- If issues: Check logs with `sudo journalctl -u caddy` or `sudo journalctl -u flask-app`.

## Step 9: Monitor Requests in Real-Time
All requests are logged to `/var/log/caddy/access.log`. Tail it for live viewing:

```bash
sudo tail -f /var/log/caddy/access.log
```

Example output (JSON format):

```
{"level":"info","ts":1730726400.123456,"logger":"http.log.access","msg":"handled request","request":{"remote_ip":"203.0.113.1","remote_port":"12345","client_ip":"203.0.113.1","proto":"HTTP/1.1","method":"GET","host":"yourdomain.com","uri":"/","headers":{"User-Agent":["curl/7.68.0"]}},"bytes_read":0,"observer_name":"https://yourdomain.com","common_log":"203.0.113.1 - - [04/Nov/2025:12:00:00 +0000] \"GET / HTTP/1.1\" 200 28","duration":0.001234567,"size":28,"status":200}
```

- Hit your site with `curl http://yourdomain.com` to see logs update live.
- Press Ctrl+C to stop tailing.
- For human-readable format, add `format console` inside the `log` block in Caddyfile and reload.

## Troubleshooting
- **Permission errors**: Ensure `www-data` owns the app dir: `sudo chown -R www-data:www-data ~/flask-app`.
- **Socket not found**: Verify socket creation with `ls /home/yourusername/flask-app/flask-app.sock`.
- **HTTPS issues**: Ensure DNS points to your IP; Caddy retries cert issuance.
- **Logs not writing**: Check dir permissions: `sudo mkdir -p /var/log/caddy && sudo chown caddy:caddy /var/log/caddy`.
- Restart services: `sudo systemctl restart flask-app caddy`.

## Next Steps
- Scale Gunicorn workers in the service file for production.
- Add static file serving in Caddyfile if needed (e.g., `file_server` directive).
- Secure with environment variables for secrets.
- Monitor with tools like Prometheus.

This setup is production-ready for small apps. For high traffic, consider load balancers. If you encounter errors, share logs for further help!
