from logging import Logger
from traceback import print_stack

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.configs.setting import setting
from app.models.user import User

client = AsyncIOMotorClient(setting.MONGO_URI)
logger = Logger("mongodb")


async def init_db():
    try:
        await init_beanie(database=client.get_database("app"), document_models=[User])
    except Exception as e:
        print_stack()
        logger.error("mongodb init error: {}".format(e))
