# -*- coding: utf-8 -*-

# @Time : 2021/10/19 18:02
# @Author : Mandy
from __future__ import print_function
import sys
from imp import reload


reload(sys) #重新加载sys
sys.setdefaultencoding('utf8')

xmppclientlist = []
sendAll = 0
resource = 'desktop.win.dc40936d9ed9641c59bf3c37033a2bc4_2db15f9a6d1516f219df1ed0ee7001c7_202b82fb150e0c0a94bfdd945093eb20'

GROUP_TEXT_MESSAGE = """<message xmlns="" id="%s" type="groupchat" to="%s" from="%s">
<body>%s</body>
<properties xmlns="http://www.jivesoftware.com/xmlns/xmpp/properties">
<property><name>message.prop.type</name><value type="string">message.prop.type.chat</value></property>
<property><name>message.prop.destroy</name><value type="string">never_burn</value></property>
<property><name>message.prop.chattype</name><value type="string">group</value></property>
<property><name>message.prop.id</name><value type="string">%s</value></property>
<property><name>message.prop.security</name><value type="string">plain</value></property>
<property><name>message.prop.with</name><value type="string">%s</value></property>
<property><name>message.prop.akey</name><value type="string">akey.sw</value></property>
<property><name>message.prop.im.msgtype</name><value type="string">text</value></property>
<property><name>message.prop.encryptVer</name><value type="string">1</value></property>
<property><name>message.prop.timestamp</name><value type="string">%s</value></property>
</properties></message>"""

GROUP_ENC_TEXT_MESSAGE = """<message xmlns="" id="%s" type="groupchat" to="%s" from="%s">
<body>CAAS0AFbz8NFRVM/Mx2Nbhutt2BJgZP6hSrtFaD9auzYgy9CP0DzEz6gYAl2tFLXMIrozwaMRaXlm5BFeEe2BPpWD5Dd6/vWpI7cr/fEt+kl7nJxW4D7eSJdIK8rNC+moNeOtZU6i/xjJpzCjgtSR2X71PVIk9kHQnzCIGQTL1WWvcV+rYsGd2Fcum7gt9kWtyPqORVshsvZHODdBkpwZ4mDhNsJ7RnW6qy8s0WRGyA0aCe3S46ugSbQVOIP1Bo4MMCk0QTIpdJVTjSD+xqy3QiwXVPbGiAEiIHYnYtqjNUXe/EY2N3AUPbQ+P0hGctyh1WhrB6BuA==</body>
<properties xmlns="http://www.jivesoftware.com/xmlns/xmpp/properties">
<property><name>message.prop.type</name><value type="string">message.prop.type.chat</value></property>
<property><name>message.prop.destroy</name><value type="string">never_burn</value></property>
<property><name>message.prop.chattype</name><value type="string">group</value></property>
<property><name>message.prop.id</name><value type="string">%s</value></property>
<property><name>message.prop.security</name><value type="string">encryption</value></property>
<property><name>message.prop.with</name><value type="string">%s</value></property>
<property><name>message.prop.akey</name><value type="string">akey.sw</value></property>
<property><name>message.prop.im.msgtype</name><value type="string">text</value></property>
<property><name>message.prop.encryptVer</name><value type="string">1</value></property>
<property><name>message.prop.timestamp</name><value type="string">%s</value></property>
</properties></message>"""




