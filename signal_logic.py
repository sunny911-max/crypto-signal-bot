import requests
import numpy as np

def get_klines(symbol, interval='1m', limit=100):
    url = f"https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(url, params=params)
    return response.json()

def calculate_rsi(prices, period=14):
    deltas = np.diff(prices)
    seed = deltas[:period]
    up = seed[seed > 0].sum() / period
    down = -seed[seed < 0].sum() / period if len(seed[seed < 0]) > 0 else 0.001
    rs = up / down
    return 100 - (100 / (1 + rs))

def check_signals():
    signals = []
    coins = ["BTCUSDT", "ETHUSDT"]

    for symbol in coins:
        try:
            data = get_klines(symbol)
            close_prices = [float(candle[4]) for candle in data]
            rsi = calculate_rsi(close_prices[-15:])

            if rsi < 60:
                signals.append(f"🟢 [BUY TEST] {symbol}\nRSI: {rsi:.2f}")
            elif rsi > 40:
                signals.append(f"🔴 [SELL TEST] {symbol}\nRSI: {rsi:.2f}")
        except Exception as e:
            print(f"❌ Error with {symbol}: {e}")
    
    return signals
