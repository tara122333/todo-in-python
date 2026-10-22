from task import _now
from pymongo.asynchronous.collection import AsyncCollection
from typing import Any, Optional

def _serialize(doc: dict[str, Any]) -> dict[str, Any]:
  return {
    "id": str(doc["_id"]),
    "name": doc["name"],
    "password": "*********",
    "status": doc["status"],
    "created_at": doc["created_at"],
    "updated_at": doc["updated_at"],
  }


async def create_user_db(
  user_collection: AsyncCollection,
  *,
  email: str,
  hashed_pass: str,
  name: str,
  status: str,
) -> dict[str, Any]:
  doc = {
    "email": email,
    "name": name,
    "password_hash": hashed_pass,
    "status": status,
    "created_at": _now(),
    "updated_at": _now()
  }
  result = await user_collection.insert_one(doc)
  doc["_id"] = result.inserted_id
  return _serialize(doc)

async def get_user_by_email_db(
  user_collection: AsyncCollection,
  email: str,
) -> Optional[dict[str, Any]]:
  return await user_collection.find_one({ "email": email })