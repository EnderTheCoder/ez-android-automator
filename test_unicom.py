"""
@Time: 2023/11/21 下午7:08
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: test_unicom.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import uiautomator2
from ez_android_automator.client import AndroidClient, TaskExceptionHandler
from ez_android_automator.unicom_task import UnicomSignTask


class TestHandler(TaskExceptionHandler):
    def handle(self, _client, task):
        print(client.xml)
        raise task.exception


client = AndroidClient(uiautomator2.connect_usb())
client.set_task(UnicomSignTask('152625198812114523', '御东新区文兴路璀璨天城9号楼11103'))
client.set_exception_handler(TestHandler())
client.run_current_task()
pass
