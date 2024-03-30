# main.py

import logging
import telegram
from config.settings import Settings
from app.utils.msg_processing import generate_chatgpt_reply
from flask import Flask, request, jsonify


# --- (1) SETUP --- #

logging.basicConfig(level=logging.INFO,
                    format="%(funcName)s - %(levelname)s - %(message)s")

settings = Settings()
bot = telegram.Bot(token=settings.TG_TOKEN)
app = Flask(__name__)


# --- (2) ENDPOINTS --- #

@app.route(f"/{settings.TG_TOKEN}", methods=["POST"])
async def respond():
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        logging.info(update)

        if hasattr(update, "message"):
            chat_id = update.message.chat.id
            text = update.message.text
            response_msg = generate_chatgpt_reply(text)
            await bot.send_message(chat_id=chat_id, text=response_msg)
        else:
            logging.info("The update does not contain a text message.")
    except Exception as e:
        logging.error(f"An error has occurred: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

    return jsonify({"status": "success"}), 200


# --- (3) APP STARTUP --- #


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)