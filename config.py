from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    api_bot: str = Field(env_prefix = "API_BOT")
    api_assistant: str =  Field(env_prefix = "API_ASSISTANT")

settings = Settings()

TOKEN_API_BOT = settings.api_bot
TOKEN_API_ASSISTANT = settings.api_assistant