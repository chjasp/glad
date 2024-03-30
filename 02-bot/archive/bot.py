import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseSettings
from google.cloud import firestore

### (1) SETUP ###

logging.basicConfig(level=logging.INFO,
                    format="%(funcName)s - %(levelname)s - %(message)s")

load_dotenv()


class Settings(BaseSettings):
    TG_TOKEN: str
    OPENAI_API_KEY: str
    MODEL_NAME: str


settings = Settings()
client = OpenAI(api_key=settings.OPENAI_API_KEY)
dispatcher = Dispatcher()
db = firestore.Client()

### (2) CHAT HISTORY ###


class Reference:
    def __init__(self) -> None:
        self.response = ""


reference = Reference()


def clear_past():
    reference.response = ""

### (3) ROUTES  ###


@dispatcher.message(Command("start"))
async def welcome(message: types.Message):
    clear_past()
    await message.reply(f"Hi {message.from_user.first_name}!\nWelcome to Gulch!")


@dispatcher.message(Command("clear"))
async def clear(message: types.Message) -> None:
    clear_past()
    await message.reply("I have cleared past information.")


@dispatcher.message(Command["set_wakeup"])
async def set_wakeup_time(message: types.Message):
    wakeup_time = message.text.split(" ")[1]

    doc_ref = db.collection("users").document(str(message.from_user.id))



@dispatcher.message(Command("help"))
async def help(message: types.Message) -> None:
    help_msg = """
    Hi there, I'm Gulch. Please use the followings commands:
    \n/start - to start the conversion
    \n/clear - to clear the past conversation and context
    \n/help - to get help from the menu (was just used)
    """
    await message.reply(help_msg)


@dispatcher.message()
async def chatgpt(message: types.Message) -> None:
    logging.info(f">>> USER: \n\t{message.text}")

    history_prompt = "Hello, I'm your helpful assistant."

    response = client.chat.completions.create(
        messages=[
            {"role": "assistant", "content": history_prompt},
            {"role": "user", "content": message.text}
        ],
        model=settings.MODEL_NAME
    )

    if response.choices and len(response.choices) > 0:
        logging.info(response.choices[0])
        response_msg = response.choices[0].message.content.strip()
    else:
        response_msg = "Sorry, I couldn't generate a response. Please try again."

    logging.info(f">>> {settings.MODEL_NAME}: \n\t{response_msg}")
    await message.reply(response_msg)

### (4) START LISTENING PROCESS ###


async def main() -> None:
    bot = Bot(settings.TG_TOKEN)
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
