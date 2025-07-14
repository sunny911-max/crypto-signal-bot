import time
from signal_logic import check_signals
from telegram_bot import send_telegram_message
import threading
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

# Start thread
threading.Thread(target=run_bot_loop, daemon=True).start()

# Keep service alive
import web
