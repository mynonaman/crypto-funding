"""Runner script for the daily telegram update job.

Usage:
    python run_daily.py

Can be invoked directly by a cron job or container entrypoint.
"""
import argparse
from datetime import datetime
import asyncio

from config import load_config
from job import daily_telegram_update


async def main():
    parser = argparse.ArgumentParser(description='Run daily telegram update once')
    parser.add_argument('--symbol', default=None)
    parser.add_argument('--start', default=None)
    parser.add_argument('--end', default=None)
    parser.add_argument('--config', default='config.json')
    args = parser.parse_args()

    cfg = load_config(args.config)
    symbol = args.symbol or cfg.get('binance', {}).get('symbol', 'BTCUSDT')
    # start = args.start or cfg.get('binance', {}).get('start_date', datetime.utcnow().strftime('%Y-%m-%d'))
    # end = args.end or cfg.get('binance', {}).get('end_date', datetime.utcnow().strftime('%Y-%m-%d'))
    start = args.start or cfg.get('binance', {}).get('start_date', '2026-02-24')
    end = args.end or cfg.get('binance', {}).get('end_date', '2026-03-03')
    chat_id = cfg['telegram']['chat_id']
    bot_token = cfg['telegram']['bot_token']

    await daily_telegram_update(symbol, start, end, chat_id, bot_token)


if __name__ == '__main__':
    asyncio.run(main())
