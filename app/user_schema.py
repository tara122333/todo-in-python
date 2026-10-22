from pydantic import BaseModel, EmailStr, Field, field_validator
from enum import Enum

def _clean_email(value: str) -> str:
  return value.strip().lower()

def _clear_name(value: str) -> str:
  value = " ".join(value.split())
  if not value:
    raise ValueError("Name required...")
  return value

def _check_password_bytes(value: str) -> str:
  if len(value.encode("utf-8")) > 72:
      raise ValueError("Password must be at most 72 bytes.")
  return value


class UserStatus(str, Enum):
  ACTIVE = 'active'
  IN_ACTIVE = 'in_active'

class UserCreate(BaseModel):
  email: EmailStr = Field(examples=["tara@gmail.com"])
  status: UserStatus = UserStatus.ACTIVE
  name: str = Field(min_length=1, max_length=100, examples=["Tara Chand"])
  password: str = Field(min_length=6, max_length=128, examples=["1234567890"])

  _email = field_validator("email")(_clean_email)
  _name = field_validator("name")(_clear_name)
  _password = field_validator("password")(_check_password_bytes)

class UserLogin(BaseModel):
  email: EmailStr = Field(examples=["tara@gmail.com"])
  password: str = Field(min_length=6, max_length=128, examples=["1234567890"])

  _email = field_validator("email")(_clean_email)
  _password = field_validator("password")(_check_password_bytes)
