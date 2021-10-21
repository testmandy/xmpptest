# -*- coding: utf-8 -*-

# @Time : 2021/10/20 17:08
# @Author : Mandy
from __future__ import print_function
import random
import sys
import time
from imp import reload
import conftest
from twisted.internet import reactor
import uuid

reload(sys)  # 重新加载sys
sys.setdefaultencoding('utf8')

sendedMessageCount = 0
start_time = ''
end_time = ''

class SendSingleMessage(object):
    def genTextMessage(self, sender, recipient, content):
        messageid = str(uuid.uuid4())
        currenttime = str(int(time.time() * 1000))
        textMessage = conftest.SINGLE_TEXT_MESSAGE % (
            messageid, recipient, sender, content, messageid, recipient, currenttime)

        return textMessage

    # 开始发送消息
    def startSend(self, count, interval, total):
        print('-----------------starting send message-----------------')
        if len(conftest.xmppclientlist) < count:
            reactor.callLater(5, self.startSend, count, interval, total)
            print ('case1--xmppclientlist:%s count:%d' % (conftest.xmppclientlist, count))
        else:
            print ('case2--xmppclientlist:%s count:%d' % (conftest.xmppclientlist, count))
            reactor.callLater(interval / 1000.0, self.startSend, count, interval, total)
            print('-----------------starting send message in reactor-----------------')
            si = random.randrange(count)
            sender = conftest.xmppclientlist[si]
            ri = random.randrange(count)
            # 确保不是密云消息
            while ri == si:
                print('-----------------ri==si,recreate-----------------')
                ri = random.randrange(count)

            receiver = conftest.xmppclientlist[ri]
            content = "%s to %s : " % (sender.userjid.userhost(), receiver.userjid.userhost())
            msg = self.genTextMessage(sender.userjid.userhost(), receiver.userjid.userhost(), content)
            global sendedMessageCount
            sendedMessageCount += 1
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            if sendedMessageCount == 1:
                conftest.start_time = now
            elif sendedMessageCount == total:
                conftest.sendAll = total
                conftest.end_time = now

            if sendedMessageCount <= total:
                sender.xmlstream.send(msg)
                print ('sendmessage:%s'%msg)
            else:
                sendedMessageCount -= 1
                print('sendedMessageCount:%d total:%d' % (sendedMessageCount, total))
                time.sleep(2)
                reactor.stop()

