import pandas as pd
import sys

def add_indicator(
        df: pd.DataFrame,
        ticker: str,
        study: str,
        period: int,
        dtype: str,
        value: int=0

) -> pd.DataFrame:
    if study is None:
        study = 'VALUE'

    study = study.upper()
    ref_col = f'{ticker} {dtype}'
    col_name = f'{ticker} {period} {study}'

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
        'RSI': rsi,
        'SMA': sma,
        'VALUE': val
    }

    if study != 'PRICE':
        df = indicator_functions[study]()

    supported_list = [
    'VALUE','PRICE', 'RSI', 'SMA'
    ]

    if study not in supported_list:
        raise ValueError('Please use a valid study!')
    
    df.dropna(inplace=True)

    return df
