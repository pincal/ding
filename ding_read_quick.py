#!/usr/bin/python
#coding=utf-8

from dingding_sdk import dingapi_timer
from dingding_sdk import user
from dingding_sdk import department
from dingding_sdk import utils
import MySQLdb



def connect_db(address, user, password, database):
    db = MySQLdb.connect(address, user, password, database)
    db.set_character_set('utf8') #修改MySQLdb默认编码
    cursor = db.cursor()
    cursor.execute('SET NAMES utf8;') #修改MySQLdb默认编码
    cursor.execute('SET CHARACTER SET utf8;') #修改MySQLdb默认编码
    cursor.execute('SET character_set_connection=utf8;') #修改MySQLdb默认编码
    return db, cursor



def close_db(db):
    db.close()
    return True




#初始化部门清单
def store_department_list(db, cursor, fetch_child=True, parent_id=1):
    #钉钉获取部门列表的API不会返回根部门，所以手动指定根部门，根部门不能通过API进行修改，所以名称没有意义            
    ding_root_sql = "REPLACE INTO dingding_department_list(`id`, `name`, `parentid`, `createDeptGroup`, `autoAddUser`) \
                        VALUES('1', '中国联合网络通信集团有限公司', '0', '1', '1')"
    cursor.execute(ding_root_sql)
    db.commit()
    #获取根部门以下所有部门清单
    #global result
    is_success, result = department.get_department_list(dingapi_timer.access_token, fetch_child, parent_id)
    #print result #debug only
    if is_success == True:
        for i in range(len(result['department'])):
            ding_read_sql = "REPLACE INTO dingding_department_list(%s) VALUES(%s)" % \
                        (utils.list2string(result['department'][i].keys(), 'keys'),
                         utils.list2string(result['department'][i].values(), 'values') )
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





#根据部门获取人员基本信息，对于具有相同userid的人员记录只存储一次
#确保user_list表没有重复的人员
def store_user_detail(department_id, db, cursor, offset=None, size=None, order=None):
    is_success, result = user.get_department_detail_userlist(dingapi_timer.access_token, department_id, offset, size, order)
    if is_success == True and result != None:
        for i in range(len(result['userlist'])):            
            write_db = "REPLACE INTO dingding_user_detail(%s) VALUES(%s)" % \
                (utils.list2string(result['userlist'][i].keys(), 'keys'), utils.list2string(result['userlist'][i].values(), 'values'))  
            #print write_db #debug only
            try:
                cursor.execute(write_db)
                db.commit()
            except MySQLdb.Warning, w:  
                sqlWarning =  "Warning:%s" % str(w)
                print sqlWarning
            except MySQLdb.Error, e:  
                sqlError =  "Error:%s" % str(e)
                print sqlError





def store_all_user_detail(db, cursor):
    #global db_result #debug only
    cursor.execute("SELECT id FROM dingding_department_list")
    db_result = cursor.fetchall() #获取不含根部门的所有部门id
    if db_result != None and len(db_result) > 0:
        for i in range(len(db_result)):
            store_user_detail(db_result[i][0], db, cursor)
            
    store_user_detail('1', db, cursor)

    



def ding_one_key_store():
    #获取access_token可以全局使用dingapi_timer.access_token
    dingapi_timer.access_token_timer()
    #连接数据库
    ding_db, ding_cursor = connect_db('localhost', 'root', 'yoyoball', 'dingtalk') 
    #获取所有部门基本信息存储在dingding_department_list
    store_department_list(ding_db, ding_cursor, fetch_child=True, parent_id=1)
    #获取所有人员信息人员详情并存储在dingding_user_detail
    store_all_user_detail(ding_db, ding_cursor)
    #断开数据库
    close_db(ding_db)
    return True



                    
#debug only        
#def print_dict(result):
#    for k, v in result.iteritems():
#        print '%s : %s' % (k, v)       

    
#debug only
#本函数完成一键存储和刷新钉钉侧的用户详情和组织详情【对外唯一接口】
#ding_one_key_store()

