from motor.motor_asyncio import AsyncIOMotorClient
from . import Config
from . import Bot as app
mongo_client = AsyncIOMotorClient(Config.MONGO_URI)

db = mongo_client['Lundgrow']
user_collection = db["users"]
special_user_collection = db["spusers"]
group_collection = db["groups"]
blacklist_chat = db["blchats"]
blacklist_user = db["blusers"]
