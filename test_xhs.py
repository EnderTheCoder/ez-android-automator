"""
@Time: 2023/11/20 15:57
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: test_xhs.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import uiautomator2
from ez_android_automator.client import PublishClient, TestHandler
from ez_android_automator.xhs_task import XhsPublishVideoTask

client = PublishClient(uiautomator2.connect_usb())
client.set_exception_handler(TestHandler())
client.set_task(XhsPublishVideoTask(5, '我总在', '忙忙碌碌寻宝藏', 'http://192.168.3.32:8000/media/video/17060924290060.mp4'))
client.run_current_task()
pass
XhsPublishVideoTask()
