"""
@Time: 2024/3/26 20:00
@Auth: coin
@Email: 918731093@qq.com
@File: douyinhuoshan_task.py
@IDE: PyCharm
@Motto：one coin
"""

import uiautomator2
from ez_android_automator.client import PublishClient
from ez_android_automator.douyinhuoshan_task import DouyinhuoshanPublishVideoTask

client = PublishClient(uiautomator2.connect_usb())
# print(client.dump_xml())
# exit()
client.set_task(DouyinhuoshanPublishVideoTask(5, '', '我总在忙忙碌碌寻宝藏', 'http://192.168.3.8:8000/media/videos/test.mp4'))
client.run_current_task()