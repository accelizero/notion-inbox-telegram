# notion-inbox-telegram
telegram机器人无压输入同步notion插件

## 准备工作

1. 创建一个 [telegram bot](https://t.me/botfather) 并获取token

2. 创建一个 [notion integrations](https://www.notion.com/my-integrations) 并获取token

3. 创建一个notion数据库并设置页面模板为 `Journal`

4. 从您的Notion数据库右上角 `Add connecttions` 添加连接绑定到第2步创建的integration名字。

5. 浏览器打开Notion数据库并复制database_id `www.notion.so/<username>/<database_id>?v=<view_id>`

## Docker部署

1. 安装Docker

    - ubuntu: `sudo apt install docker`
    - centos: `sudo yum install docker-ce`

2. 运行程序（填入准备工作获取的token等信息）

    ``` bash
    docker run -d \
               --name notion-inbox-telegram \
               -e TELEGRAM_TOKEN="" \
               -e NOTION_AUTH="" \
               -e NOTION_DATABASE_ID="" \
               -e NOTION_TAG_NAME="Tags" \
               -e NOTION_TAG_VALUE="日常" \
               -e TIMEZONE="Asia/Shanghai" \
    accelizero/notion-inbox-telegram:latest
    ```

## 命令行部署

1. 安装依赖

    ``` bash
    pip install -r requirements.txt
    ```

2. 在 `config.py` 中配置

    - telegram token

       `TELEGRAM_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`

    - notion integration token

       `NOTION_AUTH = "secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`

    - notion database_id
  
       `NOTION_DATABASE_ID = "xxxxxxxxxxxxxxxxxxxxxxxxx"`

   - notion标签属性
       `NOTION_TAG_NAME` = "Tags"

   - notion标签名字
       `NOTION_TAG_VALUE ` = "日常"

3. 运行程序

    ``` bash
    python3 main.py
    ```

## 使用

将 Telegram 机器人添加到聊天中，然后无压输入即可。

## 功能

1. 将来自 Telegram 的文本、图片、文档、视频笔记和语音消息记录到 Notion 数据库（notion api还不支持上传，填入的telegram资源链接会过期，所以还是尽量文本记录吧）。
2. 管理消息中的链接并将它们添加到 Notion 数据库。

## 注意事项

1. 确保您拥有 Telegram 和 Notion 所需的 API 密钥和令牌。

## 效果图
![property](https://raw.githubusercontent.com/accelizero/notion-inbox-telegram-plugin/master/property.png)
![demo](https://raw.githubusercontent.com/accelizero/notion-inbox-telegram-plugin/master/demo.png)
