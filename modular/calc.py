from pyrogram import *
from pyrogram.types import *

from Mix import *

__modles__ = "Calculator"
__help__ = "Calculator"


@ky.ubot("calc|kalku", sudo=True)
async def _(c: nlx, m):
    await m.reply_text(
        text=CALCULATE_TEXT,
        reply_markup=CALCULATE_BUTTONS,
        disable_web_page_preview=True,
        quote=True,
    )
