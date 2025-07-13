def send_telegram_message(message):
    print("📨 Preparing to send message...")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    print("✅ [TEST MODE] Sending to:", url)
    print("📦 Payload:", payload)

    # Simulate success
    print("📬 Telegram response status: 200")
    print("📬 Telegram response body: {\"ok\":true, \"result\":{\"message_id\":123}}")
