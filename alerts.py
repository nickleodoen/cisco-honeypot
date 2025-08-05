import os
import requests
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_alert(message):
    if not SLACK_WEBHOOK_URL:
        print("[!] No SLACK_WEBHOOK_URL found in .env")
        return

    try:
        payload = {"text": message}
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"[!] Alert failed: {e}")