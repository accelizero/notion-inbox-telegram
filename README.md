# notion-inbox-telegram
This is simple program that get new messages from Telegram bot and sync its to notion page block.

[中文](https://github.com/accelizero/notion-inbox-telegram-plugin/blob/main/README_ZH.md) | [English](https://github.com/accelizero/notion-inbox-telegram-plugin/blob/main/README.md)

## Prepare

1. Create a [telegram bot](https://t.me/botfather) and get the token

2. Create a [notion integrations](https://www.notion.com/my-integrations) and get token

3. Create a notion database and set the page template to `Journal`

4. From the upper right corner of your Notion database `Add connections` add connection bindings to the integration name created in step 2.

5. The browser opens the Notion database and copies the database_id `www.notion.so/<username>/<database_id>?v=<view_id>`

6. Configure in `config.py`

     - telegram token

        `TELEGRAM_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`

     - notion integration token

        `NOTION_AUTH = "secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`

     - notion database_id
  
        `NOTION_DATABASE_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxx"`

Note: For optional parameters such as custom tag attributes and names, speech-to-text, etc., please read `config.py` to configure it yourself.

## Run in Docker

1. Install Docker

     - ubuntu: `sudo apt install docker`
     - centos: `sudo yum install docker-ce`

2. Run the program

  ``` bash
  docker run -d \
              --name notion-inbox-telegram \
              -e TELEGRAM_TOKEN="" \
              -e NOTION_AUTH="" \
              -e NOTION_DATABASE_ID="" \
              -e TIMEZONE="Asia/Shanghai" \
  accelizero/notion-inbox-telegram:latest
  ```

## Run in System

1. Install dependencies

  ``` bash
  pip install -r requirements.txt
  ```

2. Quick start

  ``` bash
  python3 main.py
  ```

Add the Telegram bot to a chat and start sending messages.

## Features

1. Log text, images, documents, video notes, and voice messages from Telegram to a Notion database.
2. Automatically convert voice messages to text (optional, requires Baidu Speech API).
3. Manage links in messages and add them to the Notion database.

## Note

1. Make sure you have the required API keys and tokens for Telegram and Notion.
2. The Baidu Speech API is optional and requires additional configuration, and install ffmpeg.

## Screenshots
![property](https://github.com/accelizero/notion-inbox-telegram-plugin/raw/main/property.png)
![demo](https://github.com/accelizero/notion-inbox-telegram-plugin/raw/main/demo.png)
