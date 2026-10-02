"""MongoDB connection helpers."""

from fastapi import Request
from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection


from config import AppConfig

TODOS_COLLECTION = "task_list"

def create_mongo_client(app_config: AppConfig) -> AsyncMongoClient:
  return AsyncMongoClient(app_config.mongo_db_uri, serverSelectionTimeoutMS=5000, tz_aware=True)

def get_todos_collection(request: Request) -> AsyncCollection:
    """FastAPI dependency returning the ``todos`` collection opened at startup."""
    return request.app.state.db[TODOS_COLLECTION]
