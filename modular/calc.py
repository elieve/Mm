from base64 import urlsafe_b64decode
from struct import unpack

from attrify import Attrify as Atr
from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *

from Mix import bot, ky, nlx

__modules__ = "Calculator"
__help__ = "Calculator"

CALCULATE_TEXT = "Mix-Userbot Calculator"
hitung = []

def get_calculator_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("(", callback_data="("),
                InlineKeyboardButton(")", callback_data=")"),
                InlineKeyboardButton("CLOSE", callback_data="KLOS"),
            ],
            [
                InlineKeyboardButton("AC", callback_data="AC"),
                InlineKeyboardButton("DEL", callback_data="DEL"),
                InlineKeyboardButton("%", callback_data="%"),
                InlineKeyboardButton("÷", callback_data="/"),
            ],
            [
                InlineKeyboardButton("7", callback_data="7"),
                InlineKeyboardButton("8", callback_data="8"),
                InlineKeyboardButton("9", callback_data="9"),
                InlineKeyboardButton("×", callback_data="*"),
            ],
            [
                InlineKeyboardButton("4", callback_data="4"),
                InlineKeyboardButton("5", callback_data="5"),
                InlineKeyboardButton("6", callback_data="6"),
                InlineKeyboardButton("-", callback_data="-"),
            ],
            [
                InlineKeyboardButton("1", callback_data="1"),
                InlineKeyboardButton("2", callback_data="2"),
                InlineKeyboardButton("3", callback_data="3"),
                InlineKeyboardButton("+", callback_data="+"),
            ],
            [
                InlineKeyboardButton("00", callback_data="00"),
                InlineKeyboardButton("0", callback_data="0"),
                InlineKeyboardButton(".", callback_data="."),
                InlineKeyboardButton("=", callback_data="="),
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
    global hitung
    data = cq.data

    if data == "DEL":
        if hitung:
            hitung = hitung[:-1]
    elif data == "AC":
        hitung = []
    elif data == "=":
        try:
            expression = ''.join(hitung).replace("×", "*").replace("÷", "/").replace("^", "**")
            hasil = str(eval(expression))
            await cq.answer(f"Hasil: {hasil}", show_alert=True)
            hitung = [hasil]
        except Exception as e:
            await cq.answer(f"Error: {str(e)}", show_alert=True)
            hitung = []
    elif data == "KLOS":
        if cq.from_user.id != nlx.me.id:
            return await cq.answer(
                "Hanya pembuat Mix-Userbot yang dapat menutup kalkulator.",
                show_alert=True,
            )
        if cq.message:
            await cq.message.delete()
        elif cq.inline_message_id:
            unPacked = unpacked2(cq.inline_message_id)
            await nlx.delete_messages(unPacked.chat_id, unPacked.message_id)
        hitung = []
        return
    else:
        hitung.append(data)

    current_text = ''.join(hitung)
    try:
        await cq.message.edit_text(
            text=f"{current_text}\n\n\n{CALCULATE_TEXT}",
            disable_web_page_preview=True,
            reply_markup=get_calculator_buttons(),
        )
    except Exception as e:
        await cq.answer(f"Error: {str(e)}", show_alert=True)


@ky.inline("^calcs")
async def _(c, iq):
    if len(iq.query) == 0 or iq.query.lower() == "calcs":
        answers = [
            InlineQueryResultArticle(
                title="Calculator",
                description="New calculator",
                input_message_content=InputTextMessageContent(CALCULATE_TEXT),
                reply_markup=get_calculator_buttons(),
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
    if cq.from_user.id != nlx.me.id:
        return await cq.answer(
            "Hanya pembuat Mix-Userbot yang dapat menutup kalkulator.",
            show_alert=True,
        )

    if cq.message:
        await cq.message.delete()
    elif cq.inline_message_id:
        unPacked = unpacked2(cq.inline_message_id)
        await nlx.delete_messages(unPacked.chat_id, unPacked.message_id)
    global hitung
    hitung = []
    return
