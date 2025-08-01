import requests
from indicator_utils import get_indicators

def get_market_summary():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10, "page": 1}
    try:
        data = requests.get(url, params=params).json()
        summary = "📊 *Top 10 Coin Summary*\n"
        for coin in data:
            current = coin["current_price"]
            high = coin["high_24h"]
            low = coin["low_24h"]
            symbol = coin["symbol"].upper()
            down = round((high - current) / high * 100, 2)
            up = round((current - low) / low * 100, 2)
            summary += f"{symbol}: ${current} | 🔼 -{down}% from High | 🔽 +{up}% from Low\n"
        return summary
    except:
        return "⚠️ Failed to fetch market data."

def get_live_signals():
    coins = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", "DOTUSDT", "LTCUSDT", "MATICUSDT"]
    signals = []
    for symbol in coins:
        signal = get_indicators(symbol)
        if signal: signals.append(signal)
    return "\n\n".join(signals)
