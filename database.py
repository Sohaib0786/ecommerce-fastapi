import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")  # fallback
client = AsyncIOMotorClient(MONGO_URL)
db = client.ecommerce
