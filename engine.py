import pandas as pd
import numpy as np
import yfinance as yf
import requests

def get_yfinance_data(ticker="EURUSD=X"):
    """Puxa dados em tempo real com precisão de 1 minuto e histórico de 2 dias"""
    try:
        data = yf.download(ticker, period="2d", interval="1m", progress=False)
        if data.empty: return pd.DataFrame()
        # Ajuste para garantir que as colunas sejam simples
        df = data[['Open', 'High', 'Low', 'Close']].copy()
        df.columns = ['open', 'high', 'low', 'close']
        return df
    except:
        return pd.DataFrame()

def get_alpha_vantage_sentiment(api_key):
    """Usa Alpha Vantage apenas para conferir o Momentum Global (Oráculo)"""
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=EURUSD&apikey={api_key}'
    try:
        r = requests.get(url, timeout=3)
        data = r.json()
        change = float(data['Global Quote']['10. change percent'].replace('%', ''))
        return "BULLISH" if change > 0 else "BEARISH"
    except:
        return "NEUTRAL"

def calculate_sentinel_signals(df):
    """Lógica de Volatilidade e Probabilidade"""
    close = df['close'].iloc[-1]
    returns = df['close'].pct_change().dropna()
    
    # ATR para Stop dinâmico
    atr = (df['high'] - df['low']).rolling(14).mean().iloc[-1]
    
    # Monte Carlo (1000 caminhos para os próximos 5 min)
    sims = close * (1 + np.random.normal(returns.mean(), returns.std(), (1000, 5))).cumprod(axis=1)
    target = np.percentile(sims[:, -1], 80)
    
    # Z-Score (Força do Movimento)
    z_score = (close - df['close'].rolling(20).mean().iloc[-1]) / (df['close'].rolling(20).std().iloc[-1] + 1e-9)
    
    return close, target, close - (atr * 2.5), z_score
