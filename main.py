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
memory_group_data = []
memory_person_data = []

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
