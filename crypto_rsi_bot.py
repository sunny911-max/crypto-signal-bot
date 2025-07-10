
import requests
import pandas as pd
from ta.momentum import RSIIndicator
from telegram import Bot

# === SETUP ===
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"        # Replace with your BotFather token
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"        # Replace with your Telegram chat ID
SYMBOL = "BTCUSDT"                        # Crypto pair
TIMEFRAME = "15m"
RSI_BUY = 30
RSI_SELL = 70

bot = Bot(token=TOKEN)

# === FUNCTION: Get live Binance candles ===
def get_klines(symbol, interval="15m", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close',
        'volume', 'close_time', 'quote_asset_volume',
        'num_trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    return df

# === FUNCTION: Check RSI + Volume signal ===
def check_rsi_volume_signal():
    df = get_klines(SYMBOL, TIMEFRAME)
    rsi = RSIIndicator(close=df['close'], window=14).rsi()
    last_rsi = rsi.iloc[-1]
    avg_volume = df['volume'][:-1].mean()
    last_volume = df['volume'].iloc[-1]

    # Confidence Score
    conf = 0
    if last_rsi < RSI_BUY:
        conf += 0.6
    if last_volume > avg_volume * 1.5:
        conf += 0.4

    confidence = round(conf * 100)

    if confidence >= 70:
        direction = "Buy" if last_rsi < RSI_BUY else "Sell"
        msg = f"""
🚨 {direction} Signal: {SYMBOL} ({TIMEFRAME})
📊 RSI = {round(last_rsi, 2)}
📈 Volume: {round(last_volume)} (+{round((last_volume/avg_volume)*100 - 100)}%)
✅ Confidence: {confidence}%

🔄 Entry Price: ${df['close'].iloc[-1]}
🧠 Reason: RSI {'oversold' if last_rsi < 30 else 'overbought'} + volume surge
        """
        bot.send_message(chat_id=CHAT_ID, text=msg)

# === MAIN RUN ===
if __name__ == "__main__":
    try:
        check_rsi_volume_signal()
    except Exception as e:
        bot.send_message(chat_id=CHAT_ID, text=f"Error: {str(e)}")
