import pandas as pd

def add_sma(
        df: pd.DataFrame,
        period: int,
        ref_col: str,
        col_name: str
):
    df[col_name] = df[ref_col].rolling(period).mean()
    return df
