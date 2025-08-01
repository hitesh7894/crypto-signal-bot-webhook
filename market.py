import requests

def get_market_summary():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    try:
        res = requests.get(url).json()
        coins = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'ADAUSDT', 'DOGEUSDT', 'DOTUSDT', 'MATICUSDT', 'LTCUSDT']
        summary = "📊 *Top 10 Coin Prices*\n"
        for coin in coins:
            data = next((item for item in res if item["symbol"] == coin), None)
            if data:
                price = float(data['lastPrice'])
                high = float(data['highPrice'])
                low = float(data['lowPrice'])
                dev_high = round((price - high) / high * 100, 2)
                dev_low = round((price - low) / low * 100, 2)
                summary += f"\n{coin[:-4]}: ${price:.2f} | 📈 {dev_high}% from High | 📉 {dev_low}% from Low"
        return summary
    except:
        return "⚠️ Error fetching market summary."
