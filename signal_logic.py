import requests
import numpy as np

def get_klines(symbol="BTCUSDT", interval="1m", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    closes = [float(candle[4]) for candle in data]
    return closes

def calculate_rsi(closes, period=14):
    if len(closes) < period:
        return 50
    deltas = np.diff(closes)
    gains = deltas[deltas > 0].sum() / period
    losses = -deltas[deltas < 0].sum() / period
    if losses == 0:
        return 100
    rs = gains / losses
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)

def generate_signal(symbol="BTCUSDT"):
    try:
        closes = get_klines(symbol)
        rsi = calculate_rsi(closes)
        price = closes[-1]
        signal = None

        if rsi < 30:
            signal = f"📉 *Buy signal for* ${symbol}\nPrice: ${price:.2f}\nRSI: {rsi} (Oversold)"
        elif rsi > 70:
            signal = f"📈 *Sell signal for* ${symbol}\nPrice: ${price:.2f}\nRSI: {rsi} (Overbought)"
        else:
            signal = f"⚠️ *Neutral for* ${symbol}\nPrice: ${price:.2f}\nRSI: {rsi}"

        return signal
    except Exception as e:
        return f"❌ Error generating signal: {e}"
