import random

def check_signals():
    # Simulate signal when random number is even
    if random.randint(1, 5) == 3:
        return "📈 RSI signal: Potential buy opportunity on $TEST"
    return None
