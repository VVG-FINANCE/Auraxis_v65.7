import streamlit as st
import time
from datetime import datetime
from engine import get_data_portal, analyze_sentinel_v8
from interface import apply_ui_v8, render_didactic_hud

st.set_page_config(page_title="AURAXIS ORÁCULO v8", layout="wide")
apply_ui_v8()

API_KEY = "101SM0EBPEQUHEHJ"
placeholder = st.empty()

while True:
    with placeholder.container():
        df, pips, status_api = get_data_portal(API_KEY)
        
        if not df.empty:
            p_atual, alvo, stop, prob, estado, z_score = analyze_sentinel_v8(df)
            
            # Rodapé Técnico Discreto
            st.caption(f"Sincronização: {status_api} | Última Atualização: {datetime.now().strftime('%H:%M:%S')} | Tick: 5s")
            
            # Dashboard Principal
            render_didactic_hud(p_atual, pips, alvo, stop, prob, estado, z_score)
            
            # Explicação Didática Adicional
            if abs(z_score) > 1.5:
                st.info(f"💡 Dica do Analista: O mercado está se afastando da média com força. {"A pressão compradora é dominante." if z_score > 0 else "A pressão vendedora é dominante."}")
        else:
            st.warning("⚠️ Tentando reconectar ao fluxo de dados do mercado...")
            
    time.sleep(5)
