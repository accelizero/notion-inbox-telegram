# notion-inbox-telegram
这是一个简单的程序，可以从 Telegram bot 获取新的消息并将其同步到Notion页面块。

[English](https://github.com/accelizero/notion-inbox-telegram-plugin/blob/master/README.md)

## 准备工作

1. 创建一个 [telegram bot](https://t.me/botfather) 并获取token

2. 创建一个 [notion integrations](https://www.notion.com/my-integrations) 并获取token

3. 创建一个notion数据库并设置页面模板为 `Journal`

4. 从您的Notion数据库右上角 `Add connecttions` 添加连接绑定到第2步创建的integration名字。

5. 浏览器打开Notion数据库并复制database_id `www.notion.so/<username>/<database_id>?v=<view_id>`

6. 在 `config.py` 中配置

    - telegram token

       `TELEGRAM_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`

    - notion integration token

       `NOTION_AUTH = "secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`

    - notion database_id
  
       `NOTION_DATABASE_ID = "xxxxxxxxxxxxxxxxxxxxxxxxx"`

注意: 自定义标签属性和名字、语音转文字等可选参数，请阅读 `config.py` 自行配置。

## Docker部署

1. 安装Docker

    - ubuntu: `sudo apt install docker`
    - centos: `sudo yum install docker-ce`

2. 运行程序

    ``` bash
    docker run -d \
               --name notion-inbox-telegram \
               -e TELEGRAM_TOKEN="" \
               -e NOTION_AUTH="" \
               -e NOTION_DATABASE_ID="" \
               -e TIMEZONE="Asia/Shanghai" \
    accelizero/notion-inbox-telegram:latest
    ```

## 常规部署

1. 安装依赖

    ``` bash
    pip install -r requirements.txt
    ```

2. 快速开始

    ``` bash
    python3 main.py
    ```

将 Telegram 机器人添加到聊天中，然后开始发送消息。

## 功能

1. 将来自 Telegram 的文本、图片、文档、视频笔记和语音消息记录到 Notion 数据库。
2. 自动将语音消息转换为文本（可选，需要百度语音 API）。
3. 管理消息中的链接并将它们添加到 Notion 数据库。

## 注意事项

1. 确保您拥有 Telegram 和 Notion 所需的 API 密钥和令牌。
2. 百度语音 API 是可选的，需要额外配置，并且安装ffmpeg。

## 效果图
![property](https://raw.githubusercontent.com/accelizero/notion-inbox-telegram-plugin/master/property.png)
![demo](https://raw.githubusercontent.com/accelizero/notion-inbox-telegram-plugin/master/demo.png)
