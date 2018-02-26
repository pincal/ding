#!/usr/bin/python
#coding=utf-8

from dingding_sdk import dingapi_timer
from dingding_sdk import user
from dingding_sdk import department
from dingding_sdk import utils
import MySQLdb
import os
import threading
import math
from multiprocessing import Process, Pool, Queue


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
def store_department_list(fetch_child=True, parent_id=1):
    db, cursor = connect_db('localhost', 'root', 'yoyoball', 'dingtalk')
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
    db.close()
    return True



def store_department_detail(department_id):
    db, cursor = connect_db('localhost', 'root', 'yoyoball', 'dingtalk')
    is_success, result = department.get_department_detail(dingapi_timer.access_token, department_id)
    #print result #debug only
    if is_success == True and department_id != 1:  #id为1的为根部门，根部门钉钉不会返回parentid,在数据库中将根部门的parentid设置为0
        ding_read_sql = "REPLACE INTO dingding_department_list(`id`, `name`, `parentid`, `createDeptGroup`, `autoAddUser`) \
                        VALUES('%s', '%s', '%s', '%d', '%d')" % \
                        (result['id'], result['name'], result['parentid'], result['createDeptGroup'], result['autoAddUser'])
    else:
        ding_read_sql = "REPLACE INTO dingding_department_list(`id`, `name`, `parentid`, `createDeptGroup`, `autoAddUser`) \
                        VALUES('%s', '%s', '%s', '%d', '%d')" % \
                        (result['id'], result['name'], '0', result['createDeptGroup'], result['autoAddUser'])    

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
    db.close()
    return True


#根据部门获取人员基本信息，对于具有相同userid的人员记录只存储一次
#确保user_list表没有重复的人员
def store_user_detail(department_id, offset=None, size=None, order=None):
    db, cursor = connect_db('localhost', 'root', 'yoyoball', 'dingtalk')
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
    db.close()
    return True



def ding_one_key_store():             
    #获取access_token可以全局使用dingapi_timer.access_token
    dingapi_timer.access_token_timer()
    #连接数据库
    ding_db, ding_cursor = connect_db('localhost', 'root', 'yoyoball', 'dingtalk')
    #钉钉获取部门列表的API不会返回根部门，所以手动指定根部门，根部门不能通过API进行修改，所以名称没有意义            
    ding_root_sql = "REPLACE INTO dingding_department_list(`id`, `name`, `parentid`, `createDeptGroup`, `autoAddUser`) \
                        VALUES('1', '中国联合网络通信集团有限公司', '0', '1', '1')"
    ding_cursor.execute(ding_root_sql)
    ding_db.commit()    
    
    #获取根部门的所有直接下级id
    for i in range(5):
        status, class1_result = department.get_sub_dept_id_list(dingapi_timer.access_token, 1)
        if status == True:
            break
        if i == 4 and status == False:
            #print 'error' #debug only 
            return -1
    #print class1_result['sub_dept_id_list'] #debug only

        
##    #使用子进程获取根部门直接下级的组织清单
##    for i in range(len(class1_result['sub_dept_id_list'])):
##        store_department_detail(class1_result['sub_dept_id_list'][i])
##    department_pool = Pool()
##    for i in range(len(class1_result['sub_dept_id_list'])):
##        department_pool.apply_async(store_department_list, args=(True, class1_result['sub_dept_id_list'][i]))
##    department_pool.close()
##    department_pool.join()
##    #使用子进程获取所有人员详情
##    user_pool = Pool()
##    ding_dept_num_sql = "SELECT count(*) FROM dingtalk.dingding_department_list;"
##    ding_cursor.execute(ding_dept_num_sql)
##    ding_dept_num = ding_cursor.fetchone()
##    print ding_dept_num #debug only
##    if ding_dept_num == None:
##        return -2
##    group_factor = 10.0 #设定分组单位，需要小数位为零
##    group_number = int(math.ceil(ding_dept_num[0] / group_factor)) 
##    for i in range(group_number):        
##        ding_dept_group_sql = "SELECT `id` FROM dingtalk.dingding_department_list limit %s,%s;" % (int(i*group_factor), int((i+1)*group_factor-1))
##        print ding_dept_group_sql #debug only
##        ding_cursor.execute(ding_dept_group_sql)
##        dept_group = ding_cursor.fetchall()
##        for j in range(len(dept_group)):
##            user_pool.apply_async(store_user_detail, args=(class1_result['sub_dept_id_list'][j]))
##    user_pool.close()
##    user_pool.join()




    #多线程获取部门清单
    for i in range(len(class1_result['sub_dept_id_list'])):
        store_department_detail(class1_result['sub_dept_id_list'][i])
    for i in range(len(class1_result['sub_dept_id_list'])):
        #thread.start_new_thread(store_department_list, (True, class1_result['sub_dept_id_list'][i]))
        dept_thread = threading.Thread(target=store_department_list, args=(True, class1_result['sub_dept_id_list'][i]))
        dept_thread.start()
        dept_thread.join()

       
    #多线程获取人员详情
    ding_dept_num_sql = "SELECT count(*) FROM dingtalk.dingding_department_list;"
    ding_cursor.execute(ding_dept_num_sql)
    ding_dept_num = ding_cursor.fetchone()
    print ding_dept_num #debug only
    if ding_dept_num == None:
        return -2
    group_factor = 10.0#设定分组单位，需要小数位为零
    group_number = int(math.ceil(ding_dept_num[0] / group_factor)) 
    for i in range(group_number):        
        ding_dept_group_sql = "SELECT `id` FROM dingtalk.dingding_department_list limit %s,%s;" % (int(i*group_factor), int((i+1)*group_factor-1))
        print ding_dept_group_sql #debug only
        ding_cursor.execute(ding_dept_group_sql)
        dept_group = ding_cursor.fetchall()
        for j in range(len(dept_group)):
            #thread.start_new_thread(store_user_detail, (dept_group[j][0],))
            user_thread = threading.Thread(target=store_user_detail, args=(dept_group[j][0],))
            user_thread.start()
            user_thread.join()


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

