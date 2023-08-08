#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/8/20 9:57 PM
# @Author  : eric_chou
# @Description  : webhooks
import json
import time

import requests


def update_info(item):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=4' \
          'e7efd808756ac25dbf7bcd0619081601883cb9278a8958d02b43d2a0954cf5c'
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "今日更新",
            "text": "#### 今日更新\n" +
                    "> " + item['name'] + "\n\n" +
                    "> ![screenshot](" + item['imgUrl'] + ")\n" +
                    "> ###### Bt爬虫于 " + str(time.strftime("%H:%M:%S")) + "爬取 [详情](" + item['url'] + ") \n"
        }
    }
    requests.post(url=url, data=json.dumps(data), headers=headers)
