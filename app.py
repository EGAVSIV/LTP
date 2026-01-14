import streamlit as st
import time
from tvDatafeed import TvDatafeed, Interval

# ==============================
# STREAMLIT CONFIG
# ==============================
st.set_page_config(layout="wide", page_title="Live NSE & Commodity LTP")

# ==============================
# TV DATAFEED
# ==============================
tv = TvDatafeed()

# ==============================
# SYMBOL LISTS
# ==============================
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

# ==============================
# PRICE FETCH FUNCTION
# ==============================
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

# ==============================
# BREAKOUT / DIRECTION LOGIC
# ==============================
def check_direction(curr, prev):
    if curr is None or prev is None:
        return None
    if curr > prev:
        return "UP"
    elif curr < prev:
        return "DOWN"
    return None

# ==============================
# SOUND STATE
# ==============================
if "last_move" not in st.session_state:
    st.session_state.last_move = {}

def play_sound():
    st.audio("assets/alert.mp3", format="audio/mp3")

# ==============================
# UI HEADER
# ==============================
st.title("📊 Live NSE & Commodity Dashboard")

left, right = st.columns(2)

# ==============================
# NSE SELECTION
# ==============================
with left:
    st.subheader("🇮🇳 NSE (Index + Stocks)")
    nse_selected = st.multiselect(
        "Select NSE symbols (1–5)",
        NSE_SYMBOLS,
        max_selections=5
    )

# ==============================
# COMMODITY SELECTION
# ==============================
with right:
    st.subheader("🛢 Commodities (Capital.com)")
    com_selected = st.multiselect(
        "Select Commodities (1–5)",
        COMMODITIES,
        max_selections=5
    )

# ==============================
# VALIDATION
# ==============================
if len(nse_selected) == 0 and len(com_selected) == 0:
    st.warning("Select at least 1 symbol in NSE or Commodities")
    st.stop()

# ==============================
# AUTO REFRESH (SAFE)
# ==============================


# ==============================
# DISPLAY AREA
# ==============================
nse_col, com_col = st.columns(2)

# ==============================
# NSE PANEL
# ==============================
with nse_col:
    if nse_selected:
        st.markdown("### 🇮🇳 NSE")
        cols = st.columns(len(nse_selected))

        for i, sym in enumerate(nse_selected):
            price, prev = fetch_ltp(sym, "NSE")
            move = check_direction(price, prev)

            color = "#00ff00" if move == "UP" else "#ff3333" if move == "DOWN" else "#cccccc"

            # sound only on change
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

# ==============================
# COMMODITY PANEL
# ==============================
with com_col:
    if com_selected:
        st.markdown("### 🛢 Commodities")
        cols = st.columns(len(com_selected))

        for i, sym in enumerate(com_selected):
            price, prev = fetch_ltp(sym, "CAPITALCOM")
            move = check_direction(price, prev)

            color = "#00ff00" if move == "UP" else "#ff3333" if move == "DOWN" else "#cccccc"

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



time.sleep(1)
st.experimental_rerun()

