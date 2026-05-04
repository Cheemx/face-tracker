from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_url: str = (
        os.getenv("DATABASE_URI")
    )

settings = Settings()