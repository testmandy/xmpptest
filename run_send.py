# -*- coding: utf-8 -*-

# @Time : 2021/10/19 19:54
# @Author : Mandy

from __future__ import print_function
import hashlib
import socket
import sys
import time
from imp import reload
import logging
from common.sendGroupMessage import SendGroupMessage
from common.testGroupClient import genTestXMPPClients
from twisted.internet import reactor

reload(sys) #重新加载sys
sys.setdefaultencoding('utf8')


send = SendGroupMessage()
if __name__ == '__main__':
    hostname = socket.getfqdn(socket.gethostname())
    FORMAT = "%(asctime)-15s   %(message)s"
    logtime = time.strftime("%Y%m%d", time.localtime())
    logging.basicConfig(filename='/tmp/testlog/%s%s.log' % (hostname, str(logtime)), level=logging.DEBUG, format=FORMAT)
    logging.info('------------------starting-------------------')
    plainpwd = 'q11111111'

    m1 = hashlib.md5()
    m1.update(plainpwd.encode('utf-8'))
    password = m1.hexdigest()

    interval = 100
    startindex = int(sys.argv[1])
    count = int(sys.argv[2])
    if len(sys.argv) == 8:
        sendinterval = int(sys.argv[3])
        domain = str(sys.argv[4])
        total = int(sys.argv[5])
        testgroupname = str(sys.argv[6])
        source = '[Task%s]' % str(sys.argv[7])
    else:
        sendinterval = 100
        domain = 'perftest.pro.akeychat.cn'
        total = 100
        testgroupname = 'u21000000000_1634010735099'
        source = ''
    logging.info('start connecting')
    genTestXMPPClients(startindex, count, interval, domain, password, testgroupname=testgroupname, total=total)
    send.startSendGroupMessage(count, sendinterval, testgroupname, domain, total, source)

    reactor.run()


