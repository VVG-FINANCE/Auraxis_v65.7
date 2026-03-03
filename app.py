import streamlit as st
from datetime import datetime
from engine import fetch_api_data, run_ia_strategy, calculate_metrics, monte_carlo_target, calculate_risk_reward
from interface import apply_ui, render_heartbeat, render_strategy_cards, render_footer_metrics

st.set_page_config(page_title="AURAXIS V65.7", layout="wide")
apply_ui()

API_KEY = "101SM0EBPEQUHEHJ"
now_str = datetime.now().strftime('%H:%M:%S')

data, status_feed = fetch_api_data(API_KEY)

if not data.empty:
    p_atual = data['Close'].iloc[-1]
    prob_ia = run_ia_strategy(data)
    saturated, atr = calculate_metrics(data)
    target_mc = monte_carlo_target(p_atual, data['Returns'].std())
    
    # Cálculo de Risco:Retorno
    stop_tecnico = p_atual - (atr * 2.5)
    rr_ratio, rr_viable = calculate_risk_reward(p_atual, target_mc, stop_tecnico)
    
    # Interface
    render_heartbeat(status_feed, now_str)
    st.markdown(f"<div class='price-hero'>{p_atual:.5f}</div>", unsafe_allow_html=True)
    
    u1_trigger = prob_ia > 0.62
    u2_trigger = data['Volume'].iloc[-1] > (data['Volume'].rolling(20).mean().iloc[-1] * 1.2)
    
    render_strategy_cards(u1_trigger, u2_trigger, target_mc, stop_tecnico, prob_ia, saturated, rr_ratio, rr_viable)
    render_footer_metrics(data['Returns'].tail(10).std()*100000, target_mc, status_feed)
else:
    st.error("Sincronizando com a API...")
    render_heartbeat("RECONNECTING", now_str)

st.markdown("<script>setTimeout(function(){window.location.reload();}, 60000);</script>", unsafe_allow_html=True)
