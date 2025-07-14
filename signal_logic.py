import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO


def analyze_trade_opportunity(symbol_id="bitcoin", vs_currency="usd"):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{symbol_id}/market_chart"
        params = {"vs_currency": vs_currency, "days": "1", "interval": "minute"}
        response = requests.get(url, params=params)
        data = response.json()

        prices = data["prices"]
        volumes = data["total_volumes"]

        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["volume"] = [v[1] for v in volumes]
        df["price"] = df["price"].astype(float)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

        last_price = df["price"].iloc[-1]
        old_price = df["price"].iloc[-61] if len(df) > 61 else df["price"].iloc[0]
        price_change = ((last_price - old_price) / old_price) * 100

        df["delta"] = df["price"].diff()
        df["gain"] = df["delta"].apply(lambda x: x if x > 0 else 0)
        df["loss"] = df["delta"].apply(lambda x: -x if x < 0 else 0)
        avg_gain = df["gain"].rolling(window=14).mean().iloc[-1]
        avg_loss = df["loss"].rolling(window=14).mean().iloc[-1]
        rs = avg_gain / avg_loss if avg_loss != 0 else 1
        rsi = 100 - (100 / (1 + rs))

        avg_volume = df["volume"].rolling(window=30).mean().iloc[-1]
        current_volume = df["volume"].iloc[-1]
        volume_spike = current_volume / avg_volume if avg_volume else 1

        confidence = 0
        reason = ""

        if rsi < 30:
            confidence += 30
            reason += f"RSI={rsi:.2f} (Oversold)\n"
        elif rsi > 70:
            confidence += 30
            reason += f"RSI={rsi:.2f} (Overbought)\n"

        if volume_spike > 1.8:
            confidence += 30
            reason += f"Volume spike: {current_volume/1e6:.2f}M (avg {avg_volume/1e6:.2f}M)\n"

        if abs(price_change) >= 1.2:
            confidence += 20
            reason += f"Price moved {price_change:+.2f}% in last hour\n"

        if confidence >= 70:
            signal_type = "BUY" if rsi < 30 else "SELL"
            return (
                f"🚨 Trade Opportunity: {symbol_id.upper()}/USDT\n\n"
                f"📈 Signal: *{signal_type}*\n"
                f"{reason}"
                f"📊 Confidence Score: {confidence} / 100\n"
                f"🕒 Timeframe: 1h"
            )
        else:
            return None

    except Exception as e:
        print(f"Error analyzing {symbol_id}: {e}")
        return None


def generate_candlestick_chart(symbol_id="bitcoin", vs_currency="usd"):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{symbol_id}/market_chart"
        params = {"vs_currency": vs_currency, "days": "1", "interval": "hourly"}
        response = requests.get(url, params=params)
        data = response.json()

        prices = data["prices"]
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)

        df["open"] = df["price"].shift(1)
        df["high"] = df["price"].rolling(window=2).max()
        df["low"] = df["price"].rolling(window=2).min()
        df["close"] = df["price"]
        df = df.dropna().tail(24)

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
