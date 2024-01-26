import base64
import hashlib
import json
import requests
import time
from config import SPEECH_API_KEY, SPEECH_SECRET_KEY

def fetch_token() -> str:
    # 获取百度语音 API token
    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}".format(
        SPEECH_API_KEY, SPEECH_SECRET_KEY
    )
    response = requests.get(auth_url)
    json_data = response.json()
    return json_data["access_token"]

def speech(file: str) -> str:
    token = fetch_token()
    # 百度语音识别 API
    url = "https://vop.baidu.com/server_api"
    with open(file, "rb") as f:
        speech_data = f.read()

    # 语音文件编码
    speech_base64 = base64.b64encode(speech_data)
    # 文件长度
    speech_len = len(speech_data)
    # 计算签名
    sign_data = "{}{}{}{}".format(SPEECH_API_KEY, int(time.time()), hashlib.md5(speech_data).hexdigest(), SPEECH_SECRET_KEY)
    sign = hashlib.md5(sign_data.encode()).hexdigest()

    headers = {"Content-Type": "application/json"}
    data = {
        "format": "wav",
        "rate": 16000,
        "dev_pid": 1537,  # 1537表示普通话，有声音识别模型，您可以根据需要更改
        "channel": 1,
        "token": token,
        "cuid": "123456PYTHON",
        "len": speech_len,
        "speech": speech_base64.decode(),
        "sign": sign
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    json_data = response.json()

    # 检查错误码，返回识别结果
    if json_data["err_no"] == 0:
        return json_data["result"][0]
    else:
        return "Error: {}".format(json_data["err_msg"])

