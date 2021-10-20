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

import conftest
from textXMPPClient import genTestXMPPClients


if __name__ == '__main__':
    plainpwd = 'q11111111'
    m1 = hashlib.md5()
    m1.update(plainpwd.encode('utf-8'))
    password = m1.hexdigest()
    startindex = int(sys.argv[1])
    count = int(sys.argv[2])
    interval = int(sys.argv[3])
    domain = sys.argv[4]
    genTestXMPPClients(startindex, count, interval, domain, password, resource=conftest.resource)
    reactor.run()
