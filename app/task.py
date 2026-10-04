from typing import Any
from pymongo.asynchronous.collection import AsyncCollection
from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId
from schemas import TaskStatus
from pymongo import ReturnDocument

def _now() -> datetime:
    now = datetime.now(timezone.utc)
    return now.replace(microsecond=(now.microsecond // 1000) * 1000)

def _serialize(doc: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(doc["_id"]),
        "title": doc["title"],
        "description": doc.get("description"),
        "status": doc["status"],
        "created_at": doc["created_at"],
        "updated_at": doc["updated_at"],
    }

def _object_id(todo_id: str) -> Optional[ObjectId]:
  return ObjectId(todo_id) if ObjectId.is_valid(todo_id) else None


async def create_task_db(task_collection: AsyncCollection, data: dict[str, Any]) -> dict[str, Any]:
    now = _now()
    doc = {**data, "created_at": now, "updated_at": now}
    result = await task_collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return _serialize(doc)

async def get_all_task_db(task_collection: AsyncCollection) -> list[dict[str, Any]]:
    cursor = task_collection.find()
    all_task = []
    async for doc in cursor:
        all_task.append(_serialize(doc))
    return all_task

async def get_task_db(task_collection: AsyncCollection, task_id: str) -> Optional[dict[str, Any]]:
    valid_task_id = _object_id(task_id)
    if valid_task_id is None:
        return None
    docs = await task_collection.find_one({"_id": valid_task_id})
    return _serialize(docs) if docs else None

async def delete_task_db(task_collection: AsyncCollection, task_id: str) -> Optional[dict[str, Any]]:
    valid_task_id = _object_id(task_id)
    if valid_task_id is None:
        return None
    docs = await task_collection.find_one_and_update(
        {"_id": valid_task_id, "status": [TaskStatus.ACTIVE, TaskStatus.COMPLETED]},
        { "$set": { "status": TaskStatus.DELETED, "updated_at": _now()}},
        return_document=ReturnDocument.AFTER,
    )
    return _serialize(docs) if docs else None
