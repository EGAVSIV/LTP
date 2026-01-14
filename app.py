import streamlit as st
import time
from price_fetcher import fetch_ltp
from breakout import check_breakout
from symbols import NSE_INDICES, NSE_STOCKS, COMMODITIES

st.set_page_config(layout="wide")
st.title("📊 Live NSE & Commodity Dashboard")

# ==================== SOUND ====================
ALERT_SOUND = "assets/alert.mp3"

def play_sound():
    st.audio(ALERT_SOUND, format="audio/mp3")

# ==================== LAYOUT ====================
left, right = st.columns(2)

# ==================== NSE ====================
with left:
    st.subheader("🇮🇳 NSE (Index + Stocks)")
    nse_symbols = st.multiselect(
        "Select 5 NSE symbols",
        NSE_INDICES + NSE_STOCKS,
        max_selections=5
    )

# ==================== COMMODITIES ====================
with right:
    st.subheader("🛢 Commodities (Capital.com)")
    com_symbols = st.multiselect(
        "Select 5 Commodities",
        COMMODITIES,
        max_selections=5
    )

if len(nse_symbols) != 5 or len(com_symbols) != 5:
    st.warning("Please select exactly 5 symbols in EACH section")
    st.stop()

placeholder = st.empty()

# ==================== LOOP ====================
while True:
    with placeholder.container():
        nse_col, com_col = st.columns(2)

        # -------- NSE PANEL --------
        with nse_col:
            st.markdown("### 🇮🇳 NSE")
            cols = st.columns(5)

            for i, sym in enumerate(nse_symbols):
                price, prev = fetch_ltp(sym, "NSE")
                move = check_breakout(price, prev)

                color = "#00ff00" if move == "UP" else "#ff3333"

                with cols[i]:
                    st.markdown(
                        f"""
                        <div style="padding:20px;
                        border-radius:10px;
                        background:#111;
                        text-align:center;
                        box-shadow:0 0 10px {color};">
                        <h3 style="color:#00e6ff">{sym}</h3>
                        <h1 style="color:{color};font-size:42px">{price}</h1>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                if move:
                    play_sound()

        # -------- COMMODITY PANEL --------
        with com_col:
            st.markdown("### 🛢 Commodities")
            cols = st.columns(5)

            for i, sym in enumerate(com_symbols):
                price, prev = fetch_ltp(sym, "CAPITALCOM")
                move = check_breakout(price, prev)

                color = "#00ff00" if move == "UP" else "#ff3333"

                with cols[i]:
                    st.markdown(
                        f"""
                        <div style="padding:20px;
                        border-radius:10px;
                        background:#111;
                        text-align:center;
                        box-shadow:0 0 10px {color};">
                        <h3 style="color:#ffaa00">{sym}</h3>
                        <h1 style="color:{color};font-size:42px">{price}</h1>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                if move:
                    play_sound()

    time.sleep(1)
