import pandas as pd

def add_rsi (
        df: pd.DataFrame,
        period: int,
        ref_col: str,
        col_name: str
):
    delta = df[ref_col].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=(period-1), adjust=False).mean()
    ema_down = down.ewm(com=(period-1), adjust=False).mean()
    rs = ema_up / ema_down
    df[col_name] = (100-(100/(1+rs)))

    return df