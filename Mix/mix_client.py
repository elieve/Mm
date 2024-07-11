################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
import asyncio
import importlib
################################################################
import os
import re
import shlex
import subprocess
from io import BytesIO

from pyrogram import Client, enums, filters
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from team.nandev.class_log import LOGGER
from team.nandev.class_modules import CMD_HELP
from team.nandev.database import ndB, udB

from config import *
from modular import USER_MOD

TOKEN_BOT = ndB.get_key("BOT_TOKEN") or bot_token
OWNER = ndB.get_key("OWNER_ID")


class Userbot(Client):
    _prefix = {}
    _translate = {}

    def __init__(self, **kwargs):
        super().__init__(
            name="user",
            api_id=api_id,
            api_hash=api_hash,
            session_string=session,
            device_model="Max-Userbot",
            plugins=dict(root="modular"),
            # proxy=self._configure_proxy(),
            **kwargs,
        )

    def _configure_proxy(self):
        proxy_config = {"scheme": scheme, "hostname": hostname, "port": port}
        if username is not None and password is not None:
            proxy_config["username"] = username
            proxy_config["password"] = password

        return proxy_config

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    def set_prefix(self, user_id, prefix):
        self._prefix[user_id] = prefix

    async def get_chats_dialog(self, c, q):
        chats = []
        chat_types = {
            "grup": [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP],
            "all": [
                enums.ChatType.GROUP,
                enums.ChatType.SUPERGROUP,
                enums.ChatType.PRIVATE,
            ],
            "bot": [enums.ChatType.BOT],
            "usbot": [enums.ChatType.PRIVATE, enums.ChatType.BOT],
            "user": [enums.ChatType.PRIVATE],
            "gban": [
                enums.ChatType.GROUP,
                enums.ChatType.SUPERGROUP,
                enums.ChatType.CHANNEL,
            ],
            "ch": [enums.ChatType.CHANNEL],
        }
        try:
            async for dialog in c.get_dialogs():
                try:
                    if dialog.chat.type in chat_types[q]:
                        chats.append(dialog.chat.id)
                except Exception as e:
                    print(f"An error occurred while processing dialog: {e}")
        except Exception as e:
            print(f"An error occurred while getting dialogs: {e}")

        return chats

    async def get_prefix(self, user_id):
        return self._prefix.get(user_id, ["."])

    async def dln(self, download):
        path = await self.download_media(download)
        with open(path, "rb") as f:
            content = f.read()
        os.remove(path)
        doc = BytesIO(content)
        return doc

    def user_prefix(self, cmd):
        command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

        async def func(_, c, m):
            if m.text:
                text = m.text.strip().encode("utf-8").decode("utf-8")
                username = c.me.username or ""
                prefixes = await self.get_prefix(c.me.id)

                if not text:
                    return False

                for prefix in prefixes:
                    if not text.startswith(prefix):
                        continue

                    without_prefix = text[len(prefix) :]

                    for command in cmd.split("|"):
                        if not re.match(
                            rf"^(?:{command}(?:@?{username})?)(?:\s|$)",
                            without_prefix,
                            flags=re.IGNORECASE | re.UNICODE,
                        ):
                            continue

                        without_command = re.sub(
                            rf"{command}(?:@?{username})?\s?",
                            "",
                            without_prefix,
                            count=1,
                            flags=re.IGNORECASE | re.UNICODE,
                        )
                        m.command = [command] + [
                            re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                            for m in command_re.finditer(without_command)
                        ]

                        return True

                return False

        return filters.create(func)

    def get_m(self, m):
        msg = (
            m.reply_to_message
            if m.reply_to_message
            else "" if len(m.command) < 2 else " ".join(m.command[1:])
        )
        return msg

    def get_text(self, m):
        if m.reply_to_message:
            if len(m.command) < 2:
                text = m.reply_to_message.text or m.reply_to_message.caption
            else:
                text = (
                    (m.reply_to_message.text or m.reply_to_message.caption)
                    + "\n\n"
                    + m.text.split(None, 1)[1]
                )
        else:
            if len(m.command) < 2:
                text = ""
            else:
                text = m.text.split(None, 1)[1]
        return text

    async def bash(self, cmd):
        try:
            process = await asyncio.create_subprocess_shell(
                cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            err = stderr.decode().strip()
            out = stdout.decode().strip()
            return out, err
        except NotImplementedError:
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
            )
            stdout, stderr = process.communicate()
            err = stderr.decode().strip()
            out = stdout.decode().strip()
            return out, err

    async def run_cmd(self, cmd):
        args = shlex.split(cmd)
        try:
            process = await asyncio.create_subprocess_exec(
                *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            return (
                stdout.decode("utf-8", "replace").strip(),
                stderr.decode("utf-8", "replace").strip(),
                process.returncode,
                process.pid,
            )
        except NotImplementedError:
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
            )
            stdout, stderr = process.communicate()
            return (
                stdout.decode("utf-8", "replace").strip(),
                stderr.decode("utf-8", "replace").strip(),
                process.returncode,
                process.pid,
            )

    async def aexec(self, code, c, m):
        exec(
            "async def __aexec(c, m): " + "".join(f"\n {l_}" for l_ in code.split("\n"))
        )
        return await locals()["__aexec"](c, m)

    async def shell_exec(self, code, treat=True):
        process = await asyncio.create_subprocess_shell(
            code, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
        )

        stdout = (await process.communicate())[0]
        if treat:
            stdout = stdout.decode().strip()
        return stdout, process

    def get_arg(self, m):
        if m.reply_to_message and len(m.command) < 2:
            msg = m.reply_to_message.text or m.reply_to_message.caption
            if not msg:
                return ""
            msg = msg.encode().decode("UTF-8")
            msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
            return msg
        elif len(m.command) > 1:
            return " ".join(m.command[1:])
        else:
            return ""

    async def extract_userid(self, m, t):
        def is_int(t):
            try:
                int(t)
            except ValueError:
                return False
            return True

        text = t.strip()

        if is_int(text):
            return int(text)

        entities = m.entities
        m._client
        entity = entities[1 if m.text.startswith("/") else 0]
        if entity.type == enums.MessageEntityType.MENTION:
            return (await self.get_users(text)).id
        if entity.type == enums.MessageEntityType.TEXT_MENTION:
            return entity.user.id
        return None

    async def extract_user_and_reason(self, m, s=False):
        args = m.text.strip().split()
        text = m.text
        rg = None
        reason = None
        if m.reply_to_message:
            reply = m.reply_to_message
            if not reply.from_user:
                if reply.sender_chat and reply.sender_chat != m.chat.id and s:
                    id_ = reply.sender_chat.id
                else:
                    return None, None
            else:
                id_ = reply.from_user.id

            if len(args) < 2:
                reason = None
            else:
                reason = text.split(None, 1)[1]
            return id_, reason

        if len(args) == 2:
            rg = text.split(None, 1)[1]
            return await self.extract_userid(m, rg), None

        if len(args) > 2:
            rg, reason = text.split(None, 2)[1:]
            return await self.extract_userid(m, rg), reason

        return rg, reason

    async def extract_user(self, m):
        return (await self.extract_user_and_reason(m))[0]

    async def start(self):
        await super().start()
        handler = udB.get_pref(self.me.id)
        if OWNER is None:
            ndB.set_key("OWNER_ID", self.me.id)
        if OWNER != self.me.id:
            ndB.del_key("OWNER_ID")
            ndB.set_key("OWNER_ID", self.me.id)
        if handler:
            self._prefix[self.me.id] = handler
        else:
            self._prefix[self.me.id] = ["."]
        self._translate[self.me.id] = {"negara": "id"}
        LOGGER.info(f"Starting Userbot {self.me.id}|{self.me.username}")


class Bot(Client):
    def __init__(self, **kwargs):
        super().__init__(
            name="bot",
            api_id=api_id,
            api_hash=api_hash,
            bot_token=TOKEN_BOT,
            plugins=dict(root="assistant"),
            **kwargs,
        )

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    def on_callback_query(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(CallbackQueryHandler(func, filters), group)
            return func

        return decorator

    async def start(self):
        await super().start()
        LOGGER.info(f"Importing Modules...")
        for modul in USER_MOD:
            imported_module = importlib.import_module(f"modular." + modul)
            if hasattr(imported_module, "__modles__") and imported_module.__modles__:
                imported_module.__modles__ = imported_module.__modles__
                if hasattr(imported_module, "__help__") and imported_module.__help__:
                    CMD_HELP[imported_module.__modles__.replace(" ", "_").lower()] = (
                        imported_module
                    )
        LOGGER.info(f"Successfully Import Modules...")
        LOGGER.info(f"Starting Assistant {self.me.id}|{self.me.username}")


class _SudoManager:
    def __init__(self):
        self.db = None
        self.owner = None
        self._owner_sudos = []

    def _init_db(self):
        if not self.db:
            self.db = ndB
        return self.db

    def get_sudos(self):
        db = self._init_db()
        SUDOS = db.get_key("SUDOS")
        return SUDOS or []

    @property
    def allow_sudo(self):
        db = self._init_db()
        return db.get_key("SUDO")

    def owner_and_sudos(self):
        if not self.owner:
            db = self._init_db()
            self.owner = db.get_key("OWNER_ID")
        return [self.owner, *self.get_sudos()]

    def is_sudo(self, id_):
        return bool(id_ in self.get_sudos())


SUDO_M = _SudoManager()
owner_and_sudos = SUDO_M.owner_and_sudos
sudoers = SUDO_M.get_sudos
is_sudo = SUDO_M.is_sudo

# ------------------------------------------------ #


def append_or_update(load, func, name, arggs):
    if isinstance(load, list):
        return load.append(func)
    if isinstance(load, dict):
        if load.get(name):
            return load[name].append((func, arggs))
        return load.update({name: [(func, arggs)]})
