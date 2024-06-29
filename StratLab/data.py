import pandas as pd
import yfinance as yf
from datetime import datetime as dt

def fetch_data(
        df: pd.DataFrame=None,
        ticker: str=None,
        dtype: str=None,
        start: str='1950-01-01',
        end: str=dt.today()
):
    df[f'{ticker} {dtype}'] = yf.download(
        tickers=ticker,
        start=start,
        end=end,
        progress=False
    )[dtype]

    # df.dropna(inplace=True)

    return df
