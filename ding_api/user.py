#!/usr/bin/env python
# encoding: utf-8

from urllib import urlencode

from config import API_ADDR
from utils import http_get, http_post


def get_user(access_token, userid):
    url = 'https://%s/user/get?' % API_ADDR
    args = {
        'access_token': access_token,
        'userid': userid
    }
    url += urlencode(args)
    return http_get(url)


def create_user(access_token, userid, name, department, mobile, email=None,
                          position=None, jobnumber=None, extattr=None, orderInDepts=None,
                          tel=None, workPlace=None, remark=None, isHide=None,
                          isSenior=None):
    url = 'https://%s/user/create?' % API_ADDR
    args = {
        'access_token': access_token
    }
    url += urlencode(args)
    data = {
        'name': name,
        'department': department,
        'mobile': mobile
    }
    
    if (userid != None) and (userid != ''):
        data['userid'] = userid
    if email != None:
        data['email'] = email
    if position != None:
        data['position'] = position
    if jobnumber != None:
        data['jobnumber'] = jobnumber    
    if extattr != None:
        data['extattr'] = extattr    
    if orderInDepts != None:
        data['orderInDepts'] = orderInDepts
    if tel != None:
        data['tel'] = tel
    if workPlace != None:
        data['workPlace'] = workPlace
    if remark != None:
        data['remark'] = remark    
    if isHide != None:
        data['isHide'] = isHide 
    if isSenior != None:
        data['isSenior'] = isSenior    
    
    #print data #该print为调试接口时用    
    return http_post(url, data)

    
def create_user_kw(access_token, userid, name, department, mobile, **kw):
    url = 'https://%s/user/create?' % API_ADDR
    args = {
        'access_token': access_token
    }
    url += urlencode(args)
    data = {
        'name': name,
        'department': department,
        'mobile': mobile
    }
    data = dict(data, **kw) #合并data和kw两个dict
    
    #print data #该print为调试接口时用    
    return http_post(url, data)    
    

#如果所有参数都放在data中，就会有问题
#如果只更新某个人的1个信息，也要传递这人的所有信息。否则未传递的会被清空。
#例如用户经有workplace，但本次更新只更新邮件，结果没有传递workplace，导致workplace被清空。
#因此data中只有必须参数，并加入if判断补充额外参数    
# def update_user(access_token, userid, name, department=None, mobile=None, email=None,
                          # position=None, jobnumber=None, extattr=None, orderInDepts=None,
                          # tel=None, workPlace=None, remark=None, isHide=None,
                          # isSenior=None):
    # url = 'https://%s/user/update?' % API_ADDR
    # args = {
        # 'access_token': access_token
    # }
    # url += urlencode(args)
    # data = {
        # 'userid': userid,
        # 'name': name,
        # 'department': department,
        # 'mobile': mobile,
        # 'email': email,
        # 'position': position,
        # 'jobnumber': jobnumber,
        # 'extattr': extattr,
        # 'orderInDepts': orderInDepts,
        # 'tel': tel,
        # 'workPlace': workPlace,
        # 'remark': remark,
        # 'isHide': isHide,
        # 'isSenior': isSenior
    # }
       
    #print data #该print为调试接口时用
    # return http_post(url, data)    
    
    
def update_user(access_token, userid, name, department=None, mobile=None, email=None,
                          position=None, jobnumber=None, extattr=None, orderInDepts=None,
                          tel=None, workPlace=None, remark=None, isHide=None,
                          isSenior=None):
    url = 'https://%s/user/update?' % API_ADDR
    args = {
        'access_token': access_token
    }
    url += urlencode(args)
    data = {
        'userid': userid,
        'name': name
    }
    
    if department != None:
        data['department'] = department
    if mobile != None:
        data['mobile'] = mobile
    if email != None:
        data['email'] = email
    if position != None:
        data['position'] = position
    if jobnumber != None:
        data['jobnumber'] = jobnumber    
    if extattr != None:
        data['extattr'] = extattr    
    if orderInDepts != None:
        data['orderInDepts'] = orderInDepts
    if tel != None:
        data['tel'] = tel
    if workPlace != None:
        data['workPlace'] = workPlace
    if remark != None:
        data['remark'] = remark    
    if isHide != None:
        data['isHide'] = isHide 
    if isSenior != None:
        data['isSenior'] = isSenior
        
    #print data #该print为调试接口时用
    return http_post(url, data)

    
#kw为需要更新的人的信息，只需要传入需要修改的部分。例如：
#update_user_kw(access_token, u'135680', u'测试',email=u'test@test.com',position=u'职位3')
def update_user(access_token, userid, name, **kw):
    url = 'https://%s/user/update?' % API_ADDR
    args = {
        'access_token': access_token
    }
    url += urlencode(args)
    data = {
        'userid': userid,
        'name': name
    }
    data = dict(data, **kw) #合并data和kw两个dict
    
    #print data #该print为调试接口时用
    return http_post(url, data)
    

def delete_user(access_token, userid):
    url = 'https://%s/user/delete?' % API_ADDR
    args = {
        'access_token': access_token,
        'userid': userid
    }
    url += urlencode(args)
    return http_get(url)


def delete_user_list(access_token, useridlist):
    url = 'https://%s/user/batchdelete?' % API_ADDR
    args = {
        'access_token': access_token
    }
    url += urlencode(args)
    data = {
        'access_token': access_token,
        'useridlist': useridlist
    }
    return http_post(url, data)


def get_department_simple_userlist(access_token, department_id,
                                   offset=None, size=None, order=None):
    url = 'https://%s/user/simplelist?' % API_ADDR
    args = {
        'access_token': access_token,
        'department_id': department_id
    }
    # 可选分页参数处理
    if offset != None:
        args['offset'] = offset
    if size != None:
        args['size'] = size
    if order != None:
        args['order'] = order

    url += urlencode(args)
    return http_get(url)


def get_department_detail_userlist(access_token, department_id,
                                   offset=None, size=None, order=None):
    url = 'https://%s/user/list?' % API_ADDR
    args = {
        'access_token': access_token,
        'department_id': department_id
    }
    # 可选分页参数处理
    if offset != None:
        args['offset'] = offset
    if size != None:
        args['size'] = size
    if order != None:
        args['order'] = order

    url += urlencode(args)
    return http_get(url)