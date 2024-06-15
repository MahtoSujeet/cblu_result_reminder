from telethon import events
from tg_client import tg_client
from datetime import datetime



@tg_client.on(events.NewMessage(pattern="/ping"))
async def _(event):
    start = datetime.now()
    msg = await event.reply("**♛ Pong**")
    await msg.edit(f"**♛ Ping : **`{(datetime.now() - start).microseconds / 1000} ms`")
