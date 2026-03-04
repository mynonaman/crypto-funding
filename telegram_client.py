from telegram import Bot

async def send_telegram_photo(chat_id: str, caption: str, photo_path: str, bot_token: str):
    bot = Bot(token=bot_token)
    with open(photo_path, 'rb') as fh:
        await bot.send_photo(
            chat_id=chat_id, 
            photo=fh, 
            caption=caption
            )

