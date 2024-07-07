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
        # Define the function to calculate SAR
        high = high_col
        low = low_col
        close = close_col

        sar = [0] * len(df)
        af = initial_af
        uptrend = True
        ep = high[0]  # extreme point
        sar[0] = low[0] - (high[0] - low[0])  # Initial SAR value

        for i in range(1, len(df)):
                if uptrend:
                        sar[i] = sar[i-1] + af * (ep - sar[i-1])
                if high[i] > ep:
                        ep = high[i]
                        af = min(af + step, max_af)
                if low[i] < sar[i]:
                        uptrend = False
                        sar[i] = ep
                        ep = low[i]
                        af = initial_af
                else:
                        sar[i] = sar[i-1] + af * (ep - sar[i-1])
                if low[i] < ep:
                        ep = low[i]
                        af = min(af + step, max_af)
                if high[i] > sar[i]:
                        uptrend = True
                        sar[i] = ep
                        ep = high[i]
                        af = initial_af

        df[col_name] = sar
        return df
