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

## 📦 Setup

```bash
git clone https://github.com/yourusername/cisco-honeypot.git
cd cisco-honeypot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

