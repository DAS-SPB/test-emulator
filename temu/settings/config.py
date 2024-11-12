import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


def load_environment():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    if os.getenv("TEST_ENV") == "True":
        env_file_path = os.path.join(project_root, '.env_test')
    else:
        env_file_path = os.path.join(project_root, '.env')

    load_dotenv(env_file_path, override=True)


load_environment()


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    model_config = SettingsConfigDict()


settings = Settings()
