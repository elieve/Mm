from base64 import urlsafe_b64decode
from struct import unpack

from attrify import Attrify as Atr
from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *

from Mix import *

hitung = []


mmk = {
    "(",
    ")",
    "KLOS",
    "AC",
    "DEL",
    "%",
    "/",
    "*",
    "-",
    "+",
    "00",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    ".",
    "=",
}


def get_calculator_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("(", callback_data="("),
                InlineKeyboardButton(")", callback_data=")"),
                InlineKeyboardButton("🇮🇩", url="tg://resolve?domain=diemgausahbawel"),
            ],
            [
                InlineKeyboardButton("%", callback_data="%"),
                InlineKeyboardButton("🆑", callback_data="AC"),
                InlineKeyboardButton("⌫", callback_data="DEL"),
                InlineKeyboardButton("➗", callback_data="/"),
            ],
            [
                InlineKeyboardButton("7️⃣", callback_data="7"),
                InlineKeyboardButton("8️⃣", callback_data="8"),
                InlineKeyboardButton("9️⃣", callback_data="9"),
                InlineKeyboardButton("✖️", callback_data="*"),
            ],
            [
                InlineKeyboardButton("4️⃣", callback_data="4"),
                InlineKeyboardButton("5️⃣", callback_data="5"),
                InlineKeyboardButton("6️⃣", callback_data="6"),
                InlineKeyboardButton("➖", callback_data="-"),
            ],
            [
                InlineKeyboardButton("1️⃣", callback_data="1"),
                InlineKeyboardButton("2️⃣", callback_data="2"),
                InlineKeyboardButton("3️⃣", callback_data="3"),
                InlineKeyboardButton("➕", callback_data="+"),
            ],
            [
                InlineKeyboardButton("0️⃣0️⃣", callback_data="00"),
                InlineKeyboardButton("0️⃣", callback_data="0"),
                InlineKeyboardButton("🟰", callback_data="="),
                InlineKeyboardButton("◾", callback_data="."),
            ],
            [
                InlineKeyboardButton("❌", callback_data="KLOS"),
            ],
        ]
    )


@ky.callback("^[0-9/*\-+().=ACDEL%]{1,2}$")
async def _(c, cq):
    global hitung
    data = cq.data
    CALCULATE_TEXT = """
Mix-Userbot Calculator
© [DEV](tg://resolve?domain=diemgausahbawel)
"""

    if data not in mmk:
        return

    user = cq.from_user
    fullname = user.first_name
    if user.last_name:
        fullname += f" {user.last_name}"

    if data == "DEL":
        if hitung:
            hitung = hitung[:-1]
    elif data == "AC":
        hitung = []
    elif data == "=":
        try:
            expression = (
                "".join(hitung).replace("×", "*").replace("÷", "/").replace("^", "**")
            )
            hasil = str(eval(expression))
            await cq.answer(f"Hasil: {hasil}", show_alert=True)
            hitung = [hasil]
        except Exception as e:
            await cq.answer(f"Error: {str(e)}", show_alert=True)
            hitung = []
    elif data == "KLOS":
        if cq.from_user.id != nlx.me.id:
            return await cq.answer(
                f"{fullname} KAYA KONTOL! SIRIK AJA LO!\nGAUSAH DIPENCET! ANJING! MEMEK! NGENTOT! BELI SENDIRI SANA!!",
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
        if cq.from_user.id != nlx.me.id:
            return await cq.answer(
                f"BELI LAH Mix-Userbot WAHAI {fullname}.\nHANYA 35k, ANDA SUDAH BISA MENIKMATI SEKIAN BANYAKNYA FITUR DI Mix-Userbot!",
                show_alert=True,
            )
        hitung.append(data)

    current_text = "".join(hitung)

    if cq.message:
        try:
            await cq.message.edit_text(
                text=f"{current_text}\n\n\n{CALCULATE_TEXT}",
                disable_web_page_preview=True,
                reply_markup=get_calculator_buttons(),
            )
        except Exception as e:
            await cq.answer(f"Error: {str(e)}", show_alert=True)
    else:
        await cq.answer(f"{current_text}")


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
