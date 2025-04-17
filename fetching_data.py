import datetime
import requests
import pandas as pd

# Replace 'YOUR_API_KEY' with your actual Polygon.io API key.
api_key = '6u512poKFdRFB7PZpgNGSVqj5pVvYner'

def fetch_stock_data(ticker, api_key = '6u512poKFdRFB7PZpgNGSVqj5pVvYner', start_date = datetime.datetime.now() - datetime.timedelta(days = 250), end_date = datetime.datetime.now()):
    # Format the dates in the format required by the API (YYYY-MM-DD)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Construct the URL for fetching daily aggregated data
    url = (
        f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/"
        f"{start_date_str}/{end_date_str}?apiKey={api_key}"
    )

    # Send a GET request to the Polygon.io API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            # Create a DataFrame from the JSON response
            df = pd.DataFrame(data['results'])

            # Convert the timestamp from milliseconds to datetime and set as index.
            # Polygon.io timestamps are provided in milliseconds.
            df['date'] = pd.to_datetime(df['t'], unit='ms')
            df.set_index('date', inplace=True)

            # Rename columns to more descriptive names (suitable for Backtrader)
            df = df.rename(columns={
                'o': 'open',
                'h': 'high',
                'l': 'low',
                'c': 'close',
                'v': 'volume'
            })

            # Optionally drop the original timestamp column if not needed.
            df.drop(columns=['t',"vw","n"], inplace=True)
            df = df[["open","high","low","close","volume"]]
            return df
        else:
            return("No data found in the response. Please check the API key and date range.")
    else:
        return(f"Request failed with status code {response.status_code}: {response.text}")

