import time
import threading
from telegram_bot import send_telegram_message
from signal_logic import check_signals

def run_bot_loop():
    while True:
        print("📡 Checking for signals...")
        try:
            signals = check_signals()
            for signal in signals:
                print(f"📨 {signal}")
                send_telegram_message(signal)
        except Exception as e:
            print(f"❌ Error: {e}")
        time.sleep(60)

# 🟢 Start the bot loop in a thread
if __name__ == '__main__':
    thread = threading.Thread(target=run_bot_loop)
    thread.start()

    # Flask web server
    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Crypto Signal Bot is running!"

    app.run(host='0.0.0.0', port=10000)
