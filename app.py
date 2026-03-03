import streamlit as st
from engine import fetch_api_data, run_ia_strategy, calculate_metrics, monte_carlo_target
from interface import apply_ui, display_cards
from datetime import datetime

apply_ui()
API_KEY = "101SM0EBPEQUHEHJ"

data, status = fetch_api_data(API_KEY)

if not data.empty:
    p_atual = data['Close'].iloc[-1]
    prob_ia = run_ia_strategy(data)
    saturated, atr = calculate_metrics(data)
    target = monte_carlo_target(p_atual, data['Returns'].std())
    
    st.markdown(f"<div class='price-hero'>{p_atual:.5f}</div>", unsafe_allow_html=True)
    st.caption(f"SYNC: {datetime.now().strftime('%H:%M:%S')} | CONFIDENCE: {prob_ia*100:.1f}%")

    # Gatilhos Estratégicos Inteiros
    u1_gate = prob_ia > 0.62
    u2_gate = data['Volume'].iloc[-1] > data['Volume'].rolling(20).mean().iloc[-1] * 1.5
    
    display_cards(u1_gate, u2_gate, p_atual, target, p_atual - (atr*2), saturated)
else:
    st.error("ERRO DE SINCRONIZAÇÃO: A API Alpha Vantage atingiu o limite ou a chave está propagando.")

st.markdown("<script>setTimeout(function(){window.location.reload();}, 60000);</script>", unsafe_allow_html=True)
