# **Ultimate Guide to Creating & Controlling a Reddit Bot Using PRAW**  
*Everything you can do with **PRAW** — from basics to advanced automation, with real-world examples*

---

PRAW (**Python Reddit API Wrapper**) is the **official**, most powerful, and widely-used Python library for interacting with Reddit's API. This guide covers **everything** you can do with PRAW — from sending private messages to moderating subreddits, analyzing user behavior, and building intelligent bots.

---

## Prerequisites

| Requirement | Details |
|-----------|--------|
| **Python** | 3.8+ (recommended) |
| **Reddit Account** | Dedicated bot account (avoid using personal accounts) |
| **pip** | Python package manager |
| **Basic Python** | Functions, loops, conditionals |

---

## Step 1: Install PRAW

```bash
pip install praw
```

> Optional: `pip install praw[async]` for async support (advanced)

---

## Step 2: Create a Reddit App (OAuth Setup)

1. Go to: [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. Click **"create app"**
3. Fill in:
   - **Name**: `MyAwesomeBot`
   - **App type**: `script` (for bots)
   - **Description**: Optional
   - **Redirect URI**: `http://localhost:8080`
4. Click **create app**

You’ll get:
```text
client_id     → 14-character string (under app name)
client_secret → long string
```
Also note your **bot’s username & password**

> **SECURITY WARNING**: Never commit these to GitHub!

---

## Step 3: Secure Credentials (Best Practice)

### Option A: Environment Variables (Recommended)

```bash
# In terminal (Linux/macOS)
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USERNAME="your_bot_username"
export REDDIT_PASSWORD="your_bot_password"
export REDDIT_USER_AGENT="MyBot v1.0 by u/YourName"
```

```python
# bot.py
import os
import praw

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

print(f"Logged in as: {reddit.user.me()}")
```

### Option B: `.env` file + `python-dotenv`

```bash
pip install python-dotenv
```

```env
# .env
REDDIT_CLIENT_ID=abc123
REDDIT_CLIENT_SECRET=xyz789
REDDIT_USERNAME=MyBotAccount
REDDIT_PASSWORD=supersecret
REDDIT_USER_AGENT=MyBot v1.0 by u/YourName
```

```python
from dotenv import load_dotenv
import os
import praw

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)
```

---

## Step 4: Core PRAW Objects & Navigation

```python
subreddit = reddit.subreddit("python")
submission = reddit.submission(id="1g1v7n")  # or url="https://..."
comment = submission.comments[0]
redditor = reddit.redditor("spez")
inbox = reddit.inbox
```

---

## ALL PRAW BOT ACTIONS (WITH EXAMPLES)

---

### 1. **Read Subreddit Posts**

```python
sub = reddit.subreddit("learnpython")

# Hot, New, Top, Rising, Controversial
for post in sub.hot(limit=5):
    print(f"↑ {post.score} | {post.title}")

# Filter by time
for post in sub.top(time_filter="week", limit=3):
    print(post.title)
```

---

### 2. **Reply to Posts**

```python
for submission in sub.new(limit=10):
    if "help" in submission.title.lower() and not submission.saved:
        submission.reply("I'm here to help! Try searching the sidebar first. 🤖")
        submission.save()  # Mark as processed
        print(f"Replied to: {submission.title}")
```

---

### 3. **Reply to Comments (Stream)**

```python
for comment in sub.stream.comments(skip_existing=True):
    if "praw" in comment.body.lower():
        comment.reply("PRAW is the best way to interact with Reddit! 🚀\n\nhttps://praw.readthedocs.io")
        print(f"Replied to u/{comment.author}")
```

> `skip_existing=True` → only new comments since bot started

---

### 4. **Upvote / Downvote / Clear Vote**

```python
submission = reddit.submission(url="https://redd.it/abc123")
submission.upvote()
# submission.downvote()
# submission.clear_vote()
```

---

### 5. **Submit a Post**

```python
sub = reddit.subreddit("test")

# Text post
sub.submit(title="Bot Post!", selftext="Hello from PRAW!")

# Link post
sub.submit(title="Cool Python Tip", url="https://realpython.com")

# Crosspost
original = reddit.submission(id="abc123")
sub.submit(title="X-Post from r/python", crosspost=original)
```

---

### 6. **Send Private Message (PM) to User**

```python
user = reddit.redditor("someuser")
user.message(
    subject="Hello from my bot!",
    message="Thanks for posting! Here's a tip: use `pip install praw` 🤖"
)
```

> Use sparingly — Reddit treats mass PMs as spam

---

### 7. **Read Inbox & Reply to Messages**

```python
for item in reddit.inbox.unread(limit=None):
    if isinstance(item, praw.models.Message):
        print(f"PM from u/{item.author}: {item.subject}")
        item.reply("Thanks for your message! I'm a bot. 🤖")
        item.mark_read()
```

---

### 8. **Monitor Mentions (u/yourbot)**

```python
for mention in reddit.inbox.mentions(limit=None):
    if not mention.saved:
        mention.reply("Beep boop! You summoned me! 🔔")
        mention.save()
```

---

### 9. **Moderate Subreddit (Mod Actions)**

```python
sub = reddit.subreddit("your_subreddit")

# Remove post
submission = reddit.submission(id="abc123")
submission.mod.remove()

# Approve post
submission.mod.approve()

# Lock comments
submission.mod.lock()

# Distinguish & sticky comment
comment = submission.reply("Official bot response.")
comment.mod.distinguish(how="yes")  # or "yes sticky"
```

---

### 10. **Flair Posts & Users**

```python
# Set post flair
submission = reddit.submission(id="abc123")
flair_choices = submission.flair.choices()
submission.flair.select(flair_choices[0]['flair_template_id'], "Solved")

# Set user flair
sub.flair.set(redditor="user123", text="Top Helper", css_class="gold")
```

---

### 11. **Search Subreddit or Reddit**

```python
# Search in subreddit
for post in sub.search("praw tutorial", limit=5):
    print(post.title)

# Search all Reddit
for post in reddit.subreddit("all").search("python bot", limit=3):
    print(f"r/{post.subreddit}: {post.title}")
```

---

### 12. **Get User Info & History**

```python
user = reddit.redditor("spez")

print(f"Karma: {user.link_karma} | {user.comment_karma}")
print(f"Account age: {user.created_utc}")

# Recent comments
for comment in user.comments.new(limit=5):
    print(f"r/{comment.subreddit}: {comment.body[:100]}")
```

---

### 13. **Wiki Pages**

```python
wiki = sub.wiki["index"]
print(wiki.content_md)

# Edit wiki (mod only)
sub.wiki["index"].edit("Updated by bot!", reason="Auto-update")
```

---

### 14. **Live Threads & Updates**

```python
# Monitor live thread
live = reddit.live("live_thread_id")
for update in live.stream():
    print(update.body)
```

---

### 15. **Multireddits & User Subscriptions**

```python
user = reddit.redditor("yourusername")
subs = list(user.subreddits())
print([s.display_name for s in subs])
```

---

### 16. **Save / Unsave / Hide Posts**

```python
submission.save()        # Appears in saved
submission.unsave()
submission.hide()        # Removes from feed
submission.unhide()
```

---

### 17. **Report Posts/Comments**

```python
submission.report("Spam or rule violation")
comment.report("Harassment")
```

---

### 18. **Delete Your Own Posts/Comments**

```python
submission = reddit.submission(id="your_post_id")
submission.delete()

comment = reddit.comment(id="your_comment_id")
comment.delete()
```

---

### 19. **Gild (Give Awards)** – Requires Reddit Gold API (Limited)

```python
# Not directly supported in PRAW — use raw API
```

---

### 20. **Handle Rate Limits Gracefully**

```python
import time

for submission in sub.new(limit=50):
    try:
        submission.reply("Auto-response!")
    except praw.exceptions.APIException as e:
        if e.error_type == "RATELIMIT":
            delay = int(e.message.split("minute")[0].split()[-1]) * 60
            print(f"Rate limited! Sleeping {delay}s")
            time.sleep(delay)
    time.sleep(2)  # Be respectful
```

---

## Advanced: Continuous Bot with Error Handling

```python
import praw
import time
import logging

logging.basicConfig(level=logging.INFO)

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

sub = reddit.subreddit("test")

print("Bot is running...")

while True:
    try:
        for comment in sub.stream.comments(skip_existing=True):
            if "hello bot" in comment.body.lower():
                reply = "Hi! I'm here. 👋\n\n*Beep boop*"
                comment.reply(reply)
                logging.info(f"Replied to u/{comment.author}")
        time.sleep(1)
    except Exception as e:
        logging.error(f"Error: {e}")
        time.sleep(10)
```

---

## Example: Smart Auto-Helper Bot

```python
import praw
import time
import re

reddit = praw.Reddit(...)  # credentials
sub = reddit.subreddit("learnpython")

def help_install_package(comment):
    match = re.search(r"how (do I|to) install (\w+)", comment.body, re.I)
    if match:
        package = match.group(2)
        return f"To install `{package}`, run:\n\n```bash\npip install {package}\n```"

while True:
    for comment in sub.stream.comments(skip_existing=True):
        if not comment.saved:
            response = None
            if "install" in comment.body.lower():
                response = help_install_package(comment)
            elif "loop" in comment.body.lower():
                response = "Use `for item in list:` or `while condition:`"

            if response:
                comment.reply(response)
                comment.save()
                print(f"Helped u/{comment.author}")
    time.sleep(1)
```

---

## Best Practices & Anti-Ban Tips

| Rule | Why |
|------|-----|
| **1 request/sec** | Reddit enforces rate limits |
| `skip_existing=True` | Avoid reprocessing |
| `submission.saved` | Track processed items |
| Use `try/except` | Handle API errors |
| Log actions | Debug & audit |
| Test in `r/test` | Safe environment |
| Follow subreddit rules | Avoid bans |
| Don’t mass PM | Seen as spam |
| Use unique `user_agent` | Required by Reddit |

---

## Useful PRAW Resources

| Link | Description |
|------|-----------|
| [PRAW Docs](https://praw.readthedocs.io) | Official documentation |
| [Reddit API Rules](https://www.reddit.com/dev/api) | Must-read |
| [PRAW Models](https://praw.readthedocs.io/en/latest/code_overview/models.html) | Full object reference |
| [GitHub](https://github.com/praw-dev/praw) | Source code & issues |

---

## Final Tips

- **Never hardcode secrets**
- **Use logging, not print()**
- **Handle exceptions**
- **Test locally first**
- **Respect users & mods**
- **Add a “I’m a bot” disclaimer**

---

## You're Ready to Build Anything!

Here are **bot ideas** you can build **today**:

| Bot Type | Idea |
|--------|------|
| Auto-Moderator | Remove posts with banned words |
| Welcome Bot | Reply to new posts with rules |
| Meme Responder | Reply with image when keyword detected |
| Stats Bot | `!stats` → show subreddit stats |
| Reminder Bot | `!remindme 1h` → PM later |
| Quote Bot | `!quote` → random quote |

---

**Need a custom bot?**  
Tell me what you want — I’ll write the full code for you! 🤖

```python
# Example: Reply with this guide when someone says "!praw"
if "!praw guide" in comment.body.lower():
    comment.reply("Here's the full PRAW guide: [link]")
```

---

**You now know *everything* PRAW can do.**  
Go build something awesome! 🚀
