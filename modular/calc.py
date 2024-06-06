from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *

from Mix import bot, ky, nlx

__modules__ = "Calculator"
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
    try:
        print("Menerima perintah calc dari user")
        x = await c.get_inline_bot_results(bot.me.username, "calcs")
        print("Inline bot results berhasil didapatkan")
        await m.reply_inline_bot_result(x.query_id, x.results[0].id)
        print("Hasil inline bot dibalas ke user")
    except Exception as error:
        print(f"Error pada perintah calc: {error}")
        await m.reply_text(str(error))


@ky.callback("^.*")
async def _(c, cq):
    data = cq.data
    print(f"Callback data diterima: {data}")

    if cq.message.reply_to_message and cq.message.reply_to_message.text:
        message_text = cq.message.reply_to_message.text.split("\n")[0].strip().split("=")[0].strip()
    else:
        print("Error: cq.message.reply_to_message atau cq.message.reply_to_message.text adalah None")
        return

    text = "" if CALCULATE_TEXT in message_text else message_text
    if data == "=":
        try:
            text = str(
                eval(text.replace("×", "*").replace("÷", "/").replace("^", "**"))
            )
            print(f"Hasil evaluasi: {text}")
        except Exception as e:
            print(f"Error evaluasi: {e}")
            text = "Error"
    elif data == "DEL":
        text = message_text[:-1]
        print(f"Teks setelah DEL: {text}")
    elif data == "AC":
        text = ""
        print("Teks setelah AC: Kosong")
    else:
        text = message_text + data
        print(f"Teks setelah menambahkan data: {text}")

    await cq.message.edit_text(
        text=f"{text}\n\n\n{CALCULATE_TEXT}",
        disable_web_page_preview=True,
        reply_markup=CALCULATE_BUTTONS,
    )
    print("Pesan hasil kalkulasi diubah")


@ky.inline("^calcs")
async def _(c, iq):
    print(f"Inline query diterima: {iq.query}")
    if len(iq.query) == 0 or iq.query.lower() == "calcs":
        answers = [
            InlineQueryResultArticle(
                title="Calculator",
                description="New calculator",
                input_message_content=InputTextMessageContent(
                    message_text=CALCULATE_TEXT, disable_web_page_preview=True
                ),
                reply_markup=CALCULATE_BUTTONS,
            )
        ]
        print("Inline query kosong atau 'calcs', menampilkan kalkulator baru")
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
            print(f"Evaluasi sukses: {data} = {result}")
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
            print("Evaluasi gagal, menampilkan Invalid Expression")

    await c.answer_inline_query(iq.id, cache_time=300, results=answers)
    print("Inline query dijawab")
    