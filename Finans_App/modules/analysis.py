# modules/analysis.py
import numpy as np
import pandas as pd
import yfinance as yf

# --- SABİT YORUM VE EŞİK DEĞERLERİ (Orijinal Koddan) ---
RISK_EXPLANATIONS = {
    "Beta": {"thresholds": (0.8, 1.2), "explanation": "Piyasa volatilitesine göre risk seviyesi", "recommendation": {"below": ("Piyasadan daha az riskli", "🟢"), "above": ("Piyasadan daha riskli", "🔴"), "normal": ("Piyasa ile uyumlu risk", "🟡")}},
    "Sharpe": {"thresholds": (1, 2), "explanation": "Risk birimi başına getiri", "recommendation": {"below": ("Düşük risk-getiri dengesi", "🔴"), "above": ("İyi risk-getiri dengesi", "🟢"), "normal": ("Kabul edilebilir risk-getiri", "🟡")}},
    "Sortino": {"thresholds": (1, 2), "explanation": "Zarar riski birimi başına getiri", "recommendation": {"below": ("Düşük Sortino oranı", "🔴"), "above": ("Yüksek Sortino oranı", "🟢"), "normal": ("Kabul edilebilir Sortino", "🟡")}},
    "Volatilite": {"thresholds": (0.2, 0.4), "explanation": "Yıllık fiyat dalgalanması", "recommendation": {"below": ("Düşük Volatilite", "🟢"), "above": ("Yüksek Volatilite", "🔴"), "normal": ("Orta Volatilite", "🟡")}},
    "Max Drawdown": {"thresholds": (-0.2, -0.4), "explanation": "Maksimum düşüş değeri", "recommendation": {"below": ("Aşırı Düşüş Riski", "🔴"), "above": ("Kabul edilebilir Düşüş", "🟢"), "normal": ("Orta Düşüş Riski", "🟡")}},
    "Treynor": {"thresholds": (0.5, 1.0), "explanation": "Sistemik risk başına getiri (Beta'ya göre)", "recommendation": {"below": ("Düşük risk düzeltmeli getiri", "🔴"), "above": ("Yüksek risk düzeltmeli getiri", "🟢"), "normal": ("Kabul edilebilir risk/getiri", "🟡")}},
    "Calmar": {"thresholds": (0.5, 1.0), "explanation": "Maksimum düşüşe göre getiri oranı", "recommendation": {"below": ("Düşük düşüş direnci", "🔴"), "above": ("Yüksek düşüş direnci", "🟢"), "normal": ("Orta seviye direnç", "🟡")}},
    "R²": {"thresholds": (0.3, 0.7), "explanation": "Piyasa ile korelasyon (1 = tam uyum)", "recommendation": {"below": ("Düşük piyasa korelasyonu", "🟡"), "above": ("Yüksek piyasa korelasyonu", "🟢"), "normal": ("Orta seviye korelasyon", "🟡")}},
}

INDICATOR_EXPLANATIONS = {
    "RSI_14": {"thresholds": (30, 70), "explanation": "14 günlük RSI - 30 altı aşırı satım, 70 üstü aşırı alım", "recommendation": {"below": ("Aşırı Satım (Al Sinyali)", "🟢 Al"), "above": ("Aşırı Alım (Sat Sinyali)", "🔴 Sat"), "normal": ("Normal Bölge", "🟡 Tut")}},
    "MACD": {"comparison1": "MACD_Signal", "explanation": "MACD sinyal ilişkisi", "recommendation": {"above": ("MACD Sinyal Üstünde (Al)", "🟢 Al"), "below": ("MACD Sinyal Altında (Sat)", "🔴 Sat")}},
    "STOCH(9,6)": {"thresholds": (20, 80), "explanation": "Stokastik Osilatör", "recommendation": {"below": ("Aşırı Satım (Al Sinyali)", "🟢 Al"), "above": ("Aşırı Alım (Sat Sinyali)", "🔴 Sat"), "normal": ("Normal Bölge", "🟡 Tut")}},
    "ADX(14)": {"thresholds": (25, 25), "explanation": "Trend Gücü", "recommendation": {"above": ("Güçlü Trend", "🟢 Trend Takip"), "below": ("Zayıf Trend (Dikkatli Ol)", "🔴 Dikkat"), "normal": ("Orta Trend", "🟡 Tut")}},
    "CCI(14)": {"thresholds": (-100, 100), "explanation": "CCI", "recommendation": {"below": ("Aşırı Satım", "🟢 Al"), "above": ("Aşırı Alım", "🔴 Sat"), "normal": ("Normal Bölge", "🟡 Tut")}},
    "Williams %R": {"thresholds": (-80, -20), "explanation": "Williams %R", "recommendation": {"below": ("Aşırı Satım (Al Sinyali)", "🟢 Al"), "above": ("Aşırı Alım (Sat Sinyali)", "🔴 Sat"), "normal": ("Normal Bölge", "🟡 Tut")}},
    "Ultimate Oscillator": {"thresholds": (30, 70), "explanation": "Ultimate Osc", "recommendation": {"below": ("Aşırı Satım", "🟢 Al"), "above": ("Aşırı Alım", "🔴 Sat"), "normal": ("Normal", "🟡 Tut")}},
    "ROC": {"thresholds": (0, 0), "explanation": "Momentum", "recommendation": {"above": ("Yukarı Momentum", "🟢 Al"), "below": ("Aşağı Momentum (Sat Sinyali)", "🔴 Sat"), "normal": ("Nötr", "🟡 Tut")}},
    "ATR%(14)": {"thresholds": (1.0, 2.5), "explanation": "Volatilite", "recommendation": {"below": ("Düşük Volatilite (Güvenli Bölge)", "🟢 Al"), "above": ("Yüksek Volatilite", "🔴 Sat"), "normal": ("Orta Volatilite", "🟡 Tut")}},
    "Parabolic_SAR": {"comparison": "Close", "explanation": "Trend Yönü", "recommendation": {"above": ("Yükseliş Trendinde", "🟢 Al"), "below": ("Düşüş Trendinde (Sat Sinyali)", "🔴 Sat")}},
    
    # Hareketli Ortalamalar
    "MA_5": {"comparison": "Close", "explanation": "MA 5", "recommendation": {"above": ("Fiyat MA5 Üstünde", "🟢 Al"), "below": ("Fiyat MA5 Altında (Sat Sinyali)", "🔴 Sat")}},
    "MA_10": {"comparison": "Close", "explanation": "MA 10", "recommendation": {"above": ("Fiyat MA10 Üstünde", "🟢 Al"), "below": ("Fiyat MA10 Altında (Sat)", "🔴 Sat")}},
    "MA_20": {"comparison": "Close", "explanation": "MA 20", "recommendation": {"above": ("Fiyat MA20 Üstünde", "🟢 Al"), "below": ("Fiyat MA20 Altında (Sat)", "🔴 Sat")}},
    "MA_50": {"comparison": "Close", "explanation": "MA 50", "recommendation": {"above": ("Fiyat MA50 Üstünde (Güçlü Al)", "🟢 Al"), "below": ("Fiyat MA50 Altında (Güçlü Sat)", "🔴 Sat")}},
    "MA_100": {"comparison": "Close", "explanation": "MA 100", "recommendation": {"above": ("Fiyat MA100 Üstünde", "🟢 Al"), "below": ("Fiyat MA100 Altında (Güçlü Sat)", "🔴 Sat")}},
    "MA_200": {"comparison": "Close", "explanation": "MA 200", "recommendation": {"above": ("Fiyat MA200 Üstünde", "🟢 Al"), "below": ("Fiyat MA200 Altında (Güçlü Sat)", "🔴 Sat")}},
    
    # Üstel Hareketli Ortalamalar
    "EMA_5": {"comparison": "Close", "explanation": "EMA 5", "recommendation": {"above": ("Fiyat EMA5 Üstünde", "🟢 Al"), "below": ("Fiyat EMA5 Altında (Sat Sinyali)", "🔴 Sat")}},
    "EMA_10": {"comparison": "Close", "explanation": "EMA 10", "recommendation": {"above": ("Fiyat EMA10 Üstünde", "🟢 Al"), "below": ("Fiyat EMA10 Altında (Sat)", "🔴 Sat")}},
    "EMA_20": {"comparison": "Close", "explanation": "EMA 20", "recommendation": {"above": ("Fiyat EMA20 Üstünde", "🟢 Al"), "below": ("Fiyat EMA20 Altında (Sat)", "🔴 Sat")}},
    "EMA_50": {"comparison": "Close", "explanation": "EMA 50", "recommendation": {"above": ("Fiyat EMA50 Üstünde (Güçlü Al)", "🟢 Al"), "below": ("Fiyat EMA50 Altında (Güçlü Sat)", "🔴 Sat")}},
    "EMA_100": {"comparison": "Close", "explanation": "EMA 100", "recommendation": {"above": ("Fiyat EMA100 Üstünde", "🟢 Al"), "below": ("Fiyat EMA100 Altında (Yapısal Sat)", "🔴 Sat")}},
    "EMA_200": {"comparison": "Close", "explanation": "EMA 200", "recommendation": {"above": ("Fiyat EMA200 Üstünde", "🟢 Al"), "below": ("Fiyat EMA200 Altında (Stratejik Sat)", "🔴 Sat")}},
}

def calculate_risk_metrics(ticker):
    """Risk metriklerini hesaplar (Orijinal kodunuzdaki formüllerle)"""
    try:
        stock_data = yf.Ticker(ticker).history(period='1y', interval='1d')
        # Benchmark olarak S&P 500 kullanıyoruz
        benchmark_data = yf.Ticker("^GSPC").history(period='1y', interval='1d')
    
        if stock_data.empty or benchmark_data.empty: return None

        returns = stock_data['Close'].pct_change().dropna()
        benchmark_returns = benchmark_data['Close'].pct_change().dropna()
        
        # Verileri hizala
        aligned = pd.concat([returns, benchmark_returns], axis=1, join='inner').dropna()
        returns = aligned.iloc[:, 0]
        benchmark_returns = aligned.iloc[:, 1]
        
        total_days = len(returns)
        rf_rate = 0.04  # %4 Risksiz Faiz Oranı varsayımı

        # Temel Metrikler
        annual_return = (1 + returns).prod() - 1
        annual_volatility = returns.std() * np.sqrt(total_days)
        sharpe_ratio = (annual_return - rf_rate) / annual_volatility if annual_volatility != 0 else 0

        downside_returns = returns[returns < 0]
        downside_deviation = downside_returns.std() * np.sqrt(total_days)
        sortino_ratio = (annual_return - rf_rate) / downside_deviation if downside_deviation != 0 else 0

        # Beta ve Korelasyon
        covariance = np.cov(returns, benchmark_returns)
        variance = np.var(benchmark_returns)
        beta = covariance[0,1] / variance if variance != 0 else 0
        
        correlation = returns.rolling(total_days).corr(benchmark_returns).iloc[-1]
        r_squared = correlation ** 2

        # Treynor
        treynor_ratio = (annual_return - rf_rate) / beta if beta != 0 else 0

        # Drawdown ve Calmar
        cumulative_returns = (1 + returns).cumprod()
        peak = cumulative_returns.cummax()
        drawdown = (cumulative_returns / peak) - 1
        max_drawdown = drawdown.min()
        calmar_ratio = annual_return / abs(max_drawdown) if max_drawdown != 0 else 0

        return {
            "Beta": beta, "Sharpe": sharpe_ratio, "Sortino": sortino_ratio, 
            "Volatilite": annual_volatility, "Max Drawdown": max_drawdown,
            "Treynor": treynor_ratio, "Calmar": calmar_ratio, "R²": r_squared
        }
    except Exception as e:
        print(f"Risk Hatası: {e}")
        return None

def generate_analysis_report(ticker, df):
    """
    Orijinal kodunuzdaki çıktıyı birebir oluşturan fonksiyon.
    """
    start_date = df.index[0].strftime('%d-%m-%Y')
    end_date = df.index[-1].strftime('%d-%m-%Y')
    current_price = df['Close'].iloc[-1]
    
    report = f"Analiz Tarih Aralığı: {start_date} - {end_date}\n\n"
    report += f"{ticker} Teknik Göstergeler ve Risk Göstergeleri\n\n"
    report += f"Son Fiyat: {current_price:.2f}\n\n"
    report += "--- Teknik Göstergeler ve Yorumlar ---\n\n"
    
    # 1. Teknik İndikatörler Döngüsü
    for ind, exp in INDICATOR_EXPLANATIONS.items():
        if ind not in df.columns and "comparison" not in exp: continue
        
        try:
            # Normal Değer
            val = df[ind].iloc[-1] if ind in df.columns else 0
            comment, icon = "", ""
            
            # Eşik Değer Kontrolü (Thresholds)
            if "thresholds" in exp:
                low, high = exp["thresholds"]
                if val < low: 
                    comment, icon = exp["recommendation"]["below"]
                elif val > high: 
                    comment, icon = exp["recommendation"]["above"]
                else: 
                    comment, icon = exp["recommendation"]["normal"]
                
                report += f"{ind}: {val:.2f} {icon} - {comment}\n"

            # Karşılaştırma Kontrolü (Comparison - MAs & Parabolic SAR)
            elif "comparison" in exp:
                comp_col = exp["comparison"] # Genelde 'Close'
                comp_val = df[comp_col].iloc[-1]
                
                # İndikatör değeri (Örn: MA_50 değeri)
                ind_val = df[ind].iloc[-1]
                
                # Eğer Close > MA ise 'above', değilse 'below'
                if comp_val > ind_val:
                    comment, icon = exp["recommendation"]["above"]
                else:
                    comment, icon = exp["recommendation"]["below"]
                    
                report += f"{ind}: {ind_val:.2f} {icon} - {comment}\n"

            # MACD Özel Kontrolü
            elif "comparison1" in exp:
                signal_val = df[exp["comparison1"]].iloc[-1]
                if val > 0:
                    if val > signal_val:
                        comment, icon = "MACD Pozitif ve Sinyal Üstünde (Güçlü Al)", "🟢 Al"
                    else:
                        comment, icon = "MACD Pozitif ama Sinyal Altında (Zayıflama)", "🟡 Tut"
                else:
                    if val > signal_val:
                        comment, icon = "MACD Negatif ama Sinyal Üstünde (Toparlanma)", "🟡 Tut"
                    else:
                        comment, icon = "MACD Negatif ve Sinyal Altında (Güçlü Sat)", "🔴 Sat"
                
                report += f"{ind}: {val:.2f} {icon} - {comment}\n"
                
        except Exception as e:
            continue

    # 2. Pivot Seviyeleri (Orijinal Koddaki Gibi)
    report += "\n--- Pivot Seviyeleri ---\n\n"
    
    pivot_types = {
        "Pivot_Klasik": ["S3", "S2", "S1", "Pivot", "R1", "R2", "R3"],
        "Pivot_Fibonacci": ["S3_Fib", "S2_Fib", "S1_Fib", "Pivot_Fib", "R1_Fib", "R2_Fib", "R3_Fib"]
    }
    
    for p_type, levels in pivot_types.items():
        try:
            # Pivot verilerini al, varsa formatla
            values = {lvl: df[lvl].iloc[-1] for lvl in levels if lvl in df.columns}
            if values:
                level_text = " | ".join([f"{k}: {v:.2f}" for k, v in values.items()])
                report += f"{p_type}:\n{level_text}\n\n"
        except:
            continue

    # 3. Risk Analizi
    metrics = calculate_risk_metrics(ticker)
    if metrics:
        report += "\n--- Risk Analizi ve Yorumlar ---\n\n"
        for key, val in metrics.items():
            exp = RISK_EXPLANATIONS.get(key, {})
            if "thresholds" in exp:
                low, high = exp["thresholds"]
                comment, icon = "", ""
                
                if val < low: comment, icon = exp["recommendation"]["below"]
                elif val > high: comment, icon = exp["recommendation"]["above"]
                else: comment, icon = exp["recommendation"]["normal"]
                
                report += f"{key}: {val:.6f} {icon} - {exp['explanation']}: {comment}\n"
            
    return report