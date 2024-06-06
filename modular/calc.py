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


def get_calculator_buttons(teks):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("(", callback_data=f"{teks}("),
                InlineKeyboardButton(")", callback_data=f"{teks})"),
                InlineKeyboardButton("CLOSE", callback_data="KLOS"),
            ],
            [
                InlineKeyboardButton("AC", callback_data="AC"),
                InlineKeyboardButton("DEL", callback_data="DEL"),
                InlineKeyboardButton("%", callback_data=f"{teks}%"),
                InlineKeyboardButton("÷", callback_data=f"{teks}/"),
            ],
            [
                InlineKeyboardButton("7", callback_data=f"{teks}7"),
                InlineKeyboardButton("8", callback_data=f"{teks}8"),
                InlineKeyboardButton("9", callback_data=f"{teks}9"),
                InlineKeyboardButton("×", callback_data=f"{teks}*"),
            ],
            [
                InlineKeyboardButton("4", callback_data=f"{teks}4"),
                InlineKeyboardButton("5", callback_data=f"{teks}5"),
                InlineKeyboardButton("6", callback_data=f"{teks}6"),
                InlineKeyboardButton("-", callback_data=f"{teks}-"),
            ],
            [
                InlineKeyboardButton("1", callback_data=f"{teks}1"),
                InlineKeyboardButton("2", callback_data=f"{teks}2"),
                InlineKeyboardButton("3", callback_data=f"{teks}3"),
                InlineKeyboardButton("+", callback_data=f"{teks}+"),
            ],
            [
                InlineKeyboardButton("00", callback_data=f"{teks}00"),
                InlineKeyboardButton("0", callback_data=f"{teks}0"),
                InlineKeyboardButton(".", callback_data=f"{teks}."),
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
    data = cq.data
    if cq.message and cq.message.text:
        message_text = cq.message.text.split("\n")[0].strip().split("=")[0].strip()
        text = "" if CALCULATE_TEXT in message_text else message_text
    else:
        message_text = ""
        text = ""

    if data == "DEL":
        text = text[:-1]
    elif data == "AC":
        text = ""
    elif data == "=":
        try:
            text = ""
            hasil = str(
                eval(text.replace("×", "*").replace("÷", "/").replace("^", "**"))
            )
            cq.answer(f"{hasil}", show_alert=True)
        except Exception:
            text = "Error"
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
        return
    else:
        text = text + data

    try:
        await cq.message.edit_text(
            text=f"{text}\n\n\n{CALCULATE_TEXT}",
            disable_web_page_preview=True,
            reply_markup=get_calculator_buttons(text),
        )
    except Exception:
        await cq.answer(f"{text}")
        # await cq.answer(f"Error: {str(e)}", show_alert=True)


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
