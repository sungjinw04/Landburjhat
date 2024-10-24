import logging
from pyrogram import Client, idle
from motor.motor_asyncio import AsyncIOMotorClient
from .config import OWNER_ID, DEV_ID, TOKEN, MONGO_URI, SUPPORT, SUPPORT_CHANNEL, API_ID, API_HASH, BOTLOGS, BOT_USERNAME

class Config:
    OWNER_ID = OWNER_ID
    DEV_ID = DEV_ID
    TOKEN = TOKEN
    MONGO_URI = MONGO_URI
    SUPPORT = SUPPORT
    SUPPORT_CHANNEL = SUPPORT_CHANNEL
    API_ID = API_ID
    API_HASH = API_HASH
    BOTLOGS = BOTLOGS
    BOT_USERNAME = BOT_USERNAME

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


Bot = Client(
    "lundgrow_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.TOKEN
)
