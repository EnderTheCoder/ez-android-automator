"""
@Time: 2023/11/30 15:32
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: unicom_starter.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
from ez_android_automator.unicom_http_api import UnicomExecutorClient


if __name__ == "__main__":
    executor = UnicomExecutorClient('http://111.17.174.85:2345')
    executor.import_devices_from_usb()
    executor.start()
