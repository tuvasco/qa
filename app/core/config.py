from pydantic_settings import BaseSettings
from pydantic import AnyUrl

class Settings(BaseSettings):
    database_url: AnyUrl
app_host: str = "0.0.0.0"
app_port: int = 8000


class Config:
    env_file = ".env"

settings = Settings()
