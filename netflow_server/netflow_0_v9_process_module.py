#!/usr/bin/env python3
# -*- coding=utf-8 -*-


import struct
import os
import sqlite3
from datetime import datetime

db_dir = './Netflow_db/'


field_types = {
    0: 'UNKNOWN_FIELD_TYPE',  # fallback for unknown field types

    # Cisco specs for NetFlow v9
    # https://tools.ietf.org/html/rfc3954
    # https://www.cisco.com/en/US/technologies/tk648/tk362/technologies_white_paper09186a00800a3db9.html
    1: 'IN_BYTES',
    2: 'IN_PKTS',
    3: 'FLOWS',
    4: 'PROTOCOL',
    5: 'SRC_TOS',
    6: 'TCP_FLAGS',
    7: 'L4_SRC_PORT',
    8: 'IPV4_SRC_ADDR',
    9: 'SRC_MASK',
    10: 'INPUT_INTERFACE_ID',
    11: 'L4_DST_PORT',
    12: 'IPV4_DST_ADDR',
    13: 'DST_MASK',
    14: 'OUTPUT_INTERFACE_ID',
    15: 'IPV4_NEXT_HOP',
    16: 'SRC_AS',
    17: 'DST_AS',
    18: 'BGP_IPV4_NEXT_HOP',
    19: 'MUL_DST_PKTS',
    20: 'MUL_DST_BYTES',
    21: 'LAST_SWITCHED',
    22: 'FIRST_SWITCHED',
    23: 'OUT_BYTES',
    24: 'OUT_PKTS',
    25: 'MIN_PKT_LNGTH',
    26: 'MAX_PKT_LNGTH',
    27: 'IPV6_SRC_ADDR',
    28: 'IPV6_DST_ADDR',
    29: 'IPV6_SRC_MASK',
    30: 'IPV6_DST_MASK',
    31: 'IPV6_FLOW_LABEL',
    32: 'ICMP_TYPE',
    33: 'MUL_IGMP_TYPE',
    34: 'SAMPLING_INTERVAL',
    35: 'SAMPLING_ALGORITHM',
    36: 'FLOW_ACTIVE_TIMEOUT',
    37: 'FLOW_INACTIVE_TIMEOUT',
    38: 'ENGINE_TYPE',
    39: 'ENGINE_ID',
    40: 'TOTAL_BYTES_EXP',
    41: 'TOTAL_PKTS_EXP',
    42: 'TOTAL_FLOWS_EXP',
    # Cisco Connection_ID
    45010: 'CONNECTION_ID',
    # 43 vendor proprietary
    44: 'IPV4_SRC_PREFIX',
    45: 'IPV4_DST_PREFIX',
    46: 'MPLS_TOP_LABEL_TYPE',
    47: 'MPLS_TOP_LABEL_IP_ADDR',
    48: 'FLOW_SAMPLER_ID',
    49: 'FLOW_SAMPLER_MODE',
    50: 'NTERVAL',
    # 51 vendor proprietary
    52: 'MIN_TTL',
    53: 'MAX_TTL',
    54: 'IPV4_IDENT',
    55: 'DST_TOS',
    56: 'IN_SRC_MAC',
    57: 'OUT_DST_MAC',
    58: 'SRC_VLAN',
    59: 'DST_VLAN',
    60: 'IP_PROTOCOL_VERSION',
    61: 'DIRECTION',
    62: 'IPV6_NEXT_HOP',
    63: 'BPG_IPV6_NEXT_HOP',
    64: 'IPV6_OPTION_HEADERS',
    # 65-69 vendor proprietary
    70: 'MPLS_LABEL_1',
    71: 'MPLS_LABEL_2',
    72: 'MPLS_LABEL_3',
    73: 'MPLS_LABEL_4',
    74: 'MPLS_LABEL_5',
    75: 'MPLS_LABEL_6',
    76: 'MPLS_LABEL_7',
    77: 'MPLS_LABEL_8',
    78: 'MPLS_LABEL_9',
    79: 'MPLS_LABEL_10',
    80: 'IN_DST_MAC',
    81: 'OUT_SRC_MAC',
    82: 'IF_NAME',
    83: 'IF_DESC',
    84: 'SAMPLER_NAME',
    85: 'IN_PERMANENT_BYTES',
    86: 'IN_PERMANENT_PKTS',
    # 87 vendor property
    88: 'FRAGMENT_OFFSET',
    89: 'FORWARDING_STATUS',
    90: 'MPLS_PAL_RD',
    91: 'MPLS_PREFIX_LEN',  # Number of consecutive bits in the MPLS prefix length.
    92: 'SRC_TRAFFIC_INDEX',  # BGP Policy Accounting Source Traffic Index
    93: 'DST_TRAFFIC_INDEX',  # BGP Policy Accounting Destination Traffic Index
    94: 'APPLICATION_DESCRIPTION',  # Application description
    95: 'APPLICATION_TAG',  # 8 bits of engine ID, followed by n bits of classification
    96: 'APPLICATION_NAME',  # Name associated with a classification
    98: 'postipDiffServCodePoint',  # The value of a Differentiated Services Code Point (DSCP) encoded in the Differentiated Services Field, after modification
    99: 'replication_factor',  # Multicast replication factor
    100: 'DEPRECATED',  # DEPRECATED
    102: 'layer2packetSectionOffset',  # Layer 2 packet section offset. Potentially a generic offset
    103: 'layer2packetSectionSize',  # Layer 2 packet section size. Potentially a generic size
    104: 'layer2packetSectionData',  # Layer 2 packet section data
    # 105-127 reserved for future use by Cisco

    # ASA extensions
    # https://www.cisco.com/c/en/us/td/docs/security/asa/special/netflow/guide/asa_netflow.html
    148: 'NF_F_CONN_ID',  # An identifier of a unique flow for the device
    176: 'NF_F_ICMP_TYPE',  # ICMP type value
    177: 'NF_F_ICMP_CODE',  # ICMP code value
    178: 'NF_F_ICMP_TYPE_IPV6',  # ICMP IPv6 type value
    179: 'NF_F_ICMP_CODE_IPV6',  # ICMP IPv6 code value
    225: 'NF_F_XLATE_SRC_ADDR_IPV4',  # Post NAT Source IPv4 Address
    226: 'NF_F_XLATE_DST_ADDR_IPV4',  # Post NAT Destination IPv4 Address
    227: 'NF_F_XLATE_SRC_PORT',  # Post NATT Source Transport Port
    228: 'NF_F_XLATE_DST_PORT',  # Post NATT Destination Transport Port
    281: 'NF_F_XLATE_SRC_ADDR_IPV6',  # Post NAT Source IPv6 Address
    282: 'NF_F_XLATE_DST_ADDR_IPV6',  # Post NAT Destination IPv6 Address
    233: 'NF_F_FW_EVENT',  # High-level event code
    33002: 'NF_F_FW_EXT_EVENT',  # Extended event code
    323: 'NF_F_EVENT_TIME_MSEC',  # The time that the event occurred, which comes from IPFIX
    152: 'NF_F_FLOW_CREATE_TIME_MSEC',
    231: 'NF_F_FWD_FLOW_DELTA_BYTES',  # The delta number of bytes from source to destination
    232: 'NF_F_REV_FLOW_DELTA_BYTES',  # The delta number of bytes from destination to source
    33000: 'NF_F_INGRESS_ACL_ID',  # The input ACL that permitted or denied the flow
    33001: 'NF_F_EGRESS_ACL_ID',  # The output ACL that permitted or denied a flow
    40000: 'NF_F_USERNAME',  # AAA username

    # PaloAlto PAN-OS 8.0
    # https://www.paloaltonetworks.com/documentation/80/pan-os/pan-os/monitoring/netflow-monitoring/netflow-templates
    346: 'PANOS_privateEnterpriseNumber',
    56701: 'PANOS_APPID',
    56702: 'PANOS_USERID',
}


def createdb():
    """
    ??????????????????,?????????????????????MongoDB
    """
    # ???????????????????????????,?????????????????????
    if os.path.exists(db_dir + 'netflow.sqlite'):
        os.remove(db_dir + 'netflow.sqlite')

    # ??????SQLite?????????
    conn = sqlite3.connect(db_dir + 'netflow.sqlite')
    cursor = conn.cursor()

    # ????????????????????????
    cursor.execute("create table netflowdb (????????? varchar(40), ???????????? varchar(40), ?????? int, ????????? int, ???????????? int, ?????????ID int, ??????????????? int, ???????????? timestamp)")

    conn.commit()


def netflowdb(netflow_dict):
    """
    ???????????????,?????????????????????MongoDB
    """
    # ??????SQLite?????????
    conn = sqlite3.connect(db_dir + 'netflow.sqlite')
    cursor = conn.cursor()

    # ??????Python??????????????????????????????SQLite?????????
    cursor.execute("insert into netflowdb values (?, ?, ?, ?, ?, ?, ?, ?)", (netflow_dict['IPV4_SRC_ADDR'],
                                                                             netflow_dict['IPV4_DST_ADDR'],
                                                                             netflow_dict['PROTOCOL'],
                                                                             netflow_dict['L4_SRC_PORT'],
                                                                             netflow_dict['L4_DST_PORT'],
                                                                             netflow_dict['INPUT_INTERFACE_ID'],
                                                                             netflow_dict['IN_BYTES'],
                                                                             datetime.now()))
    # ????????????
    conn.commit()


class IP:
    """
    ????????????,?????????????????????????????????IP??????
    """
    def __init__(self, data):
        self.IP_LIST = []
        self.IP_LIST.append(str(data >> 24 & 0xff))
        self.IP_LIST.append(str(data >> 16 & 0xff))
        self.IP_LIST.append(str(data >> 8 & 0xff))
        self.IP_LIST.append(str(data & 0xff))
        self.ip_addr = '.'.join(self.IP_LIST)


class DataFlowSet:
    """
    ??????DataFlowSet??????????????????
    """
    def __init__(self, data, templates):
        pack = struct.unpack('!HH', data[:4])
        # ????????????????????????,FlowSet ID(???????????????ID??????)???DataFlowSet??????
        self.template_id = pack[0]
        self.length = pack[1]
        # ??????????????????flows????????????
        self.flows = []

        # ?????????????????????DataFlowSet??????
        offset = 4
        # ????????????templates???,???????????????(????????????ID)
        template = templates.get(self.template_id)
        if not template:
            # flow exporter Netflow-Exporter
            #  destination 10.1.1.80
            #  transport udp 9999
            #  template data timeout 30  # ???????????????30???

            # ??????: ??????Monitor(????????????)??????template, ??????????????????flow
            # FlowSet ID = 0 ???! ??????template
            print(f'???????????????ID:{self.template_id}! ??????????????????Netflow?????????! ????????????"template data timeout"')
            return
        # v9 DataFlowSet???????????????4????????????,????????????4????????????,??????????????????,?????????????????????????????????
        padding_size = 4 - (self.length % 4)  # 4 Byte

        while offset <= (self.length - padding_size):
            # ??????????????????,?????????new_record????????????
            new_record = {}

            for field in template.fields:  # ?????????????????????????????????
                # ??????????????????
                flen = field.field_length
                # ??????????????????
                fkey = field_types[field.field_type]
                # fdata = None

                # ???????????????????????????,????????????
                dataslice = data[offset:offset+flen]

                # ????????????????????????????????????????????????struct.unpack????????????
                fdata = 0
                # enumerate????????????
                # >>>seasons = ['Spring', 'Summer', 'Fall', 'Winter']
                # >>> list(enumerate(seasons))
                # [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]

                # reversed()??????????????????

                # >>> dataslice = b'\x01\x02\x03'
                # >>> bytearray(dataslice)
                # bytearray(b'\x01\x02\x03')
                # >>> reversed(bytearray(dataslice))
                # <reversed object at 0x000001192C620438>
                # >>> enumerate(reversed(bytearray(dataslice)))
                # <enumerate object at 0x000001192C61D7E0>
                # >>> for idx, bytes in enumerate(reversed(bytearray(dataslice))):
                # ...   print(idx, bytes)
                # ...
                # 0 3
                # 1 2
                # 2 1

                # ??????????????????,??????reversed??????????????????????????????????????????????????????
                for idx, byte in enumerate(reversed(bytearray(dataslice))):
                    fdata += byte << (idx * 8)
                if fkey == 'IPV4_SRC_ADDR':  # ????????????IP??????,?????????IP??????????????????
                    new_record[fkey] = IP(fdata).ip_addr
                elif fkey == 'IPV4_DST_ADDR':  # ???????????????IP??????,?????????IP??????????????????
                    new_record[fkey] = IP(fdata).ip_addr
                else:
                    new_record[fkey] = fdata

                offset += flen
            # ???????????????????????????????????????,????????????????????????,??????????????????????????????,??????????????????,????????????MongoDB
            # ?????????????????????????????????????????????????????????,?????????????????????????????????ID?????????
            # ??????ICMP ??????????????????
            if new_record.get('PROTOCOL') == 1:
                new_record['L4_DST_PORT'] = 0
            print(new_record)
            netflowdb(new_record)

    def __repr__(self):  # ???????????????????????????????????????
        return "<DataFlowSet with template {} of length {} holding {} flows>"\
            .format(self.template_id, self.length, len(self.flows))


class TemplateField:
    """
    ?????????????????????????????????????????????????????????
    """
    def __init__(self, field_type, field_length):
        self.field_type = field_type  # integer
        self.field_length = field_length  # bytes

    def __repr__(self):  # ???????????????????????????????????????
        return "<TemplateField type {}:{}, length {}>".format(
            self.field_type, field_types[self.field_type], self.field_length)


class TemplateRecord:
    """
    ??????????????????????????????,??????ID,???????????????
    """
    def __init__(self, template_id, field_count, fields):
        self.template_id = template_id
        self.field_count = field_count
        self.fields = fields

    def __repr__(self):  # ???????????????????????????????????????
        return "<TemplateRecord {} with {} fields: {}>".format(
            self.template_id, self.field_count,
            ' '.join([field_types[field.field_type] for field in self.fields]))


class TemplateFlowSet:
    """
    ??????Template FlowSet,????????????,??????????????????Data FlowSet
    """
    def __init__(self, data):
        # ??????????????????????????????,?????????FlowSet ID???Template FlowSet?????????
        pack = struct.unpack('!HH', data[:4])
        # FlowSet ID,??????ID???0????????????
        self.flowset_id = pack[0]
        # Template FlowSet?????????
        self.length = pack[1]
        # ???????????????????????????
        self.templates = {}

        # ????????????????????????????????????
        offset = 4

        # ?????????????????????template flowset??????template record
        while offset != self.length:
            # ?????????4-8?????????,???????????????ID,???????????????
            pack = struct.unpack('!HH', data[offset:offset+4])
            template_id = pack[0]
            field_count = pack[1]
            # ?????????????????????????????????
            fields = []
            for field in range(field_count):  # ??????????????????????????????????????????
                # ????????????4?????????,????????????????????????,offset += 4,???????????????????????????
                offset += 4
                # ?????????????????????????????????
                field_type, field_length = struct.unpack('!HH', data[offset:offset+4])
                # ????????????????????????field_types???,????????????0,????????????????????????UNKNOWN_FIELD_TYPE
                if field_type not in field_types:
                    field_type = 0
                # ?????????TemplateField????????????field,?????????????????????????????????????????????
                field = TemplateField(field_type, field_length)
                # ??????????????????????????????field??????fields?????????
                fields.append(field)

            # ????????????????????????ID,????????????,????????????,?????????TemplateRecord???????????????????????????
            template = TemplateRecord(template_id, field_count, fields)

            # ???????????????,???????????????ID????????????templates?????????
            self.templates[template.template_id] = template

            # ?????????????????????,?????????????????????????????????
            offset += 4

    def __repr__(self):  # ???????????????????????????????????????
        return "<TemplateFlowSet with id {} of length {} containing templates: {}>"\
            .format(self.flowset_id, self.length, self.templates.keys())


class Header:
    """
    ??????Netflow?????????
    """
    def __init__(self, data):
        pack = struct.unpack('!HHIIII', data[:20])

        self.version = pack[0]  # The version of NetFlow records exported in this packet; for Version 9, this value is 0x0009
        self.count = pack[1]  # Number of FlowSet records (both template and data) contained within this packet
        self.uptime = pack[2]  # Number of FlowSet records (both template and data) contained within this packet
        self.timestamp = pack[3]  # Time in milliseconds since this device was first booted
        # Incremental sequence counter of all export packets sent by this export device; this value is
        # cumulative, and it can be used to identify whether any export packets have been missed
        self.sequence = pack[4]
        # The Source ID field is a 32-bit value that is used to guarantee uniqueness for all flows exported from a particular device.
        self.source_id = pack[5]


class ExportPacket:
    """
    ?????????????????????????????????
    ??????????????????templates????????????{}
    """
    def __init__(self, data, templates):
        # ??????netflow??????
        self.header = Header(data)
        # ?????????????????????{},????????????templates
        self.templates = templates

        self.flows = []
        # ??????????????????20,??????????????????????????????(netflow??????20?????????)
        offset = 20

        while offset != len(data):
            # ??????flowset_id,?????????2????????????
            flowset_id = struct.unpack('!H', data[offset:offset+2])[0]
            # flowset_id == 0 ????????????,??????Template FlowSet??????????????????,????????????????????????????????????Data FlowSet????????????
            if flowset_id == 0:
                # ?????????TemplateFlowSet????????????,????????????tfs(???TemplateFlowSet)
                tfs = TemplateFlowSet(data[offset:])
                # ?????????tfs(???TemplateFlowSet)????????????templates,
                # ????????????ExportPacket??????templates???
                self.templates.update(tfs.templates)
                # ??????TemplateFlowSet??????,????????????DataFlowSet?????????
                offset += tfs.length
            else:
                # ?????????DataFlowSet????????????,????????????dfs(???DataFlowSet)
                dfs = DataFlowSet(data[offset:], self.templates)
                self.flows += dfs.flows
                offset += dfs.length

    def __repr__(self):
        # ??????????????????????????????????????????,???????????????,????????????
        return "<ExportPacket version {} counting {} records>".format(
            self.header.version, self.header.count)
