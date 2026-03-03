import streamlit as st
from datetime import datetime

# Importando os pedaços (módulos) que você criou
from engine import fetch_api_data, run_ia_strategy, calculate_metrics, monte_carlo_target
from interface import apply_ui, display_main_price, render_strategy_cards, render_heartbeat, render_footer_metrics

# 1. Configuração Inicial e Estilo
st.set_page_config(page_title="AURAXIS V65.7 - PLATINUM", layout="wide", page_icon="🧠")
apply_ui()

# 2. Identificação da Chave e Pulso do Sistema
API_KEY = "101SM0EBPEQUHEHJ"
now_str = datetime.now().strftime('%H:%M:%S')

# 3. Coleta de Dados via Engine
# O st.spinner evita que a tela fique branca enquanto a API responde
with st.spinner('Sincronizando com a Rede Neural...'):
    data, status_feed = fetch_api_data(API_KEY)

# 4. Verificação de Integridade dos Dados
if not data.empty:
    # --- PROCESSAMENTO ---
    p_atual = data['Close'].iloc[-1]
    prob_ia = run_ia_strategy(data)
    saturated, atr = calculate_metrics(data)
    target_mc = monte_carlo_target(p_atual, data['Returns'].std())
    
    # Hz Simulado baseado na volatilidade recente para o Espectro
    hz_calc = data['Returns'].tail(10).std() * 100000
    
    # --- RENDERIZAÇÃO DA INTERFACE ---
    render_heartbeat(status_feed, now_str)
    display_main_price(p_atual)
    
    # Lógica de Gatilho para os Cards
    # U1 (Sniper): IA acima de 62% e volatilidade controlada
    u1_trigger = prob_ia > 0.62 and not saturated
    
    # U2 (Flow): Volume acima da média de 20 períodos
    vol_media = data['Volume'].rolling(20).mean().iloc[-1]
    u2_trigger = data['Volume'].iloc[-1] > (vol_media * 1.2)
    
    # Exibe os Cards de Operação
    render_strategy_cards(
        u1_active=u1_trigger, 
        u2_active=u2_trigger, 
        target=target_mc, 
        stop=p_atual - (atr * 2.5), 
        confidence=prob_ia, 
        saturated=saturated
    )
    
    # Exibe as métricas de rodapé
    render_footer_metrics(hz_calc, target_mc, status_feed)

else:
    # Caso a API falhe ou atinja o limite
    st.error("⚠️ ERRO DE SINCRONIZAÇÃO")
    st.info("A API Alpha Vantage atingiu o limite de requisições ou a chave ainda não foi validada. O sistema tentará reconectar em 60 segundos.")
    render_heartbeat("RECONNECTING", now_str)

# 5. Script de Auto-Refresh (Mantém o sistema vivo)
st.markdown("""
    <script>
        setTimeout(function(){
            window.location.reload();
        }, 60000);
    </script>
""", unsafe_allow_html=True)
