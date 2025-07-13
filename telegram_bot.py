import os
import requests

BOT_TOKEN = os.getenv("7307067620:AAEOHrNskxLEWOcMKvuKtVbrJUYpD0zokMA")
CHAT_ID = os.getenv("HighRisk_scalper_bot")

def send_telegram_message(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("BOT_TOKEN or CHAT_ID not set.")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Failed to send message:", e)
