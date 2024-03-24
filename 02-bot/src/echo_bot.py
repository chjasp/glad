import sys
from os import getenv
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

load_dotenv()

TG_TOKEN = getenv("TG_TOKEN")
logging.basicConfig(level=logging.INFO)
dp = Dispatcher()

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm Gulch.")

@dp.message()
async def echo(message: types.Message):
    await message.answer(message)

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TG_TOKEN, parse_mode=ParseMode.HTML)
    # Listen to incoming requests from the Telegram bot and forward them to the dispatcher
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())