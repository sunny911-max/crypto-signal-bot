import requests
import pandas as pd
import numpy as np
import datetime

def fetch_ohlc_data(coin_id='bitcoin', currency='usd', days=1):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        'vs_currency': currency,
        'days': days,
        'interval': 'hourly'
    }
    response = requests.get(url)
    data = response.json()

    if 'prices' not in data:
        print(f"❌ Unexpected data format for {coin_id}: {data}")
        return None

    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['price'] = df['price'].astype(float)
    return df

def calculate_rsi(df, period=14):
    delta = df['price'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def generate_signal(coin_id, threshold=30):
    df = fetch_ohlc_data(coin_id)
    if df is None or len(df) < 20:
        print(f"❌ Not enough data to analyze {coin_id}")
        return None

    rsi = calculate_rsi(df)
    latest_rsi = rsi.iloc[-1]
    price = df['price'].iloc[-1]

    if latest_rsi < threshold:
        return f"✅ Potential BUY opportunity for {coin_id.upper()} at ${price:.2f} (RSI: {latest_rsi:.2f})"
    else:
        print(f"ℹ️ {coin_id.upper()} RSI is {latest_rsi:.2f} — no signal.")
        return None

def check_signals():
    coin_list = ['bitcoin', 'ethereum', 'solana', 'dogecoin']
    signals = []

    for coin in coin_list:
        try:
            signal = generate_signal(coin)
            if signal:
                signals.append(signal)
        except Exception as e:
            print(f"❌ Error generating signal for {coin}: {e}")
    
    return signals
