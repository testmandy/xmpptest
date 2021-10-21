# -*- coding: utf-8 -*-

# @Time : 2021/10/20 17:07
# @Author : Mandy

from __future__ import print_function

import uuid
import time

from twisted.words.protocols.jabber import jid
import sys
from imp import reload

import conftest
from utils.messageProtocol import MessageProtocol
import logging
import copy

reload(sys)  # 重新加载sys
sys.setdefaultencoding('utf8')
receivedMessageCount = 0


def genRecvReceipts(sender, recipient, srcmessageid):
    messageid = str(uuid.uuid4())
    currenttime = str(int(time.time() * 1000))
    recvReceiptsMessage = conftest.SINGLE_RECV_RECEIPTS_MESSAGE % (
        messageid, recipient, sender, srcmessageid, messageid, currenttime)

    return recvReceiptsMessage


def genReadReceipts(sender, recipient, srcmessageid):
    messageid = str(uuid.uuid4())
    currenttime = str(int(time.time() * 1000))
    readReceiptsMessage = conftest.SINGLE_READ_RECEIPTS_MESSAGE % (
        messageid, recipient, sender, srcmessageid, messageid, currenttime)

    return readReceiptsMessage


def is_single_chat_text_msg(message):
    messagestr = message.toXml()

    findstr = "<property><name>message.prop.im.msgtype</name><value type='string'>text</value></property>"

    if messagestr.find(findstr) >= 0:
        return True
    else:
        return False


# 收消息的处理
class SingleMessageProtocol(MessageProtocol):
    def __init__(self, total):
        self.total = total

    def onMessage(self, message):
        if message.hasAttribute('from'):
            sender = jid.internJID(message['from'])
        else:
            sender = None
        if message.hasAttribute('to'):
            recipient = jid.internJID(message['to'])
        else:
            recipient = None

        if message.hasAttribute('id'):
            messageid = jid.internJID(message['id'])
        else:
            messageid = None

        if sender is None or sender.userhost() == self.xmlstream.client.userjid.userhost():
            return

        if is_single_chat_text_msg(message):
            # 接收消息计数
            global receivedMessageCount
            receivedMessageCount += 1
            if conftest.sendAll == self.total:
                conftest.receiveAll = receivedMessageCount

            recvReceiptsMsg = genRecvReceipts(recipient.userhost(), sender.userhost(), messageid)

            self.xmlstream.send(recvReceiptsMsg)

            readReceiptsMsg = genReadReceipts(recipient.userhost(), sender.userhost(), messageid)

            self.xmlstream.send(readReceiptsMsg)
