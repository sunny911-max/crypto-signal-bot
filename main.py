import time
from signal_logic import analyze_trade_opportunity, generate_candlestick_chart
from telegram_bot import send_telegram_message, send_chart_to_telegram

# ✅ Add your desired coins here (CoinGecko IDs)
coin_list = [
    {"id": "bitcoin", "symbol": "BTC"},
    {"id": "ethereum", "symbol": "ETH"},
    {"id": "solana", "symbol": "SOL"},
    # You can add more like:
    # {"id": "dogecoin", "symbol": "DOGE"},
    # {"id": "cardano", "symbol": "ADA"},
]

# 🔄 Store last signal per coin to avoid duplicates
last_signals = {}

def run_sniper_bot():
    print("🎯 Multi-Coin Sniper Bot Activated")

    while True:
        try:
            for coin in coin_list:
                symbol_id = coin["id"]
                symbol_name = coin["symbol"]
                print(f"🔍 Scanning {symbol_name}...")

                # Analyze opportunity
                signal_message = analyze_trade_opportunity(symbol_id=symbol_id, vs_currency="usd")

                # Only send if new opportunity
                if signal_message and signal_message != last_signals.get(symbol_id):
                    print(f"✅ Signal found for {symbol_name}! Sending...")
                    send_telegram_message(signal_message)

                    # Send candlestick chart
                    chart_buffer = generate_candlestick_chart(symbol_id=symbol_id)
                    if chart_buffer:
                        send_chart_to_telegram(chart_buffer)

                    # Update last signal
                    last_signals[symbol_id] = signal_message
                else:
                    print(f"🕵️ No new sniper signal for {symbol_name}")

        except Exception as e:
            print(f"⚠️ Error: {e}")

        time.sleep(10)  # Repeat every 10 seconds

if __name__ == "__main__":
    run_sniper_bot()
