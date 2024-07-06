import pandas as pd

def add_macd(
        df: pd.DataFrame,
        short_period: int,
        long_period: int,
        signal_period: int,
        ref_col: str
) -> pd.DataFrame:
    short_ema = df[ref_col].ewm(span=short_period, adjust=False).mean()
    long_ema = df[ref_col].ewm(span=long_period, adjust=False).mean()
    df['MACD'] = short_ema - long_ema
    df['MACD_Signal'] = df['MACD'].ewm(span=signal_period, adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
    return df
