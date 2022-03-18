#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from netmiko import Netmiko
import pprint


def netmiko_show_cred(host, username, password, cmd, enable='Cisc0123', ssh=True):
    device_info = {
                    'host': host,
                    'username': username,
                    'password': password,
                    'device_type': 'cisco_ios' if ssh else 'cisco_ios_telnet',
                    'secret': enable
    }
    try:
        net_connect = Netmiko(**device_info)
        return net_connect.send_command(cmd, use_textfsm=True)

    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return


def netmiko_config_cred(host, username, password, cmds_list, enable='Cisc0123', ssh=True, verbose=False):
    device_info = {
                    'host': host,
                    'username': username,
                    'password': password,
                    'device_type': 'cisco_ios' if ssh else 'cisco_ios_telnet',
                    'secret': enable
    }
    try:
        net_connect = Netmiko(**device_info)
        if verbose:
            output = net_connect.send_config_set(cmds_list)
            return output
        else:
            net_connect.send_config_set(cmds_list)

    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return


if __name__ == '__main__':
    raw_result = netmiko_show_cred('66.0.19.111', 'admin', 'Cisc0123', 'sho ver')
    # print(type(raw_result))
    # print(raw_result)
    pprint.pprint(raw_result)
    #
    # config_commands = ['router bgp 123',
    #                    'bgp router-id 123.1.1.123',
    #                    'network 1.1.1.1 mask 255.255.255.255']
    #
    # print(netmiko_config_cred('66.0.19.92', 'admin', 'Cisc0123', config_commands, verbose=True))
