import time
from signal_logic import check_signals
from telegram_bot import send_telegram_message
import threading

def run_bot_loop():
    while True:
        print("Checking for signals...")
        signals = check_signals()
        for signal in signals:
            print("Sending signal:", signal)
            send_telegram_message(signal)
        time.sleep(30)

threading.Thread(target=run_bot_loop, daemon=True).start()