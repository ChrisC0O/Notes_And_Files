# Guide to Creating and Controlling a Reddit Bot Using PRAW

This guide will walk you through creating a **Reddit bot** using **PRAW** (Python Reddit API Wrapper), the official Python library for interacting with Reddit's API.

---

## Prerequisites

1. **Python 3.6+** installed
2. A **Reddit account** (for the bot)
3. Basic knowledge of Python
4. `pip` (Python package manager)

---

## Step 1: Install PRAW

```bash
pip install praw
```

---

## Step 2: Create a Reddit App (OAuth Credentials)

1. Go to: [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. Scroll down and click **"create app"** or **"create another app"**
3. Fill in:
   - **Name**: `MyRedditBot`
   - **App type**: Select **script**
   - **Description**: (optional)
   - **About URL**: (optional)
   - **Redirect URI**: `http://localhost:8080`
4. Click **create app**

After creation, you’ll see:
- `client_id` → (14-character string under the app name)
- `client_secret` → (longer string)
- Your bot’s **username** and **password**

> **Never share these credentials publicly!**

---

## Step 3: Set Up Your Script

Create a file called `bot.py`:

```python
import praw

# Initialize the Reddit instance
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="my_reddit_bot v1.0 (by u/YOUR_REDDIT_USERNAME)",
    username="YOUR_BOT_USERNAME",
    password="YOUR_BOT_PASSWORD"
)

# Test connection
print(f"Logged in as: {reddit.user.me()}")
```

> Replace placeholders with your actual credentials.

---

## Step 4: Basic Bot Actions

### 1. Read New Posts in a Subreddit

```python
subreddit = reddit.subreddit("learnpython")

for submission in subreddit.new(limit=5):
    print(f"Title: {submission.title}")
    print(f"Score: {submission.score}")
    print(f"URL: {submission.url}")
    print("-" * 50)
```

---

### 2. Reply to Posts

```python
for submission in subreddit.new(limit=10):
    if "help" in submission.title.lower() and not submission.saved:
        submission.reply("Hello! I'm a bot. I saw you're asking for help. Good luck! 🤖")
        print(f"Replied to: {submission.title}")
        submission.save()  # Mark as processed
```

> Use `submission.saved` to avoid replying multiple times.

---

### 3. Reply to Comments

```python
for comment in subreddit.stream.comments(skip_existing=True):
    if "praw" in comment.body.lower():
        comment.reply("PRAW is awesome! You're using the best Reddit API wrapper. 🚀")
        print(f"Replied to comment by u/{comment.author}")
```

---

### 4. Upvote/Downvote

```python
submission = reddit.submission(url="https://www.reddit.com/r/test/comments/abc123/")
submission.upvote()
# submission.downvote()
# submission.clear_vote()
```

---

### 5. Submit a Post

```python
subreddit = reddit.subreddit("test")
subreddit.submit(
    title="Hello from my bot!",
    selftext="This post was made by a Python bot using PRAW."
)
```

---

## Step 5: Avoid Getting Banned (Rate Limits & Rules)

Reddit enforces **rate limits**: ~1 request per second.

Use `time.sleep()` or PRAW’s built-in rate limiting:

```python
import time

for submission in subreddit.new(limit=25):
    print(submission.title)
    time.sleep(2)  # Be respectful
```

### Best Practices:
- Don’t spam
- Don’t reply to the same post twice
- Respect `robots.txt` and subreddit rules
- Use `skip_existing=True` in streams
- Log actions to avoid duplicates

---

## Step 6: Advanced: Run Bot Continuously

```python
import praw
import time

reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="my_bot v1.0",
    username="YOUR_BOT_USERNAME",
    password="YOUR_BOT_PASSWORD"
)

print("Bot is running...")

subreddit = reddit.subreddit("test")

while True:
    try:
        for comment in subreddit.stream.comments(skip_existing=True):
            if "hello bot" in comment.body.lower():
                comment.reply("Hi there! I'm alive! 👋")
                print(f"Replied to u/{comment.author}")
        time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
```

> Press `Ctrl+C` to stop.

---

## Step 7: Store Credentials Securely (Optional)

Use environment variables:

```bash
export REDDIT_CLIENT_ID="your_id"
export REDDIT_CLIENT_SECRET="your_secret"
export REDDIT_USERNAME="your_bot"
export REDDIT_PASSWORD="your_pass"
```

Then in Python:

```python
import os
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent="my_bot v1.0"
)
```

---

## Example: Auto-Responder Bot

```python
import praw
import time

reddit = praw.Reddit(
    client_id="xxx",
    client_secret="xxx",
    username="MyBotAccount",
    password="xxx",
    user_agent="AutoHelpBot v1.0 by u/YourName"
)

subreddit = reddit.subreddit("learnpython")

print("Bot started...")

for comment in subreddit.stream.comments(skip_existing=True):
    if "how to install" in comment.body.lower() and not comment.saved:
        reply = ("To install a Python package, use:\n\n"
                 "```bash\npip install package_name\n```\n\n"
                 "Make sure you're in the correct environment!")
        comment.reply(reply)
        comment.save()
        print(f"Helped u/{comment.author}")
    time.sleep(1)
```

---

## Useful PRAW Links

- Documentation: [https://praw.readthedocs.io](https://praw.readthedocs.io)
- GitHub: [https://github.com/reddit-archive/reddit](https://github.com/reddit-archive/reddit) (PRAW is separate)
- Reddit API Rules: [https://www.reddit.com/dev/api](https://www.reddit.com/dev/api)

---

## Final Tips

- Test in `r/yourusername` or `r/test`
- Read subreddit rules before posting
- Add logging
- Handle exceptions
- Never hardcode credentials in shared code

---

**You're now ready to build powerful Reddit bots with PRAW!** 🤖

Let me know what kind of bot you want to build — I can help customize it!
