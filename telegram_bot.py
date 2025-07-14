import threading
import time
from signal_logic import check_signals
from web import app  # your Flask app

import traceback

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

# ✅ Keep the app alive on Render (port 10000 or dynamic)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
