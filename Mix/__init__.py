import uvloop

uvloop.install()

from pyrogram.helpers import InlineKeyboard, ikb

from config import *
from Mix.core import *
from Mix.mix_client import *

git()
heroku()
bot = Bot()
nlx = Userbot()


from team.nandev.class_log import LOGGER
from team.nandev.database import ndB, udB
from team.nandev.autopilot import autobot
from team.nandev.class_handler import ky, human, TAG_LOG, refresh_cache, isFinish
from team.nandev.class_modules import CMD_HELP, paginate_modules
from team.nandev.class_emoji import Emojik
from team.nandev.class_pytgc import unpackInlineMessage, run_sync, YoutubeDownload, YouTubeSearch
from team.nandev.new_database import Greetings, Users, LOCKS, Approve, Notes, NotesSettings, Filters, GBan, GMute
from thegokil import DEVS, NO_GCAST

from langs import *
