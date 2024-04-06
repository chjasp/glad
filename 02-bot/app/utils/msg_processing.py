# msg_processing.py

import logging
import aiohttp
import json
from config.settings import Settings
from google.cloud import firestore
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(funcName)s - %(levelname)s - %(message)s")
settings = Settings()

async def generate_chatgpt_reply(message: str) -> str:
    logging.info(f">>> USER: \n\t{message}")
    response_msg = await fetch_openai_response(message)
    logging.info(f">>> {settings.MODEL_NAME}: \n\t{response_msg}")
    return response_msg

async def fetch_openai_response(message: str) -> str:
    data = {
        "model": settings.MODEL_NAME,
        "messages": [
            {"role": "assistant", "content": "Hello, I'm your helpful assistant."},
            {"role": "user", "content": message}
        ]
    }
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        response = await post_request(session, 'https://api.openai.com/v1/chat/completions', data, headers)
        return process_openai_response(response)

async def post_request(session, url: str, data, headers) -> dict:
    async with session.post(url, data=json.dumps(data), headers=headers) as response:
        if response.status == 200:
            return await response.json()
        else:
            await handle_http_error(response)
            return {}

async def handle_http_error(response):
    error_content = await response.text()
    logging.error(f"OpenAI API request failed with status {response.status}: {error_content}")

def process_openai_response(response_json: dict) -> str:
    if response_json.get('choices') and len(response_json['choices']) > 0:
        return response_json['choices'][0]['message']['content'].strip()
    else:
        return "Sorry, I couldn't generate a response. Please try again."