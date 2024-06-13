import os

from telethon import TelegramClient, events
from telethon.client.telegrambaseclient import asyncio

from cblu import CBLUAPI


APIID = os.getenv('APIID')
APIHASH = os.getenv("APIHASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

client = TelegramClient('mybot', APIID, APIHASH).start(bot_token=BOT_TOKEN)
cblu = CBLUAPI()

@client.on(events.NewMessage(pattern="/aaya"))
async def handler(event):
    mymsg = await event.reply("`Check kr riya hu...`")
    token = cblu.get_token()
    if "ERROR" in str(token):
        return await mymsg.edit(token)

    if token is None:
        await mymsg.edit("`token hi nahi aaya vumro`")

    else:
        if cblu.is_result_out(token):
            print("result is out")
            await mymsg.edit("`Aa gya vumro..`")
        else:
            await mymsg.edit("`Nahi aaya vumro.`")

@client.on(events.NewMessage(pattern="/text"))
async def _(event):
    cblu.is_result_out(cblu.get_token())
    await event.reply(cblu.text)

@client.on(events.NewMessage(pattern="/id"))
async def _(event):
    await event.reply(f"Le vumro chat ID: `{event.chat_id}`")


########## every 10 min #######
async def check():
    while True:
        if cblu.is_result_out(cblu.get_token()):
            await client.send_message(-1002137972764, "**AA GYA VUMRO AA GYA, JALDI DEKH VUMRO**")

        await asyncio.sleep(3600*6)


if __name__=="__main__":
    loop = asyncio.get_event_loop()

    # checks in every 6 hour
    loop.create_task(check())

    client.start()
    client.run_until_disconnected()

