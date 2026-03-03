import streamlit as st

def apply_ui_v8():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0e14; color: #e6edf3; }
        .main-card { 
            background: #161b22; border-radius: 15px; padding: 30px; 
            border: 1px solid #30363d; text-align: center; margin-bottom: 20px;
        }
        .price-text { font-family: 'JetBrains Mono', monospace; font-size: 5.5rem; font-weight: 800; margin:0; }
        .pips-up { color: #3fb950; font-size: 1.5rem; }
        .pips-down { color: #f85149; font-size: 1.5rem; }
        .status-box { padding: 10px; border-radius: 8px; font-weight: bold; margin-top: 10px; text-transform: uppercase; }
        .entry-detected { background: rgba(35, 134, 54, 0.2); border: 1px solid #3fb950; color: #3fb950; }
        .no-entry { background: rgba(139, 148, 158, 0.1); border: 1px solid #484f58; color: #8b949e; }
        </style>
    """, unsafe_allow_html=True)

def render_didactic_hud(preco, pips, alvo, stop, prob, estado, z_score):
    # Cabeçalho de Preço e Pips
    cor_pips = "pips-up" if pips >= 0 else "pips-down"
    sinal_pips = "+" if pips >= 0 else ""
    
    st.markdown(f"""
        <div class='main-card'>
            <p style='color:#8b949e; margin-bottom:5px;'>EUR/USD - PREÇO ATUAL</p>
            <h1 class='price-text'>{preco:.5f}</h1>
            <p class='{cor_pips}'>{sinal_pips}{pips:.1f} Pips desde ontem</p>
        </div>
    """, unsafe_allow_html=True)

    # Painel de Comunicação Clara
    st.subheader(f"📡 Estado do Mercado: {estado}")
    
    c1, c2 = st.columns(2)
    
    # Decisão de Entrada
    is_entry = abs(z_score) > 1.5 and prob > 55
    
    with c1:
        if is_entry:
            st.markdown(f"""
                <div class='status-box entry-detected'>
                    🎯 ENTRADA DETECTADA<br>
                    Sinal: {"COMPRA" if z_score > 0 else "VENDA"}<br>
                    Probabilidade: {prob:.1f}%
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div class='status-box no-entry'>⏳ AGUARDANDO ENTRADA...</div>", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div class='main-card' style='padding:15px;'>
                <p style='margin:0; font-size:0.8rem;'>ALVO DE LUCRO (TP)</p>
                <h2 style='color:#3fb950; margin:0;'>{alvo:.5f}</h2>
                <p style='margin:0; font-size:0.8rem; margin-top:10px;'>SAÍDA DE PREJUÍZO (SL)</p>
                <h2 style='color:#f85149; margin:0;'>{stop:.5f}</h2>
            </div>
        """, unsafe_allow_html=True)
