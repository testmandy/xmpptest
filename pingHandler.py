# -*- coding: utf-8 -*-

# @Time : 2021/10/19 18:03
# @Author : Mandy
from __future__ import print_function
import sys
from dis import disco
from imp import reload
from twisted.words.protocols.jabber.xmlstream import XMPPHandler
from twisted.words.protocols.jabber.xmlstream import toResponse

reload(sys)  # 重新加载sys
sys.setdefaultencoding('utf8')

NS_PING = 'urn:xmpp:ping'
PING_REQUEST = "/iq[@type='get']/ping[@xmlns='%s']" % NS_PING


class PingHandler(XMPPHandler):
    """
    Ping responder.

    This handler waits for XMPP Ping requests and sends a response.
    """

    def connectionInitialized(self):
        """
        Called when the XML stream has been initialized.

        This sets up an observer for incoming ping requests.
        """
        self.xmlstream.addObserver(PING_REQUEST, self.onPing)

    def onPing(self, iq):
        """
        Called when a ping request has been received.

        This immediately replies with a result response.
        """
        response = toResponse(iq, 'result')
        self.xmlstream.send(response)
        iq.handled = True

    def getDiscoInfo(self, requestor, target, nodeIdentifier=''):
        """
        Get identity and features from this entity, node.

        This handler supports XMPP Ping, but only without a nodeIdentifier
        specified.
        """
        if not nodeIdentifier:
            return [disco.DiscoFeature(NS_PING)]
        else:
            return []

    def getDiscoItems(self, requestor, target, nodeIdentifier=''):
        """
        Get contained items for this entity, node.

        This handler does not support items.
        """
        return []
