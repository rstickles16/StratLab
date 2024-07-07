import pandas as pd
import numpy as np

def comparison(
        df: pd.DataFrame = None,
        name: str = None,
        ticker_1: str = None,
        study_1: str = None, 
        ticker_2: str = None,
        study_2: str = None,
        operator: str = None,
        study_1_period: int = None,
        study_2_period: int = None,
        study_1_period_type: str = None,
        study_2_period_type: str = None,
        value: float = None
) -> pd.DataFrame:
    # Set period types to 'Close' when is None
    if study_1_period_type is None:
        study_1_period_type = 'Close'
    if study_2_period_type is None:
        study_2_period_type = 'Close'

    # Identify column names
    if study_1.upper() == 'PRICE':
        study_1_col = f'{ticker_1.upper()} {study_1_period_type.capitalize()}'
    else:
        study_1_col = f'{ticker_1.upper()} {study_1_period} {study_1.upper()}'
    
    if study_2 is not None:
        if study_2.upper() == 'PRICE':
            study_2_col = f'{ticker_2.upper()} {study_2_period_type.capitalize()}'
        else:
            study_2_col = f'{ticker_2.upper()} {study_2_period} {study_2.upper()}'
    else:
        study_2_col = f'Value {value}'


    # Check if conditions are true or false
    operators = {
        '<': np.less,
        '>': np.greater,
        '>=': np.greater_equal,
        '<=': np.less_equal
    }
    
    comparison = operators[operator](df[study_1_col],df[study_2_col])
    df[name] = np.where(comparison, 'True', 'False')
    return df

def add_holding(
        df: pd.DataFrame = None,
        conditions: list = None,
        flags: list = None,
        holdings: list = None,
        weights: list = None,
        compare_type: str = 'and',
        entry_type: str = 'Close',
        add_leverage: float = None,
        dca_period: int = 1
):

    # Identify comparison method
    if compare_type.lower() == 'and':
        symbol = '&'
    elif compare_type.lower() == 'or':
        symbol = '|'
    else:
        raise ValueError('Compare type must either be "and" or "or"')

    # If weights are not given, assume equal weighting
    if weights is None:
        weight = 1/len(holdings)
        weights = []
        for num, holding in enumerate(holdings):
            weights.append(weight)

    # Raise error when len of conditions does not match flag...same for weights and holdings
    if len(conditions) != len(flags):
        raise ValueError (' The len of conditions and flags must match!') 
    if len(weights) != len(holdings):
        raise ValueError ('The len of weights must match the len of holdings!')
    
    eval_list=[]
    for num, condition in enumerate(conditions):
        eval_str = f'df[{condition}]=="{flags[num]}"'
        eval_list.append(eval_str)
    
    holdings_list = []
    if add_leverage is not None and len(holdings) > 1:
        for holding in holdings:
            x = f'{str(holding).upper()} {entry_type} {add_leverage}X'
            holdings_list.append(x)
        holding_str = '/'.join(holdings_list)

    elif add_leverage is None:
        holding_str = f'{"/".join(holdings).upper()} {entry_type}'

    else:
        holding_str = f'{str(holdings[0]).upper()} {entry_type} {add_leverage}X'
    
    string_list = []
    for num, condition in enumerate(conditions):
        if len(conditions) > 1:
            try:
                flag = flags[num+1]
                string = f'((df["{condition}"] == "{flags[num]}") {symbol}'
                string_list.append(string)
            except:
                string = f'(df["{condition}"] == "{flags[num]}") & (df["Holding"] == ""))'
                string_list.append(string)
        else:
            string = f'((df["{condition}"] == "{flags[num]}") & (df["Holding"] == ""))'
            string_list.append(string)
    
    string_list = ' '.join(string_list)

    df['Holding'] = np.where(eval((string_list)), holding_str, df['Holding'])

    if 'Pos Reason' not in df.columns:
        df['Pos Reason'] = '-'
    if 'DCA' not in df.columns:
        df['DCA'] = int(1)
    
    string_list = string_list.replace(' & (df["Holding"] == "")',"")
    string_list = string_list.replace('((', '(')
    string_list = string_list.replace('))', ')')

    df['Reason'] = np.where((eval(string_list)) & (df["Pos Reason"] == "-"), '/'.join(conditions), df['Pos Reason'])
    df['Pos Reason'] = df['Reason']
    
    # df['DCA'] = np.where(((df['Holding'] == holding_str) & (df['DCA'] == 1)), dca_period, 1)
    df['DCA'] = np.where(((df['Reason'] == '/'.join(conditions)) & (df['DCA'] == int(1))), dca_period, df['DCA'])
    df['DCA'] = np.where(df['Holding'].shift(1) == df['Holding'], df['DCA'].shift(1), df['DCA'])

    return {
        'df': df
    }

def add_leverage(
        df: pd.DataFrame = None,
        ticker: str = None,
        leverage_ratio: float = None,
        entry: str = 'Close'
):
    if f'{ticker} {entry} {leverage_ratio}X' in df.columns:
        pass

    else:
        if leverage_ratio > 0:
            starting_value = 5
        else:
            starting_value = 1000000000
        
        df[f'{ticker} {leverage_ratio}x %chg'] = (df[f'{ticker} {entry}'] / df[f'{ticker} {entry}'].shift(1) - 1) * leverage_ratio
        df[f'{ticker} {entry} {leverage_ratio}X'] = starting_value

        mask =~df[f'{ticker} {leverage_ratio}x %chg'].isna()
        df.loc[mask, f'{ticker} {entry} {leverage_ratio}X'] = (
            df[f'{ticker} {entry} {leverage_ratio}X'][mask].shift(1) *
            (df[f'{ticker} {leverage_ratio}x %chg'][mask]+1).cumprod()
        )

        df.drop(columns=[f'{ticker} {leverage_ratio}x %chg'], inplace=True)
        df.reset_index(inplace=True)
        df = df.drop([0,1], inplace=True)

    return df
