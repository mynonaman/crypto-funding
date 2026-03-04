import json
import requests
from datetime import datetime
import pandas as pd
import matplotlib
# Use non-interactive backend to avoid macOS GUI errors when running in background threads
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from telegram import Bot
import asyncio
import time
from apscheduler.schedulers.background import BackgroundScheduler 

def load_config(config_file='config.json'):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

def get_binance_funding_rate(symbol, start_time, end_time):
    url = "https://fapi.binance.com/fapi/v1/fundingRate"
    params = {
        "symbol": symbol, 
        "startTime": start_time,
        "endTime": end_time
        }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        #return float(data[0]['fundingRate'])
        df = pd.DataFrame(data)
        df['fundingTime'] = pd.to_datetime(df['fundingTime'], unit='ms')
        df['fundingRate'] = df['fundingRate'].astype(float)
        df['accumulatedFundingRate'] = (1 + df['fundingRate']).cumprod()

        ax1 = df.plot(x='fundingTime', y='accumulatedFundingRate', ylabel='Accumulated Funding Rate', color='b', marker='o')
        ax2 = ax1.twinx()
        df.plot(x='fundingTime', y='fundingRate', ax=ax2, ylabel='Funding Rate', color='r', marker='x')
        plt.title(f'Funding Rate for {symbol}')
        plt.legend(loc='upper left')
        plt.tight_layout()
        #plt.show()

        return df
    else:
        print(f"Error fetching funding rate: {response.status_code}")

# def get_binance_spot(symbol, start_time, end_time):
#     url = "https://api.binance.com/api/v3/klines"
#     params = {
#         "symbol": symbol,
#         "interval": "4h",
#         "startTime": start_time,
#         "endTime": end_time
#         }
#     response = requests.get(url, params=params)

#     if response.status_code == 200:
#         data = response.json()
#         df = pd.DataFrame(data, 
#             columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
#         df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
#         df['open'] = df['open'].astype(float)
#         df.rename(columns={'open_time': 'time', 'open': 'spot_price'}, inplace=True)
#         df = df[['time', 'spot_price']]
#         return df
#     else:
#         print(f"Error fetching spot price: {response.status_code}")

def send_telegram_message(chat_id, message, jpg_path, bot_token):
    bot = Bot(token=bot_token)
    with open(jpg_path, 'rb') as jpg:
        bot.send_photo(
            chat_id=chat_id, 
            photo=jpg, 
            caption=message
            )
    print("Message sent to Telegram")

def daily_telegram_update(symbol, start, end, chat_id, bot_token):
    start_time = int(datetime.strptime(start, "%Y-%m-%d").timestamp() * 1000)
    end_time = int(datetime.strptime(end, "%Y-%m-%d").timestamp() * 1000)
    
    print(f"Fetching funding rate for {symbol} from {start} to {end}...")
    funding_rate_df = get_binance_funding_rate(symbol, start_time, end_time)
    # print(funding_rate_df)
    fig = plt.gcf()
    fig.savefig(f"{symbol}_funding_rate_plot.jpg")

    send_telegram_message(
        chat_id=chat_id,
        message=f"Daily Funding rate plot for {symbol}",
        jpg_path=f"{symbol}_funding_rate_plot.jpg"
        )
    plt.close()


def main():
    symbol = "BTCUSDT"
    start = "2026-02-01"
    end = "2026-02-28"

    config = load_config()
    chat_id = config['telegram']['chat_id']
    bot_token = config['telegram']['bot_token']

    # print(f"Fetching spot price for {symbol} from {start} to {end}...")
    # spot_df = get_binance_spot(symbol, start_time, end_time)
    # df = pd.merge_asof(funding_rate_df[['fundingTime', 'fundingRate', 'accumulatedFundingRate']], spot_df, left_on='fundingTime', right_on='time', direction='backward', tolerance=pd.Timedelta('60s'))
    # print(df)

    scheduler = BackgroundScheduler()
    # run every 1 minute
    scheduler.add_job(
        daily_telegram_update,
        trigger='cron',
        minute='*',
        timezone='Asia/Hong_Kong',
        args=[symbol, start, end, chat_id, bot_token]
    )
    scheduler.start()
    print("Scheduler started. Waiting (running job every 1 minute)...")

    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        print("Shutting down scheduler...")
        scheduler.shutdown()

if __name__ == '__main__':
    main()