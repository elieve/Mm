################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################


from pyrogram import *
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.file_id import *
from pyrogram.helpers import ikb
from pyrogram.raw.functions.messages import *
from pyrogram.raw.functions.stickers import *
from pyrogram.raw.types import *
from pyrogram.types import *

from Mix import *

help = async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    if not c.get_arg(m):
        try:
            x = await c.get_inline_bot_results(bot.me.username, "help")
            await m.reply_inline_bot_result(x.query_id, x.results[0].id)
        except Exception as error:
            await m.reply(error)
    else:
        nama = c.get_arg(m)
        if c.get_arg(m) in CMD_HELP:
            prefix = await c.get_prefix(c.me.id)
            await m.reply(
                CMD_HELP[c.get_arg(m)].__help__.format(next((p) for p in prefix))
                + f"\n<b>© Max-Userbot - @ccavolo</b>",
                quote=True,
            )
        else:
            await m.reply(cgr("hlp_1").format(em.gagal, nama))



@ky.bots("start", human.pv)
async def _(c, m):
    udB.add_served_user(m.from_user.id)
    owner_nih = nlx.me.id
    user_name = f"<a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name} {m.from_user.last_name or ''}</a>"
    user2 = f"<a href='tg://user?id={nlx.me.id}'>{nlx.me.first_name} {nlx.me.last_name or ''}</a>"
    ts_1 = cgr("asst_1").format(user_name)
    ts_2 = cgr("asst_2").format(user_name, user2)
    if m.from_user.id == owner_nih:
        button = ikb(
            [
                [(cgr("asst_3"), "clbk.bhsa"), (cgr("asst_6"), "clbk.rebot")],
                [("Repo", "https://github.com/elieve/mm", "url"), ("Buat Bot", "t.me/ccavolo", "url")],
                [(cgr("ttup"), "help")],
            ]
        )
        return await m.reply(ts_1, reply_markup=button)
    else:
        tt = ikb([[(cgr("ttup"), "close_asst")]])
        return await m.reply(ts_2, reply_markup=tt)
