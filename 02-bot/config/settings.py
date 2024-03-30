from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    TG_TOKEN: str = Field(..., env="TG_TOKEN")
    OPENAI_API_KEY: str = Field(..., env="OPENAI_KEY")
    MODEL_NAME: str = Field(..., env="GPT_MODEL_NAME")

# https://api.telegram.org/bot{my_bot_token}/setWebhook?url={url_to_send_updates_to}