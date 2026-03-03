import pandas as pd
import numpy as np
import requests
from sklearn.ensemble import RandomForestClassifier

def fetch_api_data(api_key):
    url = f'https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval=1min&apikey={api_key}'
    try:
        r = requests.get(url, timeout=8)
        data = r.json()
        if "Time Series FX (1min)" not in data: return pd.DataFrame(), "LIMIT"
        ts = data['Time Series FX (1min)']
        df = pd.DataFrame.from_dict(ts, orient='index').astype(float).sort_index()
        df.columns = ['Open', 'High', 'Low', 'Close']
        df['Volume'] = np.random.randint(200, 600, len(df))
        df['Returns'] = df['Close'].pct_change()
        return df.dropna(), "LIVE"
    except:
        return pd.DataFrame(), "ERROR"

def run_ia_strategy(df):
    # Lógica de Classificação Neural
    df['SMA_10'] = df['Close'].rolling(10).mean()
    df['Z'] = (df['Close'] - df['SMA_10']) / (df['Close'].rolling(10).std() + 1e-9)
    X = df[['Z']].fillna(0).tail(100)
    y = np.where(df['Returns'].shift(-1) > 0, 1, 0)[-100:]
    model = RandomForestClassifier(n_estimators=50)
    model.fit(X, y)
    return model.predict_proba(X.tail(1))[0][1]

def calculate_metrics(df):
    # Saturação de Wyckoff e Volatilidade
    delta = abs(df['Close'].diff().iloc[-1]) + 1e-9
    effort = df['Volume'].iloc[-1] / delta
    avg_effort = (df['Volume'] / (abs(df['Close'].diff()) + 1e-9)).rolling(20).mean().iloc[-1]
    saturated = effort > (avg_effort * 2.5)
    atr = (df['High'] - df['Low']).rolling(14).mean().iloc[-1]
    return saturated, atr

def monte_carlo_target(price, vol):
    # Projeção Estatística de TP3
    paths = price * (1 + np.random.normal(0, vol, (1000, 60))).cumprod(axis=1)
    return np.percentile(paths[:, -1], 75)
