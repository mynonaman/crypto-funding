import requests
import pandas as pd

def get_binance_funding_rate(symbol: str, start_time_ms: int, end_time_ms: int) -> pd.DataFrame:
    """Fetch funding rate data from Binance futures API and return a DataFrame.

    start_time_ms and end_time_ms are milliseconds since epoch.
    """
    url = "https://fapi.binance.com/fapi/v1/fundingRate"
    params = {
        "symbol": symbol, 
        "startTime": start_time_ms, 
        "endTime": end_time_ms
        }
    response = requests.get(url, params=params)
    # resp.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    if df.empty:
        return df
    df['fundingTime'] = pd.to_datetime(df['fundingTime'], unit='ms')
    df['fundingRate'] = df['fundingRate'].astype(float)
    df['accumulatedFundingRate'] = (1 + df['fundingRate']).cumprod()
    
    return df