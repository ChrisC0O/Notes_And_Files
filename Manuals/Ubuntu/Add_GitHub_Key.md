Perfect! To clone your GitHub projects over SSH, you need to **generate an SSH key**, add it to GitHub, and then use the SSH URL. Here’s a step-by-step guide:

---

## **1️⃣ Generate a new SSH key**

Run this command:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

* `-t ed25519` → recommended modern key type
* `-C` → a comment (usually your email)

You’ll be asked for:

```
Enter file in which to save the key (/home/chris/.ssh/id_ed25519):
```

* Press **Enter** to accept the default path.

Optional: add a passphrase for extra security (recommended).

---

## **2️⃣ Start the SSH agent and add the key**

Start the agent:

```bash
eval "$(ssh-agent -s)"
```

Add your key:

```bash
ssh-add ~/.ssh/id_ed25519
```

---

## **3️⃣ Copy the public key**

Your public key is in:

```bash
~/.ssh/id_ed25519.pub
```

Copy it to the clipboard:

```bash
cat ~/.ssh/id_ed25519.pub
```

* Copy the entire line starting with `ssh-ed25519 ...`.

---

## **4️⃣ Add the key to GitHub**

1. Go to **GitHub → Settings → SSH and GPG keys**
2. Click **New SSH key**
3. Give it a name (e.g., “Ubuntu server”)
4. Paste the public key and save.

---

## **5️⃣ Test the connection**

```bash
ssh -T git@github.com
```

* If it works, GitHub should respond:

```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

---

## **6️⃣ Clone your repository**

Now you can clone using SSH:

```bash
git clone git@github.com:username/repo.git
```

* No password required (if you added a passphrase, you’ll enter that).

---

✅ **Tip:**

* Always use **SSH** for servers — easier than HTTPS with tokens.
* Make sure your `.ssh` folder permissions are correct:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

---

I can also give you a **one-liner that generates a key, adds it to the agent, and prints it for GitHub** — saves you a few manual steps.

Do you want me to do that?
