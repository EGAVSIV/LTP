def check_breakout(curr, prev):
    if curr is None or prev is None:
        return None
    if curr > prev:
        return "UP"
    elif curr < prev:
        return "DOWN"
    return None
