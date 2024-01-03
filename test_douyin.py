"""
@Time: 2023/11/17 12:21
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: test_douyin.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import uiautomator2
from ez_android_automator.client import PublishClient
from ez_android_automator.douyin_task import DouyinVideoPublishTask

client = PublishClient(uiautomator2.connect_usb())
client.set_task(DouyinVideoPublishTask('test', '', 'test.mp4'))
client.run_current_task()