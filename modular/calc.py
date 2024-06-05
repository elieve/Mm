from pyrogram import *
from pyrogram.types import *

from Mix import *

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
async def _(c: nlx, m):
    await m.reply_text(
        text=CALCULATE_TEXT,
        reply_markup=CALCULATE_BUTTONS,
        disable_web_page_preview=True,
        quote=True,
    )


@ky.ubot(filter=False)
async def evaluate(c, m):
    try:
        data = m.text.replace("×", "*").replace("÷", "/")
        result = str(eval(data))
    except:
        return
    await m.reply_text(
        text=result,
        reply_markup=CALCULATE_BUTTONS,
        disable_web_page_preview=True,
        quote=True,
    )


@ky.callback()
async def cb_data(c, m):
    data = m.data
    try:
        message_text = m.message.text.split("\n")[0].strip().split("=")[0].strip()
        text = "" if CALCULATE_TEXT in message_text else message_text
        if data == "=":
            text = str(eval(text))
        elif data == "DEL":
            text = message_text[:-1]
        elif data == "AC":
            text = ""
        else:
            text = message_text + data
        await m.message.edit_text(
            text=f"{text}\n\n\n{CALCULATE_TEXT}",
            disable_web_page_preview=True,
            reply_markup=CALCULATE_BUTTONS,
        )
    except Exception as error:
        print(error)


@ky.inline()
async def inline(bot, update):
    if len(update.data) == 0:
        try:
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
        except Exception as error:
            print(error)
    else:
        try:
            data = update.query.replace("×", "*").replace("÷", "/")
            result = str(eval(text))
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
            pass
    await update.answer(answers)
