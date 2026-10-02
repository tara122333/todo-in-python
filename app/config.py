from pydantic_settings import BaseSettings
from functools import lru_cache

class AppConfig(BaseSettings):
  mongo_db_uri: str='mongodb://localhost:27017'
  mongo_db_name: str='todo_list'
  app_title: str = 'Tara Todo App'
  version: str = '0.0.1'
  description: str = 'Create, read, update and delete todos stored in MongoDB.'

@lru_cache
def get_app_config() -> AppConfig:
  return AppConfig()
