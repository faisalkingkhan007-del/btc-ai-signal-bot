
import json
import time
import urllib.request

API = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"

def get_btc_data():
    req = urllib.request.Request(
        API,
        headers={"User-Agent": "BTC-Signal-Bot"}
    )

    with urllib.request.urlopen(req, timeout=15) as response:
        data = json.loads(response.read().decode())

    closes = [float(candle[4]) for candle in data]
    price = closes[-1]

    changes = [
        closes[i] - closes[i - 1]
        for i in range(1, len(closes))
    ]

    gains = [max(x, 0) for x in changes[-14:]]
    losses = [max(-x, 0) for x in changes[-14:]]

    avg_gain = sum(gains) / 14
    avg_loss = sum(losses) / 14

    if avg_loss == 0:
        rsi = 100 if avg_gain > 0 else 50
    else:
        rsi = 100 - (100 / (1 + avg_gain / avg_loss))

    sma = sum(closes[-20:]) / 20

    if rsi < 30 and price > sma:
        signal = "Potential bullish setup"
    elif rsi > 70 and price < sma:
        signal = "Potential bearish setup"
    else:
        signal = "Neutral - Wait"

    print("=" * 35)
    print("BTC AI SIGNAL BOT")
    print("BTC Price:", price)
    print("RSI:", round(rsi, 2))
    print("SMA 20:", round(sma, 2))
    print("Signal:", signal)
    print("=" * 35)


if __name__ == "__main__":
    while True:
        try:
            get_btc_data()
        except Exception as error:
            print("Error:", error)

        time.sleep(300)
