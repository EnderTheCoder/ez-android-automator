"""
@Time: 2024/7/27 7:19
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: test_damai.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""

from ez_android_automator.client import create_network_client
from ez_android_automator.damai_task import DaMaiBuyTask

client = create_network_client('192.168.3.51:32963')
client.set_task(
    DaMaiBuyTask([('祁佩璇', '152701199203060928'), ('刘淑华', '652801197611293928'), ('陈蓓', '310104198910012423')],
                 "小沈阳2024", None, 0, 3))
client.run_current_task()
