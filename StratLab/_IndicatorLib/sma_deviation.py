import pandas as pd

def add_sma_deviation(
        df: pd.DataFrame,
        price_col: str,
        sma_col: str,
        col_name: str
):
        df[col_name] = df[price_col] / df[sma_col] - 1
        return df