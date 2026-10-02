from fastapi import FastAPI, status
from config import get_app_config
from db import create_mongo_client, TODOS_COLLECTION
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pymongo import DESCENDING

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app_config = get_app_config()
    client = create_mongo_client(app_config)
    await client.admin.command("ping")  # fail fast if MongoDB is unreachable
    db = client[app_config.mongo_db_name]
    await db[TODOS_COLLECTION].create_index([("created_at", DESCENDING)])
    app.state.db = db
    try:
        yield
    finally:
        await client.close()

app_config = get_app_config()
app = FastAPI(
  title=app_config.app_title,
  version=app_config.version,
  description=app_config.description,
  lifespan=lifespan,
)


@app.get("/", include_in_schema=False)
def server():
  return {
    "status": "Ok",
    "message": "Server running successfully",
    "data": app_config
  }

@app.get('/health', status_code=status.HTTP_200_OK)
def server_health():
  return {
    "status": "Ok",
    "message": "Server health is ok"
  }
