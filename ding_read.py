#!/usr/bin/python
#coding=utf-8

from dingding_sdk import dingapi_timer
from dingding_sdk import user
from dingding_sdk import department
from dingding_sdk import utils
import MySQLdb

#获取access_token
dingapi_timer.access_token_timer()

#连接数据库
db = MySQLdb.connect('localhost','root','yoyoball','dingtalk')
db.set_character_set('utf8') #修改MySQLdb默认编码
cursor= db.cursor()
cursor.execute('SET NAMES utf8;') #修改MySQLdb默认编码
cursor.execute('SET CHARACTER SET utf8;') #修改MySQLdb默认编码
cursor.execute('SET character_set_connection=utf8;') #修改MySQLdb默认编码




#初始化部门清单
def store_department_list(fetch_child=True, parent_id=1):
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

          
def store_department_detail(department_id):
    is_success, result = department.get_department_detail(dingapi_timer.access_token, department_id)
    #print result #debug only
    if is_success == True and department_id != 1:  #id为1的为根部门，根部门钉钉不会返回parentid,在数据库中将根部门的parentid设置为0
        ding_read_sql = "REPLACE INTO dingding_department_detail(%s) VALUES(%s)" % \
                        (utils.list2string(result.keys(), 'keys'), utils.list2string(result.values(), 'values'))
    else:
        ding_read_sql = "REPLACE INTO dingding_department_detail(%s, `parentid`) VALUES(%s, '0')" % \
                        (utils.list2string(result.keys(), 'keys'), utils.list2string(result.values(), 'values'))      

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
   

def store_all_department_detail():
    store_department_detail(1) #获取根部门详情
    cursor.execute("SELECT id FROM dingding_department_list")
    result = cursor.fetchall() #获取根部门以下所有部门id
    #print type(result), len(result), result #debug only 讨厌返回了一个二级的tuple
    if result != None and len(result) > 0:
        for i in range(len(result)):
            if result[i][0] != 1: #这个应该始终为真。因为department_list不应该有id=1的条目。主要是防止写重复id时出错
                store_department_detail(result[i][0]) #获取根部门以下所有部门详情
    
#一键获取所有部门的所有数据
def department_one_key_store():
    store_department_list(fetch_child=True, parent_id=1)
    store_all_department_detail()

#根据部门获取人员基本信息，对于具有相同userid的人员记录只存储一次
#确保user_list表没有重复的人员
def store_user_list(department_id, offset=None, size=None, order=None):
    is_success, result = user.get_department_simple_userlist(dingapi_timer.access_token, department_id, offset, size, order)
    if is_success == True and result['userlist'] != None and len(result['userlist']) > 0:
        for i in range(len(result['userlist'])):
            check_db = "SELECT userid FROM dingding_user_list WHERE userid=%s" % result['userlist'][i]['userid']
            cursor.execute(check_db) #确保不会出现重复主键，当然也可以去直接写，捕获错误。
            db_result = cursor.fetchone()
            if db_result == None: #查询为空时返回NONE 
                write_db = "REPLACE INTO dingding_user_list(userid, name) VALUES('%s', '%s')" % \
                (result['userlist'][i]['userid'], result['userlist'][i]['name'])
                #print sql #debug only
                try:
                    cursor.execute(write_db)
                    db.commit()
                except MySQLdb.Warning, w:  
                    sqlWarning =  "Warning:%s" % str(w)
                    print sqlWarning
                except MySQLdb.Error, e:  
                    sqlError =  "Error:%s" % str(e)
                    print sqlError
            else:
                continue

#获取用户详情           
def store_user_detail(user_id): #钉钉有一些userid为0开始的，所以userid视为字符串
    is_success, result = user.get_user(dingapi_timer.access_token, user_id)
    #global result
    #print result
    if is_success == True and result != None:
        write_db = "REPLACE INTO dingding_user_detail(%s) VALUES(%s)" % \
                    (utils.list2string(result.keys(), 'keys'), utils.list2string(result.values(), 'values'))  
        #print write_db
        try:
            cursor.execute(write_db)
            db.commit()
        except MySQLdb.Warning, w:  
            sqlWarning =  "Warning:%s" % str(w)
            print sqlWarning
        except MySQLdb.Error, e:  
            sqlError =  "Error:%s" % str(e)
            print sqlError


def store_all_user_detail():
    #global db_result #debug only
    cursor.execute("SELECT id FROM dingding_department_detail")
    db_result = cursor.fetchall() #获取含根部门的所有部门id
    if db_result != None and len(db_result) > 0:
        for i in range(len(db_result)):
            store_user_list(db_result[i][0])

    cursor.execute("SELECT userid FROM dingding_user_list")
    db_result = cursor.fetchall() #获取所有userid
    if db_result != None and len(db_result) > 0:
        for i in range(len(db_result)):
            store_user_detail(db_result[i][0])
    



def user_one_key_store():
    department_one_key_store()
    store_all_user_detail()

                    
#debug only        
#def print_dict(result):
#    for k, v in result.iteritems():
#        print '%s : %s' % (k, v)       
    
#debug only
#本函数完成一键存储和刷新钉钉侧的用户详情和组织详情【对外唯一接口】
#user_one_key_store()


        
#断开数据库
db.close()
