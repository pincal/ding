#!/usr/bin/python
#coding=utf-8

import MySQLdb
from treelib import Node, Tree



def create_ding_tree():
    #global ding_tree #debug only
    #连接数据库
    db = MySQLdb.connect('localhost','root','yoyoball','dingtalk')
    db.set_character_set('utf8') #修改MySQLdb默认编码
    cursor= db.cursor()
    cursor.execute('SET NAMES utf8;') #修改MySQLdb默认编码
    cursor.execute('SET CHARACTER SET utf8;') #修改MySQLdb默认编码
    cursor.execute('SET character_set_connection=utf8;') #修改MySQLdb默认编码

    ding_tree = Tree()
    
    sql = "SELECT `id`, `name`, `parentid` FROM dingding_department_detail"
    cursor.execute(sql)
    dept_result = cursor.fetchall()
    #print dept_result debug only
    if dept_result != None and len(dept_result) > 0:
        ding_tree.create_node('##ding_temp##', '0') #先创建虚拟根
        for i in range(len(dept_result)): #向虚拟根填充所有组织
            ding_tree.create_node(dept_result[i][1].decode('utf-8'), dept_result[i][0], '0')
        for i in range(len(dept_result)): #修改隶属关系
            if dept_result[i][0] != '1' : #只要不是实根，就要修改隶属关系
                if ding_tree.contains(dept_result[i][2]): #判断上级是否存在
                    ding_tree.move_node(dept_result[i][0], dept_result[i][2])
                else: #没有上级的不修改
                    continue
    #断开数据库
    db.close()
    return ding_tree





def create_oa_tree():
    #global oa_tree #debug only
    #连接数据库
    db = MySQLdb.connect('localhost','root','yoyoball','np020')
    db.set_character_set('utf8') #修改MySQLdb默认编码
    cursor= db.cursor()
    cursor.execute('SET NAMES utf8;') #修改MySQLdb默认编码
    cursor.execute('SET CHARACTER SET utf8;') #修改MySQLdb默认编码
    cursor.execute('SET character_set_connection=utf8;') #修改MySQLdb默认编码
    
    oa_tree = Tree()
    
    sql = "SELECT `orgid`, `shortname`, `parentorgid` FROM groupinfo"
    cursor.execute(sql)
    dept_result = cursor.fetchall()
    #print dept_result debug only
    if dept_result != None and len(dept_result) > 0:
        oa_tree.create_node('##oa_temp##', '0') #先创建虚拟根
        for i in range(len(dept_result)): #向虚拟根填充所有组织
            #print dept_result[i][1].decode('utf-8'), dept_result[i][0], dept_result[i][2]
            oa_tree.create_node(dept_result[i][1].decode('utf-8'), dept_result[i][0], '0')
        for i in range(len(dept_result)): #修改隶属关系
            if dept_result[i][0] != '001000' : #只要不是实根，就要修改隶属关系
                if oa_tree.contains(dept_result[i][2]): #判断上级是否存在
                    oa_tree.move_node(dept_result[i][0], dept_result[i][2])
                else: #没有上级的不修改
                    continue
    #断开数据库
    db.close()
    return oa_tree










#展示树形图  debug only
#create_ding_tree().show()
#create_oa_tree().show()


