import requests
import numpy as np

def check_signals():
    symbol = "BTCUSDT"
    interval = "5m"
    limit = 100

    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)

    if response.status_code != 200:
        print("❌ Failed to fetch data")
        return None

    data = response.json()
    closes = np.array([float(entry[4]) for entry in data])

    # Calculate RSI
    deltas = np.diff(closes)
    seed = deltas[:14]
    up = seed[seed > 0].sum() / 14
    down = -seed[seed < 0].sum() / 14
    rs = up / down if down != 0 else 0
    rsi = 100 - (100 / (1 + rs))

    print(f"📊 RSI: {rsi:.2f}")

    if rsi < 30:
        return f"📈 RSI Alert! {symbol} has RSI < 30: {rsi:.2f}"

    return None
