#!/usr/bin/python3
# coding=utf-8
from telnetlib import Telnet
import multiprocessing
import time
import shelve
import os

sampling_interval = 60


def storage_iface_count(ipadd, device_ID, time_interval):
    try:
        tn = Telnet(ipadd, 23)
        time.sleep(1)
        tn.write(b'root\n')
        time.sleep(1)
        tn.write(b'imish\n')
        time.sleep(1)
        tn.write(b'show inter | in packets \n')
        # time.sleep(1)
        tn.write(b'                  ')
        time.sleep(2)

        rackreply_1 = tn.expect([], timeout=1)[2].decode().strip()

        # in_packets = re.findall('\s+input\s+packets\s+(\d+),', rackreply_1)[1:49]
        # in_bytes = re.findall('\s+input.*bytes\s+(\d+)', rackreply_1)[1:49]
        # in_dropped = re.findall('\s+input.*dropped\s(\d+),', rackreply_1)[1:49]
        # in_mcast = re.findall('\s+input.*\n\s+multicast packets\s+(\d+)\s+', rackreply_1)[1:49]
        # in_bcast = re.findall('\s+input.*\n.*broadcast packets\s+(\d+)', rackreply_1)[1:49]
        # time.sleep(time_interval - 2)
        for i in range(time_interval - 2):
            current_percentage = (i / (time_interval - 2)) * 100
            os.system('clear')
            print('正在采集，请稍等' + '%4.2f' % current_percentage + '%')
            time.sleep(1)
        tn.write(b'show inter | in packets\n')
        # time.sleep(1)
        tn.write(b'                  ')
        time.sleep(2)

        rackreply_2 = tn.expect([], timeout=1)[2].decode().strip()

        # in_packets_2 = re.findall('\s+input\s+packets\s+(\d+),', rackreply_2)[1:49]
        # in_bytes_2 = re.findall('\s+input.*bytes\s+(\d+)', rackreply_2)[1:49]
        # in_dropped_2 = re.findall('\s+input.*dropped\s(\d+),', rackreply_2)[1:49]
        # in_mcast_2 = re.findall('\s+input.*\n\s+multicast packets\s+(\d+)\s+', rackreply_2)[1:49]
        # in_bcast_2 = re.findall('\s+input.*\n.*broadcast packets\s+(\d+)', rackreply_2)[1:49]

        port_count_data = shelve.open('./database/port_count.db')
        port_count_data['first_rackreply_jr' + str(device_ID)] = rackreply_1
        port_count_data['second_rackreply_jr' + str(device_ID)] = rackreply_2
        port_count_data.close()
        time.sleep(1)
        tn.write(b'exit\n')
        tn.close()
    except Exception as e:

        print(str(ID) + str(e))


if __name__ == '__main__':
    for x in range(1, 33):
        ip = '10.1.2.' + str(x)
        ID = x
        multi_test = multiprocessing.Process(target=storage_iface_count, args=(ip, ID, sampling_interval))
        multi_test.start()
        time.sleep(1)
