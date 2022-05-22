import requests
import random
from hashlib import md5
import re
import sys
import os
import json


def make_md5(s: str, encoding='utf-8') -> str:
    return md5(s.encode(encoding)).hexdigest()


def add_item(items: list, item_value: str, item_title: str) -> None:
    item = {
        'arg': item_value,
        'title': item_value,
        'subtitle': item_title,
        'icon': ''
    }
    items.append(item)


endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

appid = os.getenv("appid")
appkey = os.getenv("appkey")
query = sys.argv[1]
from_lang = 'auto'
to_lang = 'zh'
if re.search(r"[\u4e00-\u9fa5]+", query):
    to_lang = "en"
salt = random.randint(32768, 65536)
sign = make_md5(appid + query + str(salt) + appkey)
payload = {
    'appid': appid,
    'q': query,
    'from': from_lang,
    'to': to_lang,
    'salt': salt,
    'sign': sign
}

headers = {'Content-Type': 'application/x-www-form-urlencoded'}

r = requests.post(url, params=payload, headers=headers)
result = r.json()

items = []
add_item(items, result["trans_result"][0]["dst"],
         result["trans_result"][0]["src"])
print(json.dumps({'items': items}))
