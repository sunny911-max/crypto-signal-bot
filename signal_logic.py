import requests
import numpy as np

def generate_signal(symbol="BTCUSDT", interval="1m", limit=100):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
        response = requests.get(url)
        data = response.json()

        if not isinstance(data, list) or len(data) < 15:
            return f"❌ Not enough data to analyze {symbol}"

        # Extract closing prices
        closes = [float(candle[4]) for candle in data]

        # RSI calculation
        deltas = np.diff(closes)
        seed = deltas[:14]
        up = seed[seed > 0].sum() / 14
        down = -seed[seed < 0].sum() / 14 if seed[seed < 0].sum() != 0 else 1e-10
        rs = up / down
        rsi = 100 - (100 / (1 + rs))

        # Debug line (optional): print(f"RSI: {rsi:.2f}")
        if rsi < 30:
            return f"📈 Potential BUY opportunity for {symbol} (RSI={rsi:.2f})"
        elif rsi > 70:
            return f"📉 Potential SELL warning for {symbol} (RSI={rsi:.2f})"
        else:
            return f"🤖 {symbol} RSI is {rsi:.2f} — No strong signal now."

    except Exception as e:
        return f"❌ Error generating signal: {str(e)}"
