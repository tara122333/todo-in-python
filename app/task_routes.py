from fastapi import APIRouter, status, HTTPException
from schemas import TaskCreate, TaskResponse, TaskUpdate
from task import create_task_db, get_all_task_db, get_task_db, delete_task_db, update_task_db
from typing import Annotated
from fastapi import Depends
from typing import Any
from pymongo.asynchronous.collection import AsyncCollection


task_router = APIRouter(prefix="/task", tags=["Task"])

from db import get_task_collection

Tasks = Annotated[AsyncCollection, Depends(get_task_collection)]

def _task_not_found(task_id: str) -> HTTPException:
  return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task is not found for task id {task_id}")

@task_router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
async def create_task(payload: TaskCreate, task_collection: Tasks) -> dict:
  return await create_task_db(task_collection, payload.model_dump(mode="json"))

@task_router.get("/{task_id}", status_code=status.HTTP_200_OK)
async def get_task(task_id: str, task_collection: Tasks) -> dict:
  task_data = await get_task_db(task_collection, task_id)
  if task_data is None:
    raise _task_not_found(task_id)
  else:
    return task_data

@task_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_task(task_collection: Tasks) -> list[dict[str, Any]]:
  return await get_all_task_db(task_collection)

@task_router.delete("/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(task_id: str, task_collection: Tasks) -> dict:
  task_data = await delete_task_db(task_collection, task_id)
  if task_data is None:
    raise _task_not_found(task_id)
  else:
    return task_data

@task_router.patch("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskResponse)
async def update_task(payload: TaskUpdate, task_id: str, task_collection: Tasks) -> dict:
  payload_fields = payload.model_dump(mode="json", exclude_unset=True)
  task_data = None

  if payload_fields:
    task_data = await update_task_db(task_collection, task_id, payload_fields)
  else:
    task_data = await get_task(task_id, task_collection)
  
  if task_data is None:
    raise _task_not_found()
  else:
    return task_data
