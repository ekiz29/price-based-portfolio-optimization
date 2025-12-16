# Modül: optimizer.py
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from tkinter import messagebox
import tkinter as tk

# Fonksiyonlar, ana uygulama örneğini (app) alarak, onun değişkenlerine (self.text_box, self.tickers vb.) erişir.

def optimize_portfolio(app):
    """
    Seçilen varlıklar için Portföy Optimizasyonu (Monte Carlo veya Markowitz) yapar.
    """
    app.text_box.delete('1.0', tk.END)
    
    # app.get_portfolio_weights metodu app.py'de kaldığı için onu doğrudan çağırıyoruz.
    weights_dict = app.get_portfolio_weights()
    if not weights_dict:
        return

    selected_names = list(weights_dict.keys())
    tickers = [app.tickers[k] for k in selected_names]
    
    if len(tickers) < 2:
        messagebox.showwarning("Uyarı", "Optimizasyon için en az iki varlık seçilmelidir.")
        return

    try:
        # Veri çekme
        data = yf.download(tickers=tickers, period="1y", interval="1d")
        
        # Sadece Kapanış fiyatlarını al
        adj_close = pd.DataFrame()
        for ticker_code in tickers:
            # yfinance'ın multi-ticker indirme yapısını kontrol et
            if ticker_code in data.columns:
                 # Tek hisse indirilmişse
                 adj_close[ticker_code] = data[ticker_code]
            elif (ticker_code, 'Close') in data.columns:
                 # Çoklu hisse indirilmişse
                 adj_close[ticker_code] = data[(ticker_code, 'Close')]
            else:
                 raise ValueError(f"Hata: {ticker_code} için kapanış (Close) verisi bulunamadı.")


        adj_close.columns = tickers # Kolon isimlerini temizle
        returns = adj_close.pct_change().dropna()
        num_assets = len(tickers)
        num_days = len(returns)

        # Monte Carlo Simülasyonu Fonksiyonları
        def portfolio_performance(weights, returns):
            # Yıllık getiri
            annual_returns = (1 + returns.mean()) ** 252 - 1 
            port_return = np.sum(annual_returns * weights) * 100
            
            # Yıllık volatilite
            cov_matrix = returns.cov() * 252 
            port_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * 100
            
            return port_return, port_volatility

        def objective_function(weights):
            # Optimizasyon için Minimze edilecek değer (Negatif Sharpe Oranı)
            return -portfolio_performance(weights, returns)[0] / portfolio_performance(weights, returns)[1]

        # Kısıtlar ve Sınırlar
        constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}) # Ağırlıkların toplamı 1 olmalı
        bounds = tuple((0, 1) for _ in range(num_assets)) # Her ağırlık 0 ile 1 arasında olmalı
        initial_weights = np.array([1/num_assets] * num_assets)

        # Optimizasyon (Maksimum Sharpe Oranını Bul)
        optimized_results = minimize(
            objective_function, 
            initial_weights, 
            method='SLSQP', 
            bounds=bounds, 
            constraints=constraints
        )

        optimized_weights = optimized_results.x
        opt_return, opt_volatility = portfolio_performance(optimized_weights, returns)
        opt_sharpe = -optimized_results.fun # Negatif Sharpe'ı pozitife çevir

        # Sonuçları app.text_box'a yaz
        app.text_box.insert(tk.END, "=== Portföy Optimizasyon Sonuçları (Max Sharpe) ===\n\n")
        app.text_box.insert(tk.END, f"İncelenen Gün Sayısı: {num_days} gün\n")
        app.text_box.insert(tk.END, f"Optimal Yıllık Getiri: {opt_return:.2f}%\n")
        app.text_box.insert(tk.END, f"Optimal Yıllık Volatilite: {opt_volatility:.2f}%\n")
        app.text_box.insert(tk.END, f"Optimal Sharpe Oranı: {opt_sharpe:.2f}\n")
        app.text_box.insert(tk.END, "\nOptimal Varlık Dağılımı:\n")
        
        for i, ticker_code in enumerate(tickers):
             # Orijinal hisse adını bul ve yaz
             stock_name = selected_names[i]
             app.text_box.insert(tk.END, f"- {stock_name} ({ticker_code}): {optimized_weights[i]:.2%}\n")

        # Portföy seçimini temizle (Bu fonksiyon app.py'de kalmalı, çünkü GUI nesnelerini yok ediyor)
        app.clear_portfolio_selection() 

    except Exception as e:
        messagebox.showerror("Hata", f"Portföy optimizasyonu başarısız: {str(e)}")


# app.py'deki clear_portfolio_selection fonksiyonu GUI widgetlarını yönettiği için
# app.py içinde kalmalıdır. Bu modül sadece optimize_portfolio'yu içerir.