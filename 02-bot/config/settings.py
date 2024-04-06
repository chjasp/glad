from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    TG_TOKEN: str = Field(..., env="TG_TOKEN")
    OPENAI_API_KEY: str = Field(..., env="OPENAI_KEY")
    MODEL_NAME: str = Field(..., env="GPT_MODEL_NAME")
