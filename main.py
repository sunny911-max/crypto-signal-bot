import threading
import time
from flask import Flask
from signal_logic import generate_signal
from telegram_bot import send_telegram_message

app = Flask(__name__)

def run_bot_loop():
    while True:
        print("✅ Checking for signals...")
        signal = generate_signal("BTCUSDT")  # You can change this to other symbols like ETHUSDT
        print(f"📨 Signal: {signal}")
        send_telegram_message(signal)
        time.sleep(30)  # Wait 30 seconds before checking again

@app.route('/')
def home():
    return "✅ Crypto Signal Bot is running!"

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot_loop)
    bot_thread.start()
    app.run(host='0.0.0.0', port=10000)
