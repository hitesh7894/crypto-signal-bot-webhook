import requests
import numpy as np
import pandas as pd

def fetch_ohlc(symbol, interval, limit=100):
    url = f"https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    data = requests.get(url, params=params).json()
    return [list(map(float, [i[1], i[2], i[3], i[4]])) for i in data]

def calculate_rsi(close, period=14):
    delta = np.diff(close)
    up = delta.clip(min=0)
    down = -delta.clip(max=0)
    rs = np.mean(up[-period:]) / np.mean(down[-period:] or [1])
    return 100 - 100 / (1 + rs)

def calculate_macd(close):
    exp1 = pd.Series(close).ewm(span=12).mean()
    exp2 = pd.Series(close).ewm(span=26).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9).mean()
    return macd.iloc[-1], signal.iloc[-1]

def supertrend(high, low, close, period=10, multiplier=3):
    atr = np.mean([h - l for h, l in zip(high[-period:], low[-period:])])
    hl2 = [(h + l) / 2 for h, l in zip(high, low)]
    final_ub = [hl2[i] + multiplier * atr for i in range(len(hl2))]
    final_lb = [hl2[i] - multiplier * atr for i in range(len(hl2))]
    st = "BUY" if close[-1] > final_lb[-1] else "SELL"
    return st

def get_indicators(symbol):
    try:
        data_15m = fetch_ohlc(symbol, "15m")
        data_1h = fetch_ohlc(symbol, "1h")
        close_15m = [i[3] for i in data_15m]
        close_1h = [i[3] for i in data_1h]
        high_15m = [i[1] for i in data_15m]
        low_15m = [i[2] for i in data_15m]

        rsi_15 = calculate_rsi(close_15m)
        rsi_1h = calculate_rsi(close_1h)
        macd_val, signal_val = calculate_macd(close_15m)
        trend = supertrend(high_15m, low_15m, close_15m)

        if rsi_15 < 30 and rsi_1h < 30 and macd_val > signal_val and trend == "BUY":
            entry = close_15m[-1]
            return f"🔔 STRONG BUY: {symbol}\nEntry: ${entry}\nReason: RSI < 30, MACD Bullish, Supertrend Green\nTimeframes: 15m ✅ 1h ✅"
    except:
        return None
