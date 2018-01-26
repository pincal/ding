#!/usr/bin python
# _*_ coding:utf-8 _*_
# author:liuxx
# time:2018.1.23

import multiprocessing
import MySQLdb
import ConfigParser
import common
import hour
import day
import week

# 全局变量
global memory_group_data
global memory_person_data
global memory_group_num
global memory_person_num
memory_group_data = []
memory_person_data = []
memory_group_num = 0
memory_person_num = 0

def main():
    # 检查本地环境
    if(common.check()):
        hour_process = multiprocessing.Process(target = hour.hour_task)
        hour_process.start()
        day_process = multiprocessing.Process(target = day.day_task)
        day_process.start()
    else:
        week_process = multiprocessing.Process(target = week.week_task)
        week_process.start()

if __name__ == '__main__':
    main()
