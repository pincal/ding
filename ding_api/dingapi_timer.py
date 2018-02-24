#!/usr/bin/env python
# encoding: utf-8
import time
import threading
import auth
import config


#程序启动时直接调用access_token_timer函数
#在需要token的地方直接使用dingapi.access_token即可
#每隔100分钟刷新一次，刷新失败则暂停5分钟再刷新
def access_token_timer():
    global at_timer
    global access_token
    at_timer = threading.Timer(6000, access_token_timer)
    at_timer.start()
    
    is_success, result = auth.get_access_token(config.CorpID, config.Secret)
    if is_success == True:
        access_token = result.get('access_token')
        expires_in = result.get('expires_in')
        #print access_token #debug only
    else:
        sleep(300)
        #print 'sleep' #debug only