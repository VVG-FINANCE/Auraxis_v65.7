import streamlit as st
import time
from datetime import datetime
from engine import get_data_portal, analyze_sentinel_v8
from interface import apply_ui_v8, render_didactic_hud

st.set_page_config(page_title="AURAXIS ORÁCULO v8", layout="wide", page_icon="🔮")
apply_ui_v8()

placeholder = st.empty()

while True:
    with placeholder.container():
        df, pips, status_api = get_data_portal()
        
        if not df.empty:
            p_atual, alvo, stop, prob, estado, z_score = analyze_sentinel_v8(df)
            
            # Cabeçalho Técnico
            st.caption(f"Status: {status_api} | Sincronia: {datetime.now().strftime('%H:%M:%S')} | Refresh: 5s")
            
            # Dashboard Didático
            render_didactic_hud(p_atual, pips, alvo, stop, prob, estado, z_score)
            
            # Barra de Força (Visual)
            st.write("---")
            st.write("Força de Inércia (Z-Score)")
            st.progress(min(max((z_score + 3) / 6, 0.0), 1.0))
            
        else:
            st.error("Conectando ao fluxo de dados... Verifique sua conexão.")
            
    time.sleep(5)
