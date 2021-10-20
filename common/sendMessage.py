# -*- coding: utf-8 -*-

# @Time : 2021/10/19 20:04
# @Author : Mandy
from __future__ import print_function
import random
import sys
import time
from datetime import datetime
from imp import reload
import conftest
from twisted.internet import reactor
import uuid

reload(sys)  # 重新加载sys
sys.setdefaultencoding('utf8')

sendedMessageCount = 0
start_time = ''
end_time = ''


class SendMessage(object):
    # 拼接群聊消息
    def genGroupTextMessage(self, sender, groupnamejid, content):
        messageid = str(uuid.uuid4())
        currenttime = str(int(time.time() * 1000))
        textMessage = conftest.GROUP_TEXT_MESSAGE % (
            messageid, groupnamejid, sender, content, messageid, groupnamejid, currenttime)

        return textMessage

    # 拼接群聊消息2
    def genGroupEncTextMessage(self, sender, groupnamejid):
        messageid = str(uuid.uuid4())
        currenttime = str(int(time.time() * 1000))
        textMessage = conftest.GROUP_ENC_TEXT_MESSAGE % (messageid, groupnamejid, sender, messageid, groupnamejid, currenttime)

        return textMessage

    # 开始发送消息，需要等所有的客户端生成以后才发送
    def startSendGroupMessage(self, count, interval, groupname, domain, total, source):
        if len(conftest.xmppclientlist) < count:
            reactor.callLater(5, self.startSendGroupMessage, count, interval, groupname, domain, total,
                              source)
        else:
            # 把下一次调度放到发送之前，确保调度开始的间隔受处理的影响小一点
            reactor.callLater(interval / 1000.0, self.startSendGroupMessage, count, interval, groupname, domain, total,
                              source)

            si = random.randrange(count)
            sender = conftest.xmppclientlist[si]
            global sendedMessageCount, start_time, end_time
            sendedMessageCount += 1
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            if sendedMessageCount == 1:
                start_time = now
            elif sendedMessageCount == total:
                conftest.sendAll = total
                end_time = now
                startTime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                endTime = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                duration = (endTime - startTime).seconds
                print('sendCount:%d startTime:%s endTime:%s duration:%ds' % (
                    sendedMessageCount, start_time, end_time, duration))
            content = "%s-%s测试sender %s; sendtime : %s;sendedCount: %s" % (
                source, sendedMessageCount, sender.userjid.userhost(), now, sendedMessageCount)
            msg = self.genGroupTextMessage(sender.userjid.userhost(), '%s@conference.%s' % (groupname, domain), content)

            if sendedMessageCount <= total:
                sender.xmlstream.send(msg)
            else:
                sendedMessageCount -= 1
                time.sleep(2)
                reactor.stop()
