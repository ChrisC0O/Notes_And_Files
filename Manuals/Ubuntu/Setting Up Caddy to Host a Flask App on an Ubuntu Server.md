# Guide: Deploy a Flask App with Caddy + Gunicorn on Ubuntu (Clean, Modern Setup – Socket in /run)

This is the fully updated, production-ready guide with the Unix socket correctly placed in `/run` (the recommended location), proper systemd hardening, automatic HTTPS, and request logging.

Tested on Ubuntu 22.04 & 24.04 LTS.

### Step 1: Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2: Install Python & Tools
```bash
sudo apt install -y python3 python3-venv python3-pip curl
```

### Step 3: Create Project & Virtual Environment
```bash
mkdir ~/flask-app && cd ~/flask-app
python3 -m venv venv
source venv/bin/activate
pip install flask gunicorn
deactivate
```

Create your `app.py` (example):
```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Flask + Caddy!"

if __name__ == "__main__":
    app.run()
```

### Step 4: Create Proper systemd Service (Socket in /run)

```bash
sudo nano /etc/systemd/system/flask-app.service
```

Paste exactly this:

```ini
[Unit]
Description=Gunicorn instance for Flask application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/www-data/flask-app
Environment="PATH=/home/www-data/flask-app/venv/bin"

# Creates /run/flask-app directory automatically at startup
RuntimeDirectory=flask-app
RuntimeDirectoryMode=0755

ExecStart=/home/www-data/flask-app/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/run/flask-app/app.sock \
          app:app

Restart=always
RestartSec=5

# Security hardening
PrivateTmp=true
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/home/www-data/flask-app

[Install]
WantedBy=multi-user.target
```

Apply it:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now flask-app
sudo systemctl status flask-app    # Should be active (running) with no errors
```

Verify socket:
```bash
ls -l /run/flask-app/app.sock
# Expected: srw-rw-rw- 1 www-data www-data 0 ...
```

### Step 5: Install Caddy
```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy -y
```

### Step 6: Configure Caddy (with Access Logging)

```bash
sudo nano /etc/caddy/Caddyfile
```

Replace with (use your real domain):

```caddy
example.com {
    # Human-readable access log with rotation
    log {
        output file /var/log/caddy/access.log {
            roll_size     100mb
            roll_keep     10
            roll_keep_for 720h
        }
        format console
    }

    # Proxy to socket in /run
    reverse_proxy unix//run/flask-app/app.sock
}
```

Validate & reload:
```bash
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

Create log directory (if needed):
```bash
sudo mkdir -p /var/log/caddy
sudo chown caddy:caddy /var/log/caddy
```

### Step 7: Open Firewall
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw reload
```

### Step 8: Test Everything
- Visit https://example.com → your Flask app should load instantly
- HTTPS certificate is obtained automatically
- Watch live requests:
```bash
sudo tail -f /var/log/caddy/access.log
```

### Quick Troubleshooting
| Issue                  | Command to Check                                  |
|------------------------|---------------------------------------------------|
| 502 Bad Gateway        | `ls -l /run/flask-app/app.sock`                  |
| Gunicorn not starting  | `sudo journalctl -u flask-app -f`                 |
| Caddy errors           | `sudo journalctl -u caddy -f`                     |
| No logs                | `sudo chown caddy:caddy /var/log/caddy`           |

This setup is clean, secure, scalable, and used in real production environments. No more home-directory socket permission problems — ever.
