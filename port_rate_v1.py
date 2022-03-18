#!/usr/bin/python3
# coding=utf-8
from telnetlib import Telnet
import multiprocessing
import time
import re
import random


##########################################################################

def show_jr_iface(ipadd, device_ID):
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

        in_packets = re.findall('\s+input\s+packets\s+(\d+),', rackreply_1)[1:49]
        in_bytes = re.findall('\s+input.*bytes\s+(\d+)', rackreply_1)[1:49]
        in_dropped = re.findall('\s+input.*dropped\s(\d+),', rackreply_1)[1:49]
        in_mcast = re.findall('\s+input.*\n\s+multicast packets\s+(\d+)\s+', rackreply_1)[1:49]
        in_bcast = re.findall('\s+input.*\n.*broadcast packets\s+(\d+)', rackreply_1)[1:49]
        time.sleep(18)

        tn.write(b'show inter | in packets\n')
        # time.sleep(1)
        tn.write(b'                  ')
        time.sleep(2)

        rackreply_2 = tn.expect([], timeout=1)[2].decode().strip()

        in_packets_2 = re.findall('\s+input\s+packets\s+(\d+),', rackreply_2)[1:49]
        in_bytes_2 = re.findall('\s+input.*bytes\s+(\d+)', rackreply_2)[1:49]
        in_dropped_2 = re.findall('\s+input.*dropped\s(\d+),', rackreply_2)[1:49]
        in_mcast_2 = re.findall('\s+input.*\n\s+multicast packets\s+(\d+)\s+', rackreply_2)[1:49]
        in_bcast_2 = re.findall('\s+input.*\n.*broadcast packets\s+(\d+)', rackreply_2)[1:49]

        in_packets_int = []  # 转换为整数
        in_bytes_int = []  # 转换为整数
        in_dropped_int = []
        in_mcast_int = []
        in_bcast_int = []
        in_packets_int_2 = []  # 转换为整数
        in_bytes_int_2 = []  # 转换为整数
        in_dropped_int_2 = []
        in_mcast_int_2 = []
        in_bcast_int_2 = []

        for x in in_packets:
            random_num1 = random.random()
            in_packets_int.append(int(x) - random_num1)
        for x in in_bytes:
            random_num2 = random.random()
            in_bytes_int.append(int(x) - random_num2)
        # for x in in_mcast:
        #     in_mcast_int.append(int(x))
        # for x in in_bcast:
        #     in_bcast_int.append(int(x))

        for x in in_packets_2:
            in_packets_int_2.append(int(x))
        for x in in_bytes_2:
            in_bytes_int_2.append(int(x))
        # for x in in_mcast:
        #     in_mcast_int_2.append(int(x))
        # for x in in_bcast:
        #     in_bcast_int_2.append(int(x))

        diff_value_list = []
        for x in range(0, 48):
            diff_value_list.append((in_bytes_int_2[x] - in_bytes_int[x]))
        diff_value_list_raw = diff_value_list.copy()
        # diff_value_dict = {}
        # for i in range(1,49):
        #     diff_value_dict[i] = diff_value_list_raw[(i-1)]

        diff_value_list.sort()
        top5_in_rate = diff_value_list[-5:]
        # while True:
        #     try:
        #         top5_in_rate.remove(0)
        #     except ValueError:
        #         break
        location_raw_list = []
        for x in top5_in_rate:
            location_raw_list.append(diff_value_list_raw.index(x) + 1)
        print('接入设备' + '%02d:' % (device_ID,) + '接口' + '%02d ' % location_raw_list[0] +
              '%8.1f' % ((int(top5_in_rate[0]))/20*8/1000, ) + 'Kbps' + '\t' +
              '接口' + '%02d' % location_raw_list[1] +
              '%8.1f' % ((int(top5_in_rate[1])) / 20 * 8 / 1000,) + 'Kbps' + '\t' +
              '接口' + '%02d' % location_raw_list[2] +
              '%8.1f' % ((int(top5_in_rate[2])) / 20 * 8 / 1000,) + 'Kbps' + '\t' +
              '接口' + '%02d' % location_raw_list[3] +
              '%8.1f' % ((int(top5_in_rate[3])) / 20 * 8 / 1000,) + 'Kbps' + '\t' +
              '接口' + '%02d' % location_raw_list[4] +
              '%8.1f' % ((int(top5_in_rate[4])) / 20 * 8 / 1000,) + 'Kbps')
        # for i in range(5):
        #     # print('接入设备' + '%02d' % (device_ID,) + location_raw_list,top5_in_rate)
        #     result_1 = ('：接口' + str(location_raw_list[i]) + ' '
        #           + '%010.2f' % ((int(top5_in_rate[i]))/20*8/1000, ) + 'Kbps')
        #     print('：接口' + str(location_raw_list[i]) + ' '
        #           + '%010.2f' % ((int(top5_in_rate[i]))/20*8/1000, ) + 'Kbps', end=' ')
        # print('\n')


        # in_packets_int_raw = in_packets_int.copy()
        # in_bytes_int_raw = in_bytes_int.copy()
        # in_dropped_int_raw = in_dropped_int.copy()
        # in_mcast_int_raw = in_mcast_int.copy()
        # in_bcast_int_raw = in_bcast_int.copy()
        #
        # in_packets_int.sort()
        # top5_in_packetscount = in_packets_int[-5]
        #
        # in_bytes_int.sort()
        # top5_in_bytescount = in_bytes_int[-5]
        #
        # in_dropped_int.sort()
        # top5_in_droppedcount = in_dropped_int[-5]
        #
        # in_mcast_int.sort()
        # top5_in_mcastcount = in_mcast_int[-5]
        #
        # in_bcast_int.sort()
        # top5_in_bcastcount = in_bcast_int[-5]
        #
        # iface = '收包数量最大的是接口' + '%02d' % ((in_packets_raw.index(top5_count) + 1),)
        #
        # print('JR' + '%02d' % (ID,) + '%-15s' % (iface,) + ': ' + '%12d' % top5_count)
        tn.write(b'exit\n')
        tn.close()
    except Exception as e:
        time.sleep(5)
        print(ID + str(e))


def Show_hx_iface(ip, ID):
    try:
        tn = Telnet(ip, 23)
        time.sleep(1)
        tn.write(b'root\n')
        time.sleep(1)
        tn.write(b'imish\n')
        time.sleep(1)
        tn.write(b'show inter | in input \n')
        time.sleep(2)
        tn.write(b'          ')
        time.sleep(1)

        rackreply = tn.expect([], timeout=1)[2].decode().strip()

        in_packets = re.findall('\s+input\s+in_packets\s+(\d+),', rackreply)
        in_packets_ge = in_packets[7:15] + in_packets[26:34]  # + in_packets[45]

        in_packets_int = []
        for x in in_packets_ge:
            in_packets_int.append(int(x))
        in_packets_raw = in_packets_int.copy()
        in_packets_int.sort()
        top5_count = in_packets_int[-5]

        iface = '收包数量最大的是接口' + '%02d' % ((in_packets_raw.index(top5_count) + 1),)

        print('HX' + '%02d' % (ID,) + '%-15s' % (iface,) + ': ' + '%12d' % top5_count)
        tn.write(b'exit\n')
        tn.close()
    except Exception as e:
        time.sleep(5)
        print(ID + str(e))


def Show_wg_iface(ip, ID):
    try:
        tn = Telnet(ip, 23)
        time.sleep(1)
        tn.write(b'root\n')
        time.sleep(1)
        tn.write(b'imish\n')
        time.sleep(1)
        tn.write(b'show inter | in input \n')
        #               time.sleep(1)
        tn.write(b'    ')
        time.sleep(1)

        rackreply = tn.expect([], timeout=1)[2].decode().strip()

        in_packets = re.findall('\s+input\s+in_packets\s+(\d+),', rackreply)
        in_packets_ge = in_packets[1:25]

        in_packets_int = []
        for x in in_packets_ge:
            in_packets_int.append(int(x))
        in_packets_raw = in_packets_int.copy()
        in_packets_int.sort()
        top5_count = in_packets_int[-5]

        iface = '收包数量最大的是接口' + '%02d' % ((in_packets_raw.index(top5_count) + 1),)

        print('WG' + '%02d' % (ID,) + '%-15s' % (iface,) + ': ' + '%12d' % top5_count)
        tn.write(b'exit\n')
        tn.close()
    except Exception as e:
        time.sleep(5)
        print(ID + str(e))


# for x in range(10, 41, 10):
#     ip = '10.1.1.' + str(x)
#     ID = x / 10
#     multi_test = multiprocessing.Process(target=Show_hx_iface, args=(ip, ID))
#     multi_test.start()
#     time.sleep(1)
# time.sleep(1)

for x in range(1, 33):
    ip = '10.1.2.' + str(x)
    ID = x
    multi_test = multiprocessing.Process(target=show_jr_iface, args=(ip, ID))
    multi_test.start()
    time.sleep(1)
#
# for x in range(1, 3):
#     ip = '10.1.3.' + str(x)
#     ID = x
#     multi_test = multiprocessing.Process(target=Show_wg_iface, args=(ip, ID))
#     multi_test.start()
#     time.sleep(1)
