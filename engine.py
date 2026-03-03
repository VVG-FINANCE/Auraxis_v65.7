import pandas as pd
import numpy as np
import yfinance as yf

def get_data_v10(ticker="EURUSD=X"):
    try:
        # Carregamos dados robustos para análise de múltiplos tempos
        data = yf.download(ticker, period="1mo", interval="15m", progress=False)
        if data.empty: return pd.DataFrame(), 0.0
        
        p_atual = float(data['Close'].iloc[-1])
        # Cálculo de Pips em relação ao fechamento de ontem
        p_ontem = float(yf.download(ticker, period="2d", interval="1d", progress=False)['Close'].iloc[-2])
        pips_diff = (p_atual - p_ontem) * 10000
        
        df = data[['Open', 'High', 'Low', 'Close']].copy()
        df.columns = ['open', 'high', 'low', 'close']
        return df, float(pips_diff)
    except:
        return pd.DataFrame(), 0.0

def calculate_radar(df, mode="DAY", trend_direction=0):
    p_atual = float(df['close'].iloc[-1])
    
    # Configurações de "Musculatura" por Horizonte
    params = {
        "SCALPER": {"p": 10, "m": 1.5},
        "DAY": {"p": 24, "m": 2.2},
        "SWING": {"p": 50, "m": 3.8},
        "POSITION": {"p": 120, "m": 5.5}
    }
    
    p = params[mode]["p"]
    m = params[mode]["m"]
    
    # Cálculo de Inércia Institucional (Z-Score Adaptativo)
    ma = df['close'].rolling(p).mean().iloc[-1]
    std = df['close'].rolling(p).std().iloc[-1] + 1e-9
    z_score = (p_atual - ma) / std
    
    # Filtro de Fractal: Se não for Position, precisa estar alinhado com a tendência maior
    if mode != "POSITION" and trend_direction != 0:
        if (trend_direction > 0 and z_score < 0) or (trend_direction < 0 and z_score > 0):
            return None # Bloqueio por falta de alinhamento institucional

    atr = (df['high'] - df['low']).rolling(p).mean().iloc[-1]
    
    # Definição das Zonas Limites
    z_inf, z_sup = p_atual - (atr * 0.4), p_atual + (atr * 0.4)

    # Lógica de Gatilho Institucional
    if z_score > 1.3: # Acima da Inércia (Compra)
        return {
            "tipo": "COMPRA", "z_inf": z_inf, "z_sup": z_sup,
            "tp": [p_atual + (atr * m), p_atual + (atr * m * 1.3)],
            "sl": [p_atual - (atr * m * 0.7), p_atual - (atr * m)],
            "prob": min(65 + (z_score * 4), 98.8), "z": z_score
        }
    elif z_score < -1.3: # Abaixo da Inércia (Venda)
        return {
            "tipo": "VENDA", "z_inf": z_inf, "z_sup": z_sup,
            "tp": [p_atual - (atr * m), p_atual - (atr * m * 1.3)],
            "sl": [p_atual + (atr * m * 0.7), p_atual + (atr * m)],
            "prob": min(65 + (abs(z_score) * 4), 98.8), "z": z_score
        }
    return None
