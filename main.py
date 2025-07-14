import time
from signal_logic import check_signals
from telegram_bot import send_telegram_message
from flask import Flask

app = Flask(__name__)

def run_bot_loop():
    while True:
        print("Checking for signals...")
        signal = check_signals()
        if signal:
            print(f"📨 Sending signal: {signal}")
            send_telegram_message(signal)
        time.sleep(30)  # ✅ This line must align with the `if` block

@app.route('/')
def index():
    return "Bot is running"

if __name__ == '__main__':
    import threading
    threading.Thread(target=run_bot_loop).start()
    app.run(host='0.0.0.0', port=10000)
