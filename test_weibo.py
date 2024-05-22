"""
@Time: 2024/5/14 21:00
@Auth: coin
@Email: 918731093@qq.com
@File: test_weibo.py
@IDE: PyCharm
@Motto：one coin
"""
import uiautomator2
from ez_android_automator.client import PublishClient

client = PublishClient(uiautomator2.connect_usb())
print(client.dump_xml())
exit()
