# modules/portfolio.py
import yfinance as yf
import numpy as np
import pandas as pd

def optimize(weights_dict, tickers_map):
    """Portföy optimizasyonu hesaplar ve sonucu string olarak döner."""
    tickers = [tickers_map[k] for k in weights_dict.keys()]
    amounts = list(weights_dict.values())
    
    # Toplamın 1'e (veya 100'e) normalize edilmesi
    total_amount = sum(amounts)
    weights = [a/total_amount for a in amounts]
    
    try:
        data = yf.download(tickers=tickers, period="1y", interval="1d", group_by='ticker', auto_adjust=False)
        adj_close = pd.DataFrame()
        
        for ticker in tickers:
            col = data[ticker]['Adj Close'] if 'Adj Close' in data[ticker] else data[ticker]['Close']
            adj_close[ticker] = col
            
        returns = adj_close.pct_change().dropna()
        num_days = len(returns)
        
        # Hesaplamalar
        port_returns = (returns * weights).sum(axis=1)
        total_return = (1 + port_returns).prod() - 1
        
        cov_matrix = returns.cov()
        port_variance = np.dot(weights, np.dot(cov_matrix, weights))
        port_volatility = np.sqrt(port_variance) * np.sqrt(num_days)
        
        # Benchmark (S&P 500)
        market = yf.download('^GSPC', period="1y")['Close'].pct_change().dropna()
        
        # Metrikler
        rf_rate = 0.04
        sharpe = (total_return - rf_rate) / port_volatility
        
        # Çıktı Metni Hazırla
        result = "=== Portföy Optimizasyon Sonuçları ===\n\n"
        result += f"İncelenen Gün: {num_days}\n"
        result += f"Yıllık Getiri: %{total_return*100:.2f}\n"
        result += f"Volatilite (Risk): %{port_volatility*100:.2f}\n"
        result += f"Sharpe Oranı: {sharpe:.2f}\n"
        
        result += "\nVarlık Dağılımı:\n"
        for i, ticker in enumerate(weights_dict.keys()):
            result += f"- {ticker}: %{weights[i]*100:.2f}\n"
            
        return result
        
    except Exception as e:
        return f"Hata oluştu: {str(e)}"