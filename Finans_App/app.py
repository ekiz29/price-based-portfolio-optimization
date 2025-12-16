# main.py
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf

# Modüllerimiz
from modules import plotting  # Yeni oluşturduğumuz dosya
import config
from modules import indicators, models, portfolio, analysis

class StockAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Profesyonel Borsa Analiz (Modüler)")
        self.root.geometry("1600x1200")
        
        self.colors = config.COLORS
        self.tickers = config.TICKERS
        self.portfolio_entries = {}
        
        self.setup_style()
        self.create_widgets()
        
    def setup_style(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('TButton', 
                             font=('Arial', 9, 'bold'),
                             background=self.colors['button'],
                             foreground=self.colors['text'],
                             borderwidth=1)
        self.style.map('TButton', background=[('active', '#505355')])
        
        self.style.configure('TFrame', background=self.colors['frame'])
        self.style.configure('TLabelframe', background=self.colors['frame'], foreground=self.colors['text'])
        self.style.configure('TLabelframe.Label', background=self.colors['frame'], foreground='#00FF00', font=('Arial', 10, 'bold'))
        self.style.configure('TLabel', background=self.colors['frame'], foreground=self.colors['text'])
        self.style.configure('TCombobox', fieldbackground=self.colors['button'], foreground='black')

        self.root.configure(bg=self.colors['background'])

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # --- 1. ÜST KONTROL PANELİ ---
        control_frame = ttk.Frame(main_frame, padding=5)
        control_frame.pack(fill=tk.X)
        
        # 1.1 Varlık Seçimi
        ttk.Label(control_frame, text="Varlık Seç:").grid(row=0, column=0, padx=5, sticky="w")
        self.stock_var = tk.StringVar()
        self.stock_combobox = ttk.Combobox(control_frame, textvariable=self.stock_var, values=list(self.tickers.keys()), width=18)
        self.stock_combobox.grid(row=0, column=1, padx=5, sticky="w")
        
        # 1.2 Butonlar (DÜZELTİLDİ: Analiz Et artık metin raporu veriyor)
        # Analiz Et -> Detaylı Rapor (analysis.generate_analysis_report)
        ttk.Button(control_frame, text="Analiz Et", command=self.run_detailed_analysis).grid(row=0, column=2, padx=5)
        
        # Temel Oranlar -> P/E, ROE vb. (analysis.get_fundamental_ratios)
        ttk.Button(control_frame, text="Temel Oranları Göster", command=self.run_fundamental_analysis).grid(row=0, column=3, padx=5)

        # 1.3 İndikatör Seçimi ve Grafik Çizme
        ttk.Label(control_frame, text="İndikatör Seç:").grid(row=0, column=4, padx=5, sticky="e")
        self.indicator_var = tk.StringVar()
        inds = ["RSI","MACD","Bollinger Bands","Ichimoku","ADX(14)","Pivot Points","Fibonacci Pivot","Williams %R","CCI(14)","ATR%(14)","ROC","Ultimate Oscillator","MFI(14)","OBV","VWAP","CMF","1Y Price","STOCH(9,6)","Moving Averages","Exponential Moving Averages","Parabolic_SAR","US10YEAR","VIX","DXY","USD/JPY","EUR/USD","VOLUME","Nadaraya_watson","SuperTrend","F/K"]
        self.ind_combobox = ttk.Combobox(control_frame, textvariable=self.indicator_var, values=inds, width=15)
        self.ind_combobox.grid(row=0, column=5, padx=5, sticky="w")
        self.ind_combobox.current(0)
        
        # Grafik Çiz -> Grafik Basar (plot_chart)
        ttk.Button(control_frame, text="Grafik Çiz", command=self.plot_chart).grid(row=0, column=6, padx=5)
        
        # 1.4 Portföy
        ttk.Label(control_frame, text="|  Portföy:").grid(row=0, column=7, padx=10, sticky="w")
        ttk.Button(control_frame, text="Varlık Ekle", command=self.add_stock_selection).grid(row=0, column=8, padx=2)
        ttk.Button(control_frame, text="Optimize Et", command=self.run_optimization).grid(row=0, column=9, padx=2)

        # --- 2. YAPAY ZEKA PANELİ ---
        ml_main_frame = ttk.Frame(main_frame, padding=5)
        ml_main_frame.pack(fill=tk.X, pady=5)

        self.create_model_group(ml_main_frame, "LR Modeli (Linear Regression)", "LR", side=tk.LEFT)
        self.create_model_group(ml_main_frame, "SVM Modeli (Support Vector)", "SVM", side=tk.LEFT)
        self.create_model_group(ml_main_frame, "XGBoost Modeli (Decision Tree)", "XGB", side=tk.LEFT)

        # --- 3. İÇERİK ALANI ---
        content = ttk.Frame(main_frame)
        content.pack(fill=tk.BOTH, expand=True)
        
        left_panel = ttk.Frame(content, width=450)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)
        
        self.portfolio_frame = ttk.Frame(left_panel)
        self.portfolio_frame.pack(fill=tk.X, pady=5)
        
        self.text_box = tk.Text(left_panel, width=55, height=40, bg="black", fg="#00FF00", 
                                font=("Consolas", 10), insertbackground="white")
        self.text_box.pack(fill=tk.BOTH, expand=True)
        
        self.canvas_frame = ttk.Frame(content)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def create_model_group(self, parent, title, model_code, side):
        group_frame = ttk.LabelFrame(parent, text=title, padding=10)
        group_frame.pack(side=side, fill=tk.BOTH, expand=True, padx=5)
        periods = [("10g", 10), ("1a", 30), ("3a", 90), ("6a", 180)]
        for text, days in periods:
            ttk.Button(group_frame, text=text, width=4, 
                       command=lambda m=model_code, d=days: self.run_ml(m, d)).pack(side=tk.LEFT, padx=5)

    # --- BUTON FONKSİYONLARI ---
    
    def run_detailed_analysis(self):
        """Detaylı Teknik ve Risk Raporu (Senin İstediğin)"""
        stock = self.stock_var.get()
        if not stock: return
        ticker = self.tickers[stock]
        
        self.text_box.delete('1.0', tk.END)
        self.text_box.insert(tk.END, f"{stock} Analiz Ediliyor...\n")
        self.root.update()
        
        try:
            df = yf.Ticker(ticker).history(period="1y",interval="1d")
            df = indicators.calculate_technical_indicators(df)
            # analysis.py içindeki rapor fonksiyonu çağrılır
            report = analysis.generate_analysis_report(ticker, df)
            
            self.text_box.delete('1.0', tk.END)
            self.text_box.insert(tk.END, report)
        except Exception as e:
            self.text_box.insert(tk.END, f"Hata: {e}")

    def run_fundamental_analysis(self):
        """Temel Oranları Getirir (P/E, ROE...)"""
        stock = self.stock_var.get()
        if not stock: return
        ticker = self.tickers[stock]
        
        self.text_box.delete('1.0', tk.END)
        self.text_box.insert(tk.END, "Veriler çekiliyor...\n")
        self.root.update()
        
        report = analysis.get_fundamental_ratios(ticker)
        self.text_box.insert(tk.END, report)

    def plot_chart(self):
        """Grafiği modules/plotting.py dosyasını kullanarak çizer."""
        stock = self.stock_var.get()
        ind = self.indicator_var.get()
        if not stock: 
            messagebox.showwarning("Uyarı", "Lütfen bir varlık seçin.")
            return
        
        ticker = self.tickers[stock]
        
        try:
            # 1. Veriyi Çek
            df = yf.Ticker(ticker).history(period="1y",interval="1d")
            if df.empty: raise ValueError("Veri alınamadı!")
            
            # 2. İndikatörleri Hesapla
            df = indicators.calculate_technical_indicators(df)
            
            # 3. Canvas Temizle
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            
            # 4. Modülden Grafiği Al (İŞTE SİHİR BURADA)
            # plotting.py dosyasındaki fonksiyonu çağırıyoruz
            fig = plotting.create_chart(df, stock, ind, self.colors)
            
            # 5. Ekrana Bas
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("Hata", f"Grafik çizilirken hata: {str(e)}")

    # --- PORTFÖY VE ML (Değişmedi) ---
    def add_stock_selection(self):
        row = len(self.portfolio_entries)
        entry_frame = ttk.Frame(self.portfolio_frame)
        entry_frame.pack(fill=tk.X, pady=2)
        var = tk.StringVar()
        cb = ttk.Combobox(entry_frame, textvariable=var, values=list(self.tickers.keys()), state="readonly", width=15)
        cb.pack(side=tk.LEFT, padx=2)
        cb.current(0)
        amount_var = tk.StringVar(value="1000")
        ttk.Entry(entry_frame, textvariable=amount_var, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(entry_frame, text="X", width=2, command=lambda: self.remove_stock_selection(row, entry_frame)).pack(side=tk.LEFT, padx=2)
        self.portfolio_entries[row] = (cb, amount_var, entry_frame) # Fixed variable name usage

    def remove_stock_selection(self, row, frame):
        frame.destroy()
        if row in self.portfolio_entries: del self.portfolio_entries[row]

    def run_optimization(self):
        weights = {}
        for row, (cb, entry_var, _) in self.portfolio_entries.items():
            weights[cb.get()] = float(entry_var.get())
        if len(weights) < 2: 
            messagebox.showwarning("Uyarı", "En az 2 varlık gerekli")
            return
        
        self.text_box.delete('1.0', tk.END)
        self.text_box.insert(tk.END, "Optimizasyon yapılıyor...\n")
        self.root.update()
        res = portfolio.optimize(weights, self.tickers)
        self.text_box.insert(tk.END, "\n" + res)

    def run_ml(self, model_type, days):
        stock = self.stock_var.get()
        if not stock: return
        self.text_box.delete('1.0', tk.END)
        self.text_box.insert(tk.END, f"{model_type} ({days} Gün) çalışıyor...\n")
        self.root.update()
        res = models.train_and_predict(self.tickers[stock], model_type, days)
        self.text_box.insert(tk.END, "\n" + res)

if __name__ == "__main__":
    root = tk.Tk()
    app = StockAnalysisApp(root)
    root.mainloop()