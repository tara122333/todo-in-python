from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import Field

class AppConfig(BaseSettings):
  mongo_db_uri: str='mongodb://localhost:27017'
  mongo_db_name: str='todo_list'
  app_title: str = 'Tara Todo App'
  version: str = '0.0.1'
  description: str = 'Create, read, update and delete todos stored in MongoDB.'

  jwt_secret: str = "Test_jwt_key"
  jwt_algorithm: str = "HS256"
  jwt_expire_days: int = Field(default=7, ge=1)

@lru_cache
def get_app_config() -> AppConfig:
  return AppConfig()
