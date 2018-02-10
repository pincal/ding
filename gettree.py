#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from treelib import Node, Tree



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


#因为调试可能单独调用两个create_tree函数，所以这两个函数自行建立数据库连接
def create_ding_tree():
    #global ding_tree, dept_result #debug only
    #连接数据库
    db, cursor = connect_db('localhost', 'root', 'yoyoball', 'dingtalk')

    ding_tree = Tree()
    
    sql = "SELECT `id`, `name`, `parentid` FROM dingding_department_detail"
    cursor.execute(sql)
    dept_result = cursor.fetchall()
    #print dept_result debug only
    if dept_result != None and len(dept_result) > 0:
        ding_tree.create_node('##ding_root##', '0') #先创建虚拟根
        for i in range(len(dept_result)): #向虚拟根填充所有组织
            #ding_tree.create_node(dept_result[i][1].decode('utf-8'), dept_result[i][0], '0')
            ding_tree.create_node(dept_result[i][1], dept_result[i][0], '0')
        for i in range(len(dept_result)): #修改隶属关系
            if dept_result[i][0] != '1' : #只要不是实根，就要修改隶属关系
                if ding_tree.contains(dept_result[i][2]): #判断上级是否存在
                    ding_tree.move_node(dept_result[i][0], dept_result[i][2])
                else: #没有上级的不修改
                    continue
    #断开数据库
    close_db(db)            
    return ding_tree



def create_oa_tree():
    #global oa_tree #debug only
    #连接数据库
    db, cursor = connect_db('localhost', 'root', 'yoyoball', 'np020') 
    
    oa_tree = Tree()
    
    sql = "SELECT `orgid`, `shortname`, `parentorgid` FROM groupinfo"
    cursor.execute(sql)
    dept_result = cursor.fetchall()
    #print dept_result debug only
    if dept_result != None and len(dept_result) > 0:
        oa_tree.create_node('##oa_root##', '0') #先创建虚拟根
        for i in range(len(dept_result)): #向虚拟根填充所有组织
            #print dept_result[i][1].decode('utf-8'), dept_result[i][0], dept_result[i][2]
            oa_tree.create_node(dept_result[i][1], dept_result[i][0], '0')
        for i in range(len(dept_result)): #修改隶属关系
            if dept_result[i][0] != '001000' : #只要不是实根，就要修改隶属关系
                if oa_tree.contains(dept_result[i][2]): #判断上级是否存在
                    oa_tree.move_node(dept_result[i][0], dept_result[i][2])
                else: #没有上级的不修改
                    continue
    #断开数据库
    close_db(db)
    return oa_tree


#手动指定对等部门进行搜索测试，仅作保留，不要调用
def find_peers_test():
    #global si_ding_tree, si_oa_tree, oa_result, ding_result #debug only
    #连接两侧数据库
    ding_db = MySQLdb.connect('localhost','root','yoyoball','dingtalk')
    ding_db.set_character_set('utf8') #修改MySQLdb默认编码
    ding_cursor = ding_db.cursor()
    ding_cursor.execute('SET NAMES utf8;') #修改MySQLdb默认编码
    ding_cursor.execute('SET CHARACTER SET utf8;') #修改MySQLdb默认编码
    ding_cursor.execute('SET character_set_connection=utf8;') #修改MySQLdb默认编码

    oa_db = MySQLdb.connect('localhost','root','yoyoball','np020')
    oa_db.set_character_set('utf8') #修改MySQLdb默认编码
    oa_cursor = oa_db.cursor()
    oa_cursor.execute('SET NAMES utf8;') #修改MySQLdb默认编码
    oa_cursor.execute('SET CHARACTER SET utf8;') #修改MySQLdb默认编码
    oa_cursor.execute('SET character_set_connection=utf8;') #修改MySQLdb默认编码
    
    #首先获取树形图
    ding_tree = create_ding_tree()
    oa_tree = create_oa_tree()
    #测试环境 debug only
    si_ding_tree = ding_tree.subtree('1')
    si_oa_tree = oa_tree.subtree('006953')
    si_ding_tree.show()
    si_oa_tree.show()
    #获取oa根的所有直接下属,对oa每一个下属与ding侧相同级别进行名称比较
    oa_orgs = si_oa_tree.is_branch('006953')
    ding_depts = si_ding_tree.is_branch('1')
    
    for i in range(len(oa_orgs)):
        oa_sql = "SELECT `shortname` from groupinfo WHERE `orgid`= '%s'" % oa_orgs[i]
        #print oa_sql #debug only
        oa_cursor.execute(oa_sql)
        oa_result = oa_cursor.fetchone() #得到oa侧的组织名oa_result[0]
        #print oa_result #debug only
        for j in range(len(ding_depts)):
            ding_sql = "SELECT `name` FROM dingding_department_detail WHERE `id`='%s'" % ding_depts[j]
            #print ding_sql
            ding_cursor.execute(ding_sql)
            ding_result = ding_cursor.fetchone()
            #print ding_result
            if ding_result[0] == oa_result[0]:
                #print 'ding_depts:%s,%s== oa_orgs:%s,%s ' % (ding_depts[j], ding_result[0].decode('utf-8'), oa_orgs[i], oa_result[0].decode('utf-8')) #debug only
                peer_sql = "REPLACE INTO ding_oa_department(`ding_dept_id`, \
                            `ding_dept_name`, `oa_org_id`, `oa_org_shortname` \
                            ) VALUES('%s', '%s', '%s', '%s')" % \
                            (ding_depts[j], ding_result[0], \
                            oa_orgs[i], oa_result[0])
                #print peer_sql #debug only
                ding_cursor.execute(peer_sql)
                ding_db.commit()
           
    #关闭数据库
    ding_db.close()
    oa_db.close()


def get_nodes_at_level(trees, level):
    lists = []
    for node in trees.all_nodes_itr():
        if trees.level(node.identifier) == level:
            lists.append(node.identifier)            
    return lists


def get_hierarchy(trees):
    dicts = {}
    for i in range(trees.depth()+1):
        dicts[i] = get_nodes_at_level(trees, i)
    return dicts



def find_peers_at_level(oa_cursor, ding_cursor, ding_db, oa_tree, ding_tree, level, oa_org_id, oa_hierarchy, ding_hierarchy):
    global oa_result, oa_parent_id #debug only
    oa_parent_id = oa_tree.parent(oa_org_id).identifier
    if oa_parent_id == None:
        return -1 #树中没有上级节点【不应该出现这个错误】
    #查找oa上级部门对应的钉钉部门
    find_ding_parent_sql = "SELECT `ding_dept_id` FROM ding_oa_department WHERE `oa_org_id`='%s'" % oa_parent_id
    ding_cursor.execute(find_ding_parent_sql)
    ding_parent_id = ding_cursor.fetchone()
    #print ding_parent_id #debug only
    if ding_parent_id == None: #不能查到oa上级部门对应的钉钉部门则按照级别搜索
        #print 'error : %s' % oa_org_id #debug only
        oa_sql = "SELECT `shortname` from groupinfo WHERE `orgid`='%s'" % oa_org_id
        #print oa_sql #debug only
        oa_cursor.execute(oa_sql)
        oa_result = oa_cursor.fetchone() #得到oa侧的组织名oa_result[0]
        #print type(oa_result) #debug only    
        for i in range(len(ding_hierarchy[level])):
            ding_sql = "SELECT `name` FROM dingding_department_detail WHERE `id`='%s'" % ding_hierarchy[level][i]
            #print ding_sql
            ding_cursor.execute(ding_sql)
            ding_result = ding_cursor.fetchone()
            #print ding_result
            if ding_result[0] == oa_result[0]:
                #print 'ding_depts:%s,%s== oa_orgs:%s,%s ' % (ding_hierarchy[level][i], ding_result[0], oa_org_id, oa_result[0] #debug only
                peer_sql = "REPLACE INTO ding_oa_department(`ding_dept_id`, \
                            `ding_dept_name`, `oa_org_id`, `oa_org_shortname`, \
                            `status`) VALUES('%s', '%s', '%s', '%s', 1)" % \
                            (ding_hierarchy[level][i], ding_result[0], \
                            oa_org_id, oa_result[0])
                #print peer_sql #debug only
                ding_cursor.execute(peer_sql)
                ding_db.commit()
    else: #能查到oa上级部门对应的钉钉部门则缩小查找范围
        #print ding_parent_id[0] #debug only
        oa_sql = "SELECT `shortname` from groupinfo WHERE `orgid`='%s'" % oa_org_id
        #print oa_sql #debug only
        oa_cursor.execute(oa_sql)
        oa_result = oa_cursor.fetchone() #得到oa侧的组织名oa_result[0]
        #print type(oa_result) #debug only
        #print ding_tree.is_branch(str(ding_parent_id[0])) #debug only
        ding_tree_branch = ding_tree.is_branch(ding_parent_id[0])
        for i in range(len(ding_tree_branch)):
            ding_sql = "SELECT `name` FROM dingding_department_detail WHERE `id`='%s'" % ding_tree_branch[i]
            #print ding_sql
            ding_cursor.execute(ding_sql)
            ding_result = ding_cursor.fetchone()
            #print ding_result
            if ding_result[0] == oa_result[0]:
                #print 'ding_depts:%s,%s== oa_orgs:%s,%s ' % (ding_hierarchy[level][i], ding_result[0], oa_org_id, oa_result[0] #debug only
                peer_sql = "REPLACE INTO ding_oa_department(`ding_dept_id`, \
                            `ding_dept_name`, `oa_org_id`, `oa_org_shortname`, \
                            `status`) VALUES('%s', '%s', '%s', '%s', 2)" % \
                            (ding_tree_branch[i], ding_result[0], \
                            oa_org_id, oa_result[0])
                #print peer_sql #debug only
                ding_cursor.execute(peer_sql)
                ding_db.commit()
        


            
def find_peers():
    global ding_tree, oa_tree, oa_hierarchy, ding_hierarchy ,counterA, counterB #debug only
    #counterA = 0 #debug only
    #counterB = 0 #debug only
    #连接两侧数据库
    ding_db, ding_cursor = connect_db('localhost', 'root', 'yoyoball', 'dingtalk')
    oa_db, oa_cursor = connect_db('localhost', 'root', 'yoyoball', 'np020')  

    #获取树形图
    ding_tree=create_ding_tree()
    oa_tree=create_oa_tree()

    #获取oa树深度为1234...的所有节点
    oa_hierarchy = get_hierarchy(oa_tree)
    ding_hierarchy = get_hierarchy(ding_tree)
    if len(oa_hierarchy) < len(ding_hierarchy):
        print "Waring: dingding has more detailed hierarchies!"

    #以oa侧为基准相同层级的元素进行对比
    for i in range(len(oa_hierarchy)): #i为第几层级，j为该层级下的第几个组织
        for j in range(len(oa_hierarchy[i])):
            if i != 0: #只要不是虚拟根就进行对比
                #print oa_hierarchy[i][j], oa_tree.level(oa_hierarchy[i][j])
                #counterA = counterA + 1 #debug only
                find_peers_at_level(oa_cursor, ding_cursor, ding_db, oa_tree, ding_tree, i, oa_hierarchy[i][j], oa_hierarchy, ding_hierarchy)
                #break #debug only
            else: #虚拟根手动设置
                #counterB = counterB + 1 #debug only
                peer_sql = "REPLACE INTO ding_oa_department(`ding_dept_id`, \
                        `ding_dept_name`, `oa_org_id`, `oa_org_shortname` \
                        ) VALUES('%s', '%s', '%s', '%s')" % \
                        ('0', ding_tree.get_node('0').tag, '0', oa_tree.get_node('0').tag)
            #print peer_sql #debug only
            ding_cursor.execute(peer_sql)
            ding_db.commit()
        #break #debug only



    #print counterA, counterB #debug only 用于计算循环是否丢掉了oa的元素
    #关闭两侧数据库
    close_db(ding_db)
    close_db(oa_db)




'''测试部分'''

#展示树形图  debug only
#create_ding_tree().show()
#create_oa_tree().show()

#查找组织对应关系
find_peers()

'''遗留问题'''
#1未作错误处理
#2门户数据库的一个部门，可能匹配到同级别同名的多个部门中的某个不确定的部门
