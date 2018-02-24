#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dingding_sdk import dingapi_timer
from dingding_sdk import user
from dingding_sdk import department
from dingding_sdk import utils
from find_peers import create_ding_tree, get_nodes_at_level, get_hierarchy
import MySQLdb
import time


###只能测试环境使用####
###只能测试环境使用####
###只能测试环境使用####



#debug only        
def print_dict(dicts):
    for k, v in dicts.iteritems():
        print '%s : %s' % (k, v)    




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



#向钉钉通讯录更新部门信息
def ding_create_all_department(ding_db, ding_cursor, ding_hierarchy):
    for i in range(len(ding_hierarchy)):
        for j in range(len(ding_hierarchy[i])):
            if ding_hierarchy[i][j] == '0' or ding_hierarchy[i][j] == '1':
            #print 'root %s, %s' % (i,j) #debug only
                continue  #不要更新虚根和实根
            else:
                #print 'sub department %s, %s' % (i,j) #debug only
                create_sql = "SELECT  `name` , `parentid` , `order` , \
                    `createDeptGroup` , `autoAddUser`, `deptHiding`, \
                    `deptPerimits` , `userPerimits` , `outerDept` , \
                    `outerPermitDepts`, `outerPermitUsers` , `orgDeptOwner` ,\
                    `deptManagerUseridList` , `groupContainSubDept` \
                    FROM dingding_department_detail \
                    WHERE id='%s'" % ding_hierarchy[i][j]
                ding_cursor.execute(create_sql)
                db_result = ding_cursor.fetchone()
                #第一步在根部门上新建所有部门
                for k in range(5):
##                    is_success, create_result = department.create_department(dingapi_timer.access_token, 
##                        db_result[0], '1', order=db_result[2], createDeptGroup=db_result[3], 
##                        deptHiding=db_result[5], deptPermits=db_result[6],userPermits=db_result[7], 
##                        outerDept=db_result[8], outerPermitDepts=db_result[9], outerPermitUsers=db_result[10])
                    #测试时尽可能不要打扰别人
                    is_success, create_result = department.create_department(dingapi_timer.access_token, 
                        db_result[0], '1', order=db_result[2], createDeptGroup=False, 
                        deptHiding=True, deptPermits=None, userPermits=None, 
                        outerDept=None, outerPermitDepts=None, outerPermitUsers=None)
                    if is_success == True:
                #第二步根据返回的部门id修改数据库中的数据
                        write_test_sql_a = "UPDATE dingding_department_detail SET `id`='%s' where `id`='%s' " \
                            % (create_result.get(u'id', '-1'), ding_hierarchy[i][j])
                        write_test_sql_b = "UPDATE dingding_department_detail SET `parentid`='%s' where `parentid`='%s' " \
                            % (create_result.get(u'id', '-1'), ding_hierarchy[i][j])
                        ding_cursor.execute(write_test_sql_a)
                        ding_cursor.execute(write_test_sql_b)
                        ding_db.commit()
                        ding_update_department(ding_db, ding_cursor, create_result.get(u'id', '-1'))
                        db_update_user_department(ding_db, ding_cursor, ding_hierarchy[i][j], create_result.get(u'id', '-1'))
                        break
                    else:
                        #print 'create department fail' #debug only
                        #print ding_hierarchy[i][j]
                        #print_dict(create_result) #debug only
                        time.sleep(1)                   
    return True

def db_update_user_department(ding_db, ding_cursor, old_dept_id, new_dept_id):
    get_user_sql = "SELECT `userid`, `department` FROM dingding_user_detail where department like '%%%s%%';" % old_dept_id
    ding_cursor.execute(get_user_sql)
    db_user_result = ding_cursor.fetchall()

    for i in range(len(db_user_result)):
        dept_list = db_user_result[i][1].strip('[').strip(']').strip(' ').split(',') #注意如果有空格remove可能会出错，所以必须去掉空格
        for j in range(len(dept_list)):
            if type(dept_list[j]) == str:
                dept_list[j] = dept_list[j].strip(' ')
        #print dept_list, 'old' #debug only
        dept_list.remove(old_dept_id)
        #print dept_list, 'delete'#debug only
        dept_list.append(str(new_dept_id))
        #print dept_list, 'new' #debug only
        new_dept_list = check_list(dept_list)
        #print new_dept_list, 'checked new' #debug only
        update_user_sql = "UPDATE dingding_user_detail SET `department`='%s' WHERE `userid`='%s' " % (new_dept_list, db_user_result[i][0])
        #print update_user_sql #debug only
        ding_cursor.execute(update_user_sql)
        ding_db.commit()

    return True
        

#一个检查函数，确保数据库中不会出现这种情况['58038751', 60094508]多出的引号导致sql错误，以及第二个数字前的空格   
def check_list(lists):
    if lists == None or len(lists) == 0:
        return lists
    new_list = []
    for i in range(len(lists)):
        if type(lists[i]) == str:
            lists[i] = lists[i].strip(' ')
        new_list.append(int(lists[i]))
    string = str(new_list).replace(' ','')
    return string


    

def ding_update_department(ding_db, ding_cursor, ding_dept_id):
    if ding_dept_id == '0' or ding_dept_id == '1' or ding_dept_id == '-1':
        #print 'ding_update_department %s error ' % ding_dept_id #debug only
        return False
    else:
        update_sql = "SELECT  `id`, `name` , `parentid` , `order` , \
            `createDeptGroup` , `autoAddUser`, `deptHiding`, \
            `deptPerimits` , `userPerimits` , `outerDept` , \
            `outerPermitDepts`, `outerPermitUsers` , `orgDeptOwner` ,\
            `deptManagerUseridList` , `groupContainSubDept` \
            FROM dingding_department_detail \
            WHERE id='%s'" % ding_dept_id
        ding_cursor.execute(update_sql)
        db_result = ding_cursor.fetchone()   
        for k in range(5):
##            is_success, update_result = department.update_department(dingapi_timer.access_token, 
##                db_result[0], name=db_result[1], parentid=db_result[2], order=db_result[3], 
##                createDeptGroup=db_result[4], deptHiding=db_result[6], deptPermits=None,
##                userPermits=None, outerDept=None, outerPermitDepts=None,
##                outerPermitUsers=None, autoAddUser=db_result[5], deptManagerUserList=None,
##                orgDeptOwner=None)
            #测试时尽可能不要打扰别人
            is_success, update_result = department.update_department(dingapi_timer.access_token, 
                db_result[0], name=db_result[1], parentid=db_result[2], order=db_result[3], 
                createDeptGroup=False, deptHiding=True, deptPermits=None,
                userPermits=None, outerDept=None, outerPermitDepts=None,
                outerPermitUsers=None, autoAddUser=False, deptManagerUserList=None,
                orgDeptOwner=None)  
            if is_success == True:
                break
            else:
                #print 'update all department fail' #debug only
                #print_dict(update_result) #debug only
                time.sleep(1)
    return True

 
    
def ding_update_all_department(ding_db, ding_cursor, ding_hierarchy):
    for i in range(len(ding_hierarchy)):
        for j in range(len(ding_hierarchy[i])):
            if ding_hierarchy[i][j] == '0' or ding_hierarchy[i][j] == '1':
            #print 'root %s, %s' % (i,j) #debug only
                continue
            else:
                #print 'sub department %s, %s' % (i,j) #debug only
                update_sql = "SELECT  `id`, `name` , `parentid` , `order` , \
                    `createDeptGroup` , `autoAddUser`, `deptHiding`, \
                    `deptPerimits` , `userPerimits` , `outerDept` , \
                    `outerPermitDepts`, `outerPermitUsers` , `orgDeptOwner` ,\
                    `deptManagerUseridList` , `groupContainSubDept` \
                    FROM dingding_department_detail \
                    WHERE id='%s'" % ding_hierarchy[i][j]
                ding_cursor.execute(update_sql)
                db_result = ding_cursor.fetchone()   
                for k in range(5):
##                    is_success, update_result = department.update_department(dingapi_timer.access_token, 
##                        db_result[0], name=db_result[1], parentid=db_result[2], order=db_result[3], 
##                        createDeptGroup=db_result[4], deptHiding=db_result[6], deptPermits=db_result[7],
##                        userPermits=db_result[8], outerDept=db_result[9], outerPermitDepts=db_result[10],
##                        outerPermitUsers=db_result[11], autoAddUser=db_result[5], deptManagerUserList=db_result[13],
##                        orgDeptOwner=db_result[12])
                    is_success, update_result = department.update_department(dingapi_timer.access_token, 
                        db_result[0], name=db_result[1], parentid=db_result[2], order=db_result[3], 
                        createDeptGroup=db_result[4], deptHiding=db_result[6], deptPermits=None,
                        userPermits=None, outerDept=None, outerPermitDepts=None,
                        outerPermitUsers=None, autoAddUser=db_result[5], deptManagerUserList=None,
                        orgDeptOwner=None)                    
                    if is_success == True:
                        break
                    else:
                        #print 'update department fail' #debug only
                        #print_dict(update_result) #debug only
                        time.sleep(1)
    return True
    

    
#只能删除没有人员的空部门，有人员的部门依据钉钉API说明不能直接删除  
def ding_delete_all_empty_department():
    #debug only
    dingapi_timer.access_token_timer()
    ding_db, ding_cursor = connect_db('localhost', 'root', 'yoyoball', 'dingtalk')
    delete_all_sql = "SELECT `id` FROM dingding_department_detail"
    ding_cursor.execute(delete_all_sql)
    db_result = ding_cursor.fetchall()
    for i in range(len(db_result)):
        if db_result[i][0] == '1':
            continue #钉钉的根部门不允许修改
        else :
            is_success, del_result = department.delete_department(dingapi_timer.access_token, db_result[i][0])
            #print 'delete department %s ,%s' % (db_result[i][0], is_success) #debug only
            #print_dict(del_result) #debug only
            if is_success == False and del_result.has_key('60003'): #判断错误原因是否因为部门不存在，不存在直接跳过
                pass
    close_db(ding_db)            
    return True
        
    
#这个函数没有进行测试，也不好测试
#数据库中部门存储为'[58099807]'字符串
def ding_create_all_user(ding_db, ding_cursor):
    #global user_result #debug only
    create_user_sql = "SELECT `userid`, `name`, `department`, `mobile` FROM dingding_user_detail"
    ding_cursor.execute(create_user_sql)
    user_result = ding_cursor.fetchall()
    for i in range(len(user_result)):
        for j in range(5):
            department_list = user_result[i][2].strip('[').strip(']').strip(' ').split(',')
            for k in range(len(department_list)):
                if type(department_list[k]) == str:
                    department_list[k] = department_list[k].strip(' ')
            #print department_list #debug only
            is_success, create_result = user.create_user(dingapi_timer.access_token, user_result[i][0],
                user_result[i][1], department_list, user_result[i][3], email=None, position=None,
                jobnumber=None, extattr=None, orderInDepts=None,tel=None, workPlace=None,
                remark=None, isHide=None, isSenior=None)
            if is_success == True:
                break
            else:
                print 'create user %s, %s fail' % (user_result[i][0], user_result[i][1])
                print_dict(create_result)
                time.sleep(1)
    return True





'''用于在空企业中进行测试'''
'''预备工作：【ding_read模块】读取钉钉上某实际公司的组织架构并存储'''
'''!!!!!!!!!!!!!!!!!!切记核对corpid和secret!!!!!!!!!!!!!'''
'''函数功能：一键把实际公司的组织架构上传到测试环境'''
#由于钉钉新建部门不允许指定部门id所以无法直接上传，采取新建+修改的方式进行。
def ding_one_key_create():
    #获取access_token可以全局使用dingapi_timer.access_token
    dingapi_timer.access_token_timer()
    #连接数据库
    ding_db, ding_cursor = connect_db('localhost', 'root', 'yoyoball', 'dingtalk')
    #获取树形图
    ding_tree=create_ding_tree()
    #获取ding树深度为1234...的所有节点
    ding_hierarchy = get_hierarchy(ding_tree)
    #向钉钉通讯录新建部门
    ding_create_all_department(ding_db, ding_cursor, ding_hierarchy)
    #向钉钉通讯录上传人员信息
    ding_create_all_user(ding_db, ding_cursor)
    #关闭数据库
    close_db(ding_db)
    return True

#对外接口
#ding_one_key_create()  


##存在问题：偶尔报错<urlopen error ('_ssl.c:645: The handshake operation timed out',)>错误在底层，目前不清楚如何处理

    
