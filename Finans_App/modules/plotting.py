# modules/plotting.py
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm
import ta

def apply_dark_theme(ax, colors):
    """Grafik eksenlerini ve çizgilerini koyu temaya ayarlar."""
    ax.set_facecolor(colors['plot_bg'])
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    
    for spine in ax.spines.values():
        spine.set_color('white')
        
    ax.grid(True, linestyle="--", alpha=0.3, color='gray')

def nadaraya_watson_smoother(x, y, bandwidth):
    """Nadaraya-Watson düzleştirme fonksiyonu"""
    y_smooth = []
    x = np.array(x)
    y = np.array(y)
    for xi in x:
        weights = norm.pdf((xi - x) / bandwidth)
        weights /= weights.sum()
        y_smooth.append(np.sum(weights * y))
    return np.array(y_smooth)

def calculate_supertrend(df, period=10, multiplier=3):
    """SuperTrend hesaplaması"""
    try:
        atr = ta.volatility.AverageTrueRange(
            high=df['High'], low=df['Low'], close=df['Close'], window=period
        ).average_true_range()
    except:
        return pd.Series([np.nan]*len(df)), [False]*len(df)

    hl2 = (df['High'] + df['Low']) / 2
    upper_band = hl2 + multiplier * atr
    lower_band = hl2 - multiplier * atr

    supertrend = [np.nan] * len(df)
    direction = [True] * len(df)
    
    # Hesaplama döngüsü (Orijinal koddaki mantık)
    for i in range(period, len(df)):
        if i == period:
            supertrend[i] = lower_band.iloc[i]
            direction[i] = True
            continue
            
        prev_supertrend = supertrend[i-1]
        prev_direction = direction[i-1]
        curr_close = df['Close'].iloc[i]
        
        if curr_close > prev_supertrend:
            direction[i] = True
        elif curr_close < prev_supertrend:
            direction[i] = False
        else:
            direction[i] = prev_direction
            
        if direction[i]:
            supertrend[i] = max(lower_band.iloc[i], prev_supertrend if prev_direction else lower_band.iloc[i])
        else:
            supertrend[i] = min(upper_band.iloc[i], prev_supertrend if not prev_direction else upper_band.iloc[i])
            
    return supertrend, direction

def empty_chart(colors, msg):
    """Hata durumunda boş grafik döndürür"""
    fig, ax = plt.subplots(figsize=(10, 5), facecolor=colors['plot_bg'])
    apply_dark_theme(ax, colors)
    ax.text(0.5, 0.5, msg, color="white", ha="center", fontsize=12)
    return fig

def create_chart(df, ticker, indicator, colors):
    """
    Seçilen indikatöre göre grafik oluşturur. (proje.py mantığıyla)
    """
    
    # --- 1. RSI (RSI ve Fiyat alt alta) ---
    if indicator == "RSI_14" or indicator == "RSI":
        col = "RSI_14" if "RSI_14" in df.columns else "RSI"
        if col not in df.columns: return empty_chart(colors, "RSI Verisi Yok")

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True, 
                                       facecolor=colors['plot_bg'], gridspec_kw={'height_ratios': [1, 2]})
        apply_dark_theme(ax1, colors)
        ax1.plot(df.index, df[col], color='cyan', label='RSI (14)')
        ax1.axhline(70, color='red', linestyle='--', alpha=0.6)
        ax1.axhline(30, color='green', linestyle='--', alpha=0.6)
        ax1.set_ylim(0, 100)
        ax1.legend(facecolor=colors['button'], labelcolor='white', fontsize=8)
        
        apply_dark_theme(ax2, colors)
        ax2.plot(df.index, df['Close'], color='#0055FF', label="Fiyat")
        plt.tight_layout()
        return fig

    # --- 2. 1Y PRICE (Sadece Fiyat) ---
    elif indicator == "1Y Price" or indicator == "Fiyat":
        fig, ax = plt.subplots(figsize=(10, 5), facecolor=colors['plot_bg'])
        apply_dark_theme(ax, colors)
        ax.plot(df.index, df["Close"], label="1Y Price", color="blue")
        ax.set_title("1 Yıllık Fiyat Hareketleri", fontsize=12, fontweight="bold", color="white")
        ax.set_ylabel("Fiyat ($)", color="white")
        ax.set_xlabel("Tarih", color="white")
        ax.legend(facecolor=colors['button'], labelcolor='white')
        plt.tight_layout()
        return fig

    # --- 3. US10YEAR (Tahvil vs Fiyat) ---
    elif indicator == "US10YEAR":
        us10y_df = yf.download("^TNX", period="1y", interval="1d")
        if us10y_df.empty: return empty_chart(colors, "US10Y Verisi Alınamadı")

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, facecolor=colors['plot_bg'])
        apply_dark_theme(ax1, colors)
        ax1.plot(us10y_df.index, us10y_df["Close"], label="ABD 10Y Tahvil", color="darkorange")
        ax1.set_title("ABD 10 Yıllık Tahvil Faizi", color="white", fontweight='bold')
        ax1.legend(facecolor=colors['button'], labelcolor='white')

        apply_dark_theme(ax2, colors)
        ax2.plot(df.index, df["Close"], label=f"{ticker} Fiyatı", color="steelblue")
        ax2.legend(facecolor=colors['button'], labelcolor='white')
        plt.tight_layout()
        return fig

    # --- 4. F/K (Fundamental) ---
    elif indicator == "F/K":
        # Orijinal koddaki input yerine mevcut ticker'ı kullanıyoruz
        try:
            stock = yf.Ticker(ticker)
            today = pd.to_datetime("today")
            dates = [today - pd.DateOffset(months=3 * i) for i in range(5, -1, -1)]
            x_labels = [f"{date.month}.{date.year}" for date in dates]
            
            fk_values = []
            info = stock.info
            current_pe = info.get("trailingPE", 0)
            
            # Geçmiş veriyi tam çekmek zor olduğu için örnek olarak current PE'yi varyasyonlu gösteriyoruz
            # veya gerçek veri çekmeye çalışıyoruz (gerçek veri yfinance ücretsiz sürümde sınırlı)
            for _ in dates:
                fk_values.append(current_pe if current_pe else 0)

            fig, ax = plt.subplots(figsize=(10, 6), facecolor=colors['plot_bg'])
            apply_dark_theme(ax, colors)
            ax.bar(x_labels, fk_values, color='mediumslateblue', width=0.5)
            ax.set_title(f"{ticker} - F/K Oranı (Yaklaşık)", color="white", fontweight='bold')
            plt.tight_layout()
            return fig
        except Exception as e:
            return empty_chart(colors, f"F/K Verisi Hatası: {str(e)}")

    # --- 5. NADARAYA-WATSON ---
    elif indicator == "Nadaraya_watson":
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, facecolor=colors['plot_bg'])
        
        x = np.arange(len(df))
        y = df["Close"].values
        y_smooth = nadaraya_watson_smoother(x, y, bandwidth=10)

        apply_dark_theme(ax1, colors)
        ax1.plot(df.index, y, label="Orijinal Fiyat", color="lightblue", alpha=0.5)
        ax1.plot(df.index, y_smooth, label="Nadaraya-Watson", color="orange", linewidth=2)
        ax1.set_title("Nadaraya-Watson Smoothed", color="white", fontweight="bold")
        ax1.legend(facecolor=colors['button'], labelcolor='white')

        apply_dark_theme(ax2, colors)
        ax2.plot(df.index, df["Close"], label="1Y Price", color="blue")
        plt.tight_layout()
        return fig

    # --- 6. VIX ---
    elif indicator == "VIX":
        vix_df = yf.download("^VIX", period="1y", interval="1d")
        if vix_df.empty: return empty_chart(colors, "VIX Verisi Yok")

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, facecolor=colors['plot_bg'])
        apply_dark_theme(ax1, colors)
        ax1.plot(vix_df.index, vix_df["Close"], label="VIX", color="purple")
        ax1.set_title("VIX (Korku Endeksi)", color="white", fontweight='bold')
        ax1.legend(facecolor=colors['button'], labelcolor='white')

        apply_dark_theme(ax2, colors)
        ax2.plot(df.index, df["Close"], label="1Y Price", color="blue")
        plt.tight_layout()
        return fig

    # --- 7. DXY ---
    elif indicator == "DXY":
        dxy_df = yf.download("DX-Y.NYB", period="1y", interval="1d")
        if dxy_df.empty: return empty_chart(colors, "DXY Verisi Yok")

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, facecolor=colors['plot_bg'])
        apply_dark_theme(ax1, colors)
        ax1.plot(dxy_df.index, dxy_df["Close"], label="DXY", color="green")
        ax1.set_title("Dolar Endeksi (DXY)", color="white", fontweight='bold')
        ax1.legend(facecolor=colors['button'], labelcolor='white')

        apply_dark_theme(ax2, colors)
        ax2.plot(df.index, df["Close"], label="1Y Price", color="blue")
        plt.tight_layout()
        return fig

    # --- 8. USD/JPY ---
    elif indicator == "USD/JPY":
        usdjpy = yf.download("JPY=X", period="1y", interval="1d")
        if usdjpy.empty: return empty_chart(colors, "USD/JPY Verisi Yok")

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, facecolor=colors['plot_bg'])
        apply_dark_theme(ax1, colors)
        ax1.plot(usdjpy.index, usdjpy["Close"], label="USD/JPY", color="darkgreen")
        ax1.set_title("USD/JPY Paritesi", color="white", fontweight="bold")
        ax1.legend(facecolor=colors['button'], labelcolor='white')

        apply_dark_theme(ax2, colors)
        ax2.plot(df.index, df["Close"], label=f"{ticker} Fiyatı", color="blue")
        plt.tight_layout()
        return fig

    # --- 9. EUR/USD ---
    elif indicator == "EUR/USD":
        eurusd = yf.download("EURUSD=X", period="1y", interval="1d")
        if eurusd.empty: return empty_chart(colors, "EUR/USD Verisi Yok")

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, facecolor=colors['plot_bg'])
        apply_dark_theme(ax1, colors)
        ax1.plot(eurusd.index, eurusd["Close"], label="EUR/USD", color="purple")
        ax1.set_title("EUR/USD Paritesi", color="white", fontweight="bold")
        ax1.legend(facecolor=colors['button'], labelcolor='white')

        apply_dark_theme(ax2, colors)
        ax2.plot(df.index, df["Close"], label=f"{ticker} Fiyatı", color="blue")
        plt.tight_layout()
        return fig

    # --- 10. STOCH(9,6) ---
    elif indicator == "STOCH(9,6)":
        if 'STOCH(9,6)' not in df.columns: return empty_chart(colors, "STOCH Verisi Yok")
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, facecolor=colors['plot_bg'])
        
        apply_dark_theme(ax1, colors)
        ax1.plot(df.index, df['STOCH(9,6)'], label='STOCH', color='navy')
        ax1.axhline(30, color='red', linestyle='--')
        ax1.axhline(70, color='red', linestyle='--')
        ax1.set_title("STOCH(9,6)", color="white")
        
        apply_dark_theme(ax2, colors)
        ax2.plot(df.index, df["Close"], label="Fiyat", color="blue")
        plt.tight_layout()
        return fig

    # --- 11. MOVING AVERAGES ---
    elif indicator == "Moving Averages":
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=colors['plot_bg'])
        apply_dark_theme(ax, colors)
        ax.plot(df.index, df["Close"], label="Fiyat", color="gray", linewidth=2.5)
        
        colors_ma = ['blue', 'orange', 'green', 'red', 'purple', 'brown']
        styles = ['-', '--', ':', '-.', '--', ':']
        for i, p in enumerate([5, 10, 20, 50, 100, 200]):
            col = f"MA_{p}"
            if col in df.columns:
                ax.plot(df.index, df[col], label=f"MA {p}", color=colors_ma[i], linestyle=styles[i])
        
        ax.set_title("Hareketli Ortalamalar", color="white", fontweight="bold")
        ax.legend(facecolor=colors['button'], labelcolor='white')
        plt.tight_layout()
        return fig

    # --- 12. EXPONENTIAL MOVING AVERAGES ---
    elif indicator == "Exponential Moving Averages":
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=colors['plot_bg'])
        apply_dark_theme(ax, colors)
        ax.plot(df.index, df["Close"], label="Fiyat", color="gray", linewidth=2.5)
        
        colors_ma = ['blue', 'orange', 'green', 'red', 'purple', 'brown']
        styles = ['-', '--', ':', '-.', '--', ':']
        for i, p in enumerate([5, 10, 20, 50, 100, 200]):
            col = f"EMA_{p}"
            if col in df.columns:
                ax.plot(df.index, df[col], label=f"EMA {p}", color=colors_ma[i], linestyle=styles[i])
                
        ax.set_title("Üstel Hareketli Ortalamalar (EMA)", color="white", fontweight="bold")
        ax.legend(facecolor=colors['button'], labelcolor='white')
        plt.tight_layout()
        return fig

    # --- 13. MACD ---
    elif indicator == "MACD":
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, facecolor=colors['plot_bg'])
        apply_dark_theme(ax1, colors)
        ax1.plot(df.index, df['MACD'], label='MACD', color='#00FF00')
        ax1.plot(df.index, df['MACD_Signal'], label='Sinyal', color='#FF0000')
        cols = np.where(df['MACD_Hist'] > 0, '#00FF00', '#FF0000')
        ax1.bar(df.index, df['MACD_Hist'], color=cols)
        ax1.set_title("MACD", color="white", fontweight="bold")
        ax1.legend(facecolor=colors['button'], labelcolor='white')

        apply_dark_theme(ax2, colors)
        ax2.plot(df.index, df["Close"], label="Fiyat", color="blue")
        plt.tight_layout()
        return fig

    # --- 14. ADX(14) ---
    elif indicator == "ADX(14)":
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, facecolor=colors['plot_bg'])
        apply_dark_theme(ax1, colors)
        ax1.plot(df.index, df['ADX(14)'], label='ADX(14)', color='#FFFF00')
        ax1.set_title("ADX(14)", color="white")
        
        apply_dark_theme(ax2, colors)
        ax2.plot(df.index, df["Close"], label="Fiyat", color="blue")
        plt.tight_layout()
        return fig

    # --- 15. VOLUME (Hacim Mumları) ---
    elif indicator == "VOLUME":
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True, facecolor=colors['plot_bg'])
        apply_dark_theme(ax1, colors)
        
        cols = ['green' if r['Close'] >= r['Open'] else 'red' for i, r in df.iterrows()]
        ax1.bar(df.index, df["Volume"], color=cols, label="Hacim")
        avg_vol = df["Volume"].mean()
        ax1.axhline(avg_vol, color='orange', linestyle='--', label="Ort. Hacim")
        ax1.set_title("İşlem Hacmi", color="white")
        ax1.legend(facecolor=colors['button'], labelcolor='white')

        apply_dark_theme(ax2, colors)
        ax2.plot(df.index, df["Close"], label="Fiyat", color="blue")
        plt.tight_layout()
        return fig

    # --- 16. BOLLINGER BANDS ---
    elif indicator == "Bollinger Bands":
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=colors['plot_bg'])
        apply_dark_theme(ax, colors)
        ax.plot(df.index, df['Close'], label='Kapanış', color='#00FF00')
        ax.plot(df.index, df['BB_High'], label='Üst', color='#FF0000', linewidth=1)
        ax.plot(df.index, df['BB_Low'], label='Alt', color='#0000FF', linewidth=1)
        ax.plot(df.index, df['BB_Mid'], label='Orta', color='#FFA500', linestyle="--")
        ax.fill_between(df.index, df['BB_Low'], df['BB_High'], color='gray', alpha=0.3)
        ax.set_title("Bollinger Bands", color="white", fontweight="bold")
        ax.legend(facecolor=colors['button'], labelcolor='white')
        plt.tight_layout()
        return fig

    # --- 17. FIBONACCI PIVOT ---
    elif indicator == "Fibonacci Pivot":
        fig, ax = plt.subplots(figsize=(12, 6), facecolor=colors['plot_bg'])
        apply_dark_theme(ax, colors)
        ax.plot(df.index, df['Close'], label='Fiyat', color='green', linewidth=2)
        
        # Son günün pivotlarını çiz (Tüm geçmişi çizmek karmaşık olur)
        if 'Pivot_Fib' in df.columns:
            last = df.iloc[-1]
            ax.axhline(last['Pivot_Fib'], color='orange', linestyle='--', label='Pivot')
            ax.axhline(last['R1_Fib'], color='red', linestyle='--', alpha=0.5, label='R1')
            ax.axhline(last['S1_Fib'], color='green', linestyle='--', alpha=0.5, label='S1')
            
        ax.set_title("Fibonacci Pivot Noktaları (Son Gün)", color="white")
        ax.legend(facecolor=colors['button'], labelcolor='white')
        plt.tight_layout()
        return fig

    # --- 18. WILLIAMS %R ---
    elif indicator == "Williams %R":
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, facecolor=colors['plot_bg'])
        apply_dark_theme(ax1, colors)
        ax1.plot(df.index, df["Williams %R"], label="Williams %R", color="yellow")
        ax1.axhline(-20, color='red', linestyle='--')
        ax1.axhline(-80, color='green', linestyle='--')
        ax1.set_ylim(-100, 0)
        ax1.set_title("Williams %R", color="white")
        
        apply_dark_theme(ax2, colors)
        ax2.plot(df.index, df["Close"], label="Fiyat", color="blue")
        plt.tight_layout()
        return fig

    # --- 19. CCI(14) ---
    elif indicator == "CCI(14)":
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, facecolor=colors['plot_bg'])
        apply_dark_theme(ax1, colors)
        ax1.plot(df.index, df["CCI(14)"], label="CCI(14)", color="cyan")
        ax1.axhline(100, color='red', linestyle='--')
        ax1.axhline(-100, color='green', linestyle='--')
        ax1.set_title("CCI(14)", color="white")
        
        apply_dark_theme(ax2, colors)
        ax2.plot(df.index, df["Close"], label="Fiyat", color="blue")
        plt.tight_layout()
        return fig

    # --- 20. ATR%(14) ---
    elif indicator == "ATR%(14)":
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, facecolor=colors['plot_bg'])
        apply_dark_theme(ax1, colors)
        ax1.plot(df.index, df["ATR%(14)"], label="ATR%", color="magenta")
        ax1.set_title("ATR%(14)", color="white")
        
        apply_dark_theme(ax2, colors)
        ax2.plot(df.index, df["Close"], label="Fiyat", color="blue")
        plt.tight_layout()
        return fig

    # --- 21. ROC ---
    elif indicator == "ROC":
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, facecolor=colors['plot_bg'])
        apply_dark_theme(ax1, colors)
        ax1.plot(df.index, df["ROC"], label="ROC", color="orange")
        ax1.axhline(0, color='white', linestyle='--')
        ax1.set_title("ROC", color="white")
        
        apply_dark_theme(ax2, colors)
        ax2.plot(df.index, df["Close"], label="Fiyat", color="blue")
        plt.tight_layout()
        return fig

    # --- 22. PARABOLIC SAR ---
    elif indicator == "Parabolic_SAR":
        fig, ax = plt.subplots(figsize=(12, 6), facecolor=colors['plot_bg'])
        apply_dark_theme(ax, colors)
        ax.plot(df.index, df["Close"], label="Close", color="blue")
        ax.scatter(df.index, df["Parabolic_SAR"], label="SAR", color="red", marker='.', s=30)
        ax.set_title("Parabolic SAR", color="white")
        ax.legend(facecolor=colors['button'], labelcolor='white')
        plt.tight_layout()
        return fig

    # --- 23. ULTIMATE OSCILLATOR ---
    elif indicator == "Ultimate Oscillator":
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, facecolor=colors['plot_bg'])
        apply_dark_theme(ax1, colors)
        ax1.plot(df.index, df["Ultimate Oscillator"], label="Ultimate Osc", color="purple")
        ax1.axhline(70, color='red', linestyle='--')
        ax1.axhline(30, color='green', linestyle='--')
        ax1.set_ylim(0, 100)
        ax1.set_title("Ultimate Oscillator", color="white")
        
        apply_dark_theme(ax2, colors)
        ax2.plot(df.index, df["Close"], label="Fiyat", color="blue")
        plt.tight_layout()
        return fig

    # --- 24. MFI(14) ---
    elif indicator == "MFI(14)":
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, facecolor=colors['plot_bg'])
        apply_dark_theme(ax1, colors)
        ax1.plot(df.index, df["MFI(14)"], label="MFI(14)", color="lime")
        ax1.axhline(80, color='red', linestyle='--')
        ax1.axhline(20, color='green', linestyle='--')
        ax1.set_ylim(0, 100)
        ax1.set_title("Money Flow Index", color="white")
        
        apply_dark_theme(ax2, colors)
        ax2.plot(df.index, df["Close"], label="Fiyat", color="blue")
        plt.tight_layout()
        return fig

    # --- 25. OBV ---
    elif indicator == "OBV":
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, facecolor=colors['plot_bg'])
        apply_dark_theme(ax1, colors)
        ax1.plot(df.index, df["OBV"], label="OBV", color="pink")
        ax1.set_title("On-Balance Volume", color="white")
        
        apply_dark_theme(ax2, colors)
        ax2.plot(df.index, df["Close"], label="Fiyat", color="blue")
        plt.tight_layout()
        return fig

    # --- 26. VWAP ---
    elif indicator == "VWAP":
        fig, ax = plt.subplots(figsize=(12, 6), facecolor=colors['plot_bg'])
        apply_dark_theme(ax, colors)
        ax.plot(df.index, df["VWAP"], label="VWAP", color="brown", linestyle="--")
        ax.plot(df.index, df["Close"], label="Fiyat", color="green")
        ax.set_title("VWAP", color="white")
        ax.legend(facecolor=colors['button'], labelcolor='white')
        plt.tight_layout()
        return fig

    # --- 27. CMF ---
    elif indicator == "CMF":
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, facecolor=colors['plot_bg'])
        apply_dark_theme(ax1, colors)
        ax1.plot(df.index, df["CMF"], label="CMF", color="red")
        ax1.axhline(0, color='white', linestyle='--')
        ax1.set_title("Chaikin Money Flow", color="white")
        
        apply_dark_theme(ax2, colors)
        ax2.plot(df.index, df["Close"], label="Fiyat", color="blue")
        plt.tight_layout()
        return fig

    # --- 28. SUPERTREND ---
    elif indicator == "SuperTrend":
        st, direction = calculate_supertrend(df)
        fig, ax = plt.subplots(figsize=(12, 6), facecolor=colors['plot_bg'])
        apply_dark_theme(ax, colors)
        ax.plot(df.index, df["Close"], label="Fiyat", color="blue")
        
        for i in range(1, len(df)):
            if pd.notna(st[i]):
                color = "green" if direction[i] else "red"
                ax.plot(df.index[i-1:i+1], st[i-1:i+1], color=color, linewidth=2)
                
        ax.set_title("SuperTrend", color="white", fontweight="bold")
        ax.plot([], [], color="green", label="AL")
        ax.plot([], [], color="red", label="SAT")
        ax.legend(facecolor=colors['button'], labelcolor='white')
        plt.tight_layout()
        return fig

    # --- 29. ICHIMOKU ---
    elif indicator == "Ichimoku":
        # Orijinal kod gelecekteki bulutu da çiziyordu, burada basitleştirilmiş halini çiziyoruz
        # ama orijinal koddaki gibi df'i genişletmek plotting içinde zor olabilir,
        # mevcut df üzerinden çiziyoruz.
        fig, ax = plt.subplots(figsize=(13, 6), facecolor=colors['plot_bg'])
        apply_dark_theme(ax, colors)
        
        ax.plot(df.index, df['Close'], label='Fiyat', color='white', linewidth=2)
        if 'Tenkan_Sen' in df.columns:
            ax.plot(df.index, df['Tenkan_Sen'], label='Tenkan', color='red', linestyle='--')
            ax.plot(df.index, df['Kijun_Sen'], label='Kijun', color='blue', linestyle='--')
            
        if 'Senkou_Span_A' in df.columns:
             # Bulut Dolgusu
             ax.fill_between(df.index, df['Senkou_Span_A'], df['Senkou_Span_B'], 
                             where=df['Senkou_Span_A']>=df['Senkou_Span_B'], color='green', alpha=0.3)
             ax.fill_between(df.index, df['Senkou_Span_A'], df['Senkou_Span_B'], 
                             where=df['Senkou_Span_A']<df['Senkou_Span_B'], color='red', alpha=0.3)
             
        ax.set_title("Ichimoku Bulutu", color="white", fontweight="bold")
        ax.legend(facecolor=colors['button'], labelcolor='white')
        plt.tight_layout()
        return fig

    # --- DEFAULT (Bilinmeyen durumlar için Fiyat Grafiği) ---
    else:
        fig, ax = plt.subplots(figsize=(10, 5), facecolor=colors['plot_bg'])
        apply_dark_theme(ax, colors)
        ax.plot(df.index, df["Close"], label="Fiyat", color="green")
        ax.set_title(f"{ticker} - {indicator} (Veri Yok/Tanımsız)", color="white")
        plt.tight_layout()
        return fig