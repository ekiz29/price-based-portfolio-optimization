# modules/models.py
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix
import ta

def get_ml_data(ticker, period='2y'):
    """Model için gerekli veriyi ve feature'ları hazırlar."""
    try:
        data = yf.download(ticker, period=period)
        if data.empty: return None
        df = data.copy()
        
        # Feature Engineering (Senin orijinal kodundaki feature'lar)
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA_20_bin'] = (df['EMA_20'] > df['EMA_20'].shift(1)).astype(int)
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        df['EMA_50_bin'] = (df['EMA_50'] > df['EMA_50'].shift(1)).astype(int)
        
        # RSI
        delta = df['Close'].diff(1)
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI_14'] = 100 - (100 / (1 + rs))
        
        # MACD
        ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
        ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = ema_12 - ema_26
        
        # Williams %R
        high14 = df['High'].rolling(window=14).max()
        low14 = df['Low'].rolling(window=14).min()
        df['Williams_%R'] = -100 * (high14 - df['Close']) / (high14 - low14)

        # Tahvil Faizi (TNX) - Senin kodundaki feature
        try:
            tahvil = yf.download('^TNX', start=df.index.min(), end=df.index.max())
            df['TNX'] = tahvil['Close']
            df['TNX'] = df['TNX'].fillna(method='ffill')
        except:
            df['TNX'] = 0 # Veri çekilemezse 0 ata

        # Target (Gelecek fiyat şimdikinden yüksek mi?)
        df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
        df.dropna(inplace=True)
        return df
    except Exception as e:
        return None

def train_and_predict(ticker, model_type, window_size):
    """
    Tüm modelleri ve zaman pencerelerini yöneten tek fonksiyon.
    model_type: 'LR', 'SVM', 'XGB'
    window_size: Gün sayısı (örn: 10, 30, 90, 180)
    """
    df = get_ml_data(ticker)
    if df is None: return "Veri alınamadı."
    
    # Son 386 günü al (orijinal kodundaki gibi)
    df = df[-386:]
    
    features = ['RSI_14', 'MACD', 'Williams_%R', 'TNX', 'EMA_20_bin', 'EMA_50_bin']
    train_ratio = 0.8
    train_size = int(window_size * train_ratio)
    
    scores = []
    output_log = f"=== {model_type} Analizi ({window_size} Günlük Pencere) ===\n\n"
    
    # Rolling Window döngüsü
    # Pencere sayısını sınırla (çok uzun sürmemesi için)
    max_windows = 12 if window_size < 50 else 4
    
    for i in range(max_windows):
        start_idx = i * window_size # Orijinal kodundaki mantık
        end_idx = start_idx + window_size
        
        window_df = df.iloc[start_idx:end_idx]
        if len(window_df) < window_size: continue
        
        X = window_df[features]
        y = window_df['Target']
        
        X_train, y_train = X.iloc[:train_size], y.iloc[:train_size]
        X_test, y_test = X.iloc[train_size:], y.iloc[train_size:]
        
        # Scaling
        scaler = StandardScaler()
        try:
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
        except: continue
        
        # Model Seçimi
        if model_type == 'LR':
            model = LinearRegression()
            model.fit(X_train_scaled, y_train)
            y_pred = (model.predict(X_test_scaled) > 0.5).astype(int)
            
        elif model_type == 'SVM':
            if len(y_train.unique()) < 2: continue
            model = SVC(kernel='rbf', C=1.0, gamma='scale')
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            
        elif model_type == 'XGB':
            if len(y_train.unique()) < 2: continue
            model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
            model.fit(X_train, y_train) # XGB scale istemez genelde ama verilse de olur
            y_pred = model.predict(X_test)
            
        report = classification_report(y_test, y_pred, output_dict=True)
        acc = report['accuracy']
        f1 = report['1']['f1-score'] if '1' in report else 0
        
        scores.append({'acc': acc, 'f1': f1})
        output_log += f"Pencere {i+1} (Gün {start_idx}-{end_idx}): Accuracy: {acc:.2f}, F1: {f1:.2f}\n"
        
    if scores:
        avg_acc = sum(s['acc'] for s in scores) / len(scores)
        avg_f1 = sum(s['f1'] for s in scores) / len(scores)
        output_log += f"\nORTALAMA SONUÇLAR:\nAccuracy: {avg_acc:.2f}\nF1-Score (Artış Tahmini): {avg_f1:.2f}\n"
    else:
        output_log += "Yeterli veri ile analiz yapılamadı.\n"
        
    return output_log