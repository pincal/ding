#!/usr/bin/env python
# encoding: utf-8

from urllib import urlencode

from config import API_ADDR
from utils import http_post


def send(access_token, touser, toparty, send_type, content, agentid):
    """
    参数说明
        send_type是一个string，可为text/image/voice/file/link/oa/markdown/action_card中之一
        content是一个dict，最终由http_post函数中的json.dump封装为json格式
        agentid是应用的id号
    """
    url = "https://%s/message/send?" % API_ADDR
    args = {
        "access_token": access_token
    }
    url += urlencode(args)
    data = {
        "touser": touser,
        "toparty": toparty,
        "agentid": agentid,
        "msgtype": send_type,
        send_type: content
    }
    return http_post(url, data)
