import streamlit as st

def apply_ui_v8():
    st.markdown("""
        <style>
        .stApp { background-color: #05070a; color: #e6edf3; }
        .main-card { 
            background: #11141a; border-radius: 15px; padding: 25px; 
            border: 1px solid #1f242c; text-align: center; margin-bottom: 15px;
        }
        .price-text { font-family: 'JetBrains Mono', monospace; font-size: 5rem; font-weight: 800; color: #ffffff; margin:0; }
        .pips-tag { font-size: 1.2rem; font-weight: bold; padding: 5px 15px; border-radius: 20px; }
        .entry-box { padding: 20px; border-radius: 12px; margin-top: 15px; border: 1px solid #30363d; }
        </style>
    """, unsafe_allow_html=True)

def render_didactic_hud(preco, pips, alvo, stop, prob, estado, z_score):
    # Topo: Preço e Pips
    cor_pips = "#3fb950" if pips >= 0 else "#f85149"
    seta = "▲" if pips >= 0 else "▼"
    
    st.markdown(f"""
        <div class='main-card'>
            <p style='color:#8b949e; letter-spacing: 2px;'>EUR/USD - AO VIVO</p>
            <h1 class='price-text'>{preco:.5f}</h1>
            <span class='pips-tag' style='background: {cor_pips}22; color: {cor_pips};'>
                {seta} {abs(pips):.1f} PIPS (HOJE)
            </span>
        </div>
    """, unsafe_allow_html=True)

    # Centro: Declaração de Intenção
    st.markdown(f"### 🚩 Mercado: **{estado}**")
    
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        # Lógica de Decisão Explicita
        if z_score > 1.5:
            st.markdown(f"""<div class='entry-box' style='background: #23863622; border-color: #238636;'>
                <h3 style='color:#3fb950; margin:0;'>🟢 ENTRADA DETECTADA: COMPRA</h3>
                <p>O preço rompeu a inércia para cima. Probabilidade de êxito: <b>{prob:.1f}%</b></p>
            </div>""", unsafe_allow_html=True)
        elif z_score < -1.5:
            st.markdown(f"""<div class='entry-box' style='background: #f8514922; border-color: #f85149;'>
                <h3 style='color:#f85149; margin:0;'>🔴 ENTRADA DETECTADA: VENDA</h3>
                <p>O preço rompeu a inércia para baixo. Probabilidade de êxito: <b>{100-prob:.1f}%</b></p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class='entry-box' style='background: #1f242c;'>
                <h3 style='color:#8b949e; margin:0;'>⏳ AGUARDANDO SINAL...</h3>
                <p>Sem distorção estatística suficiente para operar com segurança agora.</p>
            </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div class='main-card' style='text-align: left;'>
                <p style='color:#3fb950; margin:0;'>✓ ALVO DE LUCRO (TP)</p>
                <h2 style='margin:0;'>{alvo:.5f}</h2>
                <hr style='border-color:#222;'>
                <p style='color:#f85149; margin:0;'>✗ SAÍDA DE RISCO (SL)</p>
                <h2 style='margin:0;'>{stop:.5f}</h2>
            </div>
        """, unsafe_allow_html=True)
