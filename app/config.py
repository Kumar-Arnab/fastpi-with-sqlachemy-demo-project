from pydantic import BaseSettings

class Settings(BaseSettings):
  database_hostname: str
  database_port: str
  database_password: str
  database_name: str
  database_username: str
  database_type: str
  secret_key: str
  algorithm: str
  access_token_expire_minutes: int

  # telling pydantic to import from .env file
  class Config:
    env_file = ".env"


settings = Settings()