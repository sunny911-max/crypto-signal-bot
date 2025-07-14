from flask import Flask
import threading
import time
from signal_logic import check_signals
from telegram_bot import send_telegram_message

app = Flask(__name__)

def run_bot_loop():
    while True:
        print("Checking for signals...")
        signal = check_signals()
        if signal:
            send_telegram_message(signal)
        time.sleep(30)

@app.route('/')
def home():
    return "Crypto signal bot is running!"

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot_loop)
    bot_thread.start()
    app.run(host='0.0.0.0', port=10000)
