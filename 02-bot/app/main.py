# main.py

from telegram import Update, Bot
import asyncio
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from config.settings import Settings
from app.utils.msg_processing import generate_chatgpt_reply

settings = Settings()

def main():
    application = Application.builder().token(settings.TG_TOKEN).build()

    start_handler = CommandHandler("start", start)
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, process_message)

    application.add_handler(start_handler)
    application.add_handler(message_handler)

    application.run_polling()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your health bot.")

async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    response_message = await generate_chatgpt_reply(user_message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response_message)

if __name__ == "__main__":
    main()
