#!/usr/bin/python3
# coding=utf-8
from port_count_collector import sampling_interval
import re
import random
import shelve


def show_jr_outbound_rate():
    try:
        rackreply_sum = shelve.open('./database/port_count.db')
        for i in range(22, 23):
            rackreply_1 = rackreply_sum['first_rackreply_jr' + str(i)]
            rackreply_2 = rackreply_sum['second_rackreply_jr' + str(i)]

            # out_packets = re.findall('\s+output\s+packets\s+(\d+),', rackreply_1)[1:49]
            out_bytes = re.findall('\s+output.*bytes\s+(\d+)', rackreply_1)[1:49]
            # out_dropped = re.findall('\s+output.*dropped\s(\d+),', rackreply_1)[1:49]
            # out_mcast = re.findall('\s+output.*\n\s+multicast packets\s+(\d+)\s+', rackreply_1)[1:49]
            # out_bcast = re.findall('\s+output.*\n.*broadcast packets\s+(\d+)', rackreply_1)[1:49]

            # out_packets_2 = re.findall('\s+output\s+packets\s+(\d+),', rackreply_2)[1:49]
            out_bytes_2 = re.findall('\s+output.*bytes\s+(\d+)', rackreply_2)[1:49]
            # out_dropped_2 = re.findall('\s+output.*dropped\s(\d+),', rackreply_2)[1:49]
            # out_mcast_2 = re.findall('\s+output.*\n\s+multicast packets\s+(\d+)\s+', rackreply_2)[1:49]
            # out_bcast_2 = re.findall('\s+output.*\n.*broadcast packets\s+(\d+)', rackreply_2)[1:49]


            # out_packets_int = []  # 转换为整数
            out_bytes_int = []  # 转换为整数
            # out_dropped_int = []
            # out_mcast_int = []
            # out_bcast_int = []
            # out_packets_int_2 = []  # 转换为整数
            out_bytes_int_2 = []  # 转换为整数
            # out_dropped_int_2 = []
            # out_mcast_int_2 = []
            # out_bcast_int_2 = []

            # for x in out_packets:
            #     random_num1 = random.random()
            #     out_packets_int.append(int(x) - random_num1)
            for x in out_bytes:
                random_num2 = random.random()
                out_bytes_int.append(int(x) - random_num2)
            # for x in out_mcast:
            #     out_mcast_int.append(int(x))
            # for x in out_bcast:
            #     out_bcast_int.append(int(x))

            # for x in out_packets_2:
            #     out_packets_int_2.append(int(x))
            for x in out_bytes_2:
                out_bytes_int_2.append(int(x))
            # for x in out_mcast:
            #     out_mcast_int_2.append(int(x))
            # for x in out_bcast:
            #     out_bcast_int_2.append(int(x))
            print(out_bytes[35])
            print(out_bytes_2[35])
            diff_value_list = []
            for x in range(0, 48):
                diff_value_list.append((out_bytes_int_2[x] - out_bytes_int[x]))
            diff_value_list_raw = diff_value_list.copy()
            # diff_value_dict = {}
            # for i in range(1,49):
            #     diff_value_dict[i] = diff_value_list_raw[(i-1)]

            diff_value_list.sort()
            top5_out_rate = diff_value_list[-5:]
            # while True:
            #     try:
            #         top5_out_rate.remove(0)
            #     except ValueError:
            #         break
            location_raw_list = []
            for x in top5_out_rate:
                location_raw_list.append(diff_value_list_raw.index(x) + 1)
            # if ((int(top5_out_rate[0])) / 60 * 8 / 1000,) > 999:
            # rate = ((int(top5_out_rate[0])) / 60 * 8 / 1000,) + 'Kbps'
            # print('接入设备' + '%02d:' % (i,) + '接口' + '%02d  ' % location_raw_list[0] +
            #       '%6.3f' % ((int(top5_out_rate[0])) / sampling_interval * 8 / 1000000,) + 'Mbps' + ' | ' +
            #       '接口' + '%02d  ' % location_raw_list[1] +
            #       '%6.3f' % ((int(top5_out_rate[1])) / sampling_interval * 8 / 1000000,) + 'Mbps' + ' | ' +
            #       '接口' + '%02d  ' % location_raw_list[2] +
            #       '%6.3f' % ((int(top5_out_rate[2])) / sampling_interval * 8 / 1000000,) + 'Mbps' + ' | ' +
            #       '接口' + '%02d  ' % location_raw_list[3] +
            #       '%6.3f' % ((int(top5_out_rate[3])) / sampling_interval * 8 / 1000000,) + 'Mbps' + ' | ' +
            #       '接口' + '%02d  ' % location_raw_list[4] +
            #       '%6.3f' % ((int(top5_out_rate[4])) / sampling_interval * 8 / 1000000,) + 'Mbps')
        rackreply_sum.close()

    except Exception as e:
        print(str(e))


show_jr_outbound_rate()
