import requests
import time
from typing import Dict, Any, List
from config import TELEGRAM_TOKEN, proxies
from telegram_api import process_telegram_message

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_message(chat_id: int, text: str) -> None:
    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
    }
    requests.post(url, data=data, proxies=proxies)

def handle_updates(updates: List[Dict[str, Any]]) -> None:
    for update in updates:
        message = update.get("message", {})
        text = message.get("text")
        if text != "/start":
            process_telegram_message(message)

def main() -> None:
    last_update_id = None

    while True:
        url = f"{BASE_URL}/getUpdates"
        params = {"timeout": 600}

        if last_update_id is not None:
            params["offset"] = last_update_id + 1

        response = requests.get(url, params=params, proxies=proxies)
        updates = response.json().get("result", [])

        if updates:
            handle_updates(updates)
            last_update_id = updates[-1]["update_id"]

        time.sleep(60)

if __name__ == "__main__":
    main()
