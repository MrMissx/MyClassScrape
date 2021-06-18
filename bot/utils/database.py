"""Database moudle."""

from motor.core import AgnosticClient, AgnosticCollection, AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from bot import DB_URI, LOGGER

LOGGER.info("Conecting to Database...")

CLIENT: AgnosticClient = AsyncIOMotorClient(DB_URI)

DB: AgnosticDatabase = CLIENT["MyClassScrape"]


def get_collection(name: str) -> AgnosticCollection:
    """Get Collection from Database."""
    return DB[name]
