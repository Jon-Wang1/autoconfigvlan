#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import logging
import sys
import socketserver
from datetime import datetime
from netflow_0_v9_process_module import ExportPacket, createdb

logging.getLogger().setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
ch.setFormatter(formatter)
logging.getLogger().addHandler(ch)


class SoftflowUDPHandler(socketserver.BaseRequestHandler):
    # We need to save the templates our NetFlow device
    # send over time. Templates are not resended every
    # time a flow is sent to the collector.
    TEMPLATES = {}

    @classmethod
    def get_server(cls, host, port):
        logging.info("Listening on interface {}:{}".format(host, port))
        flow_server = socketserver.UDPServer((host, port), cls)
        return flow_server

    def handle(self):
        data = self.request[0]
        host = self.client_address[0]
        s = f"Received data from {host}, length {len(data)}, datetime {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        logging.debug(s)
        # 使用类ExportPacket处理数据,并返回实例export,这是整个处理的开始!
        export = ExportPacket(data, self.TEMPLATES)
        # 把实例export(类ExportPacket)中的属性templates更新到类SoftflowUDPHandler的属性templates,用于保存模板数据
        self.TEMPLATES.update(export.templates)
        s = f"Processed ExportPacket with {export.header.count} flows."
        logging.debug(s)


if __name__ == "__main__":
    createdb()
    server = SoftflowUDPHandler.get_server('0.0.0.0', 6666)

    logging.getLogger().setLevel(logging.DEBUG)

    try:
        logging.debug("Starting the NetFlow listener")
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        raise

    # 运行服务器后, 调用flow策略
    # interface GigabitEthernet1
    #  no ip flow monitor Monitor1 input
    #  ip flow monitor Monitor1 input
