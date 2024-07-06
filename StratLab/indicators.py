import pandas as pd
import sys

def add_indicator(
        df: pd.DataFrame,
        ticker: str,
        study: str,
        period: int,
        dtype: str,
        value: int=0,
        short_period: int = None,
        long_period: int = None
        

) -> pd.DataFrame:
    
    print(long_period)
    if study is None:
        study = 'VALUE'

    study = study.upper()
    ref_col = f'{ticker} {dtype}'
    col_name = f'{ticker} {period} {study}'

    def ema():
        from _IndicatorLib import ema
        return ema.add_ema(df, period, ref_col, col_name)

    def price():
        return df

    def rsi():
        from _IndicatorLib import rsi
        return rsi.add_rsi(df, period, ref_col, col_name)

    def sma():
        from _IndicatorLib import sma
        return sma.add_sma(df, period, ref_col, col_name)

    def val():
        df[f'Value {value}'] = value
        return df

    indicator_functions = {
        'EMA': ema,
        'PRICE': price,
        'RSI': rsi,
        'SMA': sma,
        'VALUE': val
    }

    if study != 'PRICE':
        df = indicator_functions[study]()

    if study not in indicator_functions.keys():
        raise ValueError('Please use a valid study!')
    
    df.dropna(inplace=True)

    return df
