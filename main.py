from flask import Flask
import threading
import time
from signal_logic import check_signals
from telegram_bot import send_telegram_message

app = Flask(__name__)

def run_bot_loop():
    while True:
        print("Checking for signals...")
        # Temporarily always send a message for testing
        send_telegram_message("✅ Test signal: Bot is running successfully.")
        time.sleep(30)  # ⬅️ Correctly indented under `while`

@app.route('/')
def home():
    return "Crypto signal bot is running!"

if __name__ == '__main__':
    # Start bot loop in background
    bot_thread = threading.Thread(target=run_bot_loop)
    bot_thread.start()

    # Run Flask app
    app.run(host='0.0.0.0', port=10000)
