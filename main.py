import os
import asyncio

from telethon import TelegramClient, events
from tg_client import tg_client


from cblu import CBLUAPI

cblu = CBLUAPI()


# plugins must be import after client initialisation
from plugins import speedtest, alive, eval



@tg_client.on(events.NewMessage(pattern="/aaya"))
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
            await mymsg.pin(notify=True)
        else:
            await mymsg.edit("`Nahi aaya vumro.`")

@tg_client.on(events.NewMessage(pattern="/text"))
async def _(event):
    cblu.is_result_out(cblu.get_token())
    await event.reply(cblu.text)

@tg_client.on(events.NewMessage(pattern="/id"))
async def _(event):
    msg = await event.reply(f"Le vumro chat ID: `{event.chat_id}`")

@tg_client.on(events.NewMessage(pattern="/kyabumro"))
async def handler(event):
    mymsg = await event.reply("`Are m kya kru bumro. Vase tu chinta mat kr, pass h tu`")

########## every 10 min #######
async def check():
    while True:
        if cblu.is_result_out(cblu.get_token()):
            msg = await client.send_message(-1002137972764, "**AA GYA VUMRO AA GYA, JALDI DEKH VUMRO**")

            await msg.pin(notify=True)

        await asyncio.sleep(600)


if __name__=="__main__":
    loop = asyncio.get_event_loop()

    # checks in every 10 min.
    loop.create_task(check())


    tg_client.start()
    print("BOT STARTED.")


    tg_client.run_until_disconnected()

