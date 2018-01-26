#!/usr/bin python
# _*_ coding:utf8 _*_
# author:liuxx
# time:2018.1.24

import time
import common
import main

def hour_task():
    print 'hour'
    while(True):
        # 查数量
        oa_num = common.get_data('oa', 'num')
        if(oa_num == main.memory_person_num):
            print '自从上次同步完成以后没有需要审核的修改！'
        else:
            print '有需要审核的修改'
            data = common.get_data('oa', 'verify')
            print data
            print type(data)

        break
        # time.sleep(1)

hour_task()
