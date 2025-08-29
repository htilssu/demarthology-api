from logging import Logger
from traceback import print_stack

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.configs.setting import setting
from app.domain.entities.user import User

client = AsyncIOMotorClient(setting.MONGO_URI)
logger = Logger('mongodb')


async def init_db():
    try:
        await init_beanie(database=client.get_database("app"), document_models=[User])
        logger.info("MongoDB initialized successfully")
    except Exception as e:
        print_stack()
        logger.error("mongodb init error: {}".format(e))
        logger.warning("Application will continue without database connection")
