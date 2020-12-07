"""Bot intialization."""

import os
import logging
import urllib3

from discord.ext import commands


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ClassScraper.log"),
        logging.StreamHandler(),
    ],
    level=logging.INFO)
logging.getLogger("discord").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)
LOGGER.info("Starting bot")


ENV = bool(os.environ.get("ENV", False))

if ENV:
    BOT_PREFIX = os.environ.get("BOT_PREFIX", None)
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    CS_GUILD_ID = int(os.environ.get("CS_GUILD_ID", None))
    DAILY_TASK = bool(os.environ.get("DAILY_TASK", False))
    DAILY_TASK_TIME = int(os.environ.get("DAILY_TASK_TIME", 23))  # UTC
    DB_URI = os.environ.get("DATABASE_URL", None)
    KEY = os.environ.get("KEY", None)
    SCHEDULE_CHANNEL = int(os.environ.get("SCHEDULE_CHANNEL", None))
    TASK_MSG_PLACEHOLDER = int(os.environ.get("TASK_MSG_PLACEHOLDER", None))
else:
    import config

    BOT_PREFIX = config.BOT_PREFIX
    BOT_TOKEN = config.BOT_TOKEN
    CS_GUILD_ID = config.CS_GUILD_ID
    DAILY_TASK = config.DAILY_TASK
    DAILY_TASK_TIME = config.DAILY_TASK_TIME
    DB_URI = config.DATABASE_URL
    KEY = config.KEY
    SCHEDULE_CHANNEL = config.SCHEDULE_CHANNEL
    TASK_MSG_PLACEHOLDER = config.TASK_MSG_PLACEHOLDER


# disabling warning when getting logs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
bot = commands.Bot(command_prefix=BOT_PREFIX)
bot.remove_command("help")  # removing the default help
