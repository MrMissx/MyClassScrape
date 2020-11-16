import asyncio

from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient, AgnosticDatabase, AgnosticCollection

from bot import LOGGER, DB_URI

LOGGER.info("Conecting to Database...")

CLIENT: AgnosticClient = AsyncIOMotorClient(DB_URI)
RUN = asyncio.get_event_loop().run_until_complete

if "MyClassScrape" in RUN(CLIENT.list_database_names()):
    LOGGER.info("Conected to Database")
else:
    LOGGER.info("Database Not Found, Creating New...")

DB: AgnosticDatabase = CLIENT["MyClassScrape"]


def get_collection(name: str) -> AgnosticCollection:
    """ Get Collection from Database """
    return DB[name]
