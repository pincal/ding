#!/usr/bin/python
#coding=utf-8

from dingding_sdk import dingapi_timer
from dingding_sdk import user
from dingding_sdk import department
from dingding_sdk import utils
import MySQLdb


dingapi_timer.access_token_timer()

db = MySQLdb.connect('localhost','root','yoyoball','test')
db.set_character_set('utf8') #修改MySQLdb默认编码
cursor= db.cursor()
cursor.execute('SET NAMES utf8;') #修改MySQLdb默认编码
cursor.execute('SET CHARACTER SET utf8;') #修改MySQLdb默认编码
cursor.execute('SET character_set_connection=utf8;') #修改MySQLdb默认编码


#初始化部门清单
def read_department_list_first():
    is_success, result = department.get_department_list(dingapi_timer.access_token)
    #print result #debug only
    if is_success == True:
        for i in range(len(result['department'])):
            ding_read_sql = "INSERT INTO dingding_department_list(id, \
                        name, parentid, createDeptGroup, autoAddUser) \
                        VALUES('%d', '%s', '%d', '%d', '%d')" % \
                        (result['department'][i]['id'],
                         result['department'][i]['name'],
                         result['department'][i]['parentid'],
                         result['department'][i]['createDeptGroup'],
                         result['department'][i]['autoAddUser'])
            #print ding_read_sql #debug only
            try:
                cursor.execute(ding_read_sql)
                db.commit()
            except MySQLdb.Warning, w:  
                sqlWarning =  "Warning:%s" % str(w)
                print sqlWarning
            except MySQLdb.Error, e:  
                sqlError =  "Error:%s" % str(e)
                print sqlError
            
def read_department_detail_first(departmentid):
    is_success, result = department.get_department_detail(dingapi_timer.access_token, departmentid)
    #print result #debug only
    if is_success == True and departmentid != 1:  #id为1的为根部门，根部门钉钉不会返回parentid
        ding_read_sql = "INSERT INTO dingding_department_detail(id, name, \
                        parentid, orders, createDeptGroup, autoAddUser, deptHiding, \
                        deptPermits, userPermits, outerDept, outerPermitDepts, \
                        outerPermitUsers, orgDeptOwner, deptManagerUseridList) \
                        VALUES('%d', '%s', '%d', '%d', '%d', '%d', '%d', '%s', '%s', '%d', '%s', '%s', '%s', '%s')" % \
                        (result['id'], result['name'], result['parentid'], result['order'],
                         result['createDeptGroup'], result['autoAddUser'], result['deptHiding'],
                         result['deptPerimits'], result['userPerimits'], result['outerDept'],
                         result['outerPermitDepts'], result['outerPermitUsers'],
                         result['orgDeptOwner'], result['deptManagerUseridList'])
    else:
        ding_read_sql = "INSERT INTO dingding_department_detail(id, name, \
                        orders, createDeptGroup, autoAddUser, deptHiding, \
                        deptPermits, userPermits, outerDept, outerPermitDepts, \
                        outerPermitUsers, orgDeptOwner, deptManagerUseridList) \
                        VALUES('%d', '%s', '%d', '%d', '%d', '%d', '%s', '%s', '%d', '%s', '%s', '%s', '%s')" % \
                        (result['id'], result['name'], result['order'],
                         result['createDeptGroup'], result['autoAddUser'], result['deptHiding'],
                         result['deptPerimits'], result['userPerimits'], result['outerDept'],
                         result['outerPermitDepts'], result['outerPermitUsers'],
                         result['orgDeptOwner'], result['deptManagerUseridList'])        

        print ding_read_sql #debug only
        try:
            cursor.execute(ding_read_sql)
            db.commit()
        except MySQLdb.Warning, w:  
            sqlWarning =  "Warning:%s" % str(w)
            print sqlWarning
        except MySQLdb.Error, e:  
            sqlError =  "Error:%s" % str(e)
            print sqlError

    
    
db.close()
