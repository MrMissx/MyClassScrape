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
    DAILY_TASK = os.environ.get("DAILY_TASK", False)
    CS_GUILD_ID = os.environ.get("CS_GUILD_ID", None)
    TASK_MSG_PLACEHOLDER = os.environ.get("TASK_MSG_PLACEHOLDER", None)
    DB_URI = os.environ.get("DATABASE_URL", None)
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    KEY = os.environ.get("KEY", None)
    SCHEDULE_CHANNEL = os.environ.get("SCHEDULE_CHANNEL", None)
else:
    import config

    BOT_PREFIX = config.BOT_PREFIX
    BOT_TOKEN = config.BOT_TOKEN
    TASK_MSG_PLACEHOLDER = config.TASK_MSG_PLACEHOLDER
    DAILY_TASK = config.DAILY_TASK
    CS_GUILD_ID = config.CS_GUILD_ID
    DB_URI = config.DATABASE_URL
    KEY = config.KEY
    SCHEDULE_CHANNEL = config.SCHEDULE_CHANNEL


# disabling warning when getting logs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
bot = commands.Bot(command_prefix=BOT_PREFIX)
bot.remove_command('help')  # removing the default help
