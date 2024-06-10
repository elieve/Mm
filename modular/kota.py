# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

# from countryinfo import CountryInfo

import requests

from Mix import *


__modles__ = "Country"
__help__ = get_cgr("help_negara")


def get_colok(kontol):
    url = f"https://restcountries.com/v3.1/name/{kontol}"
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            data = response.json()
            if data:
                info = {
                    "name": data[0]["name"]["common"],
                    "alt_spellings": ", ".join(data[0]["altSpellings"]),
                    "area": data[0]["area"],
                    "borders": (
                        ", ".join(data[0]["borders"])
                        if "borders" in data[0]
                        else "Tidak ada perbatasan"
                    ),
                    "calling_code": "+".join(
                        data[0]["idd"]["root"] + suffix
                        for suffix in data[0]["idd"]["suffixes"]
                    ),
                    "capital": ", ".join(data[0]["capital"]),
                    "currencies": (
                        ", ".join(data[0]["currencies"].keys())
                        if "currencies" in data[0]
                        else "Tidak ada mata uang"
                    ),
                    "flag": data[0]["flags"]["png"],
                    "demonym": data[0]["demonyms"]["eng"]["m"],
                    "iso": data[0]["cca2"],
                    "languages": ", ".join(data[0]["languages"].values()),
                    "population": data[0]["population"],
                    "region": data[0]["region"],
                    "subregion": data[0]["subregion"],
                    "timezones": ", ".join(data[0]["timezones"]),
                    "top_level_domain": ", ".join(data[0]["tld"]),
                }
                return info
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.RequestException:
        return None

    return None


@ky.ubot("negara|country", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    if len(m.command) == 1 and not m.reply_to_message:
        return await pros.edit(f"`{m.text} [negara]`")
    rep = c.get_text(m)
    country_info = get_colok(rep)
    if country_info:
        neg = country_info["name"]
        spel = country_info["alt_spellings"]
        wilneg = country_info["area"]
        bates = country_info["borders"]
        kod = country_info["calling_code"]
        kot = country_info["capital"]
        duit = country_info["currencies"]
        bende = country_info["flag"]
        demo = country_info["demonym"]
        izo = country_info["iso"]
        lang = country_info["languages"]
        popul = country_info["population"]
        wil = country_info["region"]
        subwil = country_info["subregion"]
        jon = country_info["timezones"]
        top = country_info["top_level_domain"]

        response_message = cgr("negar_1").format(neg)
        response_message += cgr("negar_2").format(spel)
        response_message += cgr("negar_3").format(wilneg)
        response_message += cgr("negar_4").format(bates)
        response_message += cgr("negar_5").format(kod)
        response_message += cgr("negar_6").format(kot)
        response_message += cgr("negar_7").format(duit)
        response_message += cgr("negar_8").format(bende)
        response_message += cgr("negar_9").format(demo)
        response_message += cgr("negar_10").format(izo)
        response_message += cgr("negar_11").format(lang)
        response_message += cgr("negar_12").format(popul)
        response_message += cgr("negar_13").format(wil)
        response_message += cgr("negar_14").format(subwil)
        response_message += cgr("negar_15").format(jon)
        response_message += cgr("negar_16").format(top)
        await pros.edit(response_message, disable_web_page_preview=True)
    else:
        await pros.edit("Maaf, informasi tidak ditemukan.")
