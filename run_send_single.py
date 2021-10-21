#!/usr/bin/python
# coding=utf-8
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
A very simple twisted xmpp-client (Jabber ID)

To run the script:
$ python xmpp_client.py <jid> <secret>
"""
from __future__ import print_function
import hashlib
import sys
import datetime
from imp import reload

import conftest
from common.sendSingleMessage import SendSingleMessage
from common.testSingleClient import genTestXMPPClients
from twisted.internet import reactor

reload(sys)  # 重新加载sys
sys.setdefaultencoding('utf8')

send = SendSingleMessage()

if __name__ == '__main__':
    plainpwd = 'q11111111'
    m1 = hashlib.md5()
    m1.update(plainpwd.encode('utf-8'))
    password = m1.hexdigest()
    interval = 100

    if len(sys.argv) == 6:
        startindex = int(sys.argv[1])
        count = int(sys.argv[2])
        sendinterval = int(sys.argv[3])
        domain = sys.argv[4]
        total = int(sys.argv[5])
    else:
        startindex = 0
        count = 10
        sendinterval = 100
        domain = 'perftest.pro.akeychat.cn'
        total = 10

    genTestXMPPClients(startindex, count, interval, domain, password, total)
    send.startSend(count, sendinterval, total)
    reactor.run()
    # startTime = datetime.datetime.strptime(conftest.start_time, "%Y-%m-%d %H:%M:%S")
    # endTime = datetime.datetime.strptime(conftest.end_time, "%Y-%m-%d %H:%M:%S")
    # duration = (endTime - startTime).seconds
    # print('sendCount:%d receiveCount:%d startTime:%s endTime:%s duration:%ds' %
    #       (conftest.sendAll, conftest.receiveAll, conftest.start_time, conftest.end_time, duration))


