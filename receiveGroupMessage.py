# -*- coding: utf-8 -*-

# @Time : 2021/10/19 19:55
# @Author : Mandy
from __future__ import print_function
from twisted.words.protocols.jabber import jid
import sys
import time
from imp import reload

import conftest
from messageProtocol import MessageProtocol
import logging
import copy

reload(sys)  # 重新加载sys
sys.setdefaultencoding('utf8')
receivedMessageCount = 0


# 判断是否是群聊消息
def is_group_chat_text_msg(message):
    messagestr = message.toXml()

    findstr = "<property><name>message.prop.im.msgtype</name><value type='string'>text</value></property>"

    if messagestr.find(findstr) >= 0:
        return True
    else:
        return False


# 获取消息序列号
def get_msg_seqno(messagestr):
    seqno = None

    findstr = "<property><name>message.prop.seqNo</name><value type='string'>"
    try:
        index = messagestr.find(findstr)
    except IndexError:
        raise '没有找到messagestr'

    if index > 0:
        try:
            indexend = index + len(findstr)
            rindex = messagestr.find('</value>', indexend)
            seqno = int(messagestr[indexend:rindex])
        except IndexError:
            raise '没有找到seqno'

    return seqno


# 收消息的处理
class GroupMessageProtocol(MessageProtocol):
    def __init__(self, count, total):
        self.currentSeqNo = None
        self.messageCount = 0
        self.total = total
        self.count = count

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
            messageid = message['id']
        else:
            messageid = None

        if is_group_chat_text_msg(message):
            global receivedMessageCount
            receivedMessageCount += 1
            seqno = get_msg_seqno(message.toXml())
            if seqno is not None:
                if self.currentSeqNo is not None and (self.currentSeqNo + 1) != seqno:
                    logging.info('receive:%s -sender %s to recipient %s last seqno %s  and current seqno %s'
                                 % (receivedMessageCount, sender, self.xmlstream.client.userjid,
                                    self.currentSeqNo, seqno))
                self.currentSeqNo = seqno

            per_receive_count = receivedMessageCount / self.count
            if conftest.sendAll == self.total:
                print('receiveTotalCount:%d per_receive_count:%d' % (receivedMessageCount, per_receive_count))

        self.messageCount += 1
        currentMessageCount = copy.copy(self.messageCount)
        if currentMessageCount % 100 == 0:
            logging.info('user %s receive %s messages ' % (self.xmlstream.client.userjid, currentMessageCount))

        if sender is None or sender.userhost() == self.xmlstream.client.userjid.userhost():
            return
