################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || Gojo_Satoru || William Butcher
 
 EH KONTOL KALO PUNYA AKAL DIPAKE YA ANJING GAUSAH APUS² CREDIT LO BAJINGAN!!
"""
################################################################


import re
from datetime import datetime, timedelta

from pyrogram.types import InlineKeyboardButton as Ikb
from pyrogram.types import InlineKeyboardMarkup as IkM

# NOTE: the url \ escape may cause double escapes
# match * (bold) (don't escape if in url)
# match _ (italics) (don't escape if in url)
# match ` (code)
# match []() (markdown link)
# else, escape *, _, `, and [

# Gojo
# William


def is_url(text):
    regex = r"(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:[/?]\S+)?|tg://\S+"
    matches = re.findall(regex, text)
    if matches:
        return True
    return False


def get_msg_button(texts: str):
    btn = []
    for z in re.findall(r"\[(.*?)\|(.*?)\]", texts):
        text, url = z
        urls = url.split("|")
        url = urls[0]
        if len(urls) > 1:
            btn[-1].append([text, url])
        else:
            btn.append([[text, url]])

    txt = texts
    for z in re.findall(r"\[.+?\|.+?\]", texts):
        txt = txt.replace(z, "")

    return txt.strip(), btn


def create_tl_btn(button: list):
    btn = []
    for z in button:
        if len(z) > 1:
            kk = []
            for x, y in z:
                if is_url(y):
                    kk.append(Ikb(text=x, url=y.strip()))
                else:
                    kk.append(Ikb(text=x, callback_data=y.strip()))
            btn.append(kk)
        else:
            x, y = z[0]
            if is_url(y):
                btn.append([Ikb(text=x, url=y.strip())])
            else:
                btn.append([Ikb(text=x, callback_data=y.strip())])
    return IkM(btn)


"""
def format_btn(buttons: list):
    txt = ""
    for i in buttons:
        a = 0
        for i in i:
            if hasattr(i.button, "url"):
                a += 1
                if a > 1:
                    txt += f"[{i.button.text} | {i.button.url} | same]"
                else:
                    txt += f"[{i.button.text} | {i.button.url}]"
    _, btn = get_msg_button(txt)
    return btn
"""


def format_btn(buttons: list, main_text: str):
    for tag, replacement in [
        ("<b>", "**"),
        ("<i>", "__"),
        ("<strike>", "~~"),
        ("<spoiler>", "||"),
        ("<u>", "--"),
    ]:
        main_text = main_text.replace(tag, replacement).replace(
            f"</{tag[1:]}>", replacement
        )

    txt = main_text
    for i in buttons:
        a = 0
        for i in i:
            if hasattr(i.button, "url"):
                a += 1
                if a > 1:
                    txt += f"[{i.button.text} | {i.button.url} | same]"
                else:
                    txt += f"[{i.button.text} | {i.button.url}]"

    _, btn = get_msg_button(txt)
    return btn


def extract_time(time_val):
    if any(time_val.endswith(unit) for unit in ("s", "m", "h", "d")):
        unit = time_val[-1]
        time_num = time_val[:-1]  # type: str
        if not time_num.isdigit():
            return None

        if unit == "s":
            bantime = datetime.now() + timedelta(seconds=int(time_num))
        elif unit == "m":
            bantime = datetime.now() + timedelta(minutes=int(time_num))
        elif unit == "h":
            bantime = datetime.now() + timedelta(hours=int(time_num))
        elif unit == "d":
            bantime = datetime.now() + timedelta(days=int(time_num))
        else:
            # how even...?
            return None
        return bantime
    else:
        return None


def format_welcome_caption(html_string, chat_member):
    return html_string.format(
        dc_id=chat_member.dc_id,
        first_name=chat_member.first_name,
        id=chat_member.id,
        last_name=chat_member.last_name,
        mention=chat_member.mention,
        username=chat_member.username,
    )
