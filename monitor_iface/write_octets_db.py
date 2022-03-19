#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import sqlite3
from snmp_getbulk import snmpv2_getbulk
from datetime import datetime
import time

ip = "66.0.19.112"
while True:
    # 进接口字节数
    result_in = snmpv2_getbulk(ip, "tcpipro", "1.3.6.1.2.1.2.2.1.10", port=161)
    # 出接口字节数
    result_out = snmpv2_getbulk(ip, "tcpipro", "1.3.6.1.2.1.2.2.1.16", port=161)

    print(result_in[9][1], result_out[9][1], result_in[10][1], result_out[10][1])

    conn = sqlite3.connect('if_octets2.sqlite')
    cursor = conn.cursor()
    # cursor.execute("create table if_octets (ip varchar(40), "
    #                "date_time varchar (60), "
    #                "date_time_s int, "
    #                "eth1_in  int, "
    #                "eth1_out  int, "
    #                "eth2_in  int, "
    #                "eth2_out  int)")
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_time_s = int(datetime.now().strftime("%s"))
    cursor.execute("insert into if_octets values ('%s','%s',%d, %d, %d, %d, %d)" % (ip, date_time, date_time_s,
                                                                                    int(result_in[9][1]),
                                                                                    int(result_out[9][1]),
                                                                                    int(result_in[10][1]),
                                                                                    int(result_out[10][1])
                                                                                    )
                   )
    conn.commit()
    time.sleep(10)



