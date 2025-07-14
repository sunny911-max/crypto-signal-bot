import requests
import pandas as pd
import numpy as np

def fetch_price_history(symbol, days=1, interval='hourly'):
    url = f'https://api.coingecko.com/api/v3/coins/{symbol}/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': days,
        'interval': interval
    }
    response = requests.get(url, params=params)
    data = response.json()
    prices = data.get('prices', [])
    if not prices or len(prices) < 15:
        return None
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['price'] = df['price'].astype(float)
    return df

def compute_rsi(data, period=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def check_signals():
    symbols = {
        'bitcoin': 'BTC',
        'ethereum': 'ETH',
        'solana': 'SOL'
    }
    results = []

    for coingecko_id, symbol in symbols.items():
        df = fetch_price_history(coingecko_id)
        if df is None or df.empty:
            results.append(f"❌ Not enough data for {symbol}")
            continue

        df['rsi'] = compute_rsi(df['price'])
        latest_rsi = df['rsi'].iloc[-1]

        if latest_rsi < 30:
            results.append(f"✅ Potential BUY signal for {symbol} | RSI: {latest_rsi:.2f}")
        elif latest_rsi > 70:
            results.append(f"🔻 Overbought {symbol} | RSI: {latest_rsi:.2f}")
        else:
            results.append(f"📉 Neutral {symbol} | RSI: {latest_rsi:.2f}")

    return results
