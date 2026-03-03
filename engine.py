import pandas as pd
import numpy as np
import yfinance as yf

def get_data_portal(ticker="EURUSD=X"):
    try:
        # Puxamos dados para cálculo de Pips (ontem vs hoje)
        data = yf.download(ticker, period="2d", interval="1m", progress=False)
        if data.empty: return pd.DataFrame(), 0.0, "OFFLINE"
        
        # Garante que estamos lidando com números escalares (float) e não Series
        close_prices = data['Close'].iloc[-1]
        if isinstance(close_prices, pd.Series):
            p_atual = float(close_prices.iloc[0])
        else:
            p_atual = float(close_prices)
            
        # Busca fechamento anterior para Pips
        hist_diario = yf.download(ticker, period="2d", interval="1d", progress=False)
        p_ontem = float(hist_diario['Close'].iloc[-2])
        pips_diff = (p_atual - p_ontem) * 10000
        
        df = data[['Open', 'High', 'Low', 'Close']].copy()
        df.columns = ['open', 'high', 'low', 'close']
        return df, float(pips_diff), "ONLINE"
    except Exception as e:
        return pd.DataFrame(), 0.0, f"ERRO: {str(e)}"

def analyze_sentinel_v8(df):
    p_atual = float(df['close'].iloc[-1])
    retornos = df['close'].pct_change().dropna()
    
    # Probabilidade Monte Carlo
    vol = retornos.std() if retornos.std() > 0 else 0.0001
    sims = p_atual * (1 + np.random.normal(0, vol, (1000, 30))).cumprod(axis=1)
    alvo_mc = float(np.percentile(sims[:, -1], 75))
    prob_sucesso = float(np.mean(sims[:, -1] > p_atual) * 100)
    
    # Estado do Mercado (Z-Score)
    media_movel = df['close'].rolling(20).mean().iloc[-1]
    desvio_padrao = df['close'].rolling(20).std().iloc[-1]
    z_score = float((p_atual - media_movel) / (desvio_padrao + 1e-9))
    
    if abs(z_score) < 0.5: 
        estado = "LATERALIZADO"
    elif z_score > 1.2: 
        estado = "TENDÊNCIA DE ALTA"
    elif z_score < -1.2: 
        estado = "TENDÊNCIA DE BAIXA"
    else: 
        estado = "AGUARDANDO DEFINIÇÃO"
    
    # Risco
    atr = float((df['high'] - df['low']).rolling(14).mean().iloc[-1])
    stop = p_atual - (atr * 2.5) if z_score > 0 else p_atual + (atr * 2.5)
    
    return p_atual, alvo_mc, float(stop), prob_sucesso, estado, z_score
