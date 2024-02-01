"""
@Time: 2024/1/30 15:00
@Auth: coin
@Email: 918731093@qq.com
@File: kuaishou_task.py
@IDE: PyCharm
@Motto：one coin
"""

import uiautomator2
from ez_android_automator.client import PublishClient, TestHandler
from ez_android_automator.kuaishou_task import KuaishouPublishVideoTask

client = PublishClient(uiautomator2.connect_usb())
client.set_exception_handler(TestHandler())
# print(client.dump_xml())
# exit()
client.set_task(
    KuaishouPublishVideoTask(5, '', '我总在忙忙碌碌寻宝藏', 'http://192.168.3.8:8000/media/videos/test1.mp4'))
client.run_current_task()
pass
