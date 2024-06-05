################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || EH KONTOL KALO PUNYA AKAL DIPAKE YA ANJING GAUSAH APUS² CREDIT MODAL NYOPAS LO BAJINGAN!!
"""
################################################################


from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *

from Mix import bot, ky

__modles__ = "Calculator"
__help__ = "Calculator"

CALCULATE_TEXT = "Mix-Userbot Calculator"

CALCULATE_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("(", callback_data="("),
            InlineKeyboardButton(")", callback_data=")"),
            InlineKeyboardButton("^", callback_data="^"),
        ],
        [
            InlineKeyboardButton("%", callback_data="%"),
            InlineKeyboardButton("AC", callback_data="AC"),
            InlineKeyboardButton("DEL", callback_data="DEL"),
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
            InlineKeyboardButton("=", callback_data="="),
            InlineKeyboardButton(".", callback_data="."),
        ],
    ]
)


@ky.ubot("calc|kalku", sudo=True)
async def calculator(c, m):
    try:
        x = await c.get_inline_bot_results(bot.me.username, "calc")
        await m.reply_inline_bot_result(x.query_id, x.results[0].id)
    except Exception as error:
        await m.reply(error)


"""
    await m.reply_text(
        text=CALCULATE_TEXT,
        reply_markup=CALCULATE_BUTTONS,
        disable_web_page_preview=True,
        quote=True,
    )
"""


@ky.callback(".*")
async def cb_data(c, cq):
    data = cq.data
    message_text = cq.message.text.split("\n")[0].strip().split("=")[0].strip()
    text = "" if CALCULATE_TEXT in message_text else message_text
    if data == "=":
        try:
            text = str(eval(text.replace("×", "*").replace("÷", "/")))
        except:
            text = "Error"
    elif data == "DEL":
        text = message_text[:-1]
    elif data == "AC":
        text = ""
    else:
        text = message_text + data

    await cq.message.edit_text(
        text=f"{text}\n\n\n{CALCULATE_TEXT}",
        disable_web_page_preview=True,
        reply_markup=CALCULATE_BUTTONS,
    )


@ky.inline("calc")
async def inline_query(bot, iq):
    if len(iq.query) == 0:
        answers = [
            InlineQueryResultArticle(
                title="Calculator",
                description="New calculator",
                input_message_content=InputTextMessageContent(
                    text=CALCULATE_TEXT, disable_web_page_preview=True
                ),
                reply_markup=CALCULATE_BUTTONS,
            )
        ]
    else:
        try:
            data = iq.query.replace("×", "*").replace("÷", "/")
            result = str(eval(data))
            answers = [
                InlineQueryResultArticle(
                    title="Answer",
                    description=f"Result: {result}",
                    input_message_content=InputTextMessageContent(
                        text=f"{data} = {result}", disable_web_page_preview=True
                    ),
                )
            ]
        except:
            answers = [
                InlineQueryResultArticle(
                    title="Error",
                    description="Invalid Expression",
                    input_message_content=InputTextMessageContent(
                        text="Invalid Expression", disable_web_page_preview=True
                    ),
                )
            ]

    await c.answer_inline_query(iq.id, cache_time=300, results=answers)
