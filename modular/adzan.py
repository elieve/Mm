import json

import requests

from Mix import *

__modles__ = "Adzan"
__help__ = get_cgr("help_ajan")


@ky.ubot("adzan", sudo=True)
async def adzan_handler(c: nlx, m):
    em = Emojik()
    em.initialize()
    lok = c.get_text(m)
    pros = await m.reply(cgr("proses").format(em.proses))
    if not lok:
        return await pros.edit(cgr("jan_1").format(em.gagal))

    url = f"http://muslimsalat.com/{lok}.json?key=bd099c5825cbedb9aa934e255a81a5fc"
    req = requests.get(url)

    if req.status_code != 200:
        return await pros.edit(cgr("jan_2").format(em.gagal, lok))

    result = json.loads(req.text)
    tanggal = result["items"][0]["date_for"]
    kueri = result["query"]
    negara = result["country"]
    terbit = result["items"][0]["shurooq"]
    pajar = result["items"][0]["fajr"]
    juhur = result["items"][0]["dhuhr"]
    asar = result["items"][0]["asr"]
    magrip = result["items"][0]["maghrib"]
    isa = result["items"][0]["isha"]

    txt = cgr("jan_tes").format(
        lok, tanggal, kueri, negara, terbit, pajar, juhur, asar, magrip, isa
    )

    await m.reply(txt)
    await pros.delete()
    """
    txt += cgr("jan_3").format(lok)
    txt += cgr("jan_kol1")
    txt += cgr("jan_4").format(result["items"][0]["date_for"])
    txt += cgr("jan_5").format(result["query"], result["country"])
    txt += cgr("jan_kol1")
    txt += cgr("jan_6").format(result["items"][0]["shurooq"])
    txt += cgr("jan_7").format(result["items"][0]["fajr"])
    txt += cgr("jan_8").format(result["items"][0]["dhuhr"])
    txt += cgr("jan_9").format(result["items"][0]["asr"])
    txt += cgr("jan_10").format(result["items"][0]["maghrib"])
    txt += cgr("jan_11").format(result["items"][0]["isha"])
    txt += cgr("jan_kol1")

    await m.reply(txt).format(
        lok, tanggal, kueri, negara, terbit, pajar, juhur, asar, magrip, isa
    )
    await pros.delete()
    return
    """
