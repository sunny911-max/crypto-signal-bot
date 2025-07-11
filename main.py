
from flask import Flask, jsonify
import requests
import pandas as pd
import ta

app = Flask(__name__)

def get_rsi_signal(symbol="BTCUSDT", interval="15m", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])
    df["close"] = pd.to_numeric(df["close"])
    rsi = ta.momentum.RSIIndicator(df["close"], window=14).rsi()
    latest_rsi = rsi.iloc[-1]

    if latest_rsi < 30:
        return {"signal": "Oversold ✅", "rsi": round(latest_rsi, 2)}
    elif latest_rsi > 70:
        return {"signal": "Overbought ⚠️", "rsi": round(latest_rsi, 2)}
    else:
        return {"signal": "Neutral", "rsi": round(latest_rsi, 2)}

@app.route("/")
def home():
    return "🟢 Crypto RSI Signal Bot"

@app.route("/signal")
def signal():
    result = get_rsi_signal()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
