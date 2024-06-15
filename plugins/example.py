from telethon import events
from tg_client import tg_client



@tg_client.on(events.NewMessage(pattern=""))
async def _(event):
    ...
