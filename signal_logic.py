import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO

def generate_candlestick_chart(symbol_id="bitcoin", vs_currency="usd"):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{symbol_id}/market_chart"
        params = {"vs_currency": vs_currency, "days": "1", "interval": "hourly"}
        response = requests.get(url, params=params)
        data = response.json()

        prices = data["prices"]  # list of [timestamp, price]
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)

        df["open"] = df["price"].shift(1)
        df["high"] = df["price"].rolling(window=2).max()
        df["low"] = df["price"].rolling(window=2).min()
        df["close"] = df["price"]
        df = df.dropna().tail(24)  # last 24 hourly candles

        fig, ax = plt.subplots(figsize=(8, 4))
        for i, (timestamp, row) in enumerate(df.iterrows()):
            color = "green" if row["close"] > row["open"] else "red"
            ax.plot([timestamp, timestamp], [row["low"], row["high"]], color="black")
            ax.plot([timestamp, timestamp], [row["open"], row["close"]], color=color, linewidth=6)

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.set_title(f"{symbol_id.upper()} 1H Candlestick Chart")
        plt.xticks(rotation=45)
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        plt.close()

        return buffer

    except Exception as e:
        print(f"Error generating chart for {symbol_id}: {e}")
        return None
