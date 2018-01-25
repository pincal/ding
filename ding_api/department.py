#!/usr/bin/env python
# encoding: utf-8

from urllib import urlencode

from config import API_ADDR
from utils import http_get, http_post


def get_department_list(access_token, fetch_child=True, parentid=1):
    url = 'https://%s/department/list?' % API_ADDR
    args = {
        'access_token': access_token,
        'fetch_chiild': fetch_child,
        'id': parentid
    }
    url += urlencode(args)
    return http_get(url)
 
 
def get_department_detail(access_token, departmentid):
    url = 'https://%s/department/get?' % API_ADDR
    args = {
        'access_token': access_token,
        'id': departmentid

    }
    url += urlencode(args)
    return http_get(url)    


def create_department(access_token, name, parentid, order=None, createDeptGroup=None,
                            deptHiding=None, deptPermits=None, userPermits=None,
                            outerDept=None, outerPermitDepts=None, outerPermitUsers=None):
    url = 'https://%s/department/create?' % API_ADDR
    args = {
        'access_token': access_token
    }
    url += urlencode(args)
    data = {
        'name': name,
        'parentid': parentid
    }
    
    if order != None:
        data['order'] = order
    if createDeptGroup != None:
        data['createDeptGroup'] = createDeptGroup
    if deptHiding != None:
        data['deptHiding'] = deptHiding
    if deptPermits != None:
        data['deptPermits'] = deptPermits        
    if userPermits != None:
        data['userPermits'] = userPermits
    if outerDept != None:
        data['outerDept'] = outerDept
    if outerPermitDepts != None:
        data['outerPermitDepts'] = outerPermitDepts
    if outerPermitUsers != None:
        data['outerPermitUsers'] = outerPermitUsers 
        
    #print data #debug only            
    return http_post(url, data)

    
def create_department_kw(access_token, name, parentid, **kw):
    url = 'https://%s/department/create?' % API_ADDR
    args = {
        'access_token': access_token
    }
    url += urlencode(args)
    data = {
        'name': name,
        'parentid': parentid
    }
    data = dict(data, **kw)
        
    #print data #debug only            
    return http_post(url, data)    
    

def update_department(access_token, departmentid, name=None, parentid=None, order=None, 
                            createDeptGroup=None, deptHiding=None, deptPermits=None,
                            userPermits=None, outerDept=None, outerPermitDepts=None,
                            outerPermitUsers=None, autoAddUser=None, deptManagerUserList=None,
                            orgDeptOwner=None):
    url = 'https://%s/department/update?' % API_ADDR
    args = {
        'access_token': access_token
    }
    url += urlencode(args)
    data = {
        'id': departmentid
    }
    
    if name != None:
        data['name'] = name
    if parentid != None:
        data['parentid'] = parentid
    if order != None:
        data['order'] = order
    if createDeptGroup != None:
        data['createDeptGroup'] = createDeptGroup
    if deptHiding != None:
        data['deptHiding'] = deptHiding
    if deptPermits != None:
        data['deptPermits'] = deptPermits        
    if userPermits != None:
        data['userPermits'] = userPermits
    if outerDept != None:
        data['outerDept'] = outerDept
    if outerPermitDepts != None:
        data['outerPermitDepts'] = outerPermitDepts
    if outerPermitUsers != None:
        data['outerPermitUsers'] = outerPermitUsers          
    if autoAddUser != None:
        data['autoAddUser'] = autoAddUser
    if deptManagerUserList != None:
        data['deptManagerUserList'] = deptManagerUserList
    if orgDeptOwner != None:
        data['orgDeptOwner'] = orgDeptOwner
        
    #print data #debug only
    return http_post(url, data)

    
def update_department_kw(access_token, departmentid, **kw):
    url = 'https://%s/department/update?' % API_ADDR
    args = {
        'access_token': access_token
    }
    url += urlencode(args)
    data = {
        'id': departmentid
    }
    
    data = dict(data, **kw)

    #print data #debug only
    return http_post(url, data)    
    

def delete_department(access_token, departmentid):
    url = 'https://%s/department/delete?' % API_ADDR
    args = {
        'access_token': access_token,
        'id': departmentid
    }
    url += urlencode(args)
    return http_get(url)

    
def get_parent_depts_by_dept(access_token, departmentid):
    url = 'https://%s/department/list_parent_depts_by_dept?' % API_ADDR
    args = {
        'access_token': access_token,
        'id': departmentid
    }
    url += urlencode(args)
    return http_get(url)
    
    
def get_parent_depts_by_user(access_token, user_id):
    url = 'https://%s/department/list_parent_depts?' % API_ADDR
    args = {
        'access_token': access_token,
        'userId': user_id
    }
    url += urlencode(args)
    return http_get(url)