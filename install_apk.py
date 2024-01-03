"""
@Time: 2024/1/3 18:36
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: install_apk.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import uiautomator2

from ez_android_automator.install_apk_task import InstallApk
from ez_android_automator.client import PublishClient, TestHandler

client = PublishClient(uiautomator2.connect('192.168.3.63:5555'))
client.set_task(InstallApk('./xhs.apk', 'com.xingin.xhs'))
client.set_exception_handler(TestHandler())
client.run_current_task()
pass
