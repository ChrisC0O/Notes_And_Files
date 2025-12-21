## Overview of the solution

1. Create a **Telegram bot**
2. Get your **chat ID**
3. Write a small **notification script**
4. Attach it to **PAM’s SSH session hook**
5. Test and secure it

---

## 1️⃣ Create a Telegram bot

In Telegram:

1. Open **@BotFather**
2. Run `/start`
3. Run `/newbot`
4. Give it a name and username
5. Copy the **Bot Token** (looks like `123456:ABC-DEF...`)

---

## 2️⃣ Get your Telegram chat ID

Send a message to your bot (anything).

Then run on your server:

```bash
curl -s "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates"
```

Look for:

```json
"chat":{"id":123456789}
```

Save that **chat ID**.

---

## 3️⃣ Create the notification script

Create the script:

```bash
sudo nano /usr/local/bin/ssh-telegram-notify.sh
```

Paste this (replace TOKEN and CHAT_ID):

```bash
#!/bin/bash

BOT_TOKEN="YOUR_BOT_TOKEN"
CHAT_ID="YOUR_CHAT_ID"

USER="$PAM_USER"
IP="$PAM_RHOST"
HOST="$(hostname)"
DATE="$(date '+%Y-%m-%d %H:%M:%S')"

MESSAGE="🔐 SSH Login
User: $USER
Host: $HOST
IP: $IP
Time: $DATE"

curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
  -d chat_id="$CHAT_ID" \
  -d text="$MESSAGE" \
  -d parse_mode="Markdown" >/dev/null
```

Make it executable:

```bash
sudo chmod 700 /usr/local/bin/ssh-telegram-notify.sh
```

⚠️ **700 is important** – the token must not be world-readable.

---

## 4️⃣ Hook it into SSH via PAM (best practice)

Edit PAM SSH config:

```bash
sudo nano /etc/pam.d/sshd
```

Add this **at the end**:

```text
session optional pam_exec.so /usr/local/bin/ssh-telegram-notify.sh
```

This triggers **only after successful authentication**.

---

## 5️⃣ Test it

From another machine:

```bash
ssh user@your-server
```

You should immediately receive a Telegram message.

---

## 🔒 Security & hardening tips (important)

* Store the script **outside `/home`**
* Keep permissions at **700**
* Use a **private Telegram chat**, not a group
* Optionally restrict SSH users via:

  ```bash
  AllowUsers user1 user2
  ```
* Combine with **Fail2Ban** for brute-force protection

---

## Optional improvements

* Add:

  * TTY info
  * SSH key fingerprint
  * GeoIP lookup
* Only notify for **non-local IPs**
* Rate-limit notifications

---

## Alternative (not recommended)

Parsing `/var/log/auth.log` with cron or systemd
❌ Less reliable
❌ Can miss events
❌ Harder to filter success vs failure

PAM is the **correct and clean** solution.

---

If you want, I can:

* Rewrite this **in Danish or German**
* Add **IP geolocation**
* Convert it to a **systemd service**
* Make it notify **only for specific users**

Just tell me 👍
