#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import sqlite3
from datetime import datetime
import time
conn = sqlite3.connect('if_octets2.sqlite')
cursor = conn.cursor()
# 基于单一条件搜索数据库表
# cursor.execute("select * from if_octets where ip = '66.0.19.112'")
# results = cursor.fetchall()

endure_value = 0

while True:
    date_time_seconds = int(datetime.now().strftime("%s")) - 22
    # 基于多重条件搜索数据库表
    cursor.execute("select eth2_out from if_octets where date_time_s > %d and ip = '66.0.19.112'" % date_time_seconds)
    results = cursor.fetchall()
    # print(results)
    interval = (len(results) - 1) * 10
    diff_value = int(results[-1][0]) - int(results[0][0])
    diff_value_1 = diff_value * 8 / 1000 / 1000 / interval
    diff_value_2 = f'E2/2的当前速率：{diff_value_1:<10.5f}' + 'Mbps'
    print(diff_value_2)
    if diff_value_1 > 30:
        endure_value += 1
    if endure_value > 2:
        print('超出忍耐值！！！')
        endure_value = 0
    time.sleep(20)
