import streamlit as st

def apply_ui():
    st.markdown("""
        <style>
        .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Inter', sans-serif; }
        .price-hero { font-family: 'JetBrains Mono', monospace; font-size: 5rem; font-weight: 800; text-align: center; color: #ffffff; margin-top: -20px; }
        .universe-box { padding: 20px; border-radius: 12px; border: 1px solid #30363d; background: rgba(22,27,34,0.9); margin-bottom: 15px; min-height: 200px; }
        .u1-active { border-left: 10px solid #238636; box-shadow: 0 0 20px rgba(35,134,54,0.1); }
        .u2-active { border-left: 10px solid #1f6feb; }
        .metric-label { font-size: 0.8rem; color: #8b949e; }
        .metric-value { font-size: 1.2rem; font-weight: bold; color: #ffffff; }
        .heartbeat { color: #10b981; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; text-align: right; }
        </style>
    """, unsafe_allow_html=True)

def render_heartbeat(status, time_str):
    st.markdown(f"<div class='heartbeat'>● SYNC_{status}: {time_str}</div>", unsafe_allow_html=True)

def render_strategy_cards(u1_active, u2_active, target, stop, confidence, saturated, rr_ratio, rr_viable):
    col1, col2 = st.columns(2)
    with col1:
        if u1_active:
            rr_color = "#3fb950" if rr_viable else "#f85149"
            rr_text = "VIÁVEL" if rr_viable else "RISCO_ALTO"
            st.markdown(f"""
                <div class='universe-box u1-active'>
                    <div style='display:flex; justify-content:space-between;'>
                        <h2 style='color:#3fb950; margin:0;'>U1: SNIPER</h2>
                        <span style='background:{rr_color}; color:black; padding:2px 8px; border-radius:5px; font-size:0.7rem; font-weight:bold;'>{rr_text}</span>
                    </div>
                    <hr style='border:0.1px solid #30363d;'>
                    <div class='metric-label'>Relação R:R</div>
                    <div class='metric-value'>1 : {rr_ratio:.2f}</div>
                    <div style='margin-top:10px;'>
                        <span class='metric-label'>Alvo (TP3):</span> <span style='color:#3fb950;'>{target:.5f}</span><br>
                        <span class='metric-label'>Stop (ATR):</span> <span style='color:#f85149;'>{stop:.5f}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div class='universe-box' style='opacity:0.3; text-align:center;'><br><h3>AGUARDANDO U1</h3><small>CONFLUÊNCIA NEURAL BAIXA</small></div>", unsafe_allow_html=True)
    with col2:
        if u2_active:
            st.markdown(f"""
                <div class='universe-box u2-active'>
                    <h2 style='color:#58a6ff; margin:0;'>U2: FLOW</h2>
                    <p style='color:#8b949e;'>VOLATILIDADE INSTITUCIONAL</p>
                    <hr style='border:0.1px solid #30363d;'>
                    <div class='metric-label'>Confiança IA</div>
                    <div class='metric-value'>{confidence*100:.1f}%</div>
                    <div class='metric-label' style='margin-top:10px;'>Saturação: <span style='color:{"#f1e05a" if saturated else "#10b981"};'>{"CRÍTICA" if saturated else "NORMAL"}</span></div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div class='universe-box' style='opacity:0.3; text-align:center;'><br><h3>AGUARDANDO U2</h3><small>VOLUME ABAIXO DA MÉDIA</small></div>", unsafe_allow_html=True)

def render_footer_metrics(hz, mc_proj, status):
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("Espectro Neural", f"{hz:.2f} Hz")
    c2.metric("Projeção MC", f"{mc_proj:.5f}")
    c3.metric("Status API", status)
