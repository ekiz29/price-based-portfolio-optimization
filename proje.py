import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import numpy as np
import pandas as pd
import ta
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC
import xgboost as xgb
from sklearn.model_selection import train_test_split
import os
from datetime import datetime
from sklearn.model_selection import GridSearchCV
from tkinter import messagebox
from sklearn.metrics import classification_report
import time
from scipy.stats import norm
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix

 
class StockAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hisse Senedi Analiz ve Portföy Optimizasyonu")
        self.root.geometry("1600x1200")

        self.colors = {
            'plot_bg': '#1E1E1E','background': '#2E2E2E','text': '#FFFFFF','button': '#3C3F41','frame': '#2E2E2E'
        }
        self.tickers = {
    "iShares Gold Trust": "IAU","iShares Silver Trust": "SLV","S&P 500":"^GSPC","CBOE Volatility Index": "^VIX","iShares 20+ Year Treasury Bond ETF":"TLT","Bitcoin USD Price" :"BTC-USD","United States Oil Fund": "USO","Solana USD Price":"SOL-USD","Ethereum USD Price":"ETH-USD","XRP USD Price":"XRP-USD","Dogecoin USD Price" :"DOGE-USD","iShares 20+ Year Treasury Bond ETF" :"TLT",
    "Abbott Laboratories": "ABT", "AbbVie": "ABBV", "Adobe": "ADBE", "Alphabet (Class A)": "GOOGL", "Alphabet (Class C)": "GOOG",
    "Amazon": "AMZN", "American Express": "AXP", "Amgen": "AMGN","AMD (Advanced Micro Devices)":"AMD", "Apple": "AAPL","ARM Holdings" :"ARM","ASML Holding": "ASML",
    "Autodesk": "ADSK",	"Bank of America":"BAC", "Berkshire Hathaway B": "BRK-B", "Biogen": "BIIB", "BlackRock": "BLK", "Boeing": "BA",
    "Bristol Myers Squibb": "BMY", "Broadcom": "AVGO", "Caterpillar": "CAT", "Chevron": "CVX", "Cisco": "CSCO",
    "Cloudflare": "NET", "Coca-Cola": "KO", "Conocophilips": "COP", "Costco": "COST", "CrowdStrike": "CRWD",
    "Datadog": "DDOG", "Delta Air Lines": "DAL", "Eli Lilly": "LLY", "ExxonMobil": "XOM", "Ferrari": "RACE",
    "Ford": "F", "General Electric": "GE", "General Motors": "GM", "Gilead Sciences": "GILD", "Goldman Sachs": "GS","HCA Holdings Inc":"HCA",
    "Hilton": "HLT", "Honeywell": "HON", "IBM": "IBM", "Illumina": "ILMN", "Intel": "INTC",
    "Intuit": "INTU", "JPMorgan Chase": "JPM", "Johnson & Johnson": "JNJ", "Lockheed Martin": "LMT","Live Nation Entertainment":"LYV","LVMH": "LVMUY",
    "Lyft": "LYFT", "Marriott": "MAR", "Mastercard": "MA", "McDonald's": "MCD", "Merck": "MRK","Microsoft":"MSFT",
    "Meta": "META", "Moderna": "MRNA", "Morgan Stanley": "MS","Newmont Corporation":"NEM", "Netflix": "NFLX", "Nike": "NKE",
    "Nvidia": "NVDA", "Novo Nordisk": "NVO", "Novartis": "NVS", "Okta": "OKTA", "Oracle": "ORCL",
    "Palantir": "PLTR", "Palo Alto Networks": "PANW", "PayPal": "PYPL", "Pepsi Co": "PEP", "Pfizer": "PFE",
    "Procter & Gamble": "PG", "Qualcomm": "QCOM", "Raytheon Technologies": "RTX", "Regeneron": "REGN", "Roche": "RHHBY",
    "Salesforce": "CRM", "Schlumberger": "SLB", "ServiceNow": "NOW","Shell plc":"SHEL","Shopify": "SHOP", "Snowflake": "SNOW",
    "Southwest Airlines": "LUV", "Square (Block)": "SQ","SoFi Technologies, Inc.":"SOFI", "S&P Global": "SPGI", "Starbucks": "SBUX", "Target": "TGT", "Tesla":"TSLA",
    "Texas Instruments": "TXN", "Thermo Fisher": "TMO", "3M": "MMM", "Toyota": "TM", "Twilio": "TWLO",
    "Uber": "UBER","Unilever PLC":"UL","United Airlines": "UAL", "UnitedHealth": "UNH", "Visa": "V", "Vertex Pharmaceuticals": "VRTX",
    "Volkswagen": "VWAGY", "Walmart": "WMT", "Zscaler": "ZS",
    "Adel": "ADEL.IS", "Adese Gayrimenkul": "ADSE.GY", "Afyon Çimento": "AFYON.IS", "Akcansa": "AKCNS.IS", "Akenerji": "AKENR.IS", "Akkök": "AKKOK.IS", "Akmerkez GYO": "AKMER.IS", "Albaraka Türk": "ALBRK.IS", "Alarko Carrier": "ALCAR.IS", "Alarko Holding": "ALARK.IS", "Alcatel Lucent": "ALTHD.IS", "Alcı Yatırım": "ALCYT.IS", "Aksu Enerji ve Ticaret": "AKSUE.IS", "Anadolu Efes Malt": "AEFES.IS", "Anadolu Sigorta": "ANSUR.IS", "Anel Elektrik": "ANELE.IS", "Arçelik": "ARCLK.IS", "Aselsan": "ASELS.IS", "Aygaz": "AYGAZ.IS", "Batikim": "BATIK.IS", "Borusan Birleşik": "BORUB.IS", "Borusan Yatırım": "BRYAT.IS", "BİM Mağazalar": "BIMAS.IS", "Coca-Cola İçecek": "CCOLA.IS", "Deva Holding": "DEVA.IS","Dogan Sirketler Grubu Holding A.S.":"DOHOL.IS", "Doğuş Otomotiv": "DOAS.IS", "Ege Endüstri": "EGEEN.IS", "Enka İnşaat": "ENKAI.IS", "Erdemir": "EREGL.IS", "Ford Otosan": "FROTO.IS", "Garanti BBVA": "GARAN.IS","Galata Wind Enerji A.S.":"GWIND.IS","Hektaş": "HEKTS.IS", "ICBC Turkey": "ICBCT.IS", "Kardemir (D)": "KRDMD.IS", "Karel": "KAREL.IS", "Koç Holding": "KCHOL.IS", "Logo Yazılım": "LOGO.IS", "Mavi Giyim": "MAVI.IS", "Migros Ticaret": "MGROS.IS", "Netas Telekom": "NETAS.IS", "Otokar": "OTKAR.IS", "Oyak Çimento": "OYAKC.IS", "Pegasus": "PGSUS.IS", "Petkim": "PETKM.IS", "Sabancı Holding": "SAHOL.IS", "Sasa Polyester": "SASA.IS", "Şişecam": "SISE.IS", "TAV Havalimanları": "TAVHL.IS", "Tekfen Holding": "TKFEN.IS", "Teknosa": "TKNSA.IS", "TSKB": "TSKB.IS", "Tümosan": "TMSN.IS", "Tüpraş": "TUPRS.IS", "Türk Hava Yolları": "THYAO.IS", "Türk Telekom": "TTKOM.IS", "Turkcell": "TCELL.IS", "Türkiye Halk Bankası": "HALKB.IS", "Türkiye İş Bankası (C)": "ISCTR.IS", "Türkiye Sigorta": "TURSG.IS", "Ülker Bisküvi": "ULKER.IS", "VakıfBank": "VAKBN.IS", "Vestel": "VESTL.IS","Tofas Türk Otomobil Fabrikasi Anonim Sirketi":"TOASO.IS", "Yapı ve Kredi Bankası": "YKBNK.IS", "Yataş": "YATAS.IS", "Zorlu Enerji": "ZOREN.IS"


  
}
       
        self.setup_style()
        self.portfolio_entries = {}
        self.analysis_stock_var = tk.StringVar()  
        self.indicator_stock_var = tk.StringVar() 
        self.create_widgets()
    
    def setup_style(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', 
                           font=('Arial', 10, 'bold'),
                           background=self.colors['button'],
                           foreground=self.colors['text'])
        self.style.configure('TFrame', background=self.colors['frame'])
        self.style.configure('TLabel', 
                            background=self.colors['frame'],
                            foreground=self.colors['text'])
        self.style.configure('TCombobox', 
                            fieldbackground=self.colors['button'],
                            foreground=self.colors['text'])
    
    
    def plot_indicator_charts(self):
        
        selected_stock = self.stock_var.get()  
        selected_indicator = self.indicator_stock_var.get()  
    
        if not selected_stock:
            messagebox.showwarning("Uyarı", "Lütfen bir finansal enstrüman seçin!")
            return

        try:
            ticker = self.tickers[selected_stock]
            df = yf.Ticker(ticker).history(period='1y', interval='1d')
            
            
            if df.empty:
                raise ValueError("Finansal enstrüman  verisi bulunamadı!")
            df = self.calculate_technical_indicators(df) 


            fig, ax = plt.subplots(figsize=(12, 5), facecolor=self.colors['plot_bg'])


            if selected_indicator == "RSI":
   
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    

                ax1.plot(df.index, df['RSI_14'], label='RSI 14', color='navy')
                ax1.axhline(30, color='red', linestyle='--', alpha=0.7)
                ax1.axhline(70, color='red', linestyle='--', alpha=0.7)
                ax1.set_ylim(0, 100)
                ax1.set_title('RSI 14 Göstergesi', fontsize=12, fontweight='bold')
                ax1.grid(True, linestyle="--", alpha=0.6)  
    

                ax2.plot(df.index, df["Close"], label="1Y Price", color="blue")
                ax2.set_title("1 Yıllık Fiyat Hareketleri", fontsize=12, fontweight="bold")
                ax2.set_ylabel("Fiyat ($)")
                ax2.set_xlabel("Tarih")
                ax2.grid(True, linestyle="--", alpha=0.6)
                plt.tight_layout()
            elif selected_indicator == "1Y Price":
                ax.plot(df.index, df["Close"], label="1Y Price", color="blue")
                ax.set_title("1 Yıllık Fiyat Hareketleri", fontsize=12, fontweight="bold",color="blue")
                ax.set_ylabel("Fiyat ($)", color="white")
                ax.set_xlabel("Tarih", color="white")
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                ax.grid(True, linestyle="--", alpha=0.6)

            elif selected_indicator == "US10YEAR":
                us10y_df = yf.download("^TNX", period="1y", interval="1d")
                if us10y_df.empty:
                    raise ValueError("US10Y verisi alınamadı!")

                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)


                ax1.plot(us10y_df.index, us10y_df["Close"], label="ABD 10Y Tahvil Faizi", color="darkorange")
                ax1.set_title("ABD 10 Yıllık Tahvil Faizi (1 Yıllık)", fontsize=12, fontweight='bold')
                ax1.set_ylabel("Faiz (%)")
                ax1.grid(True, linestyle="--", alpha=0.6)
                ax1.legend()

   
                ax2.plot(df.index, df["Close"], label=f"{selected_stock}  Finansal Varlık Fiyatı", color="steelblue")
                ax2.set_title(f"{selected_stock} - 1 Yıllık Fiyat Hareketleri", fontsize=12, fontweight="bold")
                ax2.set_ylabel("Fiyat ($)")
                ax2.set_xlabel("Tarih")
                ax2.grid(True, linestyle="--", alpha=0.6)
                ax2.legend()
                
            elif selected_indicator == "F/K":

                symbol = input("Hisse sembolünü gir (örneğin: NVDA): ").upper()
                stock = yf.Ticker(symbol)

# Bugünün tarihi
                today = pd.to_datetime("today")

# 3'er ay aralıklarla 6 tarih (en eski başta)
                dates = [today - pd.DateOffset(months=3 * i) for i in range(5, -1, -1)]

# Tarih formatını kısalt: "ay.yıl"
                x_labels = [f"{date.month}.{date.year}" for date in dates]

# Her tarih için F/K oranını al
                fk_values = []
                for date in dates:
                    try:
        # En yakın çeyrek dönemi bul (yakın olan tarihe göre ayarlanmış)
                        quarter_end = date + pd.offsets.QuarterEnd(startingMonth=12)
        # Tarih aralığına göre finansalları al
                        earnings = stock.quarterly_financials
                        info = stock.get_income_stmt(freq='quarterly')
                        fk = stock.info.get("trailingPE", None)  # Güncel değilse None

        # Ekstra: Güncel olmayanlar için fallback
                        if fk is not None:
                            fk_values.append(fk)
                        else:
                            fk_values.append(None)

                    except Exception as e:
                        print(f"{date} için veri alınamadı: {e}")
                        fk_values.append(None)

# Grafik çizimi
                    plt.figure(figsize=(10, 6))
                    plt.bar(x_labels, fk_values, color='mediumslateblue', width=0.5)
                    plt.title(f"{symbol} - F/K Oranı (3 Aylık Aralıklarla)", fontsize=14, fontweight='bold')
                    plt.ylabel("F/K Oranı")
                    plt.grid(axis='y', linestyle='--', alpha=0.6)
                    plt.tight_layout()
                    plt.show()

            elif selected_indicator == "Nadaraya_watson":
                def nadaraya_watson_smoother(x, y, bandwidth):
                    y_smooth = []
                    for xi in x:
                        weights = norm.pdf((xi - x) / bandwidth)
                        weights /= weights.sum()
                        y_smooth.append(np.sum(weights * y))
                    return np.array(y_smooth)

                x = np.arange(len(df))
                y = df["Close"].values
                bandwidth = 10 

  
                y_smooth = nadaraya_watson_smoother(x, y, bandwidth)

                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

                ax1.plot(df.index, y, label="Orijinal Fiyat", color="lightblue", alpha=0.5)
             
                ax1.plot(df.index, y_smooth, label="Nadaraya-Watson Smooth", color="orange", linewidth=2)
                ax1.set_title(f"{selected_stock} - Nadaraya-Watson Smoothed Price", fontsize=12, fontweight="bold")
                ax1.grid(True, linestyle="--", alpha=0.6)
                ax1.legend()

             
                ax2.plot(df.index, df["Close"], label="1Y Price", color="blue")
                ax2.set_title(f"{selected_stock} - 1 Yıllık Fiyat Hareketleri", fontsize=12, fontweight="bold")
                ax2.grid(True, linestyle="--", alpha=0.6)
                ax2.legend()

                plt.tight_layout()

            elif selected_indicator == "VIX":
                vix_df = yf.download("^VIX", period="1y", interval="1d")
                if vix_df.empty:
                    raise ValueError("VIX verisi alınamadı!")

                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
                ax1.plot(vix_df.index, vix_df["Close"], label="VIX", color="purple")
                ax1.set_title("VIX (Korku Endeksi)", fontsize=12, fontweight='bold')
                ax1.grid(True, linestyle="--", alpha=0.6)
                ax1.legend()

                ax2.plot(df.index, df["Close"], label="1Y Price", color="blue")
                ax2.set_title("1 Yıllık Fiyat Hareketleri", fontsize=12, fontweight="bold")
                ax2.grid(True, linestyle="--", alpha=0.6)

                last_value = round(vix_df["Close"].iloc[-1], 2)
                ax1.text(vix_df.index[-1], vix_df["Close"].iloc[-1], f"{last_value}", 
                    color="black", fontsize=10, verticalalignment="bottom")

            elif selected_indicator == "DXY":
                dxy_df = yf.download("DX-Y.NYB", period="1y", interval="1d")
                if dxy_df.empty:
                    raise ValueError("DXY verisi alınamadı!")

                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
                ax1.plot(dxy_df.index, dxy_df["Close"], label="Dolar Endeksi (DXY)", color="green")
                ax1.set_title("Dolar Endeksi (DXY)", fontsize=12, fontweight='bold')
                ax1.grid(True, linestyle="--", alpha=0.6)
                ax1.legend()

                ax2.plot(df.index, df["Close"], label="1Y Price", color="blue")
                ax2.set_title("1 Yıllık Fiyat Hareketleri", fontsize=12, fontweight="bold")
                ax2.grid(True, linestyle="--", alpha=0.6)

                last_value = round(dxy_df["Close"].iloc[-1], 2)
                ax1.text(dxy_df.index[-1], dxy_df["Close"].iloc[-1], f"{last_value}", 
                        color="black", fontsize=10, verticalalignment="bottom")
            
            elif selected_indicator == "USD/JPY":
             
                usdjpy = yf.download("JPY=X", period="1y", interval="1d")
    
                if usdjpy.empty:
                    raise ValueError("USD/JPY verisi alınamadı!")

                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
  
                ax1.plot(usdjpy.index, usdjpy["Close"], label="USD/JPY", color="darkgreen")
                ax1.set_title("USD/JPY Paritesi (1 Yıllık)", fontsize=12, fontweight="bold")
                ax1.set_ylabel("Kur")
                ax1.grid(True, linestyle="--", alpha=0.6)
                ax1.legend()

                ax2.plot(df.index, df["Close"], label="1Y Price", color="blue")
                ax2.set_title(f"{selected_stock} Hissesi - 1 Yıllık Fiyat", fontsize=12, fontweight="bold")
                ax2.set_ylabel("Fiyat ($)")
                ax2.set_xlabel("Tarih")
                ax2.grid(True, linestyle="--", alpha=0.6)
                ax2.legend()
                plt.tight_layout()
            
            elif selected_indicator == "EUR/USD":

                eurusd = yf.download("EURUSD=X", period="1y", interval="1d")
    
                if eurusd.empty:
                    raise ValueError("EUR/USD verisi alınamadı!")

  
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)


                ax1.plot(eurusd.index, eurusd["Close"], label="EUR/USD", color="purple")
                ax1.set_title("EUR/USD Paritesi (1 Yıllık)", fontsize=12, fontweight="bold")
                ax1.set_ylabel("Kur")
                ax1.grid(True, linestyle="--", alpha=0.6)
                ax1.legend()

   
                ax2.plot(df.index, df["Close"], label=f"{selected_stock} - 1Y Price", color="blue")
                ax2.set_title(f"{selected_stock} Varlığı - 1 Yıllık Fiyat", fontsize=12, fontweight="bold")
                ax2.set_ylabel("Fiyat ($)")
                ax2.set_xlabel("Tarih")
                ax2.grid(True, linestyle="--", alpha=0.6)
                ax2.legend()

                plt.tight_layout()

            elif selected_indicator == "STOCH(9,6)":
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
                ax1.plot(df.index, df['STOCH(9,6)'], label='STOCH(9,6)', color='navy')
                ax1.axhline(30, color='red', linestyle='--', alpha=0.7)
                ax1.axhline(70, color='red', linestyle='--', alpha=0.7)
                ax1.set_ylim(0, 100)
                ax1.set_title('STOCH(9,6) Göstergesi', fontsize=12, fontweight='bold')
                ax1.grid(True, linestyle="--", alpha=0.6)  

                ax2.plot(df.index, df["Close"], label="1Y Price", color="blue")
                ax2.set_title("1 Yıllık Fiyat Hareketleri", fontsize=12, fontweight="bold")
                ax2.set_ylabel("Fiyat ($)")
                ax2.set_xlabel("Tarih")
                ax2.grid(True, linestyle="--", alpha=0.6)
                plt.tight_layout()
            elif selected_indicator == "Moving Averages":
                ax.plot(df.index, df["Close"], label="Kapanış Fiyatı", color="gray", linewidth=2.5)
                ax.plot(df.index, df["MA_5"], label="MA 5", color="blue", linestyle="-",linewidth=2)
                ax.plot(df.index, df["MA_10"], label="MA 10", color="orange", linestyle="--",linewidth=2)
                ax.plot(df.index, df["MA_20"], label="MA 20", color="green", linestyle=":",linewidth=2)
                ax.plot(df.index, df["MA_50"], label="MA 50", color="red", linestyle="-.",linewidth=2)
                ax.plot(df.index, df["MA_100"], label="MA 100", color="purple", linestyle="--",linewidth=3)
                ax.plot(df.index, df["MA_200"], label="MA 200", color="brown", linestyle=":",linewidth=3)

       
                future_limit = df.index[-1] + pd.Timedelta(days=5)
                ax.set_xlim(df.index[0], future_limit)

                ax.set_title("Fiyat Grafiği ve Hareketli Ortalamalar", fontsize=12, fontweight="bold", color="blue")
                ax.set_ylabel("Fiyat", color="white")
                ax.set_xlabel("Tarih", color="white")
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                ax.legend()
                ax.grid(True, linestyle="--", alpha=0.6)
            elif selected_indicator == "Exponential Moving Averages":
                ax.plot(df.index, df["Close"], label="Kapanış Fiyatı", color="gray", linewidth=2.5)
                ax.plot(df.index, df["EMA_5"], label="EMA 5", color="blue", linestyle="-",linewidth=2)
                ax.plot(df.index, df["EMA_10"], label="EMA 10", color="orange", linestyle="--",linewidth=2)
                ax.plot(df.index, df["EMA_20"], label="EMA 20", color="green", linestyle=":",linewidth=2)
                ax.plot(df.index, df["EMA_50"], label="EMA 50", color="red", linestyle="-.",linewidth=2)
                ax.plot(df.index, df["EMA_100"], label="EMA 100", color="purple", linestyle="--",linewidth=3)
                ax.plot(df.index, df["EMA_200"], label="EMA 200", color="brown", linestyle=":",linewidth=3)
                ax.set_title("Fiyat Grafiği ve Üstel Hareketli Ortalamalar (EMA)", fontsize=12, fontweight="bold",color='blue')
                ax.set_ylabel("Fiyat", color="white")
                ax.set_xlabel("Tarih", color="white")
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                ax.legend()
                ax.grid(True, linestyle="--", alpha=0.6)

            elif selected_indicator == "MACD":
    
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)


                ax1.plot(df.index, df['MACD'], label='MACD', color='#00FF00')
                ax1.plot(df.index, df['MACD_Signal'], label='Sinyal', color='#FF0000')
                ax1.bar(df.index, df['MACD_Hist'], label='Histogram', 
                    color=np.where(df['MACD_Hist'] > 0, '#00FF00', '#FF0000'))
                ax1.set_title('MACD Göstergesi', fontsize=12, fontweight='bold')
                ax1.legend()
                ax1.grid(True, linestyle="--", alpha=0.6)

 
                ax2.plot(df.index, df["Close"], label="1Y Price", color="blue")
                ax2.set_title("1 Yıllık Fiyat Hareketleri", fontsize=12, fontweight="bold")
                ax2.set_ylabel("Fiyat ($)")
                ax2.set_xlabel("Tarih")
                ax2.grid(True, linestyle="--", alpha=0.6)
                plt.tight_layout()

            elif selected_indicator == "ADX(14)":
                    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
                    ax1.plot(df.index, df['ADX(14)'], label='ADX(14)', color='#FFFF00')
                    ax1.set_title('ADX(14)', fontsize=12, fontweight='bold')
                    ax1.grid(True, linestyle="--", alpha=0.6)
                    ax2.plot(df.index, df["Close"], label="1Y Price", color="blue")
                    ax2.set_title("1 Yıllık Fiyat Hareketleri", fontsize=12, fontweight="bold")
                    ax2.set_ylabel("Fiyat ($)")
                    ax2.set_xlabel("Tarih")
                    ax2.grid(True, linestyle="--", alpha=0.6)
                    plt.tight_layout()

            elif selected_indicator == "VOLUME":
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

                colors = ['green' if row['Close'] >= row['Open'] else 'red' for idx, row in df.iterrows()]
                ax1.bar(df.index, df["Volume"], color=colors, label="İşlem Hacmi")

 
                avg_volume = df["Volume"].mean()
                ax1.axhline(avg_volume, color='orange', linestyle='--', linewidth=2, label=f"Ortalama Hacim: {int(avg_volume/1e6)}M")

                ax1.set_title("İşlem Hacmi (Hacim Mumları)", fontsize=10)
                ax1.set_ylabel("Hacim")


                max_vol = df["Volume"].max()
                step = max_vol / 4  
                y_ticks = [int(step * i) for i in range(5)]
                ax1.set_yticks(y_ticks)
                ax1.set_yticklabels([f"{int(y/1e6)}M" for y in y_ticks])

                ax1.grid(True, linestyle="-", alpha=0.6)
                ax1.legend()
                ax2.plot(df.index, df["Close"], label="1Y Price", color="blue")
                ax2.set_title("1 Yıllık Fiyat Hareketleri", fontsize=12, fontweight="bold")
                ax2.set_ylabel("Fiyat ($)")
                ax2.set_xlabel("Tarih")
                ax2.grid(True, linestyle="--", alpha=0.6)
                ax2.legend()
                plt.tight_layout()
                
            elif selected_indicator == "Bollinger Bands":
                fig, ax = plt.subplots(figsize=(13, 6))

                ax.plot(df.index, df['Close'], label='Kapanış', color='#00FF00', linewidth=1.5)
                ax.plot(df.index, df['BB_High'], label='Üst Bant', color='#FF0000', linewidth=1)
                ax.plot(df.index, df['BB_Low'], label='Alt Bant', color='#0000FF', linewidth=1)
                ax.plot(df.index, df['BB_Mid'], label='Orta Bant', color='#FFA500', linestyle="--", linewidth=1)

                mask = ~df[['BB_High', 'BB_Low']].isnull().any(axis=1)
                ax.fill_between(df.index, df['BB_Low'], df['BB_High'], where=mask, color='gray', alpha=0.3)

                future_limit = df.index[-1] + pd.Timedelta(days=5)
                ax.set_xlim(df.index[0], future_limit)

                ax.set_title('Bollinger Bands')
                ax.set_facecolor(self.colors['plot_bg']) 
                ax.grid(True, linestyle='--', alpha=0.5)
                ax.legend(loc='upper left')
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))

                plt.tight_layout()
        
            elif selected_indicator == "Fibonacci Pivot":

                high = df['High'].iloc[-1]
                low = df['Low'].iloc[-1]
                close = df['Close'].iloc[-1]

                pivot = (high + low + close) / 3
                r1 = (2 * pivot) - low
                s1 = (2 * pivot) - high
                r2 = pivot + (r1 - s1)
                s2 = pivot - (r1 - s1)
                r3 = high + 2 * (pivot - low)
                s3 = low - 2 * (high - pivot)

                df['Pivot_Fib'] = pivot
                df['R1_Fib'] = r1
                df['S1_Fib'] = s1
                df['R2_Fib'] = r2
                df['S2_Fib'] = s2
                df['R3_Fib'] = r3
                df['S3_Fib'] = s3
   
                fig, ax = plt.subplots(figsize=(12, 6))  
                ax.plot(df.index, df['Close'], label='Fiyat', color='green', linewidth=2, linestyle='solid', alpha=0.9, zorder=5)


                ax.axhline(pivot, color='orange', linestyle='dashed', alpha=0.8, label='Pivot (P)')
                ax.axhline(r1, color='lightcoral', linestyle='dashed', alpha=0.7, label='Direnç 1 (R1)')
                ax.axhline(s1, color='lightgreen', linestyle='dashed', alpha=0.7, label='Destek 1 (S1)')
                ax.axhline(r2, color='red', linestyle='dashed', alpha=0.6, label='Direnç 2 (R2)')
                ax.axhline(s2, color='green', linestyle='dashed', alpha=0.6, label='Destek 2 (S2)')
                ax.axhline(r3, color='darkred', linestyle='dashed', alpha=0.5, label='Direnç 3 (R3)')
                ax.axhline(s3, color='darkgreen', linestyle='dashed', alpha=0.5, label='Destek 3 (S3)')

                ax.set_title('Fibonacci Pivot Noktaları', fontsize=12, fontweight='bold')
                ax.legend(loc='best')
                ax.grid(True, linestyle='--', alpha=0.6)
            
            elif selected_indicator == "Williams %R":
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
                ax1.plot(df.index, df["Williams %R"], label="Williams %R", color="yellow")
                ax1.axhline(-20, color='red', linestyle='--', alpha=0.7)  
                ax1.axhline(-80, color='green', linestyle='--', alpha=0.7) 
                ax1.set_ylim(-100, 0)
                ax1.set_title("Williams %R", fontsize=12, fontweight="bold")
                ax1.grid(True, linestyle="--", alpha=0.6)
                ax2.plot(df.index, df["Close"], label="1Y Price", color="blue")
                ax2.set_title("1 Yıllık Fiyat Hareketleri", fontsize=12, fontweight="bold")
                ax2.set_ylabel("Fiyat ($)")
                ax2.set_xlabel("Tarih")
                ax2.grid(True, linestyle="--", alpha=0.6)
                plt.tight_layout()

            elif selected_indicator == "CCI(14)":
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
                ax1.plot(df.index, df["CCI(14)"], label="CCI(14)", color="cyan")
                ax1.axhline(100, color='red', linestyle='--', alpha=0.7) 
                ax1.axhline(-100, color='green', linestyle='--', alpha=0.7) 
                ax1.set_title("CCI(14)", fontsize=12, fontweight="bold")
                ax1.grid(True, linestyle="--", alpha=0.6)
                ax2.plot(df.index, df["Close"], label="1Y Price", color="blue")
                ax2.set_title("1 Yıllık Fiyat Hareketleri", fontsize=12, fontweight="bold")
                ax2.set_ylabel("Fiyat ($)")
                ax2.set_xlabel("Tarih")
                ax2.grid(True, linestyle="--", alpha=0.6)
                plt.tight_layout()
        
            elif selected_indicator == "ATR%(14)":
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
                ax1.plot(df.index, df["ATR%(14)"], label="ATR%(14)", color="magenta")
                ax1.set_title("ATR%(14) - Average True Range", fontsize=12, fontweight="bold")
                ax1.grid(True, linestyle="--", alpha=0.6)
                ax2.plot(df.index, df["Close"], label="1Y Price", color="blue")
                ax2.set_title("1 Yıllık Fiyat Hareketleri", fontsize=12, fontweight="bold")
                ax2.set_ylabel("Fiyat ($)")
                ax2.set_xlabel("Tarih")
                ax2.grid(True, linestyle="--", alpha=0.6)
                plt.tight_layout()
       
            elif selected_indicator == "ROC":
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
                ax1.plot(df.index, df["ROC"], label="ROC", color="orange")
                ax1.axhline(0, color='white', linestyle='--', alpha=0.7)  
                ax1.set_title("ROC - Rate of Change", fontsize=12, fontweight="bold")
                ax1.grid(True, linestyle="--", alpha=0.6)
                ax2.plot(df.index, df["Close"], label="1Y Price", color="blue")
                ax2.set_title("1 Yıllık Fiyat Hareketleri", fontsize=12, fontweight="bold")
                ax2.set_ylabel("Fiyat ($)")
                ax2.set_xlabel("Tarih")
                ax2.grid(True, linestyle="--", alpha=0.6)
                plt.tight_layout()
            elif selected_indicator == "Parabolic_SAR":
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.plot(df.index, df["Close"], label="Close Price", color="blue", linewidth=2)
                ax.scatter(df.index, df["Parabolic_SAR"], label="Parabolic SAR", color="red", marker='.', s=30)
                ax.set_title("Parabolic SAR ve Fiyat Grafiği", fontsize=12, fontweight="bold")
                ax.set_ylabel("Fiyat ($)")
                ax.set_xlabel("Tarih")
                ax.grid(True, linestyle="--", alpha=0.6)
                ax.legend()
    
                plt.tight_layout()

            elif selected_indicator == "Ultimate Oscillator":
                    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
                    ax1.plot(df.index, df["Ultimate Oscillator"], label="Ultimate Oscillator", color="purple")
                    ax1.axhline(70, color='red', linestyle='--', alpha=0.7)  
                    ax1.axhline(30, color='green', linestyle='--', alpha=0.7)  
                    ax1.set_ylim(0, 100)
                    ax1.set_title("Ultimate Oscillator", fontsize=12, fontweight="bold")
                    ax1.grid(True, linestyle="--", alpha=0.6)
                    ax2.plot(df.index, df["Close"], label="1Y Price", color="blue")
                    ax2.set_title("1 Yıllık Fiyat Hareketleri", fontsize=12, fontweight="bold")
                    ax2.set_ylabel("Fiyat ($)")
                    ax2.set_xlabel("Tarih")
                    ax2.grid(True, linestyle="--", alpha=0.6)
                    plt.tight_layout()

            elif selected_indicator == "MFI(14)":
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    
                ax1.plot(df.index, df["MFI(14)"], label="MFI(14)", color="lime")
                ax1.axhline(80, color='red', linestyle='--', alpha=0.7)  
                ax1.axhline(20, color='green', linestyle='--', alpha=0.7)  
                ax1.set_ylim(0, 100)
                ax1.set_title("Money Flow Index (MFI 14)", fontsize=12, fontweight="bold")
                ax1.grid(True, linestyle="--", alpha=0.6)


                ax2.plot(df.index, df["Close"], label="1Y Fiyat", color="blue")
                ax2.set_title("1 Yıllık Fiyat Hareketleri", fontsize=12, fontweight="bold")
                ax2.set_ylabel("Fiyat ($)")
                ax2.set_xlabel("Tarih")
                ax2.grid(True, linestyle="--", alpha=0.6)
    
  
                plt.tight_layout()

            elif selected_indicator == "OBV":
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
   
                ax1.plot(df.index, df["OBV"], label="OBV", color="pink")
                ax1.set_title("On-Balance Volume (OBV)", fontsize=12, fontweight="bold")
                ax1.set_ylabel("OBV Değeri")
                ax1.grid(True, linestyle="--", alpha=0.6)
                ax1.legend(loc="upper left")
    
  
                ax2.plot(df.index, df["Close"], label="1Y Fiyat", color="blue")
                ax2.set_title("1 Yıllık Fiyat Hareketleri", fontsize=12, fontweight="bold")
                ax2.set_ylabel("Fiyat ($)")
                ax2.set_xlabel("Tarih")
                ax2.grid(True, linestyle="--", alpha=0.6)
                ax2.legend(loc="upper left")
    
                plt.tight_layout()

            elif selected_indicator == "VWAP":
                fig, ax1 = plt.subplots(figsize=(12, 6))
                ax1.plot(df.index, df["VWAP"], label="VWAP", color="brown", linestyle="--")
                ax1.plot(df.index, df["Close"], label="Anlık Fiyat", color="green")  
                ax1.set_title("VWAP ve Anlık Fiyat", fontsize=12, fontweight="bold")
                ax1.set_ylabel("Fiyat ($)")
                ax1.set_xlabel("Tarih")
                ax1.legend()
                ax1.grid(True, linestyle="--", alpha=0.6)
                plt.tight_layout()

            elif selected_indicator == "CMF":
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
                ax1.plot(df.index, df["CMF"], label="CMF", color="red")
                ax1.axhline(0, color='white', linestyle='--', alpha=0.7)  
                ax1.set_title("Chaikin Money Flow (CMF)", fontsize=12, fontweight="bold")
                ax1.grid(True, linestyle="--", alpha=0.6)
                ax2.plot(df.index, df["Close"], label="1Y Price", color="blue")
                ax2.set_title("1 Yıllık Fiyat Hareketleri", fontsize=12, fontweight="bold")
                ax2.set_ylabel("Fiyat ($)")
                ax2.set_xlabel("Tarih")
                ax2.grid(True, linestyle="--", alpha=0.6)
                plt.tight_layout()

                
            elif selected_indicator == "SuperTrend":

                def calculate_supertrend(df, period=10, multiplier=3):
                    atr = ta.volatility.AverageTrueRange(
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'],
                        window=period
                    ).average_true_range()

                    hl2 = (df['High'] + df['Low']) / 2
                    upper_band = hl2 + multiplier * atr
                    lower_band = hl2 - multiplier * atr

                    supertrend = [np.nan] * len(df)
                    direction = [True] * len(df)  

                    for i in range(period, len(df)):
                        if i == period:
                            supertrend[i] = lower_band[i]
                            direction[i] = True
                            continue

                        curr_close = df['Close'][i]

                        prev_supertrend = supertrend[i - 1]
                        prev_direction = direction[i - 1]

                   
                        if curr_close > prev_supertrend:
                            direction[i] = True
                        elif curr_close < prev_supertrend:
                            direction[i] = False
                        else:
                            direction[i] = prev_direction

                        if direction[i]:
                       
                            supertrend[i] = max(lower_band[i], prev_supertrend if prev_direction else lower_band[i])
                        else:
                        
                            supertrend[i] = min(upper_band[i], prev_supertrend if not prev_direction else upper_band[i])

                    df['SuperTrend'] = supertrend
                    df['SuperTrend_Direction'] = direction
                    return df
                
                df = calculate_supertrend(df)
            
                fig, ax = plt.subplots(figsize=(14, 7), sharex=True)
                ax.plot(df.index, df["Close"], label="Fiyat", color="blue", linewidth=1.5)
                
              
                for i in range(1, len(df)):
                    if pd.notna(df["SuperTrend"].iloc[i]) and pd.notna(df["SuperTrend"].iloc[i - 1]):
                        color = "green" if df["SuperTrend_Direction"].iloc[i] else "red"
                        ax.plot(df.index[i - 1:i + 1], df["SuperTrend"].iloc[i - 1:i + 1], color=color, linewidth=2)
                
                ax.plot([], [], color="green", label="SuperTrend (AL)")
                ax.plot([], [], color="red", label="SuperTrend (SAT)")


                ax.set_title(f"{selected_stock} - SuperTrend (Fiyat ile Birlikte)", fontsize=13, fontweight="bold")
                ax.set_ylabel("Fiyat ($)")
                ax.set_xlabel("Tarih")
                ax.grid(True, linestyle="--", alpha=0.6)
                ax.legend()


                plt.tight_layout()

        
            elif selected_indicator == "Ichimoku":
                 
                    high_9 = df['High'].rolling(window=9).max()
                    low_9 = df['Low'].rolling(window=9).min()
                    df['Tenkan_Sen'] = (high_9 + low_9) / 2

                    high_26 = df['High'].rolling(window=26).max()
                    low_26 = df['Low'].rolling(window=26).min()
                    df['Kijun_Sen'] = (high_26 + low_26) / 2

                    df['Senkou_Span_A'] = ((df['Tenkan_Sen'] + df['Kijun_Sen']) / 2).shift(26)

                    high_52 = df['High'].rolling(window=52).max()
                    low_52 = df['Low'].rolling(window=52).min()
                    df['Senkou_Span_B'] = ((high_52 + low_52) / 2).shift(26)

                    df['Chikou_Span'] = df['Close'].shift(-26)

               
                    future_dates = pd.date_range(start=df.index[-1], periods=27, freq='B')[1:]
                    future_df = pd.DataFrame(index=future_dates)
                    
                   
                    future_span_a = ((df['Tenkan_Sen'].iloc[-26:] + df['Kijun_Sen'].iloc[-26:]) / 2).values
                    future_span_b = ((df['High'].rolling(window=52).max().iloc[-26:] + df['Low'].rolling(window=52).min().iloc[-26:]) / 2).values

                  
                    future_df['Senkou_Span_A'] = future_span_a
                    future_df['Senkou_Span_B'] = future_span_b

                    df = pd.concat([df, future_df])
                    df.update(future_df)

                    fig, ax = plt.subplots(figsize=(13, 6))

                    ax.plot(df.index, df['Close'], label='Kapanış Fiyatı', color='white', linewidth=2, zorder=5)

                    ax.plot(df.index, df['Tenkan_Sen'], label='Tenkan-Sen (9)', color='red', linestyle='--', linewidth=1.5)
                    ax.plot(df.index, df['Kijun_Sen'], label='Kijun-Sen (26)', color='blue', linestyle='--', linewidth=1.5)
                    ax.plot(df.index, df['Chikou_Span'], label='Chikou Span (-26)', color='yellow', linewidth=1.2, alpha=0.7)


                    span_a = df['Senkou_Span_A']
                    span_b = df['Senkou_Span_B']
                    mask = ~df[['Senkou_Span_A', 'Senkou_Span_B']].isnull().any(axis=1)

                    ax.fill_between(df.index, span_a, span_b,
                    where=(span_a >= span_b) & mask,
                    color='lightgreen', alpha=0.4, label='Bulut (Yeşil)')
                    ax.fill_between(df.index, span_a, span_b,
                    where=(span_a < span_b) & mask,
                    color='lightcoral', alpha=0.4, label='Bulut (Kırmızı)')
   
                    ax.plot(df.index, df['Senkou_Span_A'], color='green', linestyle='-', linewidth=1, label='Senkou Span A')
                    ax.plot(df.index, df['Senkou_Span_B'], color='red', linestyle='-', linewidth=1, label='Senkou Span B')

                    future_limit = df.index[-1] + pd.Timedelta(days=5) 
                    ax.set_xlim(df.index[0], future_limit)

                    ax.set_title("Ichimoku Bulutu (9, 26, 52, 26) - Yahoo Finance Stili", fontsize=12, fontweight="bold")
                    ax.set_facecolor(self.colors['plot_bg'])
                    ax.grid(True, linestyle='--', alpha=0.6)
                    ax.legend(loc='upper left')
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))

                    plt.tight_layout()

  
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()

            self.current_canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            self.current_canvas.draw()
            self.current_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Hata", f"Grafik oluşturulamadı: {str(e)}")
    
    def predict_stock_lr_rolling_10gun(self):
        self.text_box.delete('1.0', tk.END)
        selected_stock = self.stock_var.get()
        if not selected_stock:
            self.text_box.insert(tk.END, "Lütfen bir finansal enstrüman seçin!\n")
            return

        ticker = self.tickers[selected_stock]

        try:
            data = yf.download(ticker, period='2y')
            if data.empty:
                self.text_box.insert(tk.END, f"{ticker} için veri bulunamadı!\n")
                return

            df = data.copy()
            df = df[-386:]

        
            df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA_20_bin'] = (df['EMA_20'] > df['EMA_20'].shift(1)).astype(int)

            df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
            df['EMA_50_bin'] = (df['EMA_50'] > df['EMA_50'].shift(1)).astype(int)

           
            delta = df['Close'].diff(1)
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI_14'] = 100 - (100 / (1 + rs))
            ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
            ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = ema_12 - ema_26
            df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            high14 = df['High'].rolling(window=14).max()
            low14 = df['Low'].rolling(window=14).min()
            df['Williams_%R'] = -100 * (high14 - df['Close']) / (high14 - low14)

            df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
            df.dropna(inplace=True)
           
            tahvil = yf.download('^TNX', start=df.index.min(), end=df.index.max())
            df['TNX'] = tahvil['Close']
            df['TNX'] = df['TNX'].fillna(method='ffill')

    
            features = [
                'RSI_14', 'MACD', 'Williams_%R','TNX','EMA_20_bin', 'EMA_50_bin','TNX'
]
            window_size = 10
            train_ratio = 0.8
            train_size = int(window_size * train_ratio)
            test_size = window_size - train_size

            scores = []

            for i in range(36):
                start_idx = i * window_size
                end_idx = start_idx + window_size

                window_df = df.iloc[start_idx:end_idx]

                if len(window_df) < window_size:
                    self.text_box.insert(tk.END, f"{i+1}. pencere için yeterli veri yok, atlanıyor...\n")
                    continue

                X = window_df[features]
                y = window_df['Target']

                X_train = X.iloc[:train_size]
                y_train = y.iloc[:train_size]
                X_test = X.iloc[train_size:]
                y_test = y.iloc[train_size:]

                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)

                model = LinearRegression()
                model.fit(X_train_scaled, y_train)
                y_pred_proba = model.predict(X_test_scaled)
                y_pred = (y_pred_proba > 0.5).astype(int)

                cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
                report = classification_report(y_test, y_pred, output_dict=True)

                accuracy = report['accuracy']
                f1 = report.get('1', {}).get('f1-score', 0)

                self.text_box.insert(tk.END, f"{i+1}. pencere sonuçları (gün {start_idx}-{end_idx}):\n")
                self.text_box.insert(tk.END, classification_report(y_test, y_pred) + "\n")
                self.text_box.insert(tk.END, f"Confusion Matrix (gün {start_idx}-{end_idx}):\n{cm}\n\n")
                scores.append({'accuracy': accuracy, 'f1_score': f1})

            if scores:
                avg_accuracy = sum(s['accuracy'] for s in scores) / len(scores)
                avg_f1 = sum(s['f1_score'] for s in scores) / len(scores)
                self.text_box.insert(tk.END, f"Ortalama Accuracy: {avg_accuracy:.2f}\n")
                self.text_box.insert(tk.END, f"Ortalama F1-Score (class 1): {avg_f1:.2f}\n")


            df_recent = df.tail(386)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop","12345")
            filename = f"son_360_gun_verisi_{timestamp}.xlsx"
            filepath = os.path.join(desktop_path, filename)
            df_recent.to_excel(filepath)
            self.text_box.insert(tk.END, f"📂 Dosya masaüstüne kaydedildi: {filepath}\n") 

        except Exception as e:
            self.text_box.insert(tk.END, f"Hata oluştu: {e}\n")

    def predict_stock_lr_rolling_3ay(self):
        self.text_box.delete('1.0', tk.END)
        selected_stock = self.stock_var.get()
        if not selected_stock:
            self.text_box.insert(tk.END, "Lütfen bir finansal enstrüman seçin!\n")
            return

        ticker = self.tickers[selected_stock]

        try:
            data = yf.download(ticker, period='2y')
            if data.empty:
                self.text_box.insert(tk.END, f"{ticker} için veri bulunamadı!\n")
                return

            df = data.copy()
            df = df[-386:]

       
            df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA_20_bin'] = (df['EMA_20'] > df['EMA_20'].shift(1)).astype(int)

            df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
            df['EMA_50_bin'] = (df['EMA_50'] > df['EMA_50'].shift(1)).astype(int)

           
            delta = df['Close'].diff(1)
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI_14'] = 100 - (100 / (1 + rs))
            ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
            ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = ema_12 - ema_26
            df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            high14 = df['High'].rolling(window=14).max()
            low14 = df['Low'].rolling(window=14).min()
            df['Williams_%R'] = -100 * (high14 - df['Close']) / (high14 - low14)

            df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
            df.dropna(inplace=True)
           
            tahvil = yf.download('^TNX', start=df.index.min(), end=df.index.max())
            df['TNX'] = tahvil['Close']
            df['TNX'] = df['TNX'].fillna(method='ffill')

    
            features = [
                'RSI_14', 'MACD', 'Williams_%R','TNX','EMA_20_bin', 'EMA_50_bin'
]
            window_size = 90
            train_ratio = 0.8
            train_size = int(window_size * train_ratio)
            test_size = window_size - train_size

            scores = []

            for i in range(4):
                start_idx = i * window_size
                end_idx = start_idx + window_size

                window_df = df.iloc[start_idx:end_idx]

                if len(window_df) < window_size:
                    self.text_box.insert(tk.END, f"{i+1}. pencere için yeterli veri yok, atlanıyor...\n")
                    continue

                X = window_df[features]
                y = window_df['Target']

                X_train = X.iloc[:train_size]
                y_train = y.iloc[:train_size]
                X_test = X.iloc[train_size:]
                y_test = y.iloc[train_size:]

                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)

                model = LinearRegression()
                model.fit(X_train_scaled, y_train)
                y_pred_proba = model.predict(X_test_scaled)
                y_pred = (y_pred_proba > 0.5).astype(int)

                cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
                report = classification_report(y_test, y_pred, output_dict=True)

                accuracy = report['accuracy']
                f1 = report.get('1', {}).get('f1-score', 0)

                self.text_box.insert(tk.END, f"{i+1}. pencere sonuçları (gün {start_idx}-{end_idx}):\n")
                self.text_box.insert(tk.END, classification_report(y_test, y_pred) + "\n")
                self.text_box.insert(tk.END, f"Confusion Matrix (gün {start_idx}-{end_idx}):\n{cm}\n\n")
                scores.append({'accuracy': accuracy, 'f1_score': f1})

            if scores:
                avg_accuracy = sum(s['accuracy'] for s in scores) / len(scores)
                avg_f1 = sum(s['f1_score'] for s in scores) / len(scores)
                self.text_box.insert(tk.END, f"Ortalama Accuracy: {avg_accuracy:.2f}\n")
                self.text_box.insert(tk.END, f"Ortalama F1-Score (class 1): {avg_f1:.2f}\n")

        except Exception as e:
            self.text_box.insert(tk.END, f"Hata oluştu: {e}\n")

    def predict_stock_lr_rolling_6ay(self):
        self.text_box.delete('1.0', tk.END)
        selected_stock = self.stock_var.get()
        if not selected_stock:
            self.text_box.insert(tk.END, "Lütfen bir finansal enstrüman seçin!\n")
            return

        ticker = self.tickers[selected_stock]

        try:
            data = yf.download(ticker, period='2y')
            if data.empty:
                self.text_box.insert(tk.END, f"{ticker} için veri bulunamadı!\n")
                return

            df = data.copy()
            
            df = df[-386:]


            df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA_20_bin'] = (df['EMA_20'] > df['EMA_20'].shift(1)).astype(int)

            df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
            df['EMA_50_bin'] = (df['EMA_50'] > df['EMA_50'].shift(1)).astype(int)

           
            delta = df['Close'].diff(1)
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI_14'] = 100 - (100 / (1 + rs))
            ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
            ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = ema_12 - ema_26
            df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            high14 = df['High'].rolling(window=14).max()
            low14 = df['Low'].rolling(window=14).min()
            df['Williams_%R'] = -100 * (high14 - df['Close']) / (high14 - low14)

            df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
            df.dropna(inplace=True)
           
            tahvil = yf.download('^TNX', start=df.index.min(), end=df.index.max())
            df['TNX'] = tahvil['Close']
            df['TNX'] = df['TNX'].fillna(method='ffill')

    
            features = [
                'RSI_14', 'MACD', 'Williams_%R','TNX','EMA_20_bin', 'EMA_50_bin'
]
            window_size = 180
            train_ratio = 0.8
            train_size = int(window_size * train_ratio)
            test_size = window_size - train_size

            scores = []

            for i in range(2):
                start_idx = i * window_size
                end_idx = start_idx + window_size

                window_df = df.iloc[start_idx:end_idx]

                if len(window_df) < window_size:
                    self.text_box.insert(tk.END, f"{i+1}. pencere için yeterli veri yok, atlanıyor...\n")
                    continue

                X = window_df[features]
                y = window_df['Target']

                X_train = X.iloc[:train_size]
                y_train = y.iloc[:train_size]
                X_test = X.iloc[train_size:]
                y_test = y.iloc[train_size:]

                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)

                model = LinearRegression()
                model.fit(X_train_scaled, y_train)
                y_pred_proba = model.predict(X_test_scaled)
                y_pred = (y_pred_proba > 0.5).astype(int)

                cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
                report = classification_report(y_test, y_pred, output_dict=True)

                accuracy = report['accuracy']
                f1 = report.get('1', {}).get('f1-score', 0)

                self.text_box.insert(tk.END, f"{i+1}. pencere sonuçları (gün {start_idx}-{end_idx}):\n")
                self.text_box.insert(tk.END, classification_report(y_test, y_pred) + "\n")
                self.text_box.insert(tk.END, f"Confusion Matrix (gün {start_idx}-{end_idx}):\n{cm}\n\n")
                scores.append({'accuracy': accuracy, 'f1_score': f1})

            if scores:
                avg_accuracy = sum(s['accuracy'] for s in scores) / len(scores)
                avg_f1 = sum(s['f1_score'] for s in scores) / len(scores)
                self.text_box.insert(tk.END, f"Ortalama Accuracy: {avg_accuracy:.2f}\n")
                self.text_box.insert(tk.END, f"Ortalama F1-Score (class 1): {avg_f1:.2f}\n")

        except Exception as e:
            self.text_box.insert(tk.END, f"Hata oluştu: {e}\n")
    
    def predict_stock_lr_rolling_1ay(self):
        self.text_box.delete('1.0', tk.END)
        selected_stock = self.stock_var.get()
        if not selected_stock:
            self.text_box.insert(tk.END, "Lütfen bir finansal enstrüman seçin!\n")
            return

        ticker = self.tickers[selected_stock]

        try:
            data = yf.download(ticker, period='2y')
            if data.empty:
                self.text_box.insert(tk.END, f"{ticker} için veri bulunamadı!\n")
                return

            df = data.copy()
            df = df[-386:]

            df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA_20_bin'] = (df['EMA_20'] > df['EMA_20'].shift(1)).astype(int)

            df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
            df['EMA_50_bin'] = (df['EMA_50'] > df['EMA_50'].shift(1)).astype(int)

           
            delta = df['Close'].diff(1)
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI_14'] = 100 - (100 / (1 + rs))
            ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
            ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = ema_12 - ema_26
            df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            high14 = df['High'].rolling(window=14).max()
            low14 = df['Low'].rolling(window=14).min()
            df['Williams_%R'] = -100 * (high14 - df['Close']) / (high14 - low14)

            df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
            df.dropna(inplace=True)
           
            tahvil = yf.download('^TNX', start=df.index.min(), end=df.index.max())
            df['TNX'] = tahvil['Close']
            df['TNX'] = df['TNX'].fillna(method='ffill')

    
            features = [
                'RSI_14', 'MACD', 'Williams_%R', 'EMA_20_bin', 'EMA_50_bin','TNX'
]
            window_size = 30
            train_ratio = 0.8
            train_size = int(window_size * train_ratio)
            test_size = window_size - train_size
            scores = []
                

            for i in range(12):
                start_idx = i * window_size
                end_idx = start_idx + window_size
                window_df = df.iloc[start_idx:end_idx]

                if len(window_df) < window_size:
                    self.text_box.insert(tk.END, f"{i+1}. pencere için yeterli veri yok, atlanıyor...\n")
                    continue

                X = window_df[features]
                y = window_df['Target']

                X_train = X.iloc[:train_size]
                y_train = y.iloc[:train_size]
                X_test = X.iloc[train_size:]
                y_test = y.iloc[train_size:]

                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)

                model = LinearRegression()
                model.fit(X_train_scaled, y_train)
                y_pred_proba = model.predict(X_test_scaled)
                y_pred = (y_pred_proba > 0.5).astype(int)

                cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
                report = classification_report(y_test, y_pred, output_dict=True)

                accuracy = report['accuracy']
                f1 = report.get('1', {}).get('f1-score', 0)

                self.text_box.insert(tk.END, f"{i+1}. pencere sonuçları (gün {start_idx}-{end_idx}):\n")
                self.text_box.insert(tk.END, classification_report(y_test, y_pred) + "\n")
                self.text_box.insert(tk.END, f"Confusion Matrix (gün {start_idx}-{end_idx}):\n{cm}\n\n")
                scores.append({'accuracy': accuracy, 'f1_score': f1})

            if scores:
                avg_accuracy = sum(s['accuracy'] for s in scores) / len(scores)
                avg_f1 = sum(s['f1_score'] for s in scores) / len(scores)
                self.text_box.insert(tk.END, f"Ortalama Accuracy: {avg_accuracy:.2f}\n")
                self.text_box.insert(tk.END, f"Ortalama F1-Score (class 1): {avg_f1:.2f}\n")

        except Exception as e:
                self.text_box.insert(tk.END, f"Hata oluştu: {e}\n")

    def predict_stock_svm_rolling_10gun(self):
        self.text_box.delete('1.0', tk.END)
        selected_stock = self.stock_var.get()
        if not selected_stock:
            self.text_box.insert(tk.END, "Lütfen bir finansal enstrüman seçin!\n")
            return

        ticker = self.tickers[selected_stock]

        try:
        
            data = yf.download(ticker, period='2y')  
            if data.empty:
                self.text_box.insert(tk.END, f"{ticker} için veri bulunamadı!\n")
                return

            df = data.copy()
            df = df[-386:]


            df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA_20_bin'] = (df['EMA_20'] > df['EMA_20'].shift(1)).astype(int)

            df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
            df['EMA_50_bin'] = (df['EMA_50'] > df['EMA_50'].shift(1)).astype(int)

           
            delta = df['Close'].diff(1)
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI_14'] = 100 - (100 / (1 + rs))
            ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
            ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = ema_12 - ema_26
            df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            high14 = df['High'].rolling(window=14).max()
            low14 = df['Low'].rolling(window=14).min()
            df['Williams_%R'] = -100 * (high14 - df['Close']) / (high14 - low14)

            df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
            df.dropna(inplace=True)
           
            tahvil = yf.download('^TNX', start=df.index.min(), end=df.index.max())
            df['TNX'] = tahvil['Close']
            df['TNX'] = df['TNX'].fillna(method='ffill')

    
            features = [
                'RSI_14', 'MACD', 'Williams_%R','TNX' ,'EMA_20_bin', 'EMA_50_bin'
]

            window_size = 10
            train_ratio = 0.8
            train_size = int(window_size * train_ratio)  
            test_size = window_size - train_size        

            scores = []


            for i in range(36):
                start_idx = i * window_size
                end_idx = start_idx + window_size

                window_df = df.iloc[start_idx:end_idx]

                if len(window_df) < window_size:
                    self.text_box.insert(tk.END, f"{i+1}. pencere için yeterli veri yok, atlanıyor...\n")
                    continue

                X = window_df[features]
                y = window_df['Target']

                X_train = X.iloc[:train_size]
                y_train = y.iloc[:train_size]
                X_test = X.iloc[train_size:]
                y_test = y.iloc[train_size:]

                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)

                if len(y_train.unique()) < 2:
                    self.text_box.insert(tk.END, f"{i+1}. pencere için yeterli sınıf çeşitliliği yok, atlanıyor...\n")
                    continue


                model = SVC(kernel='rbf', C=1.0, gamma='scale')
                model.fit(X_train_scaled, y_train)

                y_pred = model.predict(X_test_scaled)
                cm = confusion_matrix(y_test, y_pred, labels=[0,1])
                
                report = classification_report(y_test, y_pred, output_dict=True)

                accuracy = report['accuracy']
                f1 = report.get('1', {}).get('f1-score', 0)

                self.text_box.insert(tk.END, f"{i+1}. pencere sonuçları (gün {start_idx}-{end_idx}):\n")
                self.text_box.insert(tk.END, classification_report(y_test, y_pred) + "\n")
                scores.append({'accuracy': accuracy, 'f1_score': f1})
               
                self.text_box.insert(tk.END, f"Confusion Matrix (gün {start_idx}-{end_idx}):\n{cm}\n\n")



            if scores:
                avg_accuracy = sum(s['accuracy'] for s in scores) / len(scores)
                avg_f1 = sum(s['f1_score'] for s in scores) / len(scores)
                self.text_box.insert(tk.END, f"Ortalama Accuracy: {avg_accuracy:.2f}\n")
                self.text_box.insert(tk.END, f"Ortalama F1-Score (class 1): {avg_f1:.2f}\n")

            #df_recent = df.tail(379)
            #timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            #desktop_path = os.path.join(os.path.expanduser("~"), "Desktop","12345")
            #filename = f"son_360_gun_verisi_{timestamp}.xlsx"
            #filepath = os.path.join(desktop_path, filename)
            #df_recent.to_excel(filepath)
            #self.text_box.insert(tk.END, f"📂 Dosya masaüstüne kaydedildi: {filepath}\n") 

        except Exception as e:
            self.text_box.insert(tk.END, f"Hata oluştu: {e}\n")
    
    def predict_stock_svm_rolling_3ay(self):
        self.text_box.delete('1.0', tk.END)
        selected_stock = self.stock_var.get()
        if not selected_stock:
            self.text_box.insert(tk.END, "Lütfen bir finansal enstrüman seçin!\n")
            return

        ticker = self.tickers[selected_stock]

        try:

            data = yf.download(ticker, period='2y')  
            if data.empty:
                self.text_box.insert(tk.END, f"{ticker} için veri bulunamadı!\n")
                return

            df = data.copy()
            df = df[-386:]

            df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA_20_bin'] = (df['EMA_20'] > df['EMA_20'].shift(1)).astype(int)

            df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
            df['EMA_50_bin'] = (df['EMA_50'] > df['EMA_50'].shift(1)).astype(int)

           
            delta = df['Close'].diff(1)
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI_14'] = 100 - (100 / (1 + rs))
            ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
            ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = ema_12 - ema_26
            df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            high14 = df['High'].rolling(window=14).max()
            low14 = df['Low'].rolling(window=14).min()
            df['Williams_%R'] = -100 * (high14 - df['Close']) / (high14 - low14)

            df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
            df.dropna(inplace=True)
           
            tahvil = yf.download('^TNX', start=df.index.min(), end=df.index.max())
            df['TNX'] = tahvil['Close']
            df['TNX'] = df['TNX'].fillna(method='ffill')

    
            features = [
                'RSI_14', 'MACD', 'Williams_%R','TNX' ,'EMA_20_bin', 'EMA_50_bin'
]

            window_size = 90
            train_ratio = 0.8
            train_size = int(window_size * train_ratio)  
            test_size = window_size - train_size        

            scores = []


            for i in range(4):
                start_idx = i * train_size
                end_idx = start_idx + window_size

                window_df = df.iloc[start_idx:end_idx]

                if len(window_df) < window_size:
                    self.text_box.insert(tk.END, f"{i+1}. pencere için yeterli veri yok, atlanıyor...\n")
                    continue

                X = window_df[features]
                y = window_df['Target']

                X_train = X.iloc[:train_size]
                y_train = y.iloc[:train_size]
                X_test = X.iloc[train_size:]
                y_test = y.iloc[train_size:]

                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)

                model = SVC(kernel='rbf', C=1.0, gamma='scale')
                model.fit(X_train_scaled, y_train)

                y_pred = model.predict(X_test_scaled)
                cm = confusion_matrix(y_test, y_pred, labels=[0,1])
                
                report = classification_report(y_test, y_pred, output_dict=True)

                accuracy = report['accuracy']
                f1 = report['1']['f1-score']

                self.text_box.insert(tk.END, f"{i+1}. pencere sonuçları (gün {start_idx}-{end_idx}):\n")
                self.text_box.insert(tk.END, classification_report(y_test, y_pred) + "\n")
                scores.append({'accuracy': accuracy, 'f1_score': f1})
                
                self.text_box.insert(tk.END, f"Confusion Matrix (gün {start_idx}-{end_idx}):\n{cm}\n\n")

   
            if scores:
                avg_accuracy = sum(s['accuracy'] for s in scores) / len(scores)
                avg_f1 = sum(s['f1_score'] for s in scores) / len(scores)
                self.text_box.insert(tk.END, f"Ortalama Accuracy: {avg_accuracy:.2f}\n")
                self.text_box.insert(tk.END, f"Ortalama F1-Score (class 1): {avg_f1:.2f}\n")

            #df_recent = df.tail(379)
            #timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            #desktop_path = os.path.join(os.path.expanduser("~"), "Desktop","12345")
            #filename = f"son_360_gun_verisi_{timestamp}.xlsx"
            #filepath = os.path.join(desktop_path, filename)
            #df_recent.to_excel(filepath)
            #self.text_box.insert(tk.END, f"📂 Dosya masaüstüne kaydedildi: {filepath}\n")

        except Exception as e:
            self.text_box.insert(tk.END, f"Hata oluştu: {e}\n")

    def predict_stock_svm_rolling_6ay(self):
        self.text_box.delete('1.0', tk.END)
        selected_stock = self.stock_var.get()
        if not selected_stock:
            self.text_box.insert(tk.END, "Lütfen bir finansal enstrüman seçin!\n")
            return

        ticker = self.tickers[selected_stock]

        try:

            data = yf.download(ticker, period='2y')  
            if data.empty:
                self.text_box.insert(tk.END, f"{ticker} için veri bulunamadı!\n")
                return

            df = data.copy()
            df = df[-386:]


            df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA_20_bin'] = (df['EMA_20'] > df['EMA_20'].shift(1)).astype(int)

            df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
            df['EMA_50_bin'] = (df['EMA_50'] > df['EMA_50'].shift(1)).astype(int)

           
            delta = df['Close'].diff(1)
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI_14'] = 100 - (100 / (1 + rs))
            ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
            ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = ema_12 - ema_26
            df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

            high14 = df['High'].rolling(window=14).max()
            low14 = df['Low'].rolling(window=14).min()
            df['Williams_%R'] = -100 * (high14 - df['Close']) / (high14 - low14)

            df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
            df.dropna(inplace=True)
           
            tahvil = yf.download('^TNX', start=df.index.min(), end=df.index.max())
            df['TNX'] = tahvil['Close']
            df['TNX'] = df['TNX'].fillna(method='ffill')

    
            features = [
                'RSI_14', 'MACD', 'Williams_%R','TNX','EMA_20_bin', 'EMA_50_bin'
]

            window_size = 180
            train_ratio = 0.8
            train_size = int(window_size * train_ratio)  
            test_size = window_size - train_size         

            scores = []


            for i in range(2):
                start_idx = i * window_size
                end_idx = start_idx + window_size

                window_df = df.iloc[start_idx:end_idx]

                if len(window_df) < window_size:
                    self.text_box.insert(tk.END, f"{i+1}. pencere için yeterli veri yok, atlanıyor...\n")
                    continue

                X = window_df[features]
                y = window_df['Target']

                X_train = X.iloc[:train_size]
                y_train = y.iloc[:train_size]
                X_test = X.iloc[train_size:]
                y_test = y.iloc[train_size:]

                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)

                model = SVC(kernel='rbf', C=1.0, gamma='scale')
                model.fit(X_train_scaled, y_train)

                y_pred = model.predict(X_test_scaled)
                cm = confusion_matrix(y_test, y_pred, labels=[0,1])
                
                report = classification_report(y_test, y_pred, output_dict=True)

                accuracy = report['accuracy']
                f1 = report['1']['f1-score']

                self.text_box.insert(tk.END, f"{i+1}. pencere sonuçları (gün {start_idx}-{end_idx}):\n")
                self.text_box.insert(tk.END, classification_report(y_test, y_pred) + "\n")
                scores.append({'accuracy': accuracy, 'f1_score': f1})
               
                self.text_box.insert(tk.END, f"Confusion Matrix (gün {start_idx}-{end_idx}):\n{cm}\n\n")


            if scores:
                avg_accuracy = sum(s['accuracy'] for s in scores) / len(scores)
                avg_f1 = sum(s['f1_score'] for s in scores) / len(scores)
                self.text_box.insert(tk.END, f"Ortalama Accuracy: {avg_accuracy:.2f}\n")
                self.text_box.insert(tk.END, f"Ortalama F1-Score (class 1): {avg_f1:.2f}\n")

            #df_recent = df.tail(379)
            #timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            #desktop_path = os.path.join(os.path.expanduser("~"), "Desktop","12345")
            #filename = f"son_360_gun_verisi_{timestamp}.xlsx"
            #filepath = os.path.join(desktop_path, filename)
            #df_recent.to_excel(filepath)
            #self.text_box.insert(tk.END, f"📂 Dosya masaüstüne kaydedildi: {filepath}\n")

        except Exception as e:
            self.text_box.insert(tk.END, f"Hata oluştu: {e}\n")

    def predict_stock_svm_rolling_1ay(self):
        self.text_box.delete('1.0', tk.END)
        selected_stock = self.stock_var.get()
        if not selected_stock:
            self.text_box.insert(tk.END, "Lütfen bir finansal enstrüman seçin!\n")
            return

        ticker = self.tickers[selected_stock]

        try:
            data = yf.download(ticker, period='2y')
            if data.empty:
                self.text_box.insert(tk.END, f"{ticker} için veri bulunamadı!\n")
                return

            df = data.copy()
            df = df[-386:]


            df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA_20_bin'] = (df['EMA_20'] > df['EMA_20'].shift(1)).astype(int)

            df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
            df['EMA_50_bin'] = (df['EMA_50'] > df['EMA_50'].shift(1)).astype(int)

           
            delta = df['Close'].diff(1)
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI_14'] = 100 - (100 / (1 + rs))
            ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
            ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = ema_12 - ema_26
            df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            high14 = df['High'].rolling(window=14).max()
            low14 = df['Low'].rolling(window=14).min()
            df['Williams_%R'] = -100 * (high14 - df['Close']) / (high14 - low14)

            df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
            df.dropna(inplace=True)
           
            tahvil = yf.download('^TNX', start=df.index.min(), end=df.index.max())
            df['TNX'] = tahvil['Close']
            df['TNX'] = df['TNX'].fillna(method='ffill')

    
            features = [
                'RSI_14', 'MACD', 'Williams_%R','TNX' ,'EMA_20_bin', 'EMA_50_bin'
]

            window_size = 30
            train_ratio = 0.8
            train_size = int(window_size * train_ratio)  
            test_size = window_size - train_size        

            scores = []

            for i in range(12):
                start_idx = i * window_size
                end_idx = start_idx + window_size

                window_df = df.iloc[start_idx:end_idx]

                if len(window_df) < window_size:
                    self.text_box.insert(tk.END, f"{i+1}. pencere için yeterli veri yok, atlanıyor...\n")
                    continue

                X = window_df[features]
                y = window_df['Target']

                X_train = X.iloc[:train_size]
                y_train = y.iloc[:train_size]
                X_test = X.iloc[train_size:]
                y_test = y.iloc[train_size:]

                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)

                model = SVC(kernel='rbf', C=1.0, gamma='scale')
                model.fit(X_train_scaled, y_train)

                y_pred = model.predict(X_test_scaled)
                cm = confusion_matrix(y_test, y_pred, labels=[0,1])
               
                report = classification_report(y_test, y_pred, output_dict=True)

                accuracy = report['accuracy']
                f1 = report['1']['f1-score']

                self.text_box.insert(tk.END, f"{i+1}. pencere sonuçları (gün {start_idx}-{end_idx}):\n")
                self.text_box.insert(tk.END, classification_report(y_test, y_pred) + "\n")
                scores.append({'accuracy': accuracy, 'f1_score': f1})
                
                self.text_box.insert(tk.END, f"Confusion Matrix (gün {start_idx}-{end_idx}):\n{cm}\n\n")

            if scores:
                avg_accuracy = sum(s['accuracy'] for s in scores) / len(scores)
                avg_f1 = sum(s['f1_score'] for s in scores) / len(scores)
                self.text_box.insert(tk.END, f"Ortalama Accuracy: {avg_accuracy:.2f}\n")
                self.text_box.insert(tk.END, f"Ortalama F1-Score (class 1): {avg_f1:.2f}\n")

            #df_recent = df.tail(379)
            #timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            #desktop_path = os.path.join(os.path.expanduser("~"), "Desktop","12345")
            #filename = f"son_360_gun_verisi_{timestamp}.xlsx"
            #filepath = os.path.join(desktop_path, filename)
            #df_recent.to_excel(filepath)
            #self.text_box.insert(tk.END, f"📂 Dosya masaüstüne kaydedildi: {filepath}\n")

        except Exception as e:
         self.text_box.insert(tk.END, f"Hata oluştu: {e}\n")

    def predict_stock_xgboost_rolling_10gun(self):
        self.text_box.delete('1.0', tk.END)
        selected_stock = self.stock_var.get()
        if not selected_stock:
            self.text_box.insert(tk.END, "Lütfen bir finansal enstrüman seçin!\n")
            return

        ticker = self.tickers[selected_stock]

        try:
            data = yf.download(ticker, period='2y')

            if data.empty:
                self.text_box.insert(tk.END, f"{ticker} için veri bulunamadı!\n")
                return

            df = data.copy()
            df = df[-386:]

            df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA_20_bin'] = (df['EMA_20'] > df['EMA_20'].shift(1)).astype(int)

            df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
            df['EMA_50_bin'] = (df['EMA_50'] > df['EMA_50'].shift(1)).astype(int)

           
            delta = df['Close'].diff(1)
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI_14'] = 100 - (100 / (1 + rs))
            ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
            ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = ema_12 - ema_26
            df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            high14 = df['High'].rolling(window=14).max()
            low14 = df['Low'].rolling(window=14).min()
            df['Williams_%R'] = -100 * (high14 - df['Close']) / (high14 - low14)

            df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
            df.dropna(inplace=True)
           
            tahvil = yf.download('^TNX', start=df.index.min(), end=df.index.max())
            df['TNX'] = tahvil['Close']
            df['TNX'] = df['TNX'].fillna(method='ffill')

    
            features = [
                'RSI_14', 'MACD', 'Williams_%R','TNX','EMA_20_bin', 'EMA_50_bin'
]
            window_size = 10
            train_ratio = 0.8
            train_size = int(window_size * train_ratio)
            test_size = window_size - train_size

            scores = []

            for i in range(36):
                start_idx = i * window_size
                end_idx = start_idx + window_size
                window_df = df.iloc[start_idx:end_idx]

                if len(window_df) < window_size:
                    self.text_box.insert(tk.END, f"{i+1}. pencere için yeterli veri yok, atlanıyor...\n")
                    continue

                X = window_df[features]
                y = window_df['Target']

                X_train = X.iloc[:train_size]
                y_train = y.iloc[:train_size]
                X_test = X.iloc[train_size:]
                y_test = y.iloc[train_size:]

                if len(y_train.unique()) < 2:
                    self.text_box.insert(tk.END, f"{i+1}. pencere y_train tek sınıf içeriyor, atlanıyor...\n")
                    continue

                model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
                report = classification_report(y_test, y_pred, output_dict=True)

                accuracy = report['accuracy']
                f1 = report.get('1', {}).get('f1-score', 0)

                self.text_box.insert(tk.END, f"{i+1}. pencere sonuçları (gün {start_idx}-{end_idx}):\n")
                self.text_box.insert(tk.END, classification_report(y_test, y_pred) + "\n")
                self.text_box.insert(tk.END, f"Confusion Matrix:\n{cm}\n\n")

                scores.append({'accuracy': accuracy, 'f1_score': f1})

            if scores:
                avg_accuracy = sum(s['accuracy'] for s in scores) / len(scores)
                avg_f1 = sum(s['f1_score'] for s in scores) / len(scores)
                self.text_box.insert(tk.END, f"Ortalama Accuracy: {avg_accuracy:.2f}\n")
                self.text_box.insert(tk.END, f"Ortalama F1-Score (class 1): {avg_f1:.2f}\n")

        except Exception as e:
            self.text_box.insert(tk.END, f"Hata oluştu: {e}\n")
    
    def predict_stock_xgboost_rolling_1ay(self):
        self.text_box.delete('1.0', tk.END)
        selected_stock = self.stock_var.get()
        if not selected_stock:
            self.text_box.insert(tk.END, "Lütfen bir finansal enstrüman seçin!\n")
            return

        ticker = self.tickers[selected_stock]

        try:
            data = yf.download(ticker, period='2y')

            if data.empty:
                self.text_box.insert(tk.END, f"{ticker} için veri bulunamadı!\n")
                return

            df = data.copy()
            df = df[-386:]


            df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA_20_bin'] = (df['EMA_20'] > df['EMA_20'].shift(1)).astype(int)

            df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
            df['EMA_50_bin'] = (df['EMA_50'] > df['EMA_50'].shift(1)).astype(int)

           
            delta = df['Close'].diff(1)
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI_14'] = 100 - (100 / (1 + rs))
            ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
            ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = ema_12 - ema_26
            df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            high14 = df['High'].rolling(window=14).max()
            low14 = df['Low'].rolling(window=14).min()
            df['Williams_%R'] = -100 * (high14 - df['Close']) / (high14 - low14)

            df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
            df.dropna(inplace=True)
           
            tahvil = yf.download('^TNX', start=df.index.min(), end=df.index.max())
            df['TNX'] = tahvil['Close']
            df['TNX'] = df['TNX'].fillna(method='ffill')

    
            features = [
                'RSI_14', 'MACD', 'Williams_%R','TNX','EMA_20_bin','EMA_50_bin'
]
            window_size = 30
            train_ratio = 0.8
            train_size = int(window_size * train_ratio)
            test_size = window_size - train_size

            scores = []

            for i in range(12):
                start_idx = i * window_size
                end_idx = start_idx + window_size
                window_df = df.iloc[start_idx:end_idx]

                if len(window_df) < window_size:
                    self.text_box.insert(tk.END, f"{i+1}. pencere için yeterli veri yok, atlanıyor...\n")
                    continue

                X = window_df[features]
                y = window_df['Target']

                X_train = X.iloc[:train_size]
                y_train = y.iloc[:train_size]
                X_test = X.iloc[train_size:]
                y_test = y.iloc[train_size:]

                model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
                report = classification_report(y_test, y_pred, output_dict=True)

                accuracy = report['accuracy']
                f1 = report.get('1', {}).get('f1-score', 0)

                self.text_box.insert(tk.END, f"{i+1}. pencere sonuçları (gün {start_idx}-{end_idx}):\n")
                self.text_box.insert(tk.END, classification_report(y_test, y_pred) + "\n")
                self.text_box.insert(tk.END, f"Confusion Matrix:\n{cm}\n\n")

                scores.append({'accuracy': accuracy, 'f1_score': f1})
                
            if scores:
                avg_accuracy = sum(s['accuracy'] for s in scores) / len(scores)
                avg_f1 = sum(s['f1_score'] for s in scores) / len(scores)
                self.text_box.insert(tk.END, f"Ortalama Accuracy: {avg_accuracy:.2f}\n")
                self.text_box.insert(tk.END, f"Ortalama F1-Score (class 1): {avg_f1:.2f}\n")

        except Exception as e:
            self.text_box.insert(tk.END, f"Hata oluştu: {e}\n")

    def predict_stock_xgboost_rolling_3ay(self):
        self.text_box.delete('1.0', tk.END)
        selected_stock = self.stock_var.get()
        if not selected_stock:
            self.text_box.insert(tk.END, "Lütfen bir finansal enstrüman seçin!\n")
            return

        ticker = self.tickers[selected_stock]

        try:
            data = yf.download(ticker, period='2y')

            if data.empty:
                self.text_box.insert(tk.END, f"{ticker} için veri bulunamadı!\n")
                return

            df = data.copy()
            df = df[-386:]

            df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA_20_bin'] = (df['EMA_20'] > df['EMA_20'].shift(1)).astype(int)

            df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
            df['EMA_50_bin'] = (df['EMA_50'] > df['EMA_50'].shift(1)).astype(int)

           
            delta = df['Close'].diff(1)
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI_14'] = 100 - (100 / (1 + rs))
            ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
            ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = ema_12 - ema_26
            df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            high14 = df['High'].rolling(window=14).max()
            low14 = df['Low'].rolling(window=14).min()
            df['Williams_%R'] = -100 * (high14 - df['Close']) / (high14 - low14)

            df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
            df.dropna(inplace=True)
           
            tahvil = yf.download('^TNX', start=df.index.min(), end=df.index.max())
            df['TNX'] = tahvil['Close']
            df['TNX'] = df['TNX'].fillna(method='ffill')

    
            features = [
                'RSI_14', 'MACD', 'Williams_%R','TNX','EMA_20_bin', 'EMA_50_bin'
]
            window_size = 90
            train_ratio = 0.8
            train_size = int(window_size * train_ratio)
            test_size = window_size - train_size

            scores = []

            for i in range(4):
                start_idx = i * window_size
                end_idx = start_idx + window_size
                window_df = df.iloc[start_idx:end_idx]

                if len(window_df) < window_size:
                    self.text_box.insert(tk.END, f"{i+1}. pencere için yeterli veri yok, atlanıyor...\n")
                    continue

                X = window_df[features]
                y = window_df['Target']

                X_train = X.iloc[:train_size]
                y_train = y.iloc[:train_size]
                X_test = X.iloc[train_size:]
                y_test = y.iloc[train_size:]

                model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
                report = classification_report(y_test, y_pred, output_dict=True)

                accuracy = report['accuracy']
                f1 = report.get('1', {}).get('f1-score', 0)

                self.text_box.insert(tk.END, f"{i+1}. pencere sonuçları (gün {start_idx}-{end_idx}):\n")
                self.text_box.insert(tk.END, classification_report(y_test, y_pred) + "\n")
                self.text_box.insert(tk.END, f"Confusion Matrix:\n{cm}\n\n")

                scores.append({'accuracy': accuracy, 'f1_score': f1})
                
            if scores:
                avg_accuracy = sum(s['accuracy'] for s in scores) / len(scores)
                avg_f1 = sum(s['f1_score'] for s in scores) / len(scores)
                self.text_box.insert(tk.END, f"Ortalama Accuracy: {avg_accuracy:.2f}\n")
                self.text_box.insert(tk.END, f"Ortalama F1-Score (class 1): {avg_f1:.2f}\n")

        except Exception as e:
            self.text_box.insert(tk.END, f"Hata oluştu: {e}\n")

    def predict_stock_xgboost_rolling_6ay(self):
        self.text_box.delete('1.0', tk.END)
        selected_stock = self.stock_var.get()
        if not selected_stock:
            self.text_box.insert(tk.END, "Lütfen bir finansal enstrüman seçin!\n")
            return

        ticker = self.tickers[selected_stock]

        try:
            data = yf.download(ticker, period='2y')

            if data.empty:
                self.text_box.insert(tk.END, f"{ticker} için veri bulunamadı!\n")
                return

            df = data.copy()
            df = df[-386:]

            df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA_20_bin'] = (df['EMA_20'] > df['EMA_20'].shift(1)).astype(int)

            df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
            df['EMA_50_bin'] = (df['EMA_50'] > df['EMA_50'].shift(1)).astype(int)

           
            delta = df['Close'].diff(1)
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI_14'] = 100 - (100 / (1 + rs))
            ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
            ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = ema_12 - ema_26
            df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            high14 = df['High'].rolling(window=14).max()
            low14 = df['Low'].rolling(window=14).min()
            df['Williams_%R'] = -100 * (high14 - df['Close']) / (high14 - low14)

            df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
            df.dropna(inplace=True)
           
            tahvil = yf.download('^TNX', start=df.index.min(), end=df.index.max())
            df['TNX'] = tahvil['Close']
            df['TNX'] = df['TNX'].fillna(method='ffill')

    
            features = [
                'RSI_14', 'MACD', 'Williams_%R','TNX','EMA_20_bin', 'EMA_50_bin'
]
            window_size = 180
            train_ratio = 0.8
            train_size = int(window_size * train_ratio)
            test_size = window_size - train_size

            scores = []

            for i in range(2):
                start_idx = i * window_size
                end_idx = start_idx + window_size
                window_df = df.iloc[start_idx:end_idx]

                if len(window_df) < window_size:
                    self.text_box.insert(tk.END, f"{i+1}. pencere için yeterli veri yok, atlanıyor...\n")
                    continue

                X = window_df[features]
                y = window_df['Target']

                X_train = X.iloc[:train_size]
                y_train = y.iloc[:train_size]
                X_test = X.iloc[train_size:]
                y_test = y.iloc[train_size:]

        
                model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
                report = classification_report(y_test, y_pred, output_dict=True)

                accuracy = report['accuracy']
                f1 = report.get('1', {}).get('f1-score', 0)

                self.text_box.insert(tk.END, f"{i+1}. pencere sonuçları (gün {start_idx}-{end_idx}):\n")
                self.text_box.insert(tk.END, classification_report(y_test, y_pred) + "\n")
                self.text_box.insert(tk.END, f"Confusion Matrix:\n{cm}\n\n")

                scores.append({'accuracy': accuracy, 'f1_score': f1})
                
            if scores:
                avg_accuracy = sum(s['accuracy'] for s in scores) / len(scores)
                avg_f1 = sum(s['f1_score'] for s in scores) / len(scores)
                self.text_box.insert(tk.END, f"Ortalama Accuracy: {avg_accuracy:.2f}\n")
                self.text_box.insert(tk.END, f"Ortalama F1-Score (class 1): {avg_f1:.2f}\n")

        except Exception as e:
            self.text_box.insert(tk.END, f"Hata oluştu: {e}\n")

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

    
        control_frame = ttk.Frame(main_frame, padding=10)
        control_frame.pack(fill=tk.X)

   
        ttk.Label(control_frame, text="Varlık Seç:").grid(row=0, column=0, padx=5)
        self.stock_var = tk.StringVar()
        self.stock_combobox = ttk.Combobox(
            control_frame, 
            textvariable=self.stock_var, 
            values=list(self.tickers.keys()),
            width=20
        )
        self.stock_combobox.grid(row=0, column=1, padx=5)
        self.stock_combobox.bind('<KeyRelease>', self.filter_stock_list)
        ttk.Button(control_frame, text="Analiz Et", command=self.analyze_stock).grid(row=0, column=2, padx=10)
        ttk.Button(control_frame, text="Temel Oranları Göster", command=self.analyze_stock1).grid(row=1, column=2, padx=10)
        
        ttk.Label(control_frame, text="İndikatör Seç:").grid(row=0, column=3, padx=10)
        self.indicator_stock_var = tk.StringVar()
        self.indicator_combobox = ttk.Combobox(
            control_frame,
            textvariable=self.indicator_stock_var,  
            values=["RSI","MACD","Bollinger Bands","Ichimoku","ADX(14)","Pivot Points","Fibonacci Pivot","Williams %R","CCI(14)","ATR%(14)","ROC","Ultimate Oscillator","MFI(14)","OBV","VWAP","CMF","1Y Price","STOCH(9,6)","Moving Averages","Exponential Moving Averages","Parabolic_SAR","US10YEAR","VIX","DXY","USD/JPY","EUR/USD","VOLUME","Nadaraya_watson","SuperTrend","F/K"], 
            state="readonly",
            width=20
        )
        self.indicator_combobox.grid(row=0, column=4, padx=5)  
        self.indicator_combobox.current(0)
        ttk.Button(control_frame, text="Grafiği Göster", command=self.plot_indicator_charts).grid(row=0, column=5, padx=10)

        ttk.Label(control_frame, text="Portföy Optimizasyon:").grid(row=0, column=6, padx=10)
        ttk.Button(control_frame, text="Varlık Ekle", command=self.add_stock_selection).grid(row=0, column=7, padx=10)
        ttk.Button(control_frame, text="Portföyü Optimize Et", command=self.optimize_portfolio).grid(row=0, column=8, padx=10)

       
        ttk.Label(control_frame, text="LR Modeli İle Tahmin:").grid(row=2, column=0, padx=10, sticky="e")


        lr_button_frame = ttk.Frame(control_frame)
        lr_button_frame.grid(row=2, column=1, columnspan=2, sticky="w")

        ttk.Button(lr_button_frame, text="10g", command=self.predict_stock_lr_rolling_10gun, width=3).pack(side="left", padx=1)
        ttk.Button(lr_button_frame, text="1a", command=self.predict_stock_lr_rolling_1ay, width=3).pack(side="left", padx=1)
        ttk.Button(lr_button_frame, text="3a", command=self.predict_stock_lr_rolling_3ay, width=3).pack(side="left", padx=1)
        ttk.Button(lr_button_frame, text="6a", command=self.predict_stock_lr_rolling_6ay, width=3).pack(side="left", padx=1)


        ttk.Label(control_frame, text="SVM Modeli İle Tahmin: ").grid(row=2, column=3, padx=10, sticky="e")
        svm_button_frame = ttk.Frame(control_frame)
        svm_button_frame.grid(row=2, column=4, columnspan=4, sticky="w")  


        ttk.Button(svm_button_frame, text="10g", command=self.predict_stock_svm_rolling_10gun, width=3).pack(side="left", padx=1)
        ttk.Button(svm_button_frame, text="1a", command=self.predict_stock_svm_rolling_1ay, width=3).pack(side="left", padx=1)
        ttk.Button(svm_button_frame, text="3a", command=self.predict_stock_svm_rolling_3ay, width=3).pack(side="left", padx=1)
        ttk.Button(svm_button_frame, text="6a", command=self.predict_stock_svm_rolling_6ay, width=3).pack(side="left", padx=1)

   
        ttk.Label(control_frame, text="XGBOOST Modeli İle Tahmin: ").grid(row=2, column=5, padx=10, sticky="e")
        xgb_button_frame = ttk.Frame(control_frame)
        xgb_button_frame.grid(row=2, column=6, columnspan=4, sticky="w")


        ttk.Button(xgb_button_frame, text="10g", command=self.predict_stock_xgboost_rolling_10gun, width=3).pack(side="left", padx=1)
        ttk.Button(xgb_button_frame, text="1a", command=self.predict_stock_xgboost_rolling_1ay, width=3).pack(side="left", padx=1)
        ttk.Button(xgb_button_frame, text="3a", command=self.predict_stock_xgboost_rolling_3ay, width=3).pack(side="left", padx=1)
        ttk.Button(xgb_button_frame, text="6a", command=self.predict_stock_xgboost_rolling_6ay, width=3).pack(side="left", padx=1)

        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        left_panel = ttk.Frame(content_frame, width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.text_box = tk.Text(left_panel, height=80, width=80, wrap=tk.WORD)
        self.text_box.pack(fill=tk.Y, pady=5)

        self.canvas_frame = ttk.Frame(content_frame)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.portfolio_selection_frame = ttk.Frame(left_panel)
        self.portfolio_selection_frame.pack(fill=tk.X, pady=10)

    def filter_stock_list(self, event):
        value = self.stock_combobox.get().lower()
        filtered = [ticker for ticker in self.tickers.keys() if value in ticker.lower()]
        self.stock_combobox['values'] = filtered

    def add_stock_selection(self):
        if hasattr(self, 'current_canvas') and self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()
            self.current_canvas = None
        
        self.text_box.delete('1.0', tk.END)
        row = len(self.portfolio_entries) + 1


        add_stock_frame = ttk.Frame(self.canvas_frame)
        add_stock_frame.pack(pady=5)  

        
        var = tk.StringVar()
        cb = ttk.Combobox(
            add_stock_frame, 
            textvariable=var,
            values=list(self.tickers.keys()), 
            state="readonly", 
            width=20
        )
        cb.grid(row=0, column=0, padx=5)
        cb.current(0)

        amount_var = tk.StringVar()
        entry = ttk.Entry(add_stock_frame, textvariable=amount_var, width=10)
        entry.grid(row=0, column=1, padx=5)
        entry.insert(0, "100")

        btn = ttk.Button(
            add_stock_frame, 
            text="X", 
            command=lambda: self.remove_stock_selection(row, add_stock_frame)
        )
        btn.grid(row=0, column=2, padx=5)

        self.portfolio_entries[row] = (cb, entry, btn)
        
    def remove_stock_selection(self, row, frame):
        frame.destroy()  
        del self.portfolio_entries[row]

    def get_portfolio_weights(self):
        weights = {}
        total = 0
        for row, (cb, entry, _) in self.portfolio_entries.items():
            try:
                amount = float(entry.get())
                total += amount
                weights[cb.get()] = weights.get(cb.get(), 0) + amount
            except ValueError:
                messagebox.showerror("Hata", "Geçersiz miktar değeri")
                return None
        
        if total == 0:
            messagebox.showerror("Hata", "Toplam yatırım sıfır olamaz")
            return None
        
        return {k: v/total for k, v in weights.items()}
        
    def optimize_portfolio(self):
        self.text_box.delete('1.0', tk.END)
        weights = self.get_portfolio_weights()
        if not weights:
            return

        tickers = [self.tickers[k] for k in weights.keys()]
        amounts = list(weights.values())

        try:
            data = yf.download(tickers=tickers,period="1y",interval="1d",group_by='ticker',auto_adjust=False,timeout=10
)
            adj_close = pd.DataFrame()
            for ticker in tickers:
                if 'Adj Close' not in data[ticker].columns:
                    raise ValueError(f"{ticker} için 'Adj Close' verisi yok.")
                adj_close[ticker] = data[ticker]['Adj Close']


            missing_tickers = set(tickers) - set(adj_close.columns)
            if missing_tickers:
                raise ValueError(f"Eksik veri: {', '.join(missing_tickers)}")

            returns = adj_close.pct_change().dropna()
            num_days = len(returns)  

            portfolio_returns = (returns * amounts).sum(axis=1)
            port_return = (1 + portfolio_returns).prod() - 1  

            cov_matrix = returns.cov() 
            port_variance = np.dot(amounts, np.dot(cov_matrix, amounts)) 
            port_volatility = np.sqrt(port_variance) * np.sqrt(num_days)  
            
            market_data = yf.download('^GSPC', period="1y", interval="1d")
            market_returns = market_data.get('Adj Close', market_data.get('Close')).pct_change().dropna()

            
            aligned = pd.concat([portfolio_returns, market_returns], axis=1, join='inner')
            aligned.columns = ['Portfolio', 'Market']

           
            beta = np.cov(aligned['Portfolio'], aligned['Market'])[0, 1] / aligned['Market'].var()

       
            downside_returns = aligned['Portfolio'][aligned['Portfolio'] < 0]
            downside_deviation = downside_returns.std() * np.sqrt(num_days)  

            rf_rate = 0.04  

            sharpe_ratio = (port_return - rf_rate) / port_volatility
            sortino_ratio = (port_return - rf_rate) / downside_deviation
            treynor_ratio = (port_return - rf_rate) / beta

          
            var_95 = np.percentile(aligned['Portfolio'], 5)
            cvar_95 = aligned['Portfolio'][aligned['Portfolio'] < var_95].mean()

            cumulative_returns = (1 + aligned['Portfolio']).cumprod()
            peak = cumulative_returns.cummax()
            drawdowns = (cumulative_returns - peak) / peak
            max_drawdown = drawdowns.min()
            calmar_ratio = port_return / abs(max_drawdown)
       
            correlation_matrix = returns.corr()


            self.text_box.insert(tk.END, "=== Portföy Optimizasyon Sonuçları ===\n\n")
            self.text_box.insert(tk.END, f"İncelenen Gün Sayısı: {num_days} gün\n")
            self.text_box.insert(tk.END, "\n=== Varlıklar Arası Korelasyonlar ===\n")
            for i in range(len(tickers)):
                for j in range(i+1, len(tickers)):
                    ticker_i = tickers[i]
                    ticker_j = tickers[j]
                    corr_value = correlation_matrix.loc[ticker_i, ticker_j]
                    self.text_box.insert(tk.END, f"{ticker_i} vs {ticker_j}: {corr_value:.2f}\n\n")
            self.text_box.insert(tk.END, f"Portföy Getirisi: {port_return:.2%}\n")
            self.text_box.insert(tk.END, f"Portföy Volatilitesi: {port_volatility:.2%}\n")
            self.text_box.insert(tk.END, f"Sharpe Oranı: {sharpe_ratio:.2f}\n")
            self.text_box.insert(tk.END, f"Beta: {beta:.2f}\n")
            self.text_box.insert(tk.END, f"Sortino Oranı: {sortino_ratio:.2f}\n")
            self.text_box.insert(tk.END, f"Treynor Oranı: {treynor_ratio:.2f}\n")
            self.text_box.insert(tk.END, f"VaR (%95): {var_95:.2%}\n")
            self.text_box.insert(tk.END, f"CVaR (%95): {cvar_95:.2%}\n")
            self.text_box.insert(tk.END, f"Max Drawdown: {max_drawdown:.2%}\n")
            self.text_box.insert(tk.END, f"Calmar Oranı: {calmar_ratio:.2f}\n")
            self.text_box.insert(tk.END, "\nVarlık Dağılımı:\n")
            for stock, weight in weights.items():
                self.text_box.insert(tk.END, f"- {stock}: {weight:.2%}\n")

            self.clear_portfolio_selection()

        except Exception as e:
            messagebox.showerror("Hata", str(e))
    
    def clear_portfolio_selection(self):
        
        for widget in self.portfolio_selection_frame.winfo_children():
            widget.destroy()
        self.portfolio_entries.clear()
        
    def calculate_technical_indicators(self, df):
        
        df['MA_5'] = df['Close'].rolling(window=5).mean()
        df['MA_10'] = df['Close'].rolling(window=10).mean()
        df['MA_20'] = df['Close'].rolling(window=20).mean()
        df['MA_50'] = df['Close'].rolling(window=50).mean()
        df['MA_100'] = df['Close'].rolling(window=100).mean()
        df['MA_200'] = df['Close'].rolling(window=200).mean()
        df['EMA_5'] = df['Close'].ewm(span=5, adjust=False).mean()
        df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        df['EMA_100'] = df['Close'].ewm(span=100, adjust=False).mean()
        df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
        df['RSI_14'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
        macd = ta.trend.MACD(df['Close'], window_slow=26, window_fast=12, window_sign=9)
        df['MACD'] = macd.macd()
        df['MACD_Signal'] = macd.macd_signal()
        df['MACD_Hist'] = macd.macd_diff()
        df["STOCH(9,6)"] = ta.momentum.StochasticOscillator(df["High"], df["Low"], df["Close"], window=9, smooth_window=6).stoch()
        df["MACD(12,26)"] = ta.trend.MACD(df["Close"]).macd()
        df["ADX(14)"] = ta.trend.ADXIndicator(df["High"], df["Low"], df["Close"]).adx()
        df["Williams %R"] = ta.momentum.WilliamsRIndicator(df["High"], df["Low"], df["Close"]).williams_r()
        df["CCI(14)"] = ta.trend.CCIIndicator(df["High"], df["Low"], df["Close"], window=14).cci()
        df["ATR(14)"] = ta.volatility.AverageTrueRange(df["High"], df["Low"], df["Close"], window=14).average_true_range()
        df["ATR%(14)"] = df["ATR(14)"] / df["Close"] * 100
        df["ROC"] = ta.momentum.ROCIndicator(df["Close"], window=12).roc()
        df["Ultimate Oscillator"] = ta.momentum.UltimateOscillator(df["High"], df["Low"], df["Close"]).ultimate_oscillator()

        df["MFI(14)"] = ta.volume.MFIIndicator(df["High"], df["Low"], df["Close"], df["Volume"], window=14).money_flow_index()
        df["Parabolic_SAR"] = ta.trend.PSARIndicator(df["High"], df["Low"], df["Close"]).psar()
        

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


        bollinger = ta.volatility.BollingerBands(close=df["Close"], window=20, window_dev=2)
        df["BB_High"] = bollinger.bollinger_hband()
        df["BB_Low"] = bollinger.bollinger_lband()
        df["BB_Mid"] = bollinger.bollinger_mavg()
        df["BB_Percent"] = bollinger.bollinger_pband()
        df["BB_Bandwidth"] = bollinger.bollinger_wband()
    

        max_close = df["Close"].rolling(window=50).max()
        min_close = df["Close"].rolling(window=50).min()
        df["OBV"] = ta.volume.OnBalanceVolumeIndicator(df["Close"], df["Volume"]).on_balance_volume()
        df["VWAP"] = (df["Volume"] * (df["High"] + df["Low"] + df["Close"]) / 3).cumsum() / df["Volume"].cumsum()
        df["CMF"] = ta.volume.ChaikinMoneyFlowIndicator(df["High"], df["Low"], df["Close"], df["Volume"], window=20).chaikin_money_flow()

        prev_high = df['High'].shift(1)
        prev_low = df['Low'].shift(1)
        prev_close = df['Close'].shift(1)
    
        df['Pivot'] = (prev_high + prev_low + prev_close) / 3
        df['R1'] = 2*df['Pivot'] - prev_low
        df['S1'] = 2*df['Pivot'] - prev_high
        df['R2'] = df['Pivot'] + (prev_high - prev_low)
        df['S2'] = df['Pivot'] - (prev_high - prev_low)
        df['R3'] = df['Pivot'] + 2*(prev_high - prev_low)
        df['S3'] = df['Pivot'] - 2*(prev_high - prev_low)

        fib_range = prev_high - prev_low
        df['Pivot_Fib'] = (prev_high + prev_low + prev_close) / 3
        df['R1_Fib'] = df['Pivot_Fib'] + 0.382 * fib_range
        df['R2_Fib'] = df['Pivot_Fib'] + 0.618 * fib_range
        df['R3_Fib'] = df['Pivot_Fib'] + 1.0 * fib_range
        df['S1_Fib'] = df['Pivot_Fib'] - 0.382 * fib_range
        df['S2_Fib'] = df['Pivot_Fib'] - 0.618 * fib_range
        df['S3_Fib'] = df['Pivot_Fib'] - 1.0 * fib_range

 
        return df

    def calculate_risk_metrics(self, ticker):
        try:
            
            stock_data = yf.Ticker(ticker).history(period='1y', interval='1d')
            benchmark_data = yf.Ticker("^GSPC").history(period='1y', interval='1d') #XU100.IS BORSA İSTANBUL İÇİN  abd ^GSPC
        
            if stock_data.empty or benchmark_data.empty:
                return None

            returns = stock_data['Close'].pct_change().dropna()
            benchmark_returns = benchmark_data['Close'].pct_change().dropna()
            aligned = pd.concat([returns, benchmark_returns], axis=1, join='inner').dropna()
            returns = aligned.iloc[:, 0]
            benchmark_returns = aligned.iloc[:, 1]
            total_days = len(returns)


             # Burası önemli kısım işte! 👇
            info = yf.Ticker(ticker).info
            fk = info.get("trailingPE")
            pd_dd = info.get("priceToBook")
        
            print(f"{ticker} için oranlar:")
            print(f"F/K: {fk}")
            print(f"PD/DD: {pd_dd}")

 
            rf_rate = 0.04  

            annual_return = (1 + returns).prod() - 1
            annual_volatility = returns.std() * np.sqrt(total_days)
            sharpe_ratio = (annual_return - rf_rate) / annual_volatility

            downside_returns = returns[returns < 0]
            downside_deviation = downside_returns.std() * np.sqrt(total_days)
            sortino_ratio = (annual_return - rf_rate) / downside_deviation if downside_deviation != 0 else 0

            beta = np.cov(returns, benchmark_returns)[0,1] / np.var(benchmark_returns)
            treynor_ratio = (annual_return - rf_rate) / beta if beta != 0 else np.nan

            var_95 = np.percentile(returns, 5)
            cvar_95 = returns[returns <= var_95].mean()
            cumulative_returns = (1 + returns).cumprod()
            peak = cumulative_returns.cummax()
            drawdown = (cumulative_returns / peak) - 1
            max_drawdown = drawdown.min()
            calmar_ratio = annual_return / abs(max_drawdown) if max_drawdown != 0 else np.nan

            correlation = returns.rolling(total_days).corr(benchmark_returns)
            r_squared = (correlation ** 2).dropna()
            r_squared_value = r_squared.iloc[-1] if not r_squared.empty else np.nan
            total_return = annual_return

            return beta, sharpe_ratio, sortino_ratio, var_95, cvar_95, annual_volatility, max_drawdown, treynor_ratio, calmar_ratio, r_squared_value ,total_return
        except Exception as e:
            print(f"Risk metrik hesaplama hatası: {str(e)}")
            return None

    def analyze_stock1(self):
        self.text_box.delete("1.0", tk.END)
        selected_stock = self.stock_var.get()
        if not selected_stock:
            self.text_box.insert(tk.END, "Lütfen bir finansal enstrüman seçiniz!\n")
            return
        ticker = self.tickers[selected_stock]


        try:
            info = yf.Ticker(ticker).info
            fk = info.get("trailingPE")
            pd_dd = info.get("priceToBook")
            roe = info.get("returnOnEquity")
            roa = info.get("returnOnAssets")
            kar_marji = info.get("profitMargins")
            borc_ozkaynak = info.get("debtToEquity")
            ps_orani = info.get("priceToSalesTrailing12Months")

            self.text_box.insert(tk.END, f"\n📈 {selected_stock} ({ticker}) için temel oranlar:\n")
            self.text_box.insert(tk.END, f"📊 F/K Oranı: {fk}\n")
            self.text_box.insert(tk.END, f"🏦 PD/DD Oranı: {pd_dd}\n")
            self.text_box.insert(tk.END, f"💸 ROE (Özkaynak Karlılığı): {roe}\n")
            self.text_box.insert(tk.END, f"🏭 ROA (Aktif Karlılığı): {roa}\n")
            self.text_box.insert(tk.END, f"📈 Kar Marjı: {kar_marji}\n")
            self.text_box.insert(tk.END, f"📉 Borç/Özkaynak Oranı: {borc_ozkaynak}\n")
            self.text_box.insert(tk.END, f"🛍️ P/S (Fiyat/Satış) Oranı: {ps_orani}\n\n")

        except Exception as e:
            self.text_box.insert(tk.END, f"Hata oluştu: {e}\n")
    
    
    def analyze_stock(self):
        selected_stock = self.stock_var.get()
        if not selected_stock:
            self.text_box.insert(tk.END, "Lütfen bir finansal enstrüman seçiniz!\n")
            return
        ticker = self.tickers[selected_stock]
        try:

            stock = yf.Ticker(ticker)
            df = stock.history(period='1y', interval='1d')

            if df.empty:
                raise ValueError("Veri alınamadı")
                
            df = self.calculate_technical_indicators(df)

            metrics = self.calculate_risk_metrics(ticker)
            if metrics is None:
                raise ValueError("Risk metrikleri hesaplanamadı")
                
            beta, sharpe_ratio, sortino_ratio, var_95, cvar_95, volatility, max_drawdown, treynor_ratio , calmar_ratio, r_squared, total_return = metrics

            self.text_box.delete('1.0', tk.END)

    
            start_date = df.index[0].strftime('%d-%m-%Y')
            end_date = df.index[-1].strftime('%d-%m-%Y')
            self.text_box.insert(tk.END, f"Analiz Tarih Aralığı: {start_date} - {end_date}\n\n")

            self.text_box.insert(tk.END, f"{selected_stock} ({ticker}) Teknik Göstergeler ve Risk Göstergeleri\n\n")
            self.text_box.insert(tk.END, f"Son Fiyat: {df['Close'].iloc[-1]:.2f}\n")
            
           
        except Exception as e:
            self.text_box.delete('1.0', tk.END)
            self.text_box.insert(tk.END, f"Hata: {str(e)}")
        
              
        INDICATOR_EXPLANATIONS = {
            "RSI_14": {"thresholds": (30, 70), "explanation": "14 günlük RSI - 30 altı aşırı satım, 70 üstü aşırı alım", "recommendation": {"below": ("Aşırı Satım (Al Sinyali)", "🟢 Al"), "above": ("Aşırı Alım (Sat Sinyali)", "🔴 Sat"), "normal": ("Normal Bölge", "🟡 Tut")}},
            "MACD": {"comparison1": "MACD_Signal", "explanation": "MACD'nin sinyal çizgisiyle ilişkisi", "recommendation": {"above": ("MACD Sinyal Üstünde (Al Sinyali)", "🟢 Al"), "below": ("MACD Sinyal Altında (Sat Sinyali)", "🔴 Sat"), "normal": ("MACD Sinyal Civarında (Bekle)", "🟡 Tut")}},
            "STOCH(9,6)": {"thresholds": (20, 80), "explanation": "Stokastik Osilatör - 20 altı aşırı satım, 80 üstü aşırı alım", "recommendation": {"below": ("Aşırı Satım (Al Sinyali)", "🟢 Al"), "above": ("Aşırı Alım (Sat Sinyali)", "🔴 Sat"), "normal": ("Normal Bölge", "🟡 Tut")}},
            "ADX(14)": {"thresholds": (25, 25), "explanation": "ADX - 25 üstü güçlü trend", "recommendation": {"above": ("Güçlü Trend (Al/Sat Sinyali destekler)", "🟢 Trend Takip"), "below": ("Zayıf Trend (Dikkatli Ol)", "🔴 Dikkat"), "normal": ("Orta Trend Gücü", "🟡 Tut")}},
            "CCI(14)": {"thresholds": (-100, 100), "explanation": "Commodity Channel Index - -100 altı aşırı satım, 100 üstü aşırı alım", "recommendation": {"below": ("Aşırı Satım (Al Sinyali)", "🟢 Al"), "above": ("Aşırı Alım (Sat Sinyali)", "🔴 Sat"), "normal": ("Normal Bölge", "🟡 Tut")}},
            "Williams %R": {"thresholds": (-80, -20), "explanation": "Williams %R - -80 altı aşırı satım, -20 üstü aşırı alım", "recommendation": {"below": ("Aşırı Satım (Al Sinyali)", "🟢 Al"), "above": ("Aşırı Alım (Sat Sinyali)", "🔴 Sat"), "normal": ("Normal Bölge", "🟡 Tut")}},
            "Ultimate Oscillator": {"thresholds": (30, 70), "explanation": "Ultimate Osilatör - 30 altı aşırı satım, 70 üstü aşırı alım", "recommendation": {"below": ("Aşırı Satım (Al Sinyali)", "🟢 Al"), "above": ("Aşırı Alım (Sat Sinyali)", "🔴 Sat"), "normal": ("Normal Bölge", "🟡 Tut")}},
            "ATR%(14)": {"thresholds": (1.0, 2.5), "explanation": "Ortalama Gerçek Aralık - Piyasa volatilitesi", "recommendation": {"below": ("Düşük Volatilite (Güvenli Bölge)", "🟢 Al"), "above": ("Yüksek Volatilite (Riskli Bölge)", "🔴 Sat"), "normal": ("Orta Volatilite (Dikkatli Ol)", "🟡 Tut")}},
            "ROC": {"thresholds": (0, 0), "explanation": "Değişim Oranı - Pozitif yukarı momentum, negatif aşağı", "recommendation": {"above": ("Yukarı Momentum (Al Sinyali)", "🟢 Al"), "below": ("Aşağı Momentum (Sat Sinyali)", "🔴 Sat"), "normal": ("Nötr Momentum", "🟡 Tut")}},
            "Parabolic_SAR": {"comparison": "Close", "explanation": "Parabolic SAR - Fiyatın yönünü gösterir. Fiyat SAR'ın üstünde ise yükseliş, altında ise düşüş trendi vardır.", "recommendation": {"above": ("Yükseliş Trendinde (Al Sinyali)", "🟢 Al"), "below": ("Düşüş Trendinde (Sat Sinyali)", "🔴 Sat")}},
            "MA_5": {"comparison": "Close", "explanation": "5 günlük Hareketli Ortalama - Fiyatın üzerinde al, altında sat", "recommendation": {"above": ("Fiyat MA5 Üstünde (Al Sinyali)", "🟢 Al"), "below": ("Fiyat MA5 Altında (Sat Sinyali)", "🔴 Sat"), "normal": ("MA5 ile Uyumlu", "🟡 Tut")}},
            "MA_10": {"comparison": "Close", "explanation": "10 günlük Hareketli Ortalama - Kısa vadeli trend takip", "recommendation": {"above": ("Fiyat MA10 Üstünde (Al)", "🟢 Al"), "below": ("Fiyat MA10 Altında (Sat)", "🔴 Sat"), "normal": ("MA10 ile Uyumlu", "🟡 Tut")}},
            "MA_20": {"comparison": "Close", "explanation": "20 günlük Hareketli Ortalama - Orta vadeli trend ölçümü", "recommendation": {"above": ("Fiyat MA20 Üstünde (Al)", "🟢 Al"), "below": ("Fiyat MA20 Altında (Sat)", "🔴 Sat"), "normal": ("MA20 ile Uyumlu", "🟡 Tut")}},
            "MA_50": {"comparison": "Close", "explanation": "50 günlük Hareketli Ortalama - Önemli destek/direnç seviyesi", "recommendation": {"above": ("Fiyat MA50 Üstünde (Güçlü Al)", "🟢 Al"), "below": ("Fiyat MA50 Altında (Güçlü Sat)", "🔴 Sat"), "normal": ("MA50 Civarında", "🟡 Tut")}},
            "MA_100": {"comparison": "Close", "explanation": "100 günlük Hareketli Ortalama - Uzun vadeli trend göstergesi", "recommendation": {"above": ("Fiyat MA100 Üstünde (Güçlü Al)", "🟢 Al"), "below": ("Fiyat MA100 Altında (Güçlü Sat)", "🔴 Sat"), "normal": ("MA100 Civarında", "🟡 Tut")}},
            "MA_200": {"comparison": "Close", "explanation": "200 günlük Hareketli Ortalama - Ana trend belirleyici", "recommendation": {"above": ("Fiyat MA200 Üstünde (Güçlü Al)", "🟢 Al"), "below": ("Fiyat MA200 Altında (Güçlü Sat)", "🔴 Sat"), "normal": ("EMA50 Civarında", "🟡 Tut")}},
            "EMA_5": {"comparison": "Close", "explanation": "5 günlük Üstel Hareketli Ortalama - Hızlı tepki veren kısa vadeli gösterge", "recommendation": {"above": ("Fiyat EMA5 Üstünde (Al Sinyali)", "🟢 Al"), "below": ("Fiyat EMA5 Altında (Sat Sinyali)", "🔴 Sat"), "normal": ("EMA5 ile Uyumlu", "🟡 Tut")}},
            "EMA_10": {"comparison": "Close", "explanation": "10 günlük Üstel Hareketli Ortalama - Kısa vadeli trend takip", "recommendation": {"above": ("Fiyat EMA10 Üstünde (Al)", "🟢 Al"), "below": ("Fiyat EMA10 Altında (Sat)", "🔴 Sat"), "normal": ("EMA10 ile Uyumlu", "🟡 Tut")}},
            "EMA_20": {"comparison": "Close", "explanation": "20 günlük Üstel Hareketli Ortalama - Orta vadeli trend ölçümü", "recommendation": {"above": ("Fiyat EMA20 Üstünde (Al)", "🟢 Al"), "below": ("Fiyat EMA20 Altında (Sat)", "🔴 Sat"), "normal": ("EMA20 ile Uyumlu", "🟡 Tut")}},
            "EMA_50": {"comparison": "Close", "explanation": "50 günlük Üstel Hareketli Ortalama - Önemli destek/direnç seviyesi", "recommendation": {"above": ("Fiyat EMA50 Üstünde (Güçlü Al)", "🟢 Al"), "below": ("Fiyat EMA50 Altında (Güçlü Sat)", "🔴 Sat"), "normal": ("EMA50 Civarında", "🟡 Tut")}},
            "EMA_100": {"comparison": "Close", "explanation": "100 günlük Üstel Hareketli Ortalama - Uzun vadeli trend göstergesi", "recommendation": {"above": ("Fiyat EMA100 Üstünde (Yapısal Al)", "🟢 Al"), "below": ("Fiyat EMA100 Altında (Yapısal Sat)", "🔴 Sat"), "normal": ("EMA100 Civarında", "🟡 Tut")}},
            "EMA_200": {"comparison": "Close", "explanation": "200 günlük üstel Hareketli Ortalama - Ana trend belirleyici", "recommendation": {"above": ("Fiyat EMA200 Üstünde (Stratejik Al)", "🟢 Al"), "below": ("Fiyat EMA200 Altında (Stratejik Sat)", "🔴 Sat"), "normal": ("EMA200 Civarında", "🟡 Tut")}}
        }   
        RISK_EXPLANATIONS = {
            "Beta": {"thresholds": (0.8, 1.2), "explanation": "Piyasa volatilitesine göre risk seviyesi", "recommendation": {"below": ("Piyasadan daha az riskli", "🟢"), "above": ("Piyasadan daha riskli", "🔴"), "normal": ("Piyasa ile uyumlu risk", "🟡")}},
            "Sharpe": {"thresholds": (1, 2), "explanation": "Risk birimi başına getiri", "recommendation": {"below": ("Düşük risk-getiri dengesi", "🔴"), "above": ("İyi risk-getiri dengesi", "🟢"), "normal": ("Kabul edilebilir risk-getiri", "🟡")}},
            "Sortino": {"thresholds": (1, 2), "explanation": "Zarar riski birimi başına getiri", "recommendation": {"below": ("Düşük Sortino oranı", "🔴"), "above": ("Yüksek Sortino oranı", "🟢"), "normal": ("Kabul edilebilir Sortino", "🟡")}},
            "Volatilite": {"thresholds": (0.2, 0.4), "explanation": "Yıllık fiyat dalgalanması", "recommendation": {"below": ("Düşük Volatilite", "🟢"), "above": ("Yüksek Volatilite", "🔴"), "normal": ("Orta Volatilite", "🟡")}},
            "Max Drawdown": {"thresholds": (-0.2, -0.4), "explanation": "Maksimum düşüş değeri", "recommendation": {"below": ("Aşırı Düşüş Riski", "🔴"), "above": ("Kabul edilebilir Düşüş", "🟢"), "normal": ("Orta Düşüş Riski", "🟡")}},
            "Treynor": {"thresholds": (0.5, 1.0), "explanation": "Sistemik risk başına getiri (Beta'ya göre)", "recommendation": {"below": ("Düşük risk düzeltmeli getiri", "🔴"), "above": ("Yüksek risk düzeltmeli getiri", "🟢"), "normal": ("Kabul edilebilir risk/getiri", "🟡")}},
            "Calmar": {"thresholds": (0.5, 1.0), "explanation": "Maksimum düşüşe göre getiri oranı", "recommendation": {"below": ("Düşük düşüş direnci", "🔴"), "above": ("Yüksek düşüş direnci", "🟢"), "normal": ("Orta seviye direnç", "🟡")}},
            "R²": {"thresholds": (0.3, 0.7), "explanation": "Piyasa ile korelasyon (1 = tam uyum)", "recommendation": {"below": ("Düşük piyasa korelasyonu", "🟡"), "above": ("Yüksek piyasa korelasyonu", "🟢"), "normal": ("Orta seviye korelasyon", "🟡")}},
            "VaR (%95)": {"thresholds": (-0.025, -0.01), "explanation": "%95 güvenle maksimum beklenen günlük kayıp", "recommendation": {"below": ("Aşırı Risk (🔴)", "🔴"), "above": ("Düşük Risk (🟢)", "🟢"), "normal": ("Orta Risk (🟡)", "🟡")}, "format": "percentage"},
            "CVaR (%95)": {"thresholds": (-0.03, -0.015), "explanation": "VaR'ı aşan durumlarda ortalama kayıp", "recommendation": {"below": ("Çok Yüksek Risk (🔴)", "🔴"), "above": ("Kabul Edilebilir Risk (🟢)", "🟢"), "normal": ("Yüksek Risk (🟡)", "🟡")}, "format": "percentage"}
        }
      
        self.text_box.insert(tk.END, "\n--- Teknik Göstergeler ve Yorumlar ---\n\n")
        
        for indicator in [
            "RSI_14", "MACD", "STOCH(9,6)", "ADX(14)", 
            "CCI(14)", "Williams %R", "Ultimate Oscillator","ROC","ATR%(14)","Parabolic_SAR","MA_5","MA_10","MA_20",
            "MA_50","MA_100","MA_200","EMA_5","EMA_10","EMA_20","EMA_50","EMA_100","EMA_200"
        ]:

            try:
                value = df[indicator].iloc[-1]
                exp = INDICATOR_EXPLANATIONS.get(indicator, {})
                comment = ""
                rec_icon = ""
                
                if "thresholds" in exp:
                    lower, upper = exp["thresholds"]
                    if value < lower:
                        comment, rec = exp["recommendation"]["below"]
                    elif value > upper:
                        comment, rec = exp["recommendation"]["above"]
                    else:
                        comment, rec = exp["recommendation"]["normal"]

                  
                elif "comparison" in exp:
                    other_value = df[exp["comparison"]].iloc[-1]
                    if other_value > value:  
                        comment, rec = exp["recommendation"]["above"]  
                    else:
                        comment, rec = exp["recommendation"]["below"]  
                        

                elif "comparison1" in exp:
                    other_value = df[exp["comparison1"]].iloc[-1]
                    if value > 0:  
                        if value > other_value:
                            comment, rec = "MACD Pozitif ve Sinyal Üstünde (Güçlü Al)", "🟢 Al"

                        else:
                            comment, rec = "MACD Pozitif ama Sinyal Altında (Trend Zayıflıyor)", "🟡 Tut"

                    else:  
                        if value > other_value:
                            comment, rec = "MACD Negatif ama Sinyal Üstünde (Olası Toparlanma)", "🟡 Tut"
                        else:
                            comment, rec = "MACD Negatif ve Sinyal Altında (Güçlü Sat)", "🔴 Sat"
  
                self.text_box.insert(tk.END, 
                    f"{indicator}: {value:.2f} {rec} - {comment}\n")
                
            except Exception as e:
                continue
        
        self.text_box.insert(tk.END, "\n--- Pivot Seviyeleri ---\n\n")
        pivot_types = {
            "Pivot_Klasik": ["S3", "S2", "S1", "Pivot", "R1", "R2", "R3"],
            "Pivot_Fibonacci": ["S3_Fib", "S2_Fib", "S1_Fib", "Pivot_Fib", "R1_Fib", "R2_Fib", "R3_Fib"]
                    }
        for p_type, levels in pivot_types.items():
            try:
                values = {level: df[level].iloc[-1] for level in levels if level in df.columns}
                level_text = " | ".join([f"{k}: {v:.2f}" for k, v in values.items()])
                self.text_box.insert(tk.END, f"{p_type}:\n{level_text}\n\n")
            except Exception as e:
                continue 
  
        self.text_box.insert(tk.END, "\n--- Risk Analizi ve Yorumlar ---\n\n")
        risk_factors = {
        "Beta": beta,"Sharpe": sharpe_ratio,"Sortino": sortino_ratio,"Volatilite": volatility,"Max Drawdown": max_drawdown,"Treynor": treynor_ratio,"Calmar": calmar_ratio,"R²": r_squared,"VaR (%95)":var_95,"CVaR (%95)":cvar_95   
   
}
        
        for metric, value in risk_factors.items():
            exp = RISK_EXPLANATIONS.get(metric, {})
            try:
                if "thresholds" in exp:
                    lower, upper = exp["thresholds"]

                    if exp.get("format") == "percentage":
                        value *= 100  
                        lower *= 100
                        upper *= 100

                    if value < lower:
                        comment, icon = exp["recommendation"]["below"]
                   
                    elif value > upper:
                        comment, icon = exp["recommendation"]["above"]
                    
                    else:
                        comment, icon = exp["recommendation"]["normal"]
                   
                    self.text_box.insert(tk.END,
                        f"{metric}: {value:.6f} {icon} - {exp['explanation']}: {comment}\n")
            except:
                continue
     
if __name__ == "__main__":
    root = tk.Tk()
    app = StockAnalysisApp(root)
    root.mainloop() 