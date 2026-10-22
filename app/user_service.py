from fastapi.concurrency import run_in_threadpool
from access_token import hash_password, verify_password, create_user_access_token
from user_schema import UserCreate, UserLogin
from pymongo.asynchronous.collection import AsyncCollection
from user_db import create_user_db, get_user_by_email_db
from fastapi import HTTPException
from config import AppConfig

async def create_user_service(user_collection: AsyncCollection, payload: UserCreate):
  password_hashed = await run_in_threadpool(hash_password, payload.password)
  return await create_user_db(user_collection, name=payload.name, email=payload.email, hashed_pass=password_hashed, status=payload.status)
  
async def login_user_service(user_collection: AsyncCollection, payload: UserLogin, config:AppConfig):
  user_db = await get_user_by_email_db(user_collection, payload.email)
  print(user_db)
  if user_db is None:
    return HTTPException(
      status_code=404,
      detail=f"User not found for email: {payload.email}"
    )
  
  check_password = await run_in_threadpool(verify_password, payload.password, user_db["password_hash"])

  if not check_password:
    return HTTPException(
      status_code=401,
      detail=f"Wrong password for email: {payload.email}"
    )
  
  token, expires_in = create_user_access_token(str(user_db["_id"]), user_db["email"], config)

  return {"access_token": token, "token_type": "bearer", "expires_in": expires_in}
