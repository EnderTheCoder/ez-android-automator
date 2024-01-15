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
client.set_task(XhsPublishVideoTask('我的世界模组开发', '自己做的，测试', 'test4.mp4'))
client.run_current_task()
pass

