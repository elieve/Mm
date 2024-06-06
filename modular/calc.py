from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *
from struct import unpack
from attrify import Attrify as Atr
from Mix import bot, ky, nlx

__modules__ = "Calculator"
__help__ = "Calculator"

CALCULATE_TEXT = "Mix-Userbot Calculator"


def get_calculator_buttons(teks):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("(", callback_data=f"({teks}"),
                InlineKeyboardButton(")", callback_data=f"){teks}"),
                InlineKeyboardButton("CLOSE", callback_data="KLOS"),
            ],
            [
                InlineKeyboardButton("%", callback_data=f"%{teks}"),
                InlineKeyboardButton("AC", callback_data="AC"),
                InlineKeyboardButton("DEL", callback_data="DEL"),
                InlineKeyboardButton("÷", callback_data=f"/{teks}"),
            ],
            [
                InlineKeyboardButton("7", callback_data=f"7{teks}"),
                InlineKeyboardButton("8", callback_data=f"8{teks}"),
                InlineKeyboardButton("9", callback_data=f"9{teks}"),
                InlineKeyboardButton("×", callback_data=f"*{teks}"),
            ],
            [
                InlineKeyboardButton("4", callback_data=f"4{teks}"),
                InlineKeyboardButton("5", callback_data=f"5{teks}"),
                InlineKeyboardButton("6", callback_data=f"6{teks}"),
                InlineKeyboardButton("-", callback_data=f"-{teks}"),
            ],
            [
                InlineKeyboardButton("1", callback_data=f"1{teks}"),
                InlineKeyboardButton("2", callback_data=f"2{teks}"),
                InlineKeyboardButton("3", callback_data=f"3{teks}"),
                InlineKeyboardButton("+", callback_data=f"+{teks}"),
            ],
            [
                InlineKeyboardButton("00", callback_data=f"00{teks}"),
                InlineKeyboardButton("0", callback_data=f"0{teks}"),
                InlineKeyboardButton("=", callback_data=f"={teks}"),
                InlineKeyboardButton(".", callback_data=f".{teks}"),
            ],
        ]
    )


@ky.ubot("calc|kalku", sudo=True)
async def _(c: nlx, m):
    try:
        x = await c.get_inline_bot_results(bot.me.username, "calcs")
        await m.reply_inline_bot_result(x.query_id, x.results[0].id)
        print("Inline bot results berhasil didapatkan")
        print("Hasil inline bot dibalas ke user")
    except Exception as error:
        print(f"Error mendapatkan hasil inline bot: {error}")
        await m.reply_text(str(error))


@ky.callback("^.*")
async def _(c, cq):
    data = cq.data
    if cq.message and cq.message.text:
        teks = cq.message.text.split("\n")[0].strip().split("=")[0].strip()
    else:
        teks = ""

    if data == "AC":
        teks = ""
    elif data == "DEL":
        teks = teks[:-1]
    elif data == "=":
        try:
            expression = data[1:]
            teks = str(
                eval(expression.replace("×", "*").replace("÷", "/").replace("^", "**"))
            )
        except Exception as e:
            print(f"Error evaluasi: {e}")
            teks = "Error"
    else:
        teks = data[1:] + data[0]

    try:
        await cq.edit_message_text(
            text=f"{teks}\n\n\n{CALCULATE_TEXT}",
            disable_web_page_preview=True,
            reply_markup=get_calculator_buttons(teks),
        )
        print(f"Pesan setelah mengedit: {teks}")
    except Exception as e:
        print(f"Error editing message: {e}")
        await cq.answer(f"Error editing message: {e}", show_alert=True)
        return


@ky.inline("^calcs")
async def _(c, iq):
    if len(iq.query) == 0 or iq.query.lower() == "calcs":
        answers = [
            InlineQueryResultArticle(
                title="Calculator",
                description="New calculator",
                input_message_content=InputTextMessageContent(CALCULATE_TEXT),
                reply_markup=get_calculator_buttons(""),
            )
        ]
    else:
        try:
            data = iq.query.replace("×", "*").replace("÷", "/").replace("^", "**")
            result = str(eval(data))
            answers = [
                InlineQueryResultArticle(
                    title="Answer",
                    description=f"Result: {result}",
                    input_message_content=InputTextMessageContent(
                        message_text=f"{data} = {result}", disable_web_page_preview=True
                    ),
                )
            ]
        except Exception as e:
            print(f"Error evaluasi pada inline query: {e}")
            answers = [
                InlineQueryResultArticle(
                    title="Error",
                    description="Invalid Expression",
                    input_message_content=InputTextMessageContent(
                        message_text="Invalid Expression", disable_web_page_preview=True
                    ),
                )
            ]

    await c.answer_inline_query(iq.id, cache_time=300, results=answers)
    print("Inline query dijawab")


def unpacked2(inline_message_id: str):
    dc_id, message_id, chat_id, query_id = unpack(
        "<iiiq",
        urlsafe_b64decode(
            inline_message_id + "=" * (len(inline_message_id) % 4),
        ),
    )
    temp = {
        "dc_id": dc_id,
        "message_id": message_id,
        "chat_id": int(str(chat_id).replace("-", "-100")),
        "query_id": query_id,
        "inline_message_id": inline_message_id,
    }
    return Atr(temp)
    

@ky.callback("^KLOS")
async def _(_, cq):
    unPacked = unpacked2(cq.inline_message_id)
    if cq.from_user.id =! nlx.me.id:
        return await cq.answer("GAUSAH PENCET-PENCET GOBLOK! ANJING! NGENTOT! LO SIAPA? MAKANYA BELI MIX-USERBOT LAH! DASAR ANJING!", show_alert=True)
    await nlx.delete_messages(unPacked.chat_id, unPacked.message_id)
    return

"""
from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *

from Mix import bot, ky, nlx

__modules__ = "Calculator"
__help__ = "Calculator"

CALCULATE_TEXT = "Mix-Userbot Calculator"


def get_calculator_buttons(teks):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("(", callback_data=f"({teks}"),
                InlineKeyboardButton(")", callback_data=f"){teks}"),
                InlineKeyboardButton("^", callback_data=f"^{teks}"),
            ],
            [
                InlineKeyboardButton("%", callback_data=f"%{teks}"),
                InlineKeyboardButton("AC", callback_data="AC"),
                InlineKeyboardButton("DEL", callback_data="DEL"),
                InlineKeyboardButton("÷", callback_data=f"/{teks}"),
            ],
            [
                InlineKeyboardButton("7", callback_data=f"7{teks}"),
                InlineKeyboardButton("8", callback_data=f"8{teks}"),
                InlineKeyboardButton("9", callback_data=f"9{teks}"),
                InlineKeyboardButton("×", callback_data=f"*{teks}"),
            ],
            [
                InlineKeyboardButton("4", callback_data=f"4{teks}"),
                InlineKeyboardButton("5", callback_data=f"5{teks}"),
                InlineKeyboardButton("6", callback_data=f"6{teks}"),
                InlineKeyboardButton("-", callback_data=f"-{teks}"),
            ],
            [
                InlineKeyboardButton("1", callback_data=f"1{teks}"),
                InlineKeyboardButton("2", callback_data=f"2{teks}"),
                InlineKeyboardButton("3", callback_data=f"3{teks}"),
                InlineKeyboardButton("+", callback_data=f"+{teks}"),
            ],
            [
                InlineKeyboardButton("00", callback_data=f"00{teks}"),
                InlineKeyboardButton("0", callback_data=f"0{teks}"),
                InlineKeyboardButton("=", callback_data=f"={teks}"),
                InlineKeyboardButton(".", callback_data=f".{teks}"),
            ],
        ]
    )


@ky.ubot("calc|kalku", sudo=True)
async def _(c: nlx, m):
    try:
        x = await c.get_inline_bot_results(bot.me.username, f"calcs")
        await m.reply_inline_bot_result(x.query_id, x.results[0].id, quote=True)
        return
    except Exception as error:
        return await m.reply_text(str(error))


@ky.callback("^.*")
async def _(c, cq):
    data = cq.data
    teks = ""
    if cq.message and cq.message.text:
        message_text = cq.message.text.split("\n")[0].strip().split("=")[0].strip()
    else:
        pass

    if data.startswith("AC"):
        teks = ""
    elif data.startswith("DEL"):
        teks = message_text.split("\n")[0].strip().split("=")[0].strip()[:-1]
    elif data.startswith("="):
        try:
            expression = data[1:]
            teks = str(
                eval(expression.replace("×", "*").replace("÷", "/").replace("^", "**"))
            )
        except Exception:
            teks = "Error"
    elif data.startswith("00"):
        teks = data[1:] + "00"
    else:
        teks = data[1:] + data[0]

    try:
        await cq.edit_message_text(
            text=f"{teks}\n\n\n{CALCULATE_TEXT}",
            disable_web_page_preview=True,
            reply_markup=get_calculator_buttons(teks),
        )
    except Exception as e:
        print(f"Error: {e}")
        await cq.answer(f"{teks}\n\n\n{CALCULATE_TEXT}")
        return


@ky.inline("^calcs")
async def _(c, iq):
    if len(iq.query) == 0 or iq.query.lower() == "calcs":
        answers = [
            InlineQueryResultArticle(
                title="Calculator",
                description="New calculator",
                input_message_content=InputTextMessageContent(
                    message_text=CALCULATE_TEXT, disable_web_page_preview=True
                ),
                reply_markup=get_calculator_buttons(""),
            )
        ]
    else:
        try:
            data = iq.query.replace("×", "*").replace("÷", "/").replace("^", "**")
            result = result = str(eval(data))
            answers = [
                InlineQueryResultArticle(
                    title="Answer",
                    description=f"Result: {result}",
                    input_message_content=InputTextMessageContent(
                        message_text=f"{data} = {result}", disable_web_page_preview=True
                    ),
                )
            ]
        except Exception:
            answers = [
                InlineQueryResultArticle(
                    title="Error",
                    description="Invalid Expression",
                    input_message_content=InputTextMessageContent(
                        message_text="Invalid Expression", disable_web_page_preview=True
                    ),
                )
            ]

    await c.answer_inline_query(iq.id, cache_time=300, results=answers)
    return
"""
