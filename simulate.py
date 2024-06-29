import pandas as pd
import numpy as np

def simulate(df: pd.DataFrame, starting_amt: float):
    df.dropna(inplace=True)
    df['Previous Holding'] = df['Holding'].shift(1)
    
    # Identify trade flag
    df['Trade Flag'] = (df['Holding'] != df['Holding'].shift(1)).astype(int)
    # Identify trade flag and trade id
    df['ID'] = np.arange(len(df))
    df['Days in Open Trade'] = 0
    df['Days in Closed Trade'] = 0
    df['Trade ID'] = 0
    df['Pct Chg'] = 0.0
    
    # Create trade ID and calculate days in trade
    trade_ids = (df['Trade Flag'] == 1).cumsum()
    df['Trade ID'] = trade_ids
    
    df['Days in Open Trade'] = df.groupby('Trade ID').cumcount()
    df['Days in Closed Trade'] = df.groupby('Trade ID').cumcount(ascending=False) + 1
    df.loc[df['Trade Flag'] == 1, 'Days in Open Trade'] = 0

    # Define account exposure (adjust for DCA days)
    df['DCA'] = np.where(df['Days in Open Trade'] >= df['DCA'].shift(1), 1, df['DCA'])
    
    df['Account Exposure'] = np.where(
        (df['DCA'].shift(1) > 1) & (df['Days in Open Trade'] > 0) & (df['Days in Open Trade'] < df['DCA'].shift(1)),
        df['Days in Open Trade'] / df['DCA'].shift(1),
        1
    )

    df['Account Exposure'] = np.where(
        (df['DCA'].shift(1) > 1) & (df['Days in Open Trade'] == 0),
        df['Days in Closed Trade'] / df['DCA'].shift(1),
        df['Account Exposure']
    )

    # Calculate running total
    df['Opening Price'] = np.where(
        (df['Trade Flag'] == 1), 
        df.apply(lambda row: row[row['Holding']] if row['Holding'] in df.columns else np.nan, axis=1), 
        np.nan
    )
    
    df['Closing Price'] = np.where(
        (pd.notnull(df['Trade Flag'])), 
        df.apply(lambda row: row[row['Previous Holding']] if row['Previous Holding'] in df.columns else np.nan, axis=1), 
        np.nan
    )

    # Calculate percent change
    df['Pct Chg'] = df['Closing Price'].pct_change()
    df['Pct Chg'] = np.where(df['Trade Flag'].shift(1) == 1, df['Closing Price'] / df['Opening Price'].shift(1) - 1, df['Pct Chg'])
    df['Pct Chg'] = np.where(pd.isna(df['Pct Chg']), 0, df['Pct Chg'])

    # Calculate running total
    iteration = 0
    for i in df.index:
        if iteration == 0:
            df.at[i, 'Running Total'] = starting_amt
            total = starting_amt
            iteration += 1
        else:
            total = total * df['Pct Chg'][i] * df['Account Exposure'][i] + total
            df.at[i, 'Running Total'] = total

    # Calculate drawdown
    df['Max Running Total'] = df['Running Total'].cummax()
    df['Drawdown'] = df['Running Total'] / df['Max Running Total'] - 1
    
    return df


