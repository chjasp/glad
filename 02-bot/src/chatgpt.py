from os import getenv
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

dispatcher = Dispatcher()

TG_TOKEN = getenv("TG_TOKEN")
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
MODEL_NAME = getenv("MODEL_NAME")

client = OpenAI(
    api_key=OPENAI_API_KEY
)

class Reference:
    def __init__(self) -> None:
        self.response = ""

reference = Reference()

def clear_past():
    reference.response = ""

@dispatcher.message(Command("start"))
async def welcome(message: types.Message):
    clear_past()
    await message.reply(f"Hi {message.from_user.first_name}!\nWelcome to Gulch!")

@dispatcher.message(Command("clear"))
async def clear(message: types.Message) -> None:
    clear_past()
    await message.reply("I have cleared past information.")

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
    print(f">>> USER: \n\t{message.text}")

    response = client.chat.completions.create(
    messages=[
            {"role": "assistant", "content": reference.response},
            {"role": "user", "content": message.text}
        ],
        model=MODEL_NAME
        )
    # Adjusting the response extraction according to the new API struture
    if response.choices and len(response.choices) > 0:
        print(response.choices[0])
        response_msg = response.choices[0].message.content.strip()
    else:
        response_msg = "Sorry, I couldn't generate a response. Please try again."

    print(f">>> {MODEL_NAME}: \n\t{response_msg}")
    reference.response += f"\n{message.text}\n{response_msg}"  # Adjusted to append both the user message and the bot response
    await message.reply(response_msg)
async def main() -> None:
    bot = Bot(TG_TOKEN)
    # Listen to incoming requests from the Telegram bot and forward them to the dispatcher
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())