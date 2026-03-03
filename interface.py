import streamlit as st

def apply_ui():
    st.markdown("""
        <style>
        .stApp { background-color: #01040a; color: #c9d1d9; }
        .price-hero { font-size: 5rem; font-weight: 800; text-align: center; color: #ffffff; }
        .universe-box { padding: 20px; border-radius: 12px; border: 1px solid #30363d; background: rgba(13,17,23,0.8); margin-bottom: 10px; }
        .u1-active { border-left: 8px solid #238636; box-shadow: 0 0 15px rgba(35,134,54,0.2); }
        .u2-active { border-left: 8px solid #1f6feb; box-shadow: 0 0 15px rgba(31,111,235,0.2); }
        .saturated { border-left-color: #f1e05a !important; }
        </style>
    """, unsafe_allow_html=True)

def display_cards(u1, u2, p, target, stop, sat):
    c1, c2 = st.columns(2)
    with c1:
        if u1:
            st.markdown(f"<div class='universe-box u1-active {'saturated' if sat else ''}'><h3>U1: SNIPER</h3><p>ALVO: {target:.5f}<br>STOP: {stop:.5f}</p></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='universe-box' style='opacity:0.3;'><h3>AGUARDANDO U1</h3></div>", unsafe_allow_html=True)
    with c2:
        if u2:
            st.markdown(f"<div class='universe-box u2-active'><h3>U2: FLOW</h3><p>MOMENTUM ATIVO</p></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='universe-box' style='opacity:0.3;'><h3>AGUARDANDO U2</h3></div>", unsafe_allow_html=True)
