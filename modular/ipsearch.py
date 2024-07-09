################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || William Butcher
 
 EH KONTOL KALO PUNYA AKAL DIPAKE YA ANJING GAUSAH APUS² CREDIT MODAL NYOPAS LO BAJINGAN!!
"""
################################################################


from asyncio import sleep

import requests
from pyrogram import *
from pyrogram.types import *

from Mix import *

__modles__ = "IpSearch"
__help__ = get_cgr("help_ips")


def get_ip_info(ip):
    url = "https://ip-geolocation-find-ip-location-and-ip-info.p.rapidapi.com/backend/ipinfo/"
    querystring = {"ip": ip}
    headers = {
        "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
        "X-RapidAPI-Host": "ip-geolocation-find-ip-location-and-ip-info.p.rapidapi.com",
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


def format_ip_info(ip_info):
    em = Emojik()
    em.initialize()
    latitude, longitude = ip_info.get("loc", "0,0").split(",")
    google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
    formatted_info = cgr("ipin_1").format(em.sukses, ip_info.get("ip", "None"))
    formatted_info += cgr("ipin_2").format(ip_info.get("ip", "None"))
    formatted_info += cgr("ipin_3").format(ip_info.get("hostname", "Unknown"))
    formatted_info += cgr("ipin_4").format(ip_info.get("city", "Unknown"))
    formatted_info += cgr("ipin_5").format(ip_info.get("region", "Unknown"))
    formatted_info += cgr("ipin_6").format(ip_info.get("country_name", "Unknown"))
    formatted_info += cgr("ipin_7").format(Location, google_maps_link)
    formatted_info += cgr("ipin_8").format(ip_info.get("postal", "Unknown"))
    formatted_info += cgr("ipin_9").format(ip_info.get("timezone", "Unknown"))
    formatted_info += cgr("ipin_10").format(
        ip_info.get("country_flag", {}).get("emoji", "Unknown")
    )
    formatted_info += cgr("ipin_11").format(
        ip_info.get("country_currency", {}).get("code", "Unknown")
    )

    return formatted_info


@ky.ubot("ipinfo")
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    try:
        pros = await m.reply(cgr("proses").format(em.proses))
        if len(m.command) > 1:
            ip = m.command[1]
            ip_info = get_ip_info(ip)
            formatted_info = format_ip_info(ip_info)
            latitude, longitude = ip_info.get("loc", "0,0").split(",")
            google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(cgr("ipin_12"), url=google_maps_link)],
                    [InlineKeyboardButton(cgr("ipin_13"), callback_data="close_ip")],
                ],
            )
            await sleep(2)
            await m.reply(
                cgr("ipin_14").format(em.sukses, ip, formatted_info),
                reply_markup=keyboard,
                reply_to_message_id=ReplyCheck(m),
                disable_web_page_preview=True,
            )
            await pros.delete()
        else:
            await pros.edit(cgr("err").format(em.gagal))
    except Exception as e:
        await pros.edit(cgr("err").format(em.gagal, str(e)))


@ky.callback("close_ip")
async def _(c, cq):
    await cq.message.delete()
