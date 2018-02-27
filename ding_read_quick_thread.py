#!/usr/bin/python
#coding=utf-8

from dingding_sdk import dingapi_timer
from dingding_sdk import user
from dingding_sdk import department
from dingding_sdk import utils
import MySQLdb
import threadpool
import math
import logging


path_log_file = '/tmp/ding_read.log'
#Windows下会向出错程序所在分区写入日志 | tmp文件夹需要预先手工建立

logger = logging.getLogger('DingRead')
file_handler = logging.FileHandler(path_log_file)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(funcName)s-->%(levelname)s %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



def connect_db(address, user, password, database):
    for i in range(10):
        try:
            db = MySQLdb.connect(address, user, password, database)
            db.set_character_set('utf8') #修改MySQLdb默认编码
            cursor = db.cursor()
            cursor.execute('SET NAMES utf8;') #修改MySQLdb默认编码
            cursor.execute('SET CHARACTER SET utf8;') #修改MySQLdb默认编码
            cursor.execute('SET character_set_connection=utf8;') #修改MySQLdb默认编码
        except MySQLdb.Warning, w:  
            sqlWarning =  "Warning:%s" % str(w)
            print sqlWarning
        except MySQLdb.Error, e:  
            sqlError =  "Error:%s" % str(e)
            print sqlError
        else:
            break
    return db, cursor



def close_db(db):
    for i in range(10):
        try:
            db.close()
        except MySQLdb.Warning, w:  
            sqlWarning =  "Warning:%s" % str(w)
            print sqlWarning
        except MySQLdb.Error, e:  
            sqlError =  "Error:%s" % str(e)
            print sqlError
        else:
            break            
    return True



#初始化部门清单
def store_department_list(access_token, fetch_child=True, parent_id=1):
    db, cursor = connect_db('localhost', 'root', 'yoyoball', 'dingtalk')
    #global result
    for i in range(5):
        is_success, result = department.get_department_list(access_token, fetch_child, parent_id)
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
            break
        else:
            logging_message = {'access_token':access_token, 'fetch_child':fetch_child, 'parent_id':parent_id}
            logger.error(logging_message)
    db.close()
    return True
    
    
    
def store_department_detail(access_token, department_id):
    db, cursor = connect_db('localhost', 'root', 'yoyoball', 'dingtalk')
    for i in range(5):
        is_success, result = department.get_department_detail(access_token, department_id)
        #print result #debug only
        if is_success == True:
            if department_id != 1:  #id为1的为根部门，根部门钉钉不会返回parentid,在数据库中将根部门的parentid设置为0
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
            break
        else:
            logging_message = {'access_token':access_token, 'department_id':department_id}
            logger.error(logging_message)           
    db.close()
    return True


    
#根据部门获取人员基本信息，对于具有相同userid的人员记录只存储一次
#确保user_list表没有重复的人员
def store_user_detail(access_token, department_id, offset=None, size=None, order=None):
    db, cursor = connect_db('localhost', 'root', 'yoyoball', 'dingtalk')
    for i in range(5):
        is_success, result = user.get_department_detail_userlist(access_token, department_id, offset, size, order)
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
            break
        else:
            logging_message = {'access_token':access_token, 'department_id':department_id, 'offset':offset, 'size':size, 'order':order}
            logger.error(logging_message)             
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
        else:
            logging_message = {'Function':'get_sub_dept_id_list', 'access_token':access_token, 'department_id':department_id}
            logger.error(logging_message)             
        if i == 4 and status == False:
            #print 'error' #debug only 
            return -1
    #print class1_result['sub_dept_id_list'] #debug only


##    #threading多线程获取部门清单
##    for i in range(len(class1_result['sub_dept_id_list'])):
##        store_department_detail(dingapi_timer.access_token, ding_db, ding_cursor, class1_result['sub_dept_id_list'][i])
##    for i in range(len(class1_result['sub_dept_id_list'])):
##        #thread.start_new_thread(store_department_list, (True, class1_result['sub_dept_id_list'][i]))
##        dept_thread = threading.Thread(target=store_department_list, args=(dingapi_timer.access_token, True, class1_result['sub_dept_id_list'][i]))
##        dept_thread.start()
##        dept_thread.join()

       
##    #threading多线程获取人员详情
##    ding_dept_num_sql = "SELECT count(*) FROM dingtalk.dingding_department_list;"
##    ding_cursor.execute(ding_dept_num_sql)
##    ding_dept_num = ding_cursor.fetchone()
##    print ding_dept_num #debug only
##    if ding_dept_num == None:
##        return -2
##    group_factor = 25.0#设定分组单位，需要小数位为零
##    group_number = int(math.ceil(ding_dept_num[0] / group_factor)) 
##    for i in range(group_number):        
##        ding_dept_group_sql = "SELECT `id` FROM dingtalk.dingding_department_list limit %s,%s;" % (int(i*group_factor), int((i+1)*group_factor-1))
##        print ding_dept_group_sql #debug only
##        ding_cursor.execute(ding_dept_group_sql)
##        dept_group = ding_cursor.fetchall()
##        for j in range(len(dept_group)):
##            #thread.start_new_thread(store_user_detail, (dept_group[j][0],))
##            user_thread = threading.Thread(target=store_user_detail, args=(dingapi_timer.access_token, dept_group[j][0]))
##            user_thread.start()
##        user_thread.join()




    #threadpool多线程获取部门清单
    for i in range(len(class1_result['sub_dept_id_list'])):
        store_department_detail(dingapi_timer.access_token, class1_result['sub_dept_id_list'][i])
    department_pool = threadpool.ThreadPool(25)
    for i in range(len(class1_result['sub_dept_id_list'])):
        dict_vars = {'access_token':dingapi_timer.access_token, 'fetch_child':True, 'parent_id':class1_result['sub_dept_id_list'][i]}
        func_vars = [(None, dict_vars)]
        requests = threadpool.makeRequests(store_department_list, func_vars)
        [department_pool.putRequest(req) for req in requests]
    department_pool.wait()



    #threadpool多线程获取人员详情
    user_pool = threadpool.ThreadPool(50)
        
    ding_dept_num_sql = "SELECT count(*) FROM dingtalk.dingding_department_list;"
    ding_cursor.execute(ding_dept_num_sql)
    ding_dept_num = ding_cursor.fetchone()
    print 'The number of departments is %d' % ding_dept_num #debug only
    if ding_dept_num == None:
        return -2
    group_factor = 100#设定分组单位，必须为整数，目前计划为100或者25
    group_number = int(math.ceil(float(ding_dept_num[0]) / group_factor))
    #print float(ding_dept_num[0]), group_number
    for i in range(group_number):        
        ding_dept_group_sql = "SELECT `id` FROM dingtalk.dingding_department_list limit %s,%s;" % (i*group_factor, group_factor)
        print ding_dept_group_sql #debug only
        ding_cursor.execute(ding_dept_group_sql)
        dept_group = ding_cursor.fetchall()
        for j in range(len(dept_group)): #len(dept_group)除去最后一个group都应该等于group_factor
            dict_vars = {'access_token':dingapi_timer.access_token, 'department_id':dept_group[j][0]}
            func_vars = [(None, dict_vars)]
            requests = threadpool.makeRequests(store_user_detail, func_vars)
            [user_pool.putRequest(req) for req in requests]
        user_pool.wait()

     
        
        

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

