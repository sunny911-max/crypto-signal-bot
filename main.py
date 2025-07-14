import threading
import time
from signal_logic import check_signals
from telegram_bot import send_telegram_message
from web import app
import traceback
import os

def run_bot_loop():
    try:
        while True:
            print("Checking for signals...")
            signals = check_signals()
            for signal in signals:
                print("Sending signal:", signal)
                send_telegram_message(signal)
            time.sleep(30)
    except Exception as e:
        print("❌ Exception in run_bot_loop:", e)
        traceback.print_exc()

# ✅ Start background thread
threading.Thread(target=run_bot_loop, daemon=True).start()

# ✅ Keep the app alive for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
