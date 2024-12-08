import pandas as pd

def add_rsi (
        df: pd.DataFrame,
        period: int,
        ref_col: str,
        col_name: str
):
        # Add calculation for RSI to dataframe
        delta = df[ref_col].diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        ema_up = up.ewm(com=(period-1), adjust=False).mean()
        ema_down = down.ewm(com=(period-1), adjust=False).mean()
        rs = ema_up / ema_down
        df[col_name] = (100-(100/(1+rs)))

        # Remove the first x number of observations from the dataframe
           # where x is the period...this ensures that the lookback period
           # has enough data to create accurate calculation
        df = df.iloc[period-1:].copy()
        return df