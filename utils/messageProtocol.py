# -*- coding: utf-8 -*-

# @Time : 2021/10/19 18:04
# @Author : Mandy

from __future__ import print_function
import sys
from imp import reload

reload(sys)  # 重新加载sys
sys.setdefaultencoding('utf8')

from twisted.words.protocols.jabber.xmlstream import XMPPHandler


# 定义消息协议
class MessageProtocol(XMPPHandler):
    """
    Generic XMPP subprotocol handler for incoming message stanzas.
    """

    messageTypes = None, 'normal', 'chat', 'headline', 'groupchat'

    def connectionInitialized(self):
        self.xmlstream.addObserver("/message", self._onMessage)

    def _onMessage(self, message):
        if message.handled:
            return

        messageType = message.getAttribute("type")

        if messageType == 'error':
            return

        if messageType not in self.messageTypes:
            message["type"] = 'normal'

        self.onMessage(message)

    def onMessage(self, message):
        """
        Called when a message stanza was received.
        """
