"""MongoDB connection helpers."""

from fastapi import Request
from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection

from config import AppConfig

TASKS_COLLECTION = "task_list"
USER_COLLECTION = "user"

def create_mongo_client(app_config: AppConfig) -> AsyncMongoClient:
  return AsyncMongoClient(app_config.mongo_db_uri, serverSelectionTimeoutMS=5000, tz_aware=True)

def get_task_collection(request: Request) -> AsyncCollection:
  return request.app.state.db[TASKS_COLLECTION]

def get_user_collection(request: Request) -> AsyncCollection:
  return request.app.state.db[USER_COLLECTION]
