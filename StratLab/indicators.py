import pandas as pd
import sys
import data

def add_indicator(
        df: pd.DataFrame,
        ticker: str,
        start: str,
        end: str,
        study: str,
        period: int,
        dtype: str,
        value: int=0,
        short_period: int = None,
        long_period: int = None
) -> pd.DataFrame:
    
    if study is None:
        study = 'VALUE'

    for i in df:
        print(df)
    study = study.upper()
    ref_col = f'{ticker} {dtype}'
    col_name = f'{ticker} {period} {study}'
    high_col = f'{ticker} High'
    low_col = f'{ticker} Low'

    # Define functions for adding all indicators...

    def ema():
        from _IndicatorLib import ema
        return ema.add_ema(df, period, ref_col, col_name)

    def macd():
        from _IndicatorLib import macd
        return macd.add_macd(df, short_period, long_period, period, ref_col, col_name)

    def price():
        return df

    def rsi():
        from _IndicatorLib import rsi
        return rsi.add_rsi(df, period, ref_col, col_name)
    
    def sar():
        from _IndicatorLib import sar
        if high_col not in df.columns:
            df = data.fetch_data(df, ticker, 'High', start, end)
        if low_col not in df.columns:
            df = data.fetch_data(df, ticker, 'Low', start, end)
        return sar.add_sar(
            df=df,
            col_name=col_name,
            high_col=high_col,
            low_col=low_col,
            close_col=ref_col
        )

    def sma():
        from _IndicatorLib import sma
        return sma.add_sma(df, period, ref_col, col_name)

    def val():
        df[f'Value {value}'] = value
        return df

    indicator_functions = {
        'EMA': ema,
        'MACD': macd,
        'PRICE': price,
        'RSI': rsi,
        'SAR': sar,
        'SMA': sma,
        'VALUE': val
    }

    if study != 'PRICE':
        df = indicator_functions[study]()

    if study not in indicator_functions.keys():
        raise ValueError('Please use a valid study!')
    
    df.dropna(inplace=True)

    return df
