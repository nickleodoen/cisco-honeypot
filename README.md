# 🛡️ Cisco SSH Honeypot

A simple fake SSH server that simulates a Cisco router CLI, logs attacker commands, and sends real-time Slack alerts.

## 🚀 Features
- Simulates Cisco IOS CLI: `Router>`, `enable`, `show version`, etc.
- Logs all SSH login attempts and commands
- Sends Slack alerts for logins and commands
- Easy to customize, Dockerizable, and extendable

## ⚙️ Requirements

- Python 3.7+
- `asyncssh`, `requests`, `python-dotenv`

```bash
pip install asyncssh
pip install requests
pip install python-dotenv
```
---

## 📦 Setup

### 1. Clone the repository

```bash
git clone https://github.com/nickleodoen/cisco-honeypot.git
cd cisco-honeypot
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


### 3. Generate a host SSH key

```bash
ssh-keygen -f ssh_host_key -N ''
```


### 4. 🔐 Slack Webhook Setup

Create a .env file in the project directory

```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/your/actual/webhook
```

Make sure .env is listed in .gitignore so it doesn't get pushed

### 5. ▶️ Run the Honeypot

```bash
python honeypot.py
```

You should see

```bash
SSH honeypot running on port 2222...
```

### 6. 🧪 Test the Honeypot

In another terminal:

```bash
ssh -p 2222 attacker@localhost
```

- Use any password (it will be accepted)
- Try Fake Cisco commands

```bash
show version
enable
show running-config
exit
```

### Check:
- Slack for real-time alerts
