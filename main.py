from signal_logic import check_signals

def run_bot_loop():
    while True:
        print("📡 Checking for signals...")
        try:
            signals = check_signals()
            for signal in signals:
                print(f"📨 {signal}")
                send_telegram_message(signal)
        except Exception as e:
            print(f"❌ Error: {e}")
        time.sleep(60)
