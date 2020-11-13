import os
import logging

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
    DEC_SEC = os.environ.get("DEC_SEC", None)
    ENC_SEC = os.environ.get("ENC_SEC", None)
else:
    import config

    BOT_PREFIX = config.BOT_PREFIX
    BOT_TOKEN = config.BOT_TOKEN
    CS_GUILD_ID = config.CS_GUILD_ID    
    DB_URI = config.DATABASE_URL
    DEC_SEC = config.DEC_SEC
    ENC_SEC = config.ENC_SEC


bot = commands.Bot(command_prefix=BOT_PREFIX)
bot.remove_command('help')  # removing the default help
