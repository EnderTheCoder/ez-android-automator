"""
@Time: 2024/7/27 7:19
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: test_damai.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""

from ez_android_automator.client import create_usb_client
from ez_android_automator.damai_task import DaMaiBuyTask

client = create_usb_client()
client.set_task(DaMaiBuyTask("张杰", "苏州"))
client.run_current_task()
