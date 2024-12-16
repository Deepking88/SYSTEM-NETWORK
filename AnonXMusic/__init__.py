from AnonXMusic.core.bot import Anony
from AnonXMusic.core.dir import dirr
from AnonXMusic.core.git import git
from AnonXMusic.core.userbot import Userbot
from AnonXMusic.misc import dbb, heroku
from telethon import TelegramClient, events
from .logging import LOGGER
from config import *
from telegram.ext import Application

dirr()
git()
dbb()
heroku()

app = Anony()
userbot = Userbot()

# Initialize the bot application
botxx = Application.builder().token(BOT_TOKEN).build()

botx = TelegramClient('bot', api_id=API_ID, api_hash=API_HASH).start(bot_token=BOT_TOKEN)

from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
