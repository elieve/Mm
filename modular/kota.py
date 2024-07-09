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


"""
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
"""


from io import BytesIO

import requests
from pytz import timezone


def parse_country_data(country_data):
    data = country_data.get("data", {})

    name = data.get("name", "Unknown")
    full_name = data.get("full_name", "Unknown")
    capital = data.get("capital", "Unknown")
    iso2 = data.get("iso2", "Unknown")
    iso3 = data.get("iso3", "Unknown")
    covid19_total_case = data.get("covid19", {}).get("total_case", "Unknown")
    covid19_total_deaths = data.get("covid19", {}).get("total_deaths", "Unknown")
    covid19_last_updated = data.get("covid19", {}).get("last_updated", "Unknown")
    current_president = data.get("current_president", "Unknown")
    currency = data.get("currency", "Unknown")
    phone_code = data.get("phone_code", "Unknown")
    continent = data.get("continent", "Unknown")
    description = data.get("description", "Unknown")
    size = data.get("size", "Unknown")
    independence_date = data.get("independence_date", "Unknown")
    population = data.get("population", "Unknown")
    href_self = data.get("href", {}).get("self", "Unknown")
    href_states = data.get("href", {}).get("states", "Unknown")
    href_presidents = data.get("href", {}).get("presidents", "Unknown")
    flag_url = data.get("href", {}).get("flag", "Unknown")

    return {
        "name": name,
        "full_name": full_name,
        "capital": capital,
        "iso2": iso2,
        "iso3": iso3,
        "covid19_total_case": covid19_total_case,
        "covid19_total_deaths": covid19_total_deaths,
        "covid19_last_updated": covid19_last_updated,
        "current_president": current_president,
        "currency": currency,
        "phone_code": phone_code,
        "continent": continent,
        "description": description,
        "size": size,
        "independence_date": independence_date,
        "population": population,
        "href_self": href_self,
        "href_states": href_states,
        "href_presidents": href_presidents,
        "flag_url": flag_url,
    }


def kontri(kont):
    url = f"https://restfulcountries.com/api/v1/countries/{kont}"
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer 1163|gslX6NwH9CfYDwTjaD7b99iIdVwEIms3XeHU9hSi",
    }
    try:
        response = requests.get(url, headers=headers, timeout=60)
        if response.status_code == 200:
            data = response.json()
            if data:
                return parse_country_data(data)
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.RequestException:
        return None

    return None


@ky.ubot("negara|country")
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    if len(m.command) == 1 and not m.reply_to_message:
        return await pros.edit(f"`{m.text} [negara]`")
    rep = c.get_text(m)
    country_info = kontri(rep)
    if country_info:
        neg = country_info["name"]
        spel = country_info["full_name"]
        wilneg = country_info["size"]
        bates = country_info["covid19_total_case"]
        kod = country_info["phone_code"]
        kot = country_info["capital"]
        duit = country_info["currency"]
        bende = country_info["flag_url"]
        demo = country_info["current_president"]
        izo = country_info["iso2"]
        lang = country_info["description"]
        popul = country_info["population"]
        wil = country_info["continent"]
        subwil = country_info["independence_date"]
        country_info["covid19_last_updated"]
        try:
            tz = (
                timezone(country_info.get("capital", "UTC")[0])
                if "capital" in country_info
                else timezone("UTC")
            )
            local_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            local_time = "Unknown timezone"

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
        response_message += cgr("negar_15").format(local_time)
        # response_message += cgr("negar_16").format(top)

        try:
            flag_response = requests.get(bende)
            if flag_response.status_code == 200:
                flag_image = BytesIO(flag_response.content)
                await c.send_photo(
                    m.chat.id,
                    flag_image,
                    caption=response_message,
                    reply_to_message_id=ReplyCheck(m),
                )
                await pros.delete()
            else:
                await pros.edit(response_message, disable_web_page_preview=True)
        except requests.RequestException:
            await pros.edit("Maaf, terjadi kesalahan.")
    else:
        await pros.edit("Maaf, informasi tidak ditemukan.")
