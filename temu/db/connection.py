from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient

from ..settings.config import settings

uri = settings.DATABASE_URL

client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))

db = client['test-emulator']
collection_orders = db['orders']
