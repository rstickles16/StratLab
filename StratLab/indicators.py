import pandas as pd

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
    col_name = f"{ticker} {period} {study}"
    col_name = f'{ticker} {period} {study}'

    if study == 'VALUE':
        df[f'Value {value}'] = value

    if study == 'SMA':
        df[col_name] = df[ref_col].rolling(period).mean()

    if study == 'RSI':
        delta = df[ref_col].diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        ema_up = up.ewm(com=(period-1), adjust=False).mean()
        ema_down = down.ewm(com=(period-1), adjust=False).mean()
        rs = ema_up / ema_down
        df[col_name] = (100-(100/(1+rs)))

    supported_list = [
        'VALUE','PRICE', 'RSI', 'SMA'
    ]
    if study not in supported_list:
        raise ValueError('Please use a valid study!')

    df.dropna(inplace=True)

    return df
