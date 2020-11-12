import discord
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
    BOT_TOKEN = os.environ.get("BOT_TOKEN", False)
    BOT_PREFIX = os.environ.get("BOT_PREFIX", False)
    DB_URI = os.environ.get("DB_URI", False)
    ENC_SEC = os.environ.get("ENC_SEC", None)
    DEC_SEC = os.environ.get("DEC_SEC", None)
    DB_URI = os.environ.get("DATABASE_URL", None)
else:
    import config

    BOT_TOKEN = config.BOT_TOKEN    
    BOT_PREFIX = config.BOT_PREFIX
    ENC_SEC = config.ENC_SEC
    DEC_SEC = config.DEC_SEC
    DB_URI = config.DATABASE_URL


bot = commands.Bot(command_prefix=BOT_PREFIX)
bot.remove_command('help')  # removing the default help

