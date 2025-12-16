# modules/indicators.py
import pandas as pd
import ta
import numpy as np

def calculate_technical_indicators(df):
    """DataFrame'e teknik indikatörleri ekler."""
    if df.empty: return df
    
    # Hareketli Ortalamalar
    for w in [5, 10, 20, 50, 100, 200]:
        df[f'MA_{w}'] = df['Close'].rolling(window=w).mean()
        df[f'EMA_{w}'] = df['Close'].ewm(span=w, adjust=False).mean()

    # RSI
    df['RSI_14'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    
    # MACD
    macd = ta.trend.MACD(df['Close'], window_slow=26, window_fast=12, window_sign=9)
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
    df['MACD_Hist'] = macd.macd_diff()
    
    # Bollinger Bands
    bollinger = ta.volatility.BollingerBands(close=df["Close"], window=20, window_dev=2)
    df["BB_High"] = bollinger.bollinger_hband()
    df["BB_Low"] = bollinger.bollinger_lband()
    df["BB_Mid"] = bollinger.bollinger_mavg()
    
    # Diğer İndikatörler
    df["STOCH(9,6)"] = ta.momentum.StochasticOscillator(df["High"], df["Low"], df["Close"], window=9, smooth_window=6).stoch()
    df["ADX(14)"] = ta.trend.ADXIndicator(df["High"], df["Low"], df["Close"]).adx()
    df["Williams %R"] = ta.momentum.WilliamsRIndicator(df["High"], df["Low"], df["Close"]).williams_r()
    df["CCI(14)"] = ta.trend.CCIIndicator(df["High"], df["Low"], df["Close"], window=14).cci()
    df["ATR(14)"] = ta.volatility.AverageTrueRange(df["High"], df["Low"], df["Close"], window=14).average_true_range()
    df["ATR%(14)"] = df["ATR(14)"] / df["Close"] * 100
    df["ROC"] = ta.momentum.ROCIndicator(df["Close"], window=12).roc()
    df["Ultimate Oscillator"] = ta.momentum.UltimateOscillator(df["High"], df["Low"], df["Close"]).ultimate_oscillator()
    df["MFI(14)"] = ta.volume.MFIIndicator(df["High"], df["Low"], df["Close"], df["Volume"], window=14).money_flow_index()
    df["Parabolic_SAR"] = ta.trend.PSARIndicator(df["High"], df["Low"], df["Close"]).psar()
    df["OBV"] = ta.volume.OnBalanceVolumeIndicator(df["Close"], df["Volume"]).on_balance_volume()
    df["VWAP"] = (df["Volume"] * (df["High"] + df["Low"] + df["Close"]) / 3).cumsum() / df["Volume"].cumsum()
    df["CMF"] = ta.volume.ChaikinMoneyFlowIndicator(df["High"], df["Low"], df["Close"], df["Volume"], window=20).chaikin_money_flow()

    # Ichimoku
    high9 = df["High"].rolling(window=9).max()
    low9 = df["Low"].rolling(window=9).min()
    df["Tenkan_Sen"] = (high9 + low9) / 2
    high26 = df["High"].rolling(window=26).max()
    low26 = df["Low"].rolling(window=26).min()
    df["Kijun_Sen"] = (high26 + low26) / 2
    high52 = df["High"].rolling(window=52).max()
    low52 = df["Low"].rolling(window=52).min()
    df["Senkou_Span_A"] = ((df["Tenkan_Sen"] + df["Kijun_Sen"]) / 2).shift(26)
    df["Senkou_Span_B"] = ((high52 + low52) / 2).shift(26)

    # --- PIVOT HESAPLAMALARI (Eksik Olan Kısım Eklendi) ---
    # Bir önceki günün verileri kullanılır
    prev_high = df['High'].shift(1)
    prev_low = df['Low'].shift(1)
    prev_close = df['Close'].shift(1)
    
    # 1. Klasik Pivotlar
    df['Pivot'] = (prev_high + prev_low + prev_close) / 3
    df['R1'] = 2 * df['Pivot'] - prev_low
    df['S1'] = 2 * df['Pivot'] - prev_high
    df['R2'] = df['Pivot'] + (prev_high - prev_low)
    df['S2'] = df['Pivot'] - (prev_high - prev_low)
    df['R3'] = prev_high + 2 * (df['Pivot'] - prev_low)
    df['S3'] = prev_low - 2 * (prev_high - df['Pivot'])

    # 2. Fibonacci Pivotlar
    fib_range = prev_high - prev_low
    df['Pivot_Fib'] = df['Pivot']
    df['R1_Fib'] = df['Pivot_Fib'] + 0.382 * fib_range
    df['S1_Fib'] = df['Pivot_Fib'] - 0.382 * fib_range
    df['R2_Fib'] = df['Pivot_Fib'] + 0.618 * fib_range
    df['S2_Fib'] = df['Pivot_Fib'] - 0.618 * fib_range
    df['R3_Fib'] = df['Pivot_Fib'] + 1.0 * fib_range
    df['S3_Fib'] = df['Pivot_Fib'] - 1.0 * fib_range
    
    return df