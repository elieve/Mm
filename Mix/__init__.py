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


from team.nandev.autopilot import autobot
from team.nandev.class_emoji import Emojik
from team.nandev.class_handler import (TAG_LOG, human, isFinish, ky,
                                       refresh_cache)
from team.nandev.class_log import LOGGER
from team.nandev.class_modules import CMD_HELP, paginate_modules
from team.nandev.class_pytgc import (YoutubeDownload, YouTubeSearch, run_sync,
                                     unpackInlineMessage)
from team.nandev.database import ndB, udB
from team.nandev.new_database import (LOCKS, Approve, Filters, GBan, GMute,
                                      Greetings, Notes, NotesSettings, Users)
from thegokil import DEVS, NO_GCAST

from langs import *
