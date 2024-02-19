import os
from uuid import uuid1
import requests
from notion_api import insert
from config import TELEGRAM_TOKEN, proxies

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_file_path(file_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile?file_id={file_id}"
    r = requests.get(url, proxies=proxies)
    return r.json()["result"]["file_path"]

def get_file_url(file_path):
    url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"
    return url

def process_telegram_message(message):
    print(message)
    text = message.get("text", "") or message.get("caption", "")
    link_list = []
    if message.get("entities") or message.get("caption_entities"):
        for item in message.get("entities") or message.get("caption_entities"):
            if item.get("url"):
                link_list.append((item['offset'],item['offset']+item['length'],text[item['offset']:item['offset']+item['length']],item['url']))
    if message.get("document"):
        file_type = message["document"]["mime_type"]
        file_id = message["document"]["file_id"]
        file_url = get_file_url(get_file_path(file_id))
        insert(text, file_type, file_url, link_list)
    elif message.get("photo"):
        file_type = "image/jpeg"
        file_id = message["photo"][-1]["file_id"]
        file_url = get_file_url(get_file_path(file_id))
        insert(text, file_type, file_url, link_list)
    elif message.get("video_note"):
        file_type = "video/mp4"
        file_id = message["video_note"]["file_id"]
        file_url = get_file_url(get_file_path(file_id))
        insert(text, file_type, file_url, link_list)
    elif message.get("voice"):
        file_type = "audio/ogg"
        file_id = message["voice"]["file_id"]
        file_url = get_file_url(get_file_path(file_id))
        insert(text, file_type, file_url, link_list)
    else:
        insert(text, link_list=link_list)
