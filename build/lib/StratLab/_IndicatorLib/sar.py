import pandas as pd

def add_sar(
        df: pd.DataFrame,
        col_name: str,
        high_col: str,
        low_col: str,
        close_col: str,
        initial_af: float = 0.02,
        max_af: float = 0.2,
        step: float = 0.02
):
    # Ensure the columns are numeric
    df[high_col] = pd.to_numeric(df[high_col])
    df[low_col] = pd.to_numeric(df[low_col])
    df[close_col] = pd.to_numeric(df[close_col])
    
    # Define the function to calculate SAR
    high = df[high_col]
    low = df[low_col]
    close = df[close_col]

    sar = [0] * len(df)
    af = initial_af
    uptrend = True
    ep = high.iloc[0]  # extreme point
    sar[0] = low.iloc[0] - (high.iloc[0] - low.iloc[0])  # Initial SAR value for uptrend
    if close.iloc[1] < close.iloc[0]:
        uptrend = False
        ep = low.iloc[0]
        sar[0] = high.iloc[0] + (high.iloc[0] - low.iloc[0])  # Initial SAR value for downtrend

    for i in range(1, len(df)):
        if uptrend:
            sar[i] = sar[i-1] + af * (ep - sar[i-1])
            if high.iloc[i] > ep:
                ep = high.iloc[i]
                af = min(af + step, max_af)
            if low.iloc[i] < sar[i]:
                uptrend = False
                sar[i] = ep
                ep = low.iloc[i]
                af = initial_af
        else:
            sar[i] = sar[i-1] + af * (ep - sar[i-1])
            if low.iloc[i] < ep:
                ep = low.iloc[i]
                af = min(af + step, max_af)
            if high.iloc[i] > sar[i]:
                uptrend = True
                sar[i] = ep
                ep = high.iloc[i]
                af = initial_af

    df[col_name] = sar
    return df
