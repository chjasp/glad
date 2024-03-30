# msg_processing.py
import logging
from openai import OpenAI
from config.settings import Settings


# --- (1) SETUP --- #

logging.basicConfig(level=logging.INFO,
                    format="%(funcName)s - %(levelname)s - %(message)s")

settings = Settings()
client = OpenAI(api_key=settings.OPENAI_API_KEY)
# db = firestore.Client()


# --- (2) FUNCTIONS --- #

def generate_chatgpt_reply(message: str) -> str:
    logging.info(f">>> USER: \n\t{message}")

    # Change to history
    history_prompt = "Hello, I'm your helpful assistant."

    response = client.chat.completions.create(
        messages=[
            {"role": "assistant", "content": history_prompt},
            {"role": "user", "content": message}
        ],
        model=settings.MODEL_NAME
    )

    if response.choices and len(response.choices) > 0:
        response_msg = response.choices[0].message.content.strip()
    else:
        response_msg = "Sorry, I couldn't generate a response. Please try again."

    logging.info(f">>> {settings.MODEL_NAME}: \n\t{response_msg}")
    return response_msg