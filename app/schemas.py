from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from enum import Enum
from typing import Optional

class TaskStatus(str, Enum):
  ACTIVE = 'active'
  COMPLETED = 'completed'
  DELETED = 'deleted'

def _clean_title(value: str) -> str:
  value = value.strip()
  if not value:
      raise ValueError("Title cannot be blank.")
  return value

def _clean_description(value: Optional[str]) -> Optional[str]:
  if value is None:
      return None
  value = value.strip()
  return value or None

class TaskCreate(BaseModel):
  title: str = Field(min_length=1, max_length=200, examples=["Buy milk"])
  description: Optional[str] = Field(default=None, max_length=2000, examples=["2 litres"])
  status: TaskStatus = TaskStatus.ACTIVE

  _title = field_validator("title")(_clean_title)
  _description = field_validator("description")(_clean_description)

class TaskResponse(BaseModel):
  id: str = Field(examples=["665f1c2e9d6a4b4c0f9a7e1b"])
  title: str
  description: Optional[str] = None
  status: TaskStatus
  created_at: datetime
  updated_at: datetime
