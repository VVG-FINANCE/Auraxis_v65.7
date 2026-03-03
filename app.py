import streamlit as st
import time
from datetime import datetime
from engine import get_yfinance_data, get_alpha_vantage_sentiment, calculate_sentinel_signals
from interface import apply_ui_sentinel, render_dashboard

st.set_page_config(page_title="AURAXIS SENTINEL v7", layout="wide")
apply_ui_sentinel()

# Barra lateral para controle e chave
API_KEY = "101SM0EBPEQUHEHJ"
TICKER = "EURUSD=X"

# Placeholder para atualização em tempo real sem refresh de página
placeholder = st.empty()

# Loop de 5 segundos
while True:
    with placeholder.container():
        df = get_yfinance_data(TICKER)
        
        if not df.empty:
            sentiment = get_alpha_vantage_sentiment(API_KEY)
            price, target, stop, z_score = calculate_sentinel_signals(df)
            
            # Cabeçalho de Status
            st.markdown(f"<div class='status-bar'>HIFI_DATA_ACTIVE | TICK_RATE: 5s | SYNC: {datetime.now().strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
            
            # Dashboard
            render_dashboard(price, target, stop, z_score, sentiment)
            
            # Lógica de Gatilho
            if z_score > 1.2 and sentiment == "BULLISH":
                st.success(f"🚀 SINAL CONFIRMADO: COMPRA | TP: {target:.5f} | SL: {stop:.5f}")
        else:
            st.warning("Aguardando fluxo de dados do yfinance...")
            
    time.sleep(5)
