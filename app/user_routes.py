from fastapi import APIRouter, status, Depends, HTTPException
from typing import Annotated, Optional
from pymongo.asynchronous.collection import AsyncCollection
from user_schema import UserCreate, UserLogin
from pymongo.errors import DuplicateKeyError
from user_service import create_user_service, login_user_service
from config import AppConfig, get_app_config

user_router = APIRouter(prefix="/user", tags=["User"])

from db import get_user_collection

Users = Annotated[AsyncCollection, Depends(get_user_collection)]
Config = Annotated[AppConfig, Depends(get_app_config)]

@user_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, user_collection: Users):
  try:
    return await create_user_service(user_collection, payload)
  except DuplicateKeyError:
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail="Email is already registered"
    ) from None

@user_router.post("/login")
async def login_user(payload: UserLogin, user_collection: Users, config: Config):
  return await login_user_service(user_collection, payload, config)
