

from Mix import bot, ky, nlx

__modles__ = "Calculator"
__help__ = "Calculator"


@ky.ubot("calc|kalku", sudo=True)
async def _(c: nlx, m):
    try:
        x = await c.get_inline_bot_results(bot.me.username, "calcs")
        await m.reply_inline_bot_result(x.query_id, x.results[0].id)
    except Exception as error:
        await m.reply_text(str(error))
