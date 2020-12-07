"""Database moudle."""

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient, AgnosticDatabase, AgnosticCollection

from bot import LOGGER, DB_URI

LOGGER.info("Conecting to Database...")

CLIENT: AgnosticClient = AsyncIOMotorClient(DB_URI)

DB: AgnosticDatabase = CLIENT["MyClassScrape"]


def get_collection(name: str) -> AgnosticCollection:
    """Get Collection from Database."""
    return DB[name]
