import requests
import pandas as pd

# Replace with your Polygon.io API key
API_KEY = 'enter_your_key_here'
BASE_URL = 'https://api.polygon.io'

def fetch_4h_data(ticker, start_date, end_date):
    url = f"{BASE_URL}/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}?adjusted=true&sort=asc&limit=50000&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if 'results' in data:
        df = pd.DataFrame(data['results'])
        df['timestamp'] = pd.to_datetime(df['t'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df.drop(columns=['t'], inplace=True)
        return df
    else:
        print("No data found or an error occurred.")
        return None

# Fetch data
ticker = 'SPY'
start_date = '2000-01-01'
end_date = '2024-07-03'
data = fetch_4h_data(ticker, start_date, end_date)

if data is not None:
    print(data.tail())
    print(data.head())

print(len(data.index))