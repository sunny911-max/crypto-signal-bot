from datetime import datetime
import random

def generate_dummy_stats():
    coins = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT', 'DOGE/USDT']
    coin = random.choice(coins)
    price = round(random.uniform(0.1, 50000), 2)
    rsi = round(random.uniform(10, 40), 1)
    volume = round(random.uniform(10, 200), 1)
    confidence = random.randint(60, 95)
    timestamp = datetime.utcnow().strftime("%H:%M UTC")

    message = (
        f"✅ Buy Signal for {coin}\n"
        f"🔸 Price: ${price}\n"
        f"📉 RSI: {rsi} (Oversold)\n"
        f"📈 Volume Surge: +{volume}%\n"
        f"🧠 Confidence: {confidence}%\n"
        f"⏱ Time: {timestamp}"
    )
    return message
