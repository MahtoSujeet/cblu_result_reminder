import os
from telethon import TelegramClient

APIID = os.getenv('APIID')
APIHASH = os.getenv("APIHASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")


tg_client = TelegramClient('mybot', APIID, APIHASH).start(bot_token=BOT_TOKEN)
