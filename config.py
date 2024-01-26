import os
import json

# Telegram configuration
TELEGRAM_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Notion configuration
# create an [integration](https://www.notion.com/my-integrations) and find the token.
NOTION_AUTH = "secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# https://www.notion.so/<username>/<database_id>?v=<view_id>
NOTION_DATABASE_ID = "xxxxxxxxxxxxxxxxxxxxxxxxx"

# 标签名称
NOTION_TAG_NAME = "Tags"

# 标签属性
NOTION_TAG_VALUE = "Daily"

# 从环境变量获取
env = os.environ
if env.get("TELEGRAM_TOKEN"):
    TELEGRAM_TOKEN = env.get("TELEGRAM_TOKEN")
if env.get("NOTION_AUTH"):
    NOTION_AUTH = env.get("NOTION_AUTH")
if env.get("NOTION_DATABASE_ID"):
    NOTION_DATABASE_ID = env.get("NOTION_DATABASE_ID")
if env.get("NOTION_TAG_NAME"):
    NOTION_TAG_NAME = env.get("NOTION_TAG_NAME")
if env.get("NOTION_TAG_VALUE"):
    NOTION_TAG_VALUE = env.get("NOTION_TAG_VALUE")

PROXY_URL = ""
proxies = {"http": PROXY_URL, "https": PROXY_URL}
