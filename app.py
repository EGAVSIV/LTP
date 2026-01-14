import streamlit as st
import time
from symbols import SYMBOLS
from price_fetcher import fetch_ltp

st.set_page_config(
    page_title="Live Market Dashboard",
    layout="wide"
)

st.title("📈 Live Symbol Price Dashboard")

# ==============================
# Symbol Selection
# ==============================
selected = st.multiselect(
    "Select exactly 5 symbols",
    SYMBOLS,
    max_selections=5
)

if len(selected) != 5:
    st.warning("Please select exactly 5 symbols")
    st.stop()

# ==============================
# Auto refresh every 1 second
# ==============================
placeholder = st.empty()

while True:
    with placeholder.container():
        cols = st.columns(5)

        for idx, symbol in enumerate(selected):
            price = fetch_ltp(symbol)

            with cols[idx]:
                st.markdown(
                    f"""
                    <div style="
                        background-color:#0e1117;
                        border-radius:10px;
                        padding:25px;
                        text-align:center;
                        box-shadow:0 0 10px #00ffcc;
                    ">
                        <h2 style="color:#00ffcc">{symbol}</h2>
                        <h1 style="color:white;font-size:48px">
                            {price if price else '—'}
                        </h1>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    time.sleep(1)
