import requests
import pandas as pd
import ta

def fetch_candles(symbol, interval='15m', limit=100):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    res = requests.get(url).json()
    df = pd.DataFrame(res, columns=['time','open','high','low','close','vol','c1','c2','c3','c4','c5'])
    df['close'] = pd.to_numeric(df['close'])
    return df

def get_live_signals():
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT']
    final_signals = ""
    for sym in symbols:
        df = fetch_candles(sym, '15m')
        if df is None or df.empty: continue
        try:
            rsi = ta.momentum.RSIIndicator(df['close'], 14).rsi().iloc[-1]
            macd = ta.trend.MACD(df['close']).macd_diff().iloc[-1]
            supertrend = ta.trend.STCIndicator(df['close']).stc().iloc[-1]
            stochrsi = ta.momentum.StochRSIIndicator(df['close']).stochrsi_k().iloc[-1]

            if rsi < 30 and macd > 0 and stochrsi < 20:
                final_signals += f"✅ STRONG BUY: {sym[:-4]}\n"
            elif rsi > 70 and macd < 0 and stochrsi > 80:
                final_signals += f"🔴 STRONG SELL: {sym[:-4]}\n"
        except:
            continue
    return final_signals or "No signal right now"

