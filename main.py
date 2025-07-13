import time
from signal_logic import check_signals
from telegram_bot import send_telegram_message

def main():
    while True:
        signals = check_signals()
        for signal in signals:
            send_telegram_message(signal)
        time.sleep(60)

if __name__ == "__main__":
    main()