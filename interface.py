import streamlit as st

def apply_ui_sentinel():
    st.markdown("""
        <style>
        .stApp { background-color: #050505; color: #e0e0e0; }
        .price-container { 
            text-align: center; padding: 10px; border-radius: 15px;
            background: linear-gradient(180deg, rgba(255,255,255,0.05) 0%, rgba(0,0,0,0) 100%);
        }
        .main-price { font-family: 'JetBrains Mono', monospace; font-size: 6rem; font-weight: 800; margin: 0; }
        .card-sentinel { 
            background: #111; border: 1px solid #222; padding: 15px; 
            border-radius: 10px; text-align: center; height: 100%;
        }
        .status-bar { font-size: 0.8rem; color: #666; font-family: monospace; }
        </style>
    """, unsafe_allow_html=True)

def render_dashboard(price, target, stop, z_score, sentiment):
    st.markdown(f"<div class='price-container'><p class='main-price'>{price:.5f}</p></div>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='card-sentinel'>INÉRCIA<br><h2 style='color:#58a6ff;'>{z_score:.2f}σ</h2></div>", unsafe_allow_html=True)
    with c2:
        rr = abs(target - price) / abs(price - stop)
        st.markdown(f"<div class='card-sentinel'>RISCO:RETORNO<br><h2 style='color:#3fb950;'>1:{rr:.2f}</h2></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='card-sentinel'>SENTIMENTO<br><h2 style='color:#f1e05a;'>{sentiment}</h2></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='card-sentinel'>ALVO MC<br><h2>{target:.5f}</h2></div>", unsafe_allow_html=True)
