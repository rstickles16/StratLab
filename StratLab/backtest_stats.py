import pandas as pd
import numpy as np
from datetime import datetime as dt

def run_stats(
        df: pd.DataFrame = None,
        starting_amt: float = None,
        show_stats: bool = True
):
    df['Year'] = df['Date'].dt.year
    year_list = list(pd.unique(df['Year']))
    year_list.sort()
    
    year_start_amt = []
    year_end_amt = []
    year_pct_gain = []
    def yearly_amts():
        for num, year in enumerate(year_list):
            df1 = df[df['Year'] == year]
            max_id = df1['ID'].max()
            if num == 0:
                start_amt = starting_amt
            else:
                start_amt = end_amt
            
            end_amt = df1[df1['ID'] == max_id]['Running Total'].iloc[0]
            pct_gain = end_amt/start_amt-1

            year_start_amt.append(start_amt)
            year_end_amt.append(end_amt)
            year_pct_gain.append(pct_gain)
        
        return {
            'Year List': year_list,
            'Starting Amt': year_start_amt,
            'Ending Amt': year_end_amt,
            'Pct': year_pct_gain
        }

    yearly = yearly_amts()
    start_list = yearly['Starting Amt']
    end_list = yearly['Ending Amt']
    pct_list = yearly['Pct']

    beginning_date = df['Date'].iloc[0]
    ending_date = df['Date'].iloc[-1]
    beginning_year = beginning_date.year
    ending_year = ending_date.year
    years = df['ID'].max()/252
    beginning_amt = df['Running Total'].iloc[0]
    ending_amt = df['Running Total'].iloc[df['ID'].max()]
    
    cagr = (ending_amt / beginning_amt)**(1/years)-1
    total_return = ending_amt / beginning_amt
    
    stats_dict = {
        'Beginning Date': beginning_date,
        'Ending Date': ending_date,
        'Beginning Year': beginning_year,
        'Ending Year': ending_year,
        'Years Backtested': years,
        'Beginning Amt': beginning_amt,
        'Ending Amt': ending_amt,
        'Total Return': total_return,
        'CAGR': cagr,
        'Years': years,
        'Starting Amts': start_list,
        'Ending Amts': end_list,
        'Pct': pct_list,
        'Max Drawdown': np.min(df['Drawdown'])
    }

    if show_stats is True:
        print('~ YEARLY PERFORMANCE ~')
        for num, year in enumerate(year_list):
            yr_performance = yearly['Pct'][num]
            print(f'{year}: {yr_performance*100:,.2f}%')
        print('')
        print('~ GENERAL STATS ~ ')
        print(f'Beginning Date: {dt.date(stats_dict["Beginning Date"])}')
        print(f'End Date: {dt.date(stats_dict["Ending Date"])}')
        print(f'Years Traded: {stats_dict["Years Backtested"]:,.2f}')
        print('')
        print('~ PERFORMANCE ~')
        print(f'Beginning Amount: {stats_dict["Beginning Amt"]:,.2f}')
        print(f'Ending Amount: {stats_dict["Ending Amt"]:,.2f}')
        print(f'CAGR: {stats_dict["CAGR"]*100:,.2f}%')
        print(f'Med Return: {np.median(stats_dict["Pct"])*100:,.2f}%')
        print(f'Avg Return: {np.average(stats_dict["Pct"])*100:,.2f}%')
        print(f'Best Return: {np.max(stats_dict["Pct"])*100:,.2f}%')
        print(f'Worst Return: {np.min(stats_dict["Pct"])*100:,.2f}%')
        print(f'Max Drawdown: {stats_dict["Max Drawdown"]*100:,.2f}%')
        print('')

    return stats_dict
