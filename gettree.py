#!/usr/bin/python
#coding=utf-8

import MySQLdb
from treelib import Node, Tree

def create_ding_tree():
    #连接数据库
    db = MySQLdb.connect('localhost','root','yoyoball','dingtalk')
    db.set_character_set('utf8') #修改MySQLdb默认编码
    cursor= db.cursor()
    cursor.execute('SET NAMES utf8;') #修改MySQLdb默认编码
    cursor.execute('SET CHARACTER SET utf8;') #修改MySQLdb默认编码
    cursor.execute('SET character_set_connection=utf8;') #修改MySQLdb默认编码
    #global ding_tree #debug only
    ding_tree = Tree()
    
    sql = "SELECT `id`, `name`, `parentid` FROM dingding_department_detail"
    cursor.execute(sql)
    dept_result = cursor.fetchall()
    #print dept_result debug only
    if dept_result != None and len(dept_result) > 0:
        for i in range(len(dept_result)):
            if dept_result[i][0] == '1' :
                #print 'create_root', i, dept_result[i][1].decode('utf-8'), dept_result[i][0]
                ding_tree.create_node(dept_result[i][1].decode('utf-8'), dept_result[i][0]) 
            else:
                #print 'create_node', i, dept_result[i][1].decode('utf-8'), dept_result[i][0]
                ding_tree.create_node(dept_result[i][1].decode('utf-8'), dept_result[i][0], '1')
        for i in range(len(dept_result)):
            if dept_result[i][0] != '1' :
                #print 'move_node', i
                ding_tree.move_node(dept_result[i][0], dept_result[i][2])
    #断开数据库
    db.close()
    return ding_tree
