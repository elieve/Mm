from datetime import datetime

import requests
from pyrogram import *
from pyrogram.types import *

from Mix import *

__modles__ = "Mail"
__help__ = get_cgr("help_mail")


def generate_temp_gmail():
    url = "https://temporary-gmail-account.p.rapidapi.com/GmailGetAccount"
    payload = {"generateNewAccount": 1}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
        "X-RapidAPI-Host": "temporary-gmail-account.p.rapidapi.com",
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


async def format_temp_gmail(temp_gmail_info):
    if "address" in temp_gmail_info and "token" in temp_gmail_info:
        em = Emojik()
        em.initialize()
        emel = temp_gmail_info["address"]
        toket = temp_gmail_info["token"]
        return cgr("mail_1").format(em.sukses, emel, toket, em.warn)
    else:
        raise ValueError(cgr("mail_err"))


@ky.ubot("genmail")
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    try:
        temp_gmail_info = generate_temp_gmail()
        formatted_temp_gmail_info = await format_temp_gmail(temp_gmail_info)
        await pros.edit(f"{em.sukses} {formatted_temp_gmail_info}")
    except Exception as e:
        await pros.edit(f"{em.gagal} {str(e)}")


def get_messages_temp_email(gmail, token):
    url = "https://temporary-gmail-account.p.rapidapi.com/GmailGetMessages"
    payload = {
        "address": gmail,
        "token": token,
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
        "X-RapidAPI-Host": "temporary-gmail-account.p.rapidapi.com",
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response)
    return response.json()


async def format_messages(messages):
    if "totalItems" in messages and "member" in messages:
        total_items = messages["totalItems"]
        member = messages["member"]

        formatted_messages = ""

        for msg in member:
            sms = msg["to"]["address"]
            tipee = msg["@type"]
            idsms = msg["@id"]
            dia = msg["from"]["name"]
            imeldia = msg["from"]["address"]
            refres = msg["updatedAt"]
            formatted_messages += cgr("mail_2").format(sms)
            formatted_messages += cgr("mail_3").format(total_items)
            formatted_messages += cgr("mail_4").format(tipee)
            formatted_messages += cgr("mail_5").format(idsms)
            formatted_messages += cgr("mail_6").format(dia)
            formatted_messages += cgr("mail_7").format(imeldia)
            formatted_messages += cgr("mail_8").format(refres)
            formatted_messages += cgr("mail_separator")

        return formatted_messages
    else:
        raise ValueError(cgr("mail_err1"))


@ky.ubot("getmail")
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    try:
        if len(m.command) >= 3:
            gmail = m.command[1]
            token = m.command[2]
            messages = get_messages_temp_email(gmail, token)
            formatted_messages = await format_messages(messages)
            await pros.edit(f"{em.sukses} {formatted_messages}")
        else:
            await pros.edit(cgr("get_mail").format(em.gagal))
    except Exception as e:
        await pros.edit(cgr("err").format(em.gagal, {str(e)}))


# COMING SOON! LIMIT BRE!
def get_message(messid, addres, token):
    url = "https://temporary-gmail-account.p.rapidapi.com/GmailGetMessage"

    payload = {
        "messageId": messid,
        "address": addres,
        "token": token,
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
        "X-RapidAPI-Host": "temporary-gmail-account.p.rapidapi.com",
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def gen_temp_mail():
    url = "https://temp-mail44.p.rapidapi.com/api/v3/email/new"
    payload = {"key1": "value", "key2": "value"}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
        "X-RapidAPI-Host": "temp-mail44.p.rapidapi.com",
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


async def format_temp_mail(temp_mail):
    if "email" in temp_mail and "token" in temp_mail:
        em = Emojik()
        em.initialize()
        imel = temp_mail["email"]
        token = temp_mail["token"]
        return cgr("mail_9").format(em.sukses, imel, token, em.warn)
    else:
        raise ValueError(cgr("mail_err"))


@ky.ubot("tempmail")
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    try:
        temp_gmail_info = gen_temp_mail()
        formatted_temp_mail = await format_temp_mail(temp_gmail_info)
        await pros.edit(cgr("get_mail1").format(em.sukses, formatted_temp_mail))
    except Exception as e:
        await pros.edit(cgr("err").format(em.gagal, {str(e)}))


async def get_temp_messages(email):
    url = f"https://temp-mail44.p.rapidapi.com/api/v3/email/{email}/messages"
    headers = {
        "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
        "X-RapidAPI-Host": "temp-mail44.p.rapidapi.com",
    }
    response = requests.get(url, headers=headers)
    return response.json()


async def format_temp_messages(messages):
    formatted_messages = ""
    for email in messages:
        from_email = email["from"]
        from_name_start = from_email.find('"') + 1
        from_name_end = from_email.find('"', from_name_start)
        from_name = from_email[from_name_start:from_name_end]
        from_address_start = from_email.find("<") + 1
        from_address_end = from_email.find(">", from_address_start)
        from_address = from_email[from_address_start:from_address_end]
        id_imel = email["id"]
        imeltu = email["to"]
        cc = email.get("cc", "Unknown")
        sub = email["subject"]
        isi = email["body_text"]

        formatted_messages += cgr("mail_10").format(id_imel)
        formatted_messages += cgr("mail_11").format(from_name)
        formatted_messages += cgr("mail_12").format(from_address)
        formatted_messages += cgr("mail_13").format(imeltu)
        formatted_messages += cgr("mail_14").format(cc)
        formatted_messages += cgr("mail_15").format(sub)
        formatted_messages += cgr("mail_16").format(isi)
        created_at = email["created_at"]
        formatted_created_at = datetime.strptime(
            created_at, "%Y-%m-%dT%H:%M:%S.%fZ"
        ).strftime("%d, %b %Y")
        formatted_messages += cgr("mail_17").format(formatted_created_at)
    return formatted_messages


@ky.ubot("gettemp")
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    try:
        if len(m.command) > 1:
            email = m.command[1]
            messages = await get_temp_messages(email)
            formatted_messages = await format_temp_messages(messages)
            await pros.edit(
                cgr("get_temp").format(em.sukses, email, formatted_messages)
            )
        else:
            await pros.edit(cgr("mail_err2").format(em.gagal))
    except Exception as e:
        await pros.edit(cgr("err").format(em.gagal, str(e)))
