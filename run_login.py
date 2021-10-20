#!/usr/bin/python
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
from twisted.internet import reactor
from twisted.words.protocols.jabber.jid import JID
from textXMPPClient import genTestXMPPClients


# def main(reactor, jid, secret):
#     """
#     Connect to the given Jabber ID and return a L{Deferred} which will be
#     called back when the connection is over.
#
#     @param reactor: The reactor to use for the connection.
#     @param jid: A L{JID} to connect to.
#     @param secret: A C{str}
#     """
#     return Client(reactor, JID(jid), secret).finished


if __name__ == '__main__':
    plainpwd = 'q11111111'

    m1 = hashlib.md5()
    m1.update(plainpwd.encode('utf-8'))
    password = m1.hexdigest()

    startindex = int(sys.argv[1])
    count = int(sys.argv[2])
    interval = int(sys.argv[3])
    domain = sys.argv[4]
    resource = 'desktop.win.dc40936d9ed9641c59bf3c37033a2bc4_2db15f9a6d1516f219df1ed0ee7001c7_202b82fb150e0c0a94bfdd945093eb20'

    # Client(reactor, JID(jid), secret)

    genTestXMPPClients(startindex, count, interval, domain, password, resource=resource)
    reactor.run()
