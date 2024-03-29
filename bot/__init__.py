"""Bot intialization."""

import ast
import logging
import os

import urllib3
from discord.ext import commands
from dotenv import load_dotenv

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

load_dotenv("config.env")

BOT_PREFIX = os.environ.get("BOT_PREFIX")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
DB_URI = os.environ.get("DATABASE_URL")
KEY = os.environ.get("KEY")
REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)
CUSTOM_STATUS = os.environ.get("CUSTOM_STATUS", None)
DEF_GUILD_ID = int(os.environ.get("DEF_GUILD_ID", 0))
DAILY_TASK = ast.literal_eval(os.environ.get("DAILY_TASK") or "False")
DAILY_TASK_TIME = int(os.environ.get("DAILY_TASK_TIME") or 0)  # UTC
SCHEDULE_CHANNEL = int(os.environ.get("SCHEDULE_CHANNEL") or 0)
TASK_MSG_PLACEHOLDER = int(os.environ.get("TASK_MSG_PLACEHOLDER") or 0)

# disabling warning when getting logs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
bot = commands.Bot(command_prefix=BOT_PREFIX)  # pylint: disable = invalid-name
bot.remove_command("help")  # removing the default help
