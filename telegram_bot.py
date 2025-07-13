import requests
import traceback

BOT_TOKEN = "7750164805:AAE1H7HB5aeq5-a8onpZiIZ1PJM7SNGI1Po"
CHAT_ID = "7545235284"

def send_telegram_message(message):
    print("📨 Preparing to send message...")
    print(f"[TEST] Would send message: '{message}' to chat_id: {CHAT_ID} with token: {BOT_TOKEN}")
    try:
        response = requests.post(url, data=payload)
        print("📬 Telegram response status:", response.status_code)
        print("📬 Telegram response body:", response.text)
    except Exception as e:
        print("❌ Error sending message:", str(e))
        traceback.print_exc()
