from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    host: str = Field(default="localhost")
    database: str = Field(description="database name")
    username: str
    password: str
    # specifications
    model_config = SettingsConfigDict(env_file=".env")
