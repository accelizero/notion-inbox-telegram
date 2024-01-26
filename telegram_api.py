import os
from uuid import uuid1
import requests
from notion_api import insert
from speech import speech
from config import TELEGRAM_TOKEN, SPEECH_TO_TEXT, proxies

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_file_path(file_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile?file_id={file_id}"
    r = requests.get(url, proxies=proxies)
    return r.json()["result"]["file_path"]

def get_file_url(file_path):
    url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"
    return url

def speech_to_text(file_url):
    r = requests.get(file_url, proxies=proxies)
    filename1 = str(uuid1()) + ".oga"
    filename2 = str(uuid1()) + ".wav"
    with open(filename1, "wb") as f:
        f.write(r.content)
    os.system(f"ffmpeg -i {filename1} -ar 16000 {filename2}")
    # 拆分超过50秒的视频，以适应短语音接口
    os.system(f"ffmpeg -i {filename2} -f segment -segment_time 50 -c copy {filename2}_%03d.wav")
    file_list = [i for i in os.listdir("./")if f"{filename2}_" in i]
    file_list.sort()
    text = ""
    for filename in file_list:
        text += " " + speech(filename)
        os.remove(filename)
    os.remove(filename1)
    os.remove(filename2)
    return text

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
        if SPEECH_TO_TEXT:
            text = speech_to_text(file_url)
        insert(text, file_type, file_url, link_list)
    else:
        insert(text, link_list=link_list)
