"""
@Time: 2023/11/17 13:38
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: app.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
from client import AndroidClient
import shelve


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return _singleton


@singleton
class App:
    def __init__(self):
        self.clients = dict[str, AndroidClient]
        self.vault = shelve.open('vault')
        self.clients = self.vault['clients']

    def read_clients(self):
        pass
