"""
@Time: 2024/2/29 19:30
@Auth: coin
@Email: 918731093@qq.com
@File: test_xigua.py
@IDE: PyCharm
@Motto：one coin
"""

import uiautomator2
from ez_android_automator.client import PublishClient, TestHandler
from ez_android_automator.xigua_task import XiguaPublishVideoTask

client = PublishClient(uiautomator2.connect_usb())
client.set_exception_handler(TestHandler())
# print(client.device.app_list())
# print(client.dump_xml())
# exit()
client.set_task(
    XiguaPublishVideoTask(5, '', '我总在忙忙碌碌寻宝藏', 'http://192.168.3.8:8000/media/videos/test.mp4'))
client.run_current_task()