import os
import time
import pytz
import requests
from notion_client import Client
import datetime
from typing import Dict, Any, List
from config import NOTION_AUTH, NOTION_DATABASE_ID, NOTION_TAG_NAME, NOTION_TAG_VALUE

# Initialize Notion client
notion = Client(auth=NOTION_AUTH)
# Define database ID
database_id = NOTION_DATABASE_ID

WEEKDAYS_DICT: Dict[str, str] = {
    "Monday": "周一",
    "Tuesday": "周二",
    "Wednesday": "周三",
    "Thursday": "周四",
    "Friday": "周五",
    "Saturday": "周六",
    "Sunday": "周日",
}


def get_page(page_title: str) -> Dict[str, Any]:
    """
    Retrieve a page from the database with the given title.

    :param page_title: The title of the page to be retrieved.
    :return: A dictionary containing information about the existing page.
    """
    existing_page = notion.databases.query(
        **{
            "database_id": database_id,
            "filter": {
                "property": "title",
                "title": {
                    "equals": page_title
                }
            }
        }
    )
    return existing_page


def create_page(page_title: str, tag_value: str, tag_name: str = "tag") -> None:
    """
    Create a new page in the database with the specified title and tag.

    :param page_title: The title of the new page.
    :param tag_value: The value of the tag to be added to the new page.
    :param tag_name: The name of the tag property. Default is "tag".
    """
    new_page = {
        "title": {
            "title": [{"text": {"content": page_title}}]
        },
        tag_name: {"multi_select": [{"name": tag_value}]},
    }
    new_page_content = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": page_title,
                        }
                    }
                ]
            }
        }
    ]
    notion.pages.create(parent={"database_id": database_id}, properties=new_page, children=new_page_content)


def get_page_content(page_id: str) -> Dict[str, Any]:
    """
    Retrieve the content of a page with the given page_id.

    :param page_id: The ID of the page whose content is to be retrieved.
    :return: A dictionary containing information about the page's content.
    """
    content = notion.blocks.children.list(page_id)
    return content


def append_page(block_id: str, text: str, file_type: str, file_url: str, link_list: List[tuple]) -> None:
    new_block = [{"object": "block","type": "paragraph", "paragraph":{"rich_text": [{"type": "text","text":{"content":""}}]}},
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": text,
                        }
                    }
                ]
            }
        }]
    if link_list:
        last_start = 0
        last_end = 0
        new_block[1]["bulleted_list_item"]["rich_text"] = [{"type": "text","text": {"content":text.split(' - ')[0] + " - "}}]
        text = ' - '.join(text.split(' - ')[1:])
        for start,end,content,url in link_list:
            new_block[1]["bulleted_list_item"]["rich_text"].append({"type": "text","text": {"content": text[last_end:start]}})
            new_block[1]["bulleted_list_item"]["rich_text"].append({"type": "text","text": {"content": content,"link":{"url":url}}})
            last_end = end
        new_block[1]["bulleted_list_item"]["rich_text"].append({"type": "text","text": {"content": text[last_end:]}})

    if file_url:
        #file_content = requests.get(file_url).content
        #uploaded_file = notion.files.upload(file_content)
        if "image" in file_type:
            new_block.append({
                "object": "block",
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {
                        "url": file_url
                    }
                }
            })
        elif "video" in file_type:
            new_block.append({
                "object": "block",
                "type": "video",
                "video": {
                    "type": "external",
                    "external": {
                        "url": file_url
                    }
                }
            })
        elif "audio" in file_type:
            new_block.append({
                "object": "block",
                "type": "audio",
                "audio": {
                    "type": "external",
                    "external": {
                        "url": file_url
                    }
                }
            })
        else:
            new_block.append({
                "object": "block",
                "type": "file",
                "file": {
                    "type": "external",
                    "external": {
                        "url": file_url
                    }
                }
            })
    notion.blocks.children.append(block_id, children=new_block, after=False)


def update_block(existing_page: Dict[str, Any], text: str, file_type: str, file_url: str, link_list: List[tuple]) -> None:
    page_id = existing_page["results"][0]["id"]
    content = get_page_content(page_id)
    block_id = content["results"][-1]["id"]
    append_page(block_id, text, file_type, file_url, link_list)


def insert(text: str, file_type: str = "", file_url: str = "", link_list: List[tuple]=[]) -> None:
    tag_name = NOTION_TAG_NAME
    tag_value = NOTION_TAG_VALUE
    if os.environ.get("TIMEZONE"):
        tz = pytz.timezone(os.environ["TIMEZONE"])
        now = datetime.datetime.now(tz)
    else:
        now = datetime.datetime.now()
    ctime = now.strftime("%H:%M")
    text = f"{ctime} - {text}" if text else ctime
    current_date = now.strftime("%Y-%m-%d")
    weekday = WEEKDAYS_DICT[now.strftime("%A")]
    page_title = f"{current_date} {weekday}"
    existing_page = get_page(page_title)
    if not existing_page["results"]:
        create_page(page_title, tag_value, tag_name)
        existing_page = get_page(page_title)
    update_block(existing_page, text, file_type, file_url, link_list)


if __name__ == "__main__":
    insert("你感觉怎么样")
