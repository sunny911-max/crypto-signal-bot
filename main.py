from flask import Flask
import threading
import time
from signal_logic import generate_dummy_stats
from telegram_bot import send_telegram_message

app = Flask(__name__)

def run_bot_loop():
    while True:
        print("Checking for signals...")
        signal = generate_dummy_stats()
        print(f"📨 Sending signal:\n{signal}")
        try:
            send_telegram_message(signal)
        except Exception as e:
            print(f"❌ Error sending signal: {e}")
        time.sleep(30)  # Wait before checking again

@app.route('/')
def home():
    return "Crypto Signal Bot is running!"

if __name__ == '__main__':
    threading.Thread(target=run_bot_loop).start()
    app.run(host='0.0.0.0', port=10000)
