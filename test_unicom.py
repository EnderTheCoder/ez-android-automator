"""
@Time: 2023/11/21 下午7:08
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: test_unicom.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import uiautomator2
from ez_android_automator.client import AndroidClient
from ez_android_automator.unicom_task import UnicomSignTask, UnicomInstallTask

client = AndroidClient(uiautomator2.connect())
client.set_task(UnicomInstallTask())
client.run_current_task()
client.set_task(UnicomSignTask('420922198707274630', '恒大绿洲二期23号楼1单元1702'))
client.run_current_task()
pass
