"""
@Time: 2024/3/6 11:00
@Auth: coin
@Email: 918731093@qq.com
@File: test_kuaishoujisu.py
@IDE: PyCharm
@Motto：one coin
"""

import uiautomator2
from ez_android_automator.client import PublishClient
from ez_android_automator.kauishoujisu_task import KuaishoujisuPublishVideoTask

client = PublishClient(uiautomator2.connect_usb())
# print(client.device.app_list())
print(client.dump_xml())
exit()
client.set_task(
    KuaishoujisuPublishVideoTask(5, '', '我总在忙忙碌碌寻宝藏', 'http://192.168.3.8:8000/media/videos/test.mp4'))
client.run_current_task()