#!/usr/bin/env python3
# -*- coding=utf-8 -*-
from auto_config.ssh import netmiko_config_cred, netmiko_show_cred


def judge_vlan(device_id, port_id, vlan_id):
    sw_ip = '66.0.19.12' + str(device_id)
    result_raw = netmiko_show_cred(sw_ip, 'admin', 'Cisc0123', 'sho vlan')
    vlan_count = len(result_raw)
    # result_raw是个列表，通过len这个函数，得出vlan的数量
    while vlan_count:
        vlan_count -= 1
        # 一旦发现这个vlan就跳出循环。若没有发现就执行else下的动作。
        if result_raw[vlan_count]['vlan_id'] == str(vlan_id):
            print('vlan ' + str(vlan_id) + ' 已存在')
            config_commands_jr = ['interface e0/' + str(port_id),
                                  'switch mode access',
                                  'spanning-tree portfast edge',
                                  'spanning-tree bpduguard enable',
                                  'switch access vlan ' + str(vlan_id),
                                  'no shutdown']

            print(netmiko_config_cred(sw_ip, 'admin', 'Cisc0123', config_commands_jr, verbose=True))
            print('接入端口配置完成')
            break
    else:
        print('vlan ' + str(vlan_id) + ' 不存在')
        config_commands_jr = ['vlan ' + str(vlan_id),
                              'spanning-tree mst config',
                              'instance 0 vlan ' + str(vlan_id),
                              'interface range e0/0-1',
                              'switch trunk allow vlan add ' + str(vlan_id),
                              'interface e0/' + str(port_id),
                              'switch mode access',
                              'spanning-tree portfast edge',
                              'spanning-tree bpduguard enable',
                              'switch access vlan ' + str(vlan_id),
                              'no shutdown']

        print(netmiko_config_cred(sw_ip, 'admin', 'Cisc0123', config_commands_jr, verbose=True))

        # 配置核心交换机
        result_raw = netmiko_show_cred('66.0.19.111', 'admin', 'Cisc0123', 'sho vlan')
        vlan_count = len(result_raw)
        while vlan_count:
            vlan_count -= 1
            if result_raw[vlan_count]['vlan_id'] == str(vlan_id):
                print('核心交换机上已存在vlan ' + str(vlan_id) + '，不做修改')
                break
        else:
            print('vlan ' + str(vlan_id) + ' 不存在')
            config_commands_hx = ['vlan ' + str(vlan_id),
                                  'spanning-tree mst config',
                                  'instance 0 vlan ' + str(vlan_id),
                                  'interface range e2/1-2, e0/0-3',
                                  'switch trunk allow vlan add ' + str(vlan_id)]
            print(netmiko_config_cred('66.0.19.111', 'admin', 'Cisc0123', config_commands_hx, verbose=True))
            print(netmiko_config_cred('66.0.19.112', 'admin', 'Cisc0123', config_commands_hx, verbose=True))
            print(netmiko_config_cred('66.0.19.113', 'admin', 'Cisc0123', config_commands_hx, verbose=True))
            print(netmiko_config_cred('66.0.19.114', 'admin', 'Cisc0123', config_commands_hx, verbose=True))

            config_commands_hx_2 = ['inter vlan' + str(vlan_id),
                                    'ip address 192.75.' + str(vlan_id) + '.2' + ' 255.255.255.0',
                                    'vrrp 1 ip 192.75.' + str(vlan_id) + '.1',
                                    'vrrp 1 priority 200',
                                    'no shutdown'
                                    ]
            config_commands_hx_4 = ['inter vlan' + str(vlan_id),
                                    'ip address 192.75.' + str(vlan_id) + '.3' + ' 255.255.255.0',
                                    'vrrp 1 ip 192.75.' + str(vlan_id) + '.1',
                                    'vrrp 1 priority 90',
                                    'no shutdown'
                                    ]
            print(netmiko_config_cred('66.0.19.112', 'admin', 'Cisc0123', config_commands_hx_2, verbose=True))
            print(netmiko_config_cred('66.0.19.114', 'admin', 'Cisc0123', config_commands_hx_4, verbose=True))


judge_vlan(8, 3, 30)
