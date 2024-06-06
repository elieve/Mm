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
        message_text = ""

    if data.startswith("AC"):
        teks = ""
    elif data.startswith("DEL"):
        teks = message_text[:-1]
    elif data.startswith("="):
        try:
            expression = message_text
            teks = str(
                eval(expression.replace("×", "*").replace("÷", "/").replace("^", "**"))
            )
        except Exception:
            teks = "Error"
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
