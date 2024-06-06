from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *

from Mix import bot, ky, nlx

__modules__ = "Calculator"
__help__ = "Calculator"

CALCULATE_TEXT = "Mix-Userbot Calculator"


def get_calculator_buttons(current_text):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("(", callback_data=f"({current_text}"),
                InlineKeyboardButton(")", callback_data=f"){current_text}"),
                InlineKeyboardButton("^", callback_data=f"^{current_text}"),
            ],
            [
                InlineKeyboardButton("%", callback_data=f"%{current_text}"),
                InlineKeyboardButton("AC", callback_data="AC"),
                InlineKeyboardButton("DEL", callback_data="DEL"),
                InlineKeyboardButton("÷", callback_data=f"/{current_text}"),
            ],
            [
                InlineKeyboardButton("7", callback_data=f"7{current_text}"),
                InlineKeyboardButton("8", callback_data=f"8{current_text}"),
                InlineKeyboardButton("9", callback_data=f"9{current_text}"),
                InlineKeyboardButton("×", callback_data=f"*{current_text}"),
            ],
            [
                InlineKeyboardButton("4", callback_data=f"4{current_text}"),
                InlineKeyboardButton("5", callback_data=f"5{current_text}"),
                InlineKeyboardButton("6", callback_data=f"6{current_text}"),
                InlineKeyboardButton("-", callback_data=f"-{current_text}"),
            ],
            [
                InlineKeyboardButton("1", callback_data=f"1{current_text}"),
                InlineKeyboardButton("2", callback_data=f"2{current_text}"),
                InlineKeyboardButton("3", callback_data=f"3{current_text}"),
                InlineKeyboardButton("+", callback_data=f"+{current_text}"),
            ],
            [
                InlineKeyboardButton("00", callback_data=f"00{current_text}"),
                InlineKeyboardButton("0", callback_data=f"0{current_text}"),
                InlineKeyboardButton("=", callback_data=f"={current_text}"),
                InlineKeyboardButton(".", callback_data=f".{current_text}"),
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

    if cq.message and cq.message.text:
        message_text = cq.message.text.split("\n")[0].strip().split("=")[0].strip()
    else:
        message_text = ""

    if data.startswith("AC"):
        text = ""
        print("Teks setelah AC: Kosong")
    elif data.startswith("DEL"):
        text = message_text[:-1]
        print(f"Teks setelah DEL: {text}")
    elif data.startswith("="):
        try:
            expression = message_text
            text = str(eval(expression.replace("×", "*").replace("÷", "/").replace("^", "**")))
            print(f"Hasil evaluasi: {text}")
        except Exception as e:
            print(f"Error evaluasi: {e}")
            text = "Error"
    else:
        text = message_text + data[1:]
        print(f"Teks setelah menambahkan data: {text}")

    await cq.message.edit_text(
        text=f"{text}\n\n\n{CALCULATE_TEXT}",
        disable_web_page_preview=True,
        reply_markup=get_calculator_buttons(text),
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
                reply_markup=get_calculator_buttons(""),
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
