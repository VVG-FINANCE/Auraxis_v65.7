import streamlit as st

def apply_ui():
    """Aplica o DNA visual do Auraxis: Dark Mode Profundo e Tipografia Mono"""
    st.markdown("""
        <style>
        /* Fundo e Container Principal */
        .stApp { 
            background-color: #0d1117; 
            color: #c9d1d9; 
            font-family: 'Inter', sans-serif; 
        }
        
        /* Preço Central (Hero Section) */
        .price-hero { 
            font-family: 'JetBrains Mono', monospace; 
            font-size: 5.5rem; 
            font-weight: 800; 
            text-align: center; 
            color: #ffffff; 
            margin-top: -30px;
            text-shadow: 0 0 30px rgba(255,255,255,0.1);
        }

        /* Boxes de Estratégia (Universo U1/U2) */
        .universe-box { 
            padding: 25px; 
            border-radius: 15px; 
            border: 1px solid #30363d; 
            background: rgba(22, 27, 34, 0.9); 
            margin-bottom: 20px;
            min-height: 220px;
            transition: 0.4s;
        }

        /* Status Ativo: Sniper (Verde) */
        .u1-active { 
            border-left: 10px solid #238636; 
            box-shadow: 0 10px 30px rgba(35,134,54,0.15);
        }

        /* Status Ativo: Flow (Azul) */
        .u2-active { 
            border-left: 10px solid #1f6feb; 
            box-shadow: 0 10px 30px rgba(31,111,235,0.15);
        }

        /* Indicador de Saturação (Amarelo) */
        .saturated-alert {
            background: rgba(241, 224, 90, 0.1) !important;
            border: 1px solid #f1e05a !important;
        }

        /* Etiquetas de Métricas */
        .metric-label { font-size: 0.75rem; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; }
        .metric-value { font-size: 1.4rem; font-weight: bold; color: #ffffff; }
        
        /* Heartbeat Animation */
        .heartbeat-text {
            color: #10b981;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            text-align: right;
            padding-right: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

def render_heartbeat(status, time_str):
    st.markdown(f"<div class='heartbeat-text'>● NEURAL_HEARTBEAT: {time_str} | SYS: {status}</div>", unsafe_allow_html=True)

def display_main_price(price):
    st.markdown(f"<div class='price-hero'>{price:.5f}</div>", unsafe_allow_html=True)

def render_strategy_cards(u1_active, u2_active, target, stop, confidence, saturated):
    col1, col2 = st.columns(2)
    
    with col1:
        if u1_active:
            # Card Sniper Ativo
            sat_class = "saturated-alert" if saturated else ""
            st.markdown(f"""
                <div class='universe-box u1-active {sat_class}'>
                    <h2 style='color:#3fb950; margin-top:0;'>U1: SNIPER</h2>
                    <p style='color:#8b949e; font-size:0.9rem;'>SINAL DE ALTA PROBABILIDADE DETECTADO</p>
                    <hr style='border: 0.1px solid #30363d;'>
                    <div class='metric-label'>Alvo Estatístico (TP3)</div>
                    <div class='metric-value' style='color:#3fb950;'>{target:.5f}</div>
                    <div style='margin-top:10px;'>
                        <span class='metric-label'>Stop Técnico:</span> 
                        <span style='color:#f85149; font-weight:bold;'>{stop:.5f}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Card Sniper Aguardando
            st.markdown("""
                <div class='universe-box' style='opacity:0.4; display:flex; align-items:center; justify-content:center;'>
                    <div style='text-align:center;'>
                        <h3 style='color:#484f58;'>AGUARDANDO U1</h3>
                        <small>CONVERGÊNCIA IA < 62%</small>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with col2:
        if u2_active:
            # Card Flow Ativo
            st.markdown(f"""
                <div class='universe-box u2-active'>
                    <h2 style='color:#58a6ff; margin-top:0;'>U2: FLOW</h2>
                    <p style='color:#8b949e; font-size:0.9rem;'>FLUXO INSTITUCIONAL IDENTIFICADO</p>
                    <hr style='border: 0.1px solid #30363d;'>
                    <div class='metric-label'>Confiança da IA</div>
                    <div class='metric-value'>{confidence*100:.1f}%</div>
                    <div style='margin-top:10px;'>
                        <span class='metric-label'>Estado:</span> 
                        <span style='color:#58a6ff; font-weight:bold;'>MOMENTUM</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Card Flow Aguardando
            st.markdown("""
                <div class='universe-box' style='opacity:0.4; display:flex; align-items:center; justify-content:center;'>
                    <div style='text-align:center;'>
                        <h3 style='color:#484f58;'>AGUARDANDO U2</h3>
                        <small>VOLUME RELATIVO BAIXO</small>
                    </div>
                </div>
            """, unsafe_allow_html=True)

def render_footer_metrics(hz, mc_proj, status):
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("Espectro Neural", f"{hz:.2f} Hz", delta="Alta Frequência" if hz > 15 else None)
    c2.metric("Projeção Monte Carlo", f"{mc_proj:.5f}")
    c3.metric("Status do Feed", status)
