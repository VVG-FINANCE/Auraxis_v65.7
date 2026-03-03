import pandas as pd
import numpy as np
import yfinance as yf
import requests

def get_data_portal(api_key, ticker="EURUSD=X"):
    try:
        # Puxamos 5 dias para calcular a variação em relação ao fechamento de ontem
        data = yf.download(ticker, period="5d", interval="1m", progress=False)
        if data.empty: return pd.DataFrame(), 0, "OFFLINE"
        
        df = data[['Open', 'High', 'Low', 'Close']].copy()
        df.columns = ['open', 'high', 'low', 'close']
        
        # Cálculo de Pips em relação ao fechamento de ontem
        fechamento_ontem = yf.download(ticker, period="2d", interval="1d", progress=False)['Close'].iloc[-2]
        pips_diff = (df['close'].iloc[-1] - fechamento_ontem) * 10000
        
        return df, pips_diff, "ONLINE"
    except:
        return pd.DataFrame(), 0, "ERRO_CONEXAO"

def analyze_sentinel_v8(df):
    p_atual = df['close'].iloc[-1]
    retornos = df['close'].pct_change().dropna()
    
    # 1. Probabilidade via Monte Carlo (Cálculo de Convergência)
    sims = p_atual * (1 + np.random.normal(retornos.mean(), retornos.std(), (1000, 30))).cumprod(axis=1)
    alvo_mc = np.percentile(sims[:, -1], 75)
    prob_sucesso = np.mean(sims[:, -1] > p_atual) * 100
    
    # 2. Identificação de Estado do Mercado
    z_score = (p_atual - df['close'].rolling(20).mean().iloc[-1]) / (df['close'].rolling(20).std().iloc[-1] + 1e-9)
    vol_relativa = df['close'].rolling(10).std().iloc[-1] / df['close'].rolling(50).std().iloc[-1]
    
    if vol_relativa < 0.8: estado = "LATERALIZADO (SEM TENDÊNCIA)"
    elif z_score > 1.2: estado = "TENDÊNCIA DE ALTA"
    elif z_score < -1.2: estado = "TENDÊNCIA DE BAIXA"
    else: estado = "AGUARDANDO DEFINIÇÃO"
    
    # 3. Gerenciamento de Risco
    atr = (df['high'] - df['low']).rolling(14).mean().iloc[-1]
    stop = p_atual - (atr * 2.5) if z_score > 0 else p_atual + (atr * 2.5)
    
    return p_atual, alvo_mc, stop, prob_sucesso, estado, z_score
