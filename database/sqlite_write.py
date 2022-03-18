#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import sqlite3
from parser_xlsx import excel_parser_l_d
my_excel = 'access.xlsx'

# 连接SQLite数据库
conn = sqlite3.connect('test1.sqlite')
cursor = conn.cursor()
# 执行创建表的任务
cursor.execute("create table port_info3 (接入交换机 varchar(50), 接口 int, 对端设备 varchar(80))")

for i in range(1, 33):
    d = excel_parser_l_d(my_excel, str(i))
    JR_Device = 'jr' + str(i)
    for x, y in d.items():
        cursor.execute("insert into port_info3 values ('%s', %d, '%s')" % (JR_Device, x, y))

conn.commit()