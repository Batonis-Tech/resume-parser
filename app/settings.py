import os

from envparse import env
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

    OPENAI_API_KEY: str = env('OPENAI_API_KEY', default='')

    class Config:
        env_file = 'app/.env'


settings = Settings()
