from telethon import events
from tg_client import tg_client


from time import time

import speedtest



def convert_from_bytes(size):
    power = 2**10
    n = 0
    units = {0: "", 1: "Kbps", 2: "Mbps", 3: "Gbps", 4: "Tbps"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"


"""
info={
    "header": "Botserver's speedtest by ookla.",
    "options": {
        "text": "will give output as text",
        "image": (
            "Will give output as image this is default option if "
            "no input is given."
        ),
        "file": "will give output as png file.",
    },
    "usage": ["{tr}speedtest <option>", "{tr}speedtest"],
},

"""
@tg_client.on(events.NewMessage(
    pattern=r"/speedtest(?:\s|$)([\s\S]*)",
))
async def _(event):
    "Botserver's speedtest by ookla."
    input_str = event.pattern_match.group(1)
    as_text = False
    as_document = False
    if input_str == "file":
        as_document = True
    elif input_str == "image":
        as_document = False
    elif input_str == "text":
        as_text = True
    mymsg = await event.reply(
        "`Calculating my internet speed. Please wait!`"
    )
    start = time()
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    end = time()
    ms = round(end - start, 2)
    response = s.results.dict()
    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    client_infos = response.get("client")
    i_s_p = client_infos.get("isp")
    i_s_p_rating = client_infos.get("isprating")
    reply_msg_id = event.id
    try:
        response = s.results.share()
        speedtest_image = response
        if as_text:
            await mymsg.edit(
                """`SpeedTest completed in {} seconds`

`Download: {} (or) {} MB/s`
`Upload: {} (or) {} MB/s`
`Ping: {} ms`
`Internet Service Provider: {}`
`ISP Rating: {}`""".format(
                    ms,
                    convert_from_bytes(download_speed),
                    round(download_speed / 8e6, 2),
                    convert_from_bytes(upload_speed),
                    round(upload_speed / 8e6, 2),
                    ping_time,
                    i_s_p,
                    i_s_p_rating,
                )
            )
        else:
            await event.client.send_file(
                event.chat_id,
                speedtest_image,
                caption=f"**SpeedTest** completed in {ms} seconds",
                force_document=as_document,
                reply_to=reply_msg_id,
                allow_cache=False,
            )

            await mymsg.delete()
    except Exception as exc:
        await mymsg.edit(
            """**SpeedTest** completed in {} seconds
Download: {} (or) {} MB/s
Upload: {} (or) {} MB/s
Ping: {} ms

__With the Following ERRORs__
{}""".format(
                ms,
                convert_from_bytes(download_speed),
                round(download_speed / 8e6, 2),
                convert_from_bytes(upload_speed),
                round(upload_speed / 8e6, 2),
                ping_time,
                str(exc),
            )
        )

