from datetime import datetime
# from . import binance, plot, telegram_client
from binance import get_binance_funding_rate
from plot import save_funding_plot
from telegram_client import send_telegram_photo

async def daily_telegram_update(symbol: str, start: str, end: str, chat_id: str, bot_token: str, out_path=None):
    """Fetch funding data, create plot, and send it to Telegram once.

    `start` and `end` are YYYY-MM-DD strings.
    """
    start_time = int(datetime.strptime(start, "%Y-%m-%d").timestamp() * 1000)
    end_time = int(datetime.strptime(end, "%Y-%m-%d").timestamp() * 1000)

    df = get_binance_funding_rate(symbol, start_time, end_time)
    if out_path is None:
        out_path = f"{symbol}_funding_rate_plot.jpg"

    save_funding_plot(df, symbol, out_path)

    caption = f"Funding rate plot for {symbol} ({start} to {end})"
    await send_telegram_photo(chat_id, caption, out_path, bot_token)

