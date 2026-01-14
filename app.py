import streamlit as st
import time
from tvDatafeed import TvDatafeed, Interval

# ==============================
# CONFIG
# ==============================
st.set_page_config(layout="wide", page_title="Live NSE & Commodity LTP")

tv = TvDatafeed()

NSE_STOCKS  = [
    'NIFTY','BANKNIFTY','CNXFINANCE','CNXMIDCAP','NIFTYJR','360ONE','ABB','ABCAPITAL',
    'ADANIENSOL','ADANIENT','ADANIGREEN','ADANIPORTS','ALKEM','AMBER','AMBUJACEM',
    'ANGELONE','APLAPOLLO','APOLLOHOSP','ASHOKLEY','ASIANPAINT','ASTRAL','AUBANK',
    'AUROPHARMA','AXISBANK','BAJAJ_AUTO','BAJAJFINSV','BRITANNIA','INDIANB','INDHOTEL',
    'HFCL','HAVELLS','BAJFINANCE','BANDHANBNK','BANKBARODA','BANKINDIA','BDL','BEL',
    'BHARATFORG','BHARTIARTL','BHEL','BIOCON','BLUESTARCO','BOSCHLTD','BPCL','BSE',
    'CAMS','CANBK','CDSL','CGPOWER','CHOLAFIN','CIPLA','COALINDIA','COFORGE','COLPAL',
    'CONCOR','CROMPTON','CUMMINSIND','CYIENT','DABUR','DALBHARAT','DELHIVERY',
    'DIVISLAB','DIXON','DLF','DMART','DRREDDY','EICHERMOT','ETERNAL','EXIDEIND',
    'FEDERALBNK','FORTIS','GAIL','GLENMARK','GMRAIRPORT','GODREJCP','GODREJPROP',
    'GRASIM','HAL','HDFCAMC','HDFCBANK','HDFCLIFE','HEROMOTOCO','HINDALCO','HINDPETRO',
    'HINDUNILVR','HINDZINC','HUDCO','ICICIBANK','ICICIGI','ICICIPRULI','IDEA',
    'IDFCFIRSTB','IEX','IGL','IIFL','INDIGO','INDUSINDBK','INDUSTOWER','INFY',
    'INOXWIND','IOC','IRCTC','IREDA','IRFC','ITC','JINDALSTEL','JIOFIN','JSWENERGY',
    'JSWSTEEL','JUBLFOOD','KALYANKJIL','KAYNES','KEI','KFINTECH','KOTAKBANK',
    'KPITTECH','LAURUSLABS','LICHSGFIN','LICI','LODHA','LT','LTF','LTIM','LUPIN','M&M',
    'MANAPPURAM','MANKIND','MARICO','MARUTI','MAXHEALTH','MAZDOCK','MCX','MFSL',
    'MOTHERSON','MPHASIS','MUTHOOTFIN','NATIONALUM','NAUKRI','NBCC','NCC','NESTLEIND',
    'NMDC','NTPC','NUVAMA','NYKAA','OBEROIRLTY','OFSS','OIL','ONGC','PAGEIND',
    'PATANJALI','PAYTM','PFC','PGEL','PHOENIXLTD','PIIND','PNB','PNBHOUSING',
    'POLICYBZR','POLYCAB','PIDILITIND','PERSISTENT','PETRONET','NHPC','HCLTECH',
    'POWERGRID','PPLPHARMA','PRESTIGE','RBLBANK','RECLTD','RELIANCE','RVNL','SAIL',
    'SAMMAANCAP','SBICARD','SBILIFE','SBIN','SHREECEM','SHRIRAMFIN','SIEMENS',
    'SOLARINDS','SONACOMS','SRF','SUNPHARMA','SUPREMEIND','SUZLON','SYNGENE',
    'TATACONSUM','TATAELXSI','TATAMOTORS','TATAPOWER','TATASTEEL','TATATECH','TCS',
    'TECHM','TIINDIA','TITAGARH','TITAN','TORNTPHARM','TORNTPOWER','TRENT','TVSMOTOR',
    'ULTRACEMCO','UNIONBANK','UNITDSPR','UNOMINDA','UPL','VBL','VEDL','VOLTAS',
    'WIPRO','YESBANK','ZYDUSLIFE'
]
COMMODITIES = [
    "NATURALGAS",
    "CRUDEOIL",
    "COPPER",
    "SILVER",
    "ALUMINIUM"
]

NSE_INDICES = [
    "NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"
]

# ==============================
# FETCH PRICE
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
# DIRECTION
# ==============================
def direction(curr, prev):
    if curr is None or prev is None:
        return None
    if curr > prev:
        return "UP"
    if curr < prev:
        return "DOWN"
    return None

# ==============================
# SESSION STATE
# ==============================
if "last_move" not in st.session_state:
    st.session_state.last_move = {}

def play_sound():
    st.audio("assets/alert.mp3", format="audio/mp3")

# ==============================
# UI
# ==============================
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

# ==============================
# DISPLAY
# ==============================
nse_col, com_col = st.columns(2)

with nse_col:
    if nse_selected:
        st.markdown("### 🇮🇳 NSE")
        cols = st.columns(len(nse_selected))

        for i, sym in enumerate(nse_selected):
            price, prev = fetch_ltp(sym, "NSE")
            move = direction(price, prev)

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
                        <h3 style="color:#00e6ff">{sym}</h3>
                        <h1 style="color:{color}; font-size:44px;">
                            {price if price else "—"}
                        </h1>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

with com_col:
    if com_selected:
        st.markdown("### 🛢 Commodities")
        cols = st.columns(len(com_selected))

        for i, sym in enumerate(com_selected):
            price, prev = fetch_ltp(sym, "CAPITALCOM")
            move = direction(price, prev)

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

# ==============================
# REFRESH
# ==============================
time.sleep(1)
st.experimental_rerun()
