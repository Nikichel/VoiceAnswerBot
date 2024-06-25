from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    api_bot: str = Field(env_prefix = "API_BOT")
    api_client: str =  Field(env_prefix = "API_CLIENT")
    id_assistant: str = Field(env_prefix = "ID_ASSISTANT")
    api_amplitude: str = Field(env_prefix = "API_AMPLITUDE")

    DB_HOST: str = Field(env_prefix = "DB_HOST")
    DB_PORT: int = Field(env_prefix = "DB_PORT")
    DB_USER: str = Field(env_prefix = "DB_USER")
    DB_PASS: str = Field(env_prefix = "DB_PASS")
    DB_NAME: str = Field(env_prefix = "DB_NAME")

    REDIS_HOST: str = Field(env_prefix = "REDIS_HOST")
    REDIS_PORT: int = Field(env_prefix = "REDIS_PORT")

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()

TOKEN_API_BOT = settings.api_bot
TOKEN_API_CLIENT = settings.api_client
ID_ASSISTANT = settings.id_assistant
TOKEN_AMPLITUDE = settings.api_amplitude

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT