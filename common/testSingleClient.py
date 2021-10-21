# -*- coding: utf-8 -*-

# @Time : 2021/10/19 19:52
# @Author : Mandy
from __future__ import print_function
import time
import conftest
from common.receiveSingleMessage import SingleMessageProtocol
from common.receiveGroupMessage import GroupMessageProtocol
from utils.pingHandler import PingHandler
import sys
from imp import reload
import uuid
from twisted.internet import reactor
from twisted.names.srvconnect import SRVConnector
from twisted.words.xish import domish
from twisted.words.protocols.jabber import xmlstream, client
from twisted.words.protocols.jabber.jid import JID
from twisted.words.protocols.jabber.xmlstream import StreamManager

reload(sys)  # 重新加载sys
sys.setdefaultencoding('utf8')

login_count = 0


# 生成count个客户端，按interval 间隔 生成
def genTestXMPPClients(startindex, count, interval, domain, password, total):
    print('-----------------starting create clients in reactor-----------------')
    for i in range(count):
        index = i + startindex
        reactor.callLater(i * interval / 1000.0,lambda i: TestXMPPClient(i, domain, password, total),index)
    return


class TestXMPPClient(object):
    print('-----------------starting create clients-----------------')
    def __init__(self, index, domain, password,  total):
        print('-----------------init clients -----------------')
        # self.reactor = reactor
        self.username = 'u2100%07d' % (index)
        self.domain = domain
        self.userjid = JID('%s@%s' % (self.username, self.domain))

        f = client.XMPPClientFactory(self.userjid, password)

        sm = StreamManager(f)
        f.addBootstrap(xmlstream.STREAM_CONNECTED_EVENT, self.connected)
        f.addBootstrap(xmlstream.STREAM_END_EVENT, self.disconnected)
        f.addBootstrap(xmlstream.STREAM_AUTHD_EVENT, self.authenticated)
        f.addBootstrap(xmlstream.INIT_FAILED_EVENT, self.init_failed)

        pingHandler = PingHandler()
        pingHandler.setHandlerParent(sm)

        singleMessageProtocol = SingleMessageProtocol(total)
        singleMessageProtocol.setHandlerParent(sm)

        connector = SRVConnector(reactor, 'xmpp-client', self.userjid.host, f, defaultPort=5222)
        connector.connect()

    def rawDataIn(self, buf):
        print("RECV: %r" % buf)

    def rawDataOut(self, buf):
        print("SEND: %r" % buf)

    def connected(self, xs):
        print('Connected.')
        self.xmlstream = xs
        self.xmlstream.client = self

    def disconnected(self, xs):
        print('Disconnected.')
        conftest.xmppclientlist.remove(self)

    def authenticated(self, xs):
        print("Authenticated.")
        # 上线
        presence = domish.Element((None, 'presence'))
        xs.send(presence)
        conftest.xmppclientlist.append(self)
        print ('xmppclientlist:%s' % conftest.xmppclientlist)

    def init_failed(self, failure):
        print("Initialization failed.")
        print(failure)

        self.xmlstream.sendFooter()
