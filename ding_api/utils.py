#!/usr/bin/env python
# encoding: utf-8

import urllib2
import logging
import json

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

path_log_file = '/tmp/DingAPI.log'
#Windows下会向出错程序所在分区写入日志 | tmp文件夹需要预先手工建立

logger = logging.getLogger('DingAPI')
file_handler = logging.FileHandler(path_log_file)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(funcName)s-->%(levelname)s %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def http_get(url):
    result = -1
    try:
        response = urllib2.urlopen(url, timeout=30)
        result = json.loads(response.read())
    except urllib2.URLError, e:
        logger.error(e)    
    return handle_result(result)


def http_post(url, data):
    result = -1
    headers = {
        "Content-Type": "application/json",
        "Accept-Charset": "utf-8"
    }
    request = urllib2.Request(url, json.dumps(data), headers)
    try:
        response = urllib2.urlopen(request, timeout=30)
        result = json.loads(response.read())
    except urllib2.URLError, e:
        logger.error(e)
    return handle_result(result)


def http_upload(url, data):
    result = -1
    # 在urllib2上注册http流处理句炳
    register_openers()
    # datagen 是一个生成器对象，返回编码过后的参数
    datagen, headers = multipart_encode(data)
    request = urllib2.Request(url, datagen, headers)

    try:
        response = urllib2.urlopen(request, timeout=30)
        result = json.loads(response.read())
    except urllib2.URLError, e:
        logger.error(e)
    return handle_result(result)


def http_download(url, media_file):
    try:
        response = urllib2.urlopen(url, timeout=30)
        media_file.write(response.read())
        media_file.close()
    except urllib2.URLError, e:
        logger.error(e)
        
    return True, 'success'


def handle_result(result):    
    #成功则返回True和结果，否则返回False和错误信息并写入日志
    if result == -1:
        errcode = -1
        errmsg = 'http result is empty!'
        logger.error("Error: %s | %s" % (errcode, errmsg))
        return False, {errcode:errmsg}
    if result.get('errcode') == 0:
        result.pop('errcode')   #删除成功时的固定状态信息errcode=0
        result.pop('errmsg')    #删除成功时的固定状态信息errmsg=ok
        return True, result
    else:
        errcode = result.get('errcode')
        errmsg = result.get('errmsg')
        logger.error("Error: %s | %s" % (errcode, errmsg))
        #return False, errmsg
        return False, {errcode:errmsg} 
        #API调用出错的时候，第二个返回值为一个dict
        #key为错误代码，value为错误信息
        

        
#一个把list处理为string作为sql语句的函数        
def list2string(sqlist, types):
    string=''
    #type为keys表示键，values表示值。键加``值加""。
    if types == 'keys': 
        for i in range(len(sqlist)):
            if i != len(sqlist)-1: #最后一个特殊处理
                if type(sqlist[i]) == bool:
                    string = string + '`%d`,' % sqlist[i]
                elif type(sqlist[i]) == unicode:
                    string = string + '`%s`,'% sqlist[i]
                else:
                    string = string + '`' + str(sqlist[i]) + '`,'
            else:
                if type(sqlist[i]) == bool:
                    string = string + '`%d`' % sqlist[i]
                elif type(sqlist[i]) == unicode:
                    string = string + '`%s`'% sqlist[i]
                else:
                    string = string + '`' + str(sqlist[i]) + '`'        
    elif types == 'values':
        for i in range(len(sqlist)):
            if i != len(sqlist)-1: #最后一个特殊处理
                if type(sqlist[i]) == bool:
                    string = string + '\'%d\',' % sqlist[i]
                elif type(sqlist[i]) == unicode:
                    string = string + '\'%s\','% sqlist[i]
                elif type(sqlist[i]) == dict:
                    string = string + '\'' + json.dumps(sqlist[i], ensure_ascii=False) + '\','
                elif type(sqlist[i]) == list:
                    string = string + '\'[' + list2string(sqlist[i], types='no_wrapper') + ']\','
                else:
                    string = string + '\'' + str(sqlist[i]) + '\', '
            else:
                if type(sqlist[i]) == bool:
                    string = string + '\'%d\'' % sqlist[i]
                elif type(sqlist[i]) == unicode:
                    string = string + '\'%s\''% sqlist[i]
                elif type(sqlist[i]) == dict:
                    string = string + '\'' + json.dumps(sqlist[i], ensure_ascii=False) + '\''
                elif type(sqlist[i]) == list:
                    string = string + '\'[' + list2string(sqlist[i], types='no_wrapper') + ']\''
                else:
                    string = string + '\'' + str(sqlist[i]) + '\''
    elif types == 'no_wrapper':
        for i in range(len(sqlist)):
            if i != len(sqlist)-1: #最后一个特殊处理
                if type(sqlist[i]) == bool:
                    string = string + '%d,' % sqlist[i]
                elif type(sqlist[i]) == unicode:
                    string = string + '%s,' % sqlist[i]
                elif type(sqlist[i]) == dict:
                    string = string + json.dumps(sqlist[i], ensure_ascii=False) + ','
                elif type(sqlist[i]) == list:
                    string = string + list2string(sqlist[i], types='no_wrapper') + ','
                else:
                    string = string + str(sqlist[i]) + ','
            else:
                if type(sqlist[i]) == bool:
                    string = string + '%d' % sqlist[i]
                elif type(sqlist[i]) == unicode:
                    string = string + '%s'% sqlist[i]
                elif type(sqlist[i]) == dict:
                    string = string + json.dumps(sqlist[i], ensure_ascii=False)
                elif type(sqlist[i]) == list:
                    string = string + list2string(sqlist[i], types='no_wrapper')
                else:
                    string = string + str(sqlist[i])
    else:
        string = string + ''
    return string
