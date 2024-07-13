import pandas as pd

def add_ema(
        df: pd.DataFrame,
        period: int,
        ref_col: str,
        col_name: str
):
    df[col_name] = df[ref_col].ewm(span=period, adjust=False).mean()
    return df