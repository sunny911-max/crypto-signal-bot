import time
from signal_logic import analyze_trade_opportunity
from telegram_bot import send_telegram_message

bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
chat_id = "YOUR_CHAT_ID"
tracked_coins = ["bitcoin", "ethereum", "dogecoin", "solana"]

def run_bot():
    sent_signals = set()

    while True:
        for coin in tracked_coins:
            try:
                signal = analyze_trade_opportunity(coin)
                if signal and signal not in sent_signals:
                    send_telegram_message(bot_token, chat_id, signal)
                    sent_signals.add(signal)
            except Exception as e:
                print(f"Error processing {coin}: {e}")
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    run_bot()
