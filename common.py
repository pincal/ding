#!/usr/bin python
# _*_ coding:utf-8 _*_
# author:liuxx
# time:2018.1.24

import MySQLdb
import ConfigParser

# 检查本地环境
def check():
    conf = ConfigParser.ConfigParser()
    conf.read('config.ini')
    host = conf.get('local_database', 'host')
    user = conf.get('local_database', 'user')
    password = conf.get('local_database', 'password')
    port = int(conf.get('local_database', 'port'))
    db = MySQLdb.connect(host, user, password, port = port, charset = 'utf8')
    cur = db.cursor()
    cur.execute('show databases;')
    databases = cur.fetchall()
    mysql_flag = False
    for database in databases:
        if(database[0] == 'ding'):
            print 'local database ding exist!'
            mysql_flag = True
            break
            return True
    if(not mysql_flag):
        print 'local database has not been created!'
        return False

# 取本地/门户数据
def get_data(source, data_type):
    if(source == 'local'):
        config_item = 'local_database'
        print "get local data!"
    elif(source == 'oa'):
        config_item = 'oa_database'
        print 'get oa data!'
    else:
        print "param error!"
    conf = ConfigParser.ConfigParser()
    conf.read('config.ini')
    host = conf.get(config_item, 'host')
    user = conf.get(config_item, 'user')
    password = conf.get(config_item, 'password')
    port = int(conf.get(config_item, 'port'))
    database = conf.get(config_item, 'database')
    db = MySQLdb.connect(host, user, password, port = port, db = database, charset = 'utf8')
    cur = db.cursor()
    if(data_type == 'all'):
        data = {}
        cur.execute('select * from GROUPINFO;')
        data['groups'] = cur.fetchall()
        cur.execute('select * from PERSONINFO;')
        data['persons'] = cur.fetchall()
        print 'get data of ' + source + ' success!'
        print data
        return data
    elif(data_type == 'num'):
        cur.execute('select * from GROUPINFO;')
        num = cur.fetchall()
        print "get num of " + source + " success!"
        print num
        return num
    else:
        print "param error!"

# 数据整理
def data_processing(data):
    print 'pro!'
    print data
    print type(data)
