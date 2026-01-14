from tvDatafeed import TvDatafeed, Interval

tv = TvDatafeed()   # guest login

def fetch_ltp(symbol, exchange="NSE"):
    try:
        df = tv.get_hist(
            symbol=symbol,
            exchange=exchange,
            interval=Interval.in_1_minute,
            n_bars=1
        )
        if df is None or df.empty:
            return None
        return float(df["close"].iloc[-1])
    except Exception:
        return None
