from tvDatafeed import TvDatafeed, Interval

tv = TvDatafeed()

def fetch_ltp(symbol, exchange, interval=Interval.in_1_minute):
    try:
        df = tv.get_hist(
            symbol=symbol,
            exchange=exchange,
            interval=interval,
            n_bars=2
        )
        if df is None or df.empty:
            return None, None

        close = float(df["close"].iloc[-1])
        prev = float(df["close"].iloc[-2])
        return close, prev

    except Exception:
        return None, None
