#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ssl
import json
import base64
from urllib import request
from urllib import parse
from urllib.request import urlopen

def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')

    text = json.loads(pubsub_message)
    print(text)
    ssl._create_default_https_context = ssl._create_unverified_context
    if text['status'] == 'SUCCESS':
        build_time = text['finishTime'] - text['startTime']
        message = "專案：" + text['substitutions']['REPO_NAME'] + "\n建置分支：" + text['substitutions']['BRANCH_NAME'] + "\nCOMMIT：" + text['substitutions']['SHORT_SHA'] + "\n建置結果：" + text['status'] + "\n花費時間：" + build_time
    elif text['status'] == 'QUEUED':
        message = "專案：" + text['substitutions']['REPO_NAME'] + "\n建置分支：" + text['substitutions']['BRANCH_NAME'] + "\nCOMMIT：" + text['substitutions']['SHORT_SHA'] + "\n於" + text['createTime'] +  "等待建置"
    elif text['status'] == 'WORKING':
        message = "專案：" + text['substitutions']['REPO_NAME'] + "\n建置分支：" + text['substitutions']['BRANCH_NAME'] + "\nCOMMIT：" + text['substitutions']['SHORT_SHA'] + "\n於" + text['startTime'] +  "開始建置"


    values = {"method": "sendMessage", "chat_id":"<CHAT_ID>", "text": message}
    data = parse.urlencode(values).encode('utf-8')
    url = 'https://api.telegram.org/bot<TG_BOT_TOKEN>/'
    req = request.Request(url, data)
    res = urlopen(req)
    print(res.read().decode())

