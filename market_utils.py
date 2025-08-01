# market_utils.py
import requests

def get_market_summary():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false"
    }

    try:
        res = requests.get(url, params=params)
        coins = res.json()

        msg = "📊 *Top 10 Coins Market Snapshot:*\n"
        for coin in coins:
            name = coin["symbol"].upper()
            price = coin["current_price"]
            high = coin["high_24h"]
            low = coin["low_24h"]

            deviation_high = round((price - high) / high * 100, 2)
            deviation_low = round((price - low) / low * 100, 2)

            msg += (
                f"\n{name} - ${price}\n"
                f"📈 High: {high} ({deviation_high}%)\n"
                f"📉 Low: {low} ({deviation_low}%)\n"
            )

        return msg
    except Exception as e:
        return f"❌ Error fetching data: {e}"
