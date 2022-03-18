#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import sqlite3

conn = sqlite3.connect('test1.sqlite')
cursor = conn.cursor()
# 基于单一条件搜索数据库表
# cursor.execute("select 接口 from port_info3 where 对端设备 = '5号火灾图像现场控制箱 5FZP'")
cursor.execute("select * from port_info3 where 对端设备 = '5号火灾图像现场控制箱 5FZP'")
results = cursor.fetchall()

print(results)

conn.commit()