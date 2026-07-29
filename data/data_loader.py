import yfinance as yf
import pandas as pd 

def fetch_historical_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch historical data for a given ticker from Yahoo Finance.
    
    Args:
        ticker (str): The ticker symbol of the stock to fetch data for.
        start_date (str): The start date of the data to fetch.
        end_date (str): The end date of the data to fetch.
    
    Returns:
        A pandas DataFrame containing the historical data.
    """

    #Fetch data from Yahoo Finance
    data = yf.download(ticker, start=start_date, end=end_date)
    data.columns = [col[0].lower() if isinstance(col, tuple) else col.lower() for col in data.columns]

    #Fill missing values
    data = data.ffill().bfill()

    #Calculate daily pct returns efficiently
    data['daily_return'] = data['close'].pct_change()

    data = data.dropna()

    return data

if __name__ == "__main__":
    df = fetch_historical_data("AAPL", "2023-01-01", "2024-01-01")
    print(df.head())