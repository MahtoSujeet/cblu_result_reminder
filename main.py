import random
import requests
import asyncio

from telethon import events
from tg_client import tg_client

from cblu import CBLUAPI


RAHUL_ID = 7037814844
SUJEET_ID = 6164352361
cblu = CBLUAPI()


# plugins must be import after client initialisation
from plugins import speedtest, alive, eval



@tg_client.on(events.NewMessage(pattern="/aaya"))
async def _(event):
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

            if random.randint(1, 3)==1:
                return await mymsg.edit("`kya baar baar /aaya /aaya lga rkha h, check kr riya hu na har 10min me, aayega to bta dunga khud mai. Nahi aaya abhi.`")
            await mymsg.edit("`Nahi aaya vumro.`")

@tg_client.on(events.NewMessage(pattern="/text"))
async def _(event):
    cblu.is_result_out(cblu.get_token())
    await event.reply(cblu.text)

@tg_client.on(events.NewMessage(pattern="/id"))
async def _(event):
    await event.reply(f"Le vumro chat ID: `{event.chat_id}`")

@tg_client.on(events.NewMessage(pattern="/kyabumro"))
async def handler(event):
    if event.sender_id == RAHUL_ID:
        return await event.reply("`Kya kyaburmo, 2000 taiyar rakh tu bas`")

    return await event.reply("`Are m kya kru bumro. Vase tu chinta mat kr, pass h tu`")

########## every 10 min #######
async def check():
    while True:
        requests.get("https://cblu-result-reminder-1.onrender.com")

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

