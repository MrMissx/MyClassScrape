import os
import logging
import urllib3

from discord.ext import commands


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)
LOGGER.info("Starting bot")


ENV = bool(os.environ.get("ENV", False))

if ENV:
    BOT_PREFIX = os.environ.get("BOT_PREFIX", None)
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    CS_GUILD_ID = os.environ.get("CS_GUILD_ID", None)
    DB_URI = os.environ.get("DATABASE_URL", None)
    KEY = os.environ.get("KEY", None)
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
else:
    import config

    BOT_PREFIX = config.BOT_PREFIX
    BOT_TOKEN = config.BOT_TOKEN
    CS_GUILD_ID = config.CS_GUILD_ID    
    DB_URI = config.DATABASE_URL
    KEY = config.KEY


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # disabling warning when getting logs
bot = commands.Bot(command_prefix=BOT_PREFIX)
bot.remove_command('help')  # removing the default help
