from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    api_bot: str = Field(env_prefix = "API_BOT")
    api_client: str =  Field(env_prefix = "API_CLIENT")
    id_assistant: str = Field(env_prefix = "ID_ASSISTANT")

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()

TOKEN_API_BOT = settings.api_bot
TOKEN_API_CLIENT = settings.api_client
ID_ASSISTANT = settings.id_assistant