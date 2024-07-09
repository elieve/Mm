import asyncio
import random

from pyrogram import *
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.types import *

from Mix import *

__modles__ = "Mention"
__help__ = get_cgr("help_mention")

jalan = False
status_per_grup = {}


def random_emoji():
    emojis = "⌚️ 📱 📲 💻 ⌨️ 🖥 🖨 🖱 🖲 🕹 🗜 💽 💾 💿 📀 📼 📷 📸 📹 🎥 📽 🎞 📞 ☎️ 📟 📠 📺 📻 🎙 🎚 🎛 🧭 ⏱ ⏲ ⏰ 🕰 ⌛️ ⏳ 📡 🔋 🪫 🔌 💡 🔦 🕯 🪔 🧯 🛢 🛍️ 💸 💵 💴 💶 💷 🪙 💰 💳 💎 ⚖️ 🪮 🪜 🧰 🪛 🔧 🔨 ⚒ 🛠 ⛏ 🪚 🔩 ⚙️ 🪤 🧱 ⛓ ⛓️‍💥 🧲 🔫 💣 🧨 🪓 🔪 🗡 ⚔️ 🛡 🚬 ⚰️ 🪦 ⚱️ 🏺 🔮 📿 🧿 🪬 💈 ⚗️ 🔭 🔬 🕳 🩹 🩺 🩻 🩼 💊 💉 🩸 🧬 🦠 🧫 🧪 🌡 🧹 🪠 🧺 🧻 🚽 🚰 🚿 🛁 🛀 🧼 🪥 🪒 🧽 🪣 🧴 🛎 🔑 🗝 🚪 🪑 🛋 🛏 🛌 🧸 🪆 🖼 🪞 🪟 🛍 🛒 🎁 🎈 🎏 🎀 🪄 🪅 🎊 🎉 🪩 🎎 🏮 🎐 🧧 ✉️ 📩 📨 📧 💌 📥 📤 📦 🏷 🪧 📪 📫 📬 📭 📮 📯 📜 📃 📄 📑 🧾 📊 📈 📉 🗒 🗓 📆 📅 🗑 🪪 📇 🗃 🗳 🗄 📋 📁 📂 🗂 🗞 📰 📓 📔 📒 📕 📗 📘 📙 📚 📖 🔖 🧷 🔗 📎 🖇 📐 📏 🧮 📌 📍 ✂️ 🖊 🖋 ✒️ 🖌 🖍 📝 ✏️ 🔍 🔎 🔏 🔐 🔒 🔓".split(
        " "
    )
    return random.choice(emojis)


@ky.ubot("tagall|mention")
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    chat_id = m.chat.id
    if chat_id not in status_per_grup:
        status_per_grup[chat_id] = {
            "jalan": False,
            "mentioned_count": 0,
            "total_members": [],
        }

    status = status_per_grup[chat_id]

    if status["jalan"]:
        await m.reply(cgr("ment_5").format(em.gagal))
        return

    status["jalan"] = True
    status["mentioned_count"] = 0
    status["total_members"] = []
    progres = await m.reply(cgr("ment_6").format(em.proses))

    async for member in c.get_chat_members(chat_id):
        user = member.user
        if not user.is_bot and not user.is_self and not user.is_deleted:
            status["total_members"].append(user.id)

    if not m.reply_to_message and len(m.command) < 2:
        await progres.edit(cgr("ment_2").format(em.gagal))
        status["jalan"] = False
        return

    text = c.get_text(m)
    jummem = len(status["total_members"])
    mention_texts = []

    for member_id in status["total_members"]:
        if not status["jalan"]:
            break
        mention_texts.append(f"[{random_emoji()}](tg://user?id={member_id})")
        status["mentioned_count"] += 1
        if len(mention_texts) == 4:
            mention_text = f"{text}\n\n{' ★ '.join(mention_texts)}"
            try:
                await c.send_message(chat_id, mention_text)
                await asyncio.sleep(3)
            except FloodWait as e:
                tunggu = int(e.value)
                if tunggu > 200:
                    status["jalan"] = False
                    await asyncio.sleep(tunggu)
                    await c.send_message(
                        chat_id,
                        cgr("ment_7").format(
                            em.gagal,
                            tunggu,
                            em.sukses,
                            status["mentioned_count"],
                            jummem,
                        ),
                    )
                    return
                await asyncio.sleep(tunggu)
                try:
                    await c.send_message(chat_id, mention_text)
                    await asyncio.sleep(3)
                except:
                    await c.send_message(
                        chat_id,
                        cgr("ment_8").format(
                            em.sukses, status["mentioned_count"], jummem
                        ),
                    )
            mention_texts = []

    if mention_texts:
        mention_text = f"{text}\n\n{' ★ '.join(mention_texts)}"
        try:
            await c.send_message(chat_id, mention_text)
            await asyncio.sleep(3)
        except FloodWait as e:
            tunggu = int(e.value)
            if tunggu > 200:
                status["jalan"] = False
                await asyncio.sleep(tunggu)
                await c.send_message(
                    chat_id,
                    cgr("ment_7").format(
                        em.gagal, tunggu, em.sukses, status["mentioned_count"], jummem
                    ),
                )
                return
            await asyncio.sleep(tunggu)
            try:
                await c.send_message(chat_id, mention_text)
                await asyncio.sleep(3)
            except:
                await c.send_message(
                    chat_id,
                    cgr("ment_8").format(em.sukses, status["mentioned_count"], jummem),
                )

    status["jalan"] = False
    await progres.delete()
    await c.send_message(
        m.chat.id, cgr("ment_9").format(em.sukses, status["mentioned_count"], jummem)
    )


@ky.ubot("stop|cancel|batal")
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    chat_id = m.chat.id
    if chat_id not in status_per_grup:
        status_per_grup[chat_id] = {
            "jalan": False,
            "mentioned_count": 0,
            "total_members": [],
        }

    status = status_per_grup[chat_id]
    xx = await m.edit(cgr("proses").format(em.proses))

    if not status["jalan"]:
        await xx.edit(cgr("ment_10").format(em.gagal))
        await asyncio.sleep(2)
        await xx.delete()
        return

    status["jalan"] = False
    await xx.edit(cgr("ment_11").format(em.sukses))
    await asyncio.sleep(3)
    await xx.delete()
