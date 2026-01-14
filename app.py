import streamlit as st
import time
from tvDatafeed import TvDatafeed, Interval

# =================================================
# PAGE CONFIG (MUST BE FIRST STREAMLIT CALL)
# =================================================
st.set_page_config(layout="wide", page_title="Live NSE & Commodity LTP")

# =================================================
# TV DATAFEED INIT
# =================================================
tv = TvDatafeed()

# =================================================
# SYMBOL MASTER LISTS  (<<< FIXED LOCATION)
# =================================================
NSE_SYMBOLS = [
    "NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY",
    "RELIANCE", "HDFCBANK", "ICICIBANK", "INFY",
    "TCS", "SBIN", "AXISBANK", "ITC"
]

COMMODITIES = [
    "NATURALGAS",
    "CRUDEOIL",
    "COPPER",
    "SILVER"
]

# =================================================
# PRICE FETCH
# =================================================
def fetch_ltp(symbol, exchange):
    try:
        df = tv.get_hist(
            symbol=symbol,
            exchange=exchange,
            interval=Interval.in_1_minute,
            n_bars=2
        )
        if df is None or df.empty:
            return None, None

        return float(df["close"].iloc[-1]), float(df["close"].iloc[-2])
    except Exception:
        return None, None

# =================================================
# PRICE DIRECTION
# =================================================
def price_direction(curr, prev):
    if curr is None or prev is None:
        return None
    if curr > prev:
        return "UP"
    if curr < prev:
        return "DOWN"
    return None

# =================================================
# SESSION STATE
# =================================================
if "last_move" not in st.session_state:
    st.session_state.last_move = {}

def play_sound():
    st.audio("assets/alert.mp3", format="audio/mp3")

# =================================================
# UI
# =================================================
st.title("📊 Live NSE & Commodity Dashboard")

left, right = st.columns(2)

with left:
    st.subheader("🇮🇳 NSE")
    nse_selected = st.multiselect(
        "Select NSE symbols (1–5)",
        NSE_SYMBOLS,
        max_selections=5
    )

with right:
    st.subheader("🛢 Commodities")
    com_selected = st.multiselect(
        "Select Commodities (1–5)",
        COMMODITIES,
        max_selections=5
    )

if not nse_selected and not com_selected:
    st.warning("Select at least one symbol")
    st.stop()

# =================================================
# DISPLAY PANELS
# =================================================
nse_col, com_col = st.columns(2)

# ----------------- NSE -----------------
with nse_col:
    if nse_selected:
        st.markdown("### 🇮🇳 NSE")
        cols = st.columns(len(nse_selected))

        for i, sym in enumerate(nse_selected):
            price, prev = fetch_ltp(sym, "NSE")
            move = price_direction(price, prev)

            color = (
                "#00ff00" if move == "UP"
                else "#ff3333" if move == "DOWN"
                else "#cccccc"
            )

            if move and st.session_state.last_move.get(sym) != move:
                play_sound()
                st.session_state.last_move[sym] = move

            with cols[i]:
                st.markdown(
                    f"""
                    <div style="
                        padding:20px;
                        border-radius:12px;
                        background:#0e1117;
                        text-align:center;
                        box-shadow:0 0 12px {color};
                    ">
                        <h3 style="color:#00e6ff">{sym}</h3>
                        <h1 style="color:{color}; font-size:44px;">
                            {price if price else "—"}
                        </h1>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# ----------------- COMMODITIES -----------------
with com_col:
    if com_selected:
        st.markdown("### 🛢 Commodities")
        cols = st.columns(len(com_selected))

        for i, sym in enumerate(com_selected):
            price, prev = fetch_ltp(sym, "CAPITALCOM")
            move = price_direction(price, prev)

            color = (
                "#00ff00" if move == "UP"
                else "#ff3333" if move == "DOWN"
                else "#cccccc"
            )

            if move and st.session_state.last_move.get(sym) != move:
                play_sound()
                st.session_state.last_move[sym] = move

            with cols[i]:
                st.markdown(
                    f"""
                    <div style="
                        padding:20px;
                        border-radius:12px;
                        background:#0e1117;
                        text-align:center;
                        box-shadow:0 0 12px {color};
                    ">
                        <h3 style="color:#ffaa00">{sym}</h3>
                        <h1 style="color:{color}; font-size:44px;">
                            {price if price else "—"}
                        </h1>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# =================================================
# SAFE AUTO REFRESH
# =================================================
time.sleep(1)
st.experimental_rerun()
