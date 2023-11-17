"""
@Time: 2023/11/17 12:21
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: client.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.

This file contains classes and helper functions relating wrapped uiautomator2 client.
"""
import bs4
import uiautomator2
from bs4 import BeautifulSoup
import time


def create_network_client(addr):
    return AndroidClient(uiautomator2.connect(addr))


def create_usb_client(serial: str = None, init: bool = False):
    return AndroidClient(uiautomator2.connect_usb(serial, init))


"""
Base client for controlling android device
"""


class AndroidClient:
    def __init__(self, device: uiautomator2.Device):
        self.device = device
        self.xml = ''

    def dump_xml(self):
        return self.device.dump_hierarchy()

    def refresh_xml(self):
        self.xml = self.dump_xml()

    def find_xml_by_attr(self, attrs) -> bs4.ResultSet:
        parser = BeautifulSoup(self.xml, 'xml')
        return parser.find_all(attrs=attrs)

    """
    Block current thread until this client reached its destination.
    @param bool_func Pass in a quick detection lambda function to check if the condition is full filled, which will end
    this loop.
    @param refresh_xml Deside if this client's xml will be refreshed in every loop. 
    """

    def wait_until_finish(self, bool_func, refresh_xml: bool = True, timeout=5):
        start_time = time.time()
        while True:
            if refresh_xml:
                self.refresh_xml()
            if bool_func():
                return True
            current_time = time.time()
            if start_time + timeout < current_time:
                return False
            time.sleep(0.1)

    """
    Click center on a set of coordinates, usually works on simple buttons.
    @param coordinates: (x1, x2, y1, y2)
    """
    def click_center(self, coordinates: (int, int, int, int)):
        x = (coordinates[0] + coordinates[1]) / 2
        y = (coordinates[2] + coordinates[3]) / 2
        self.device.click(x, y)


"""
Client for publishing content on social media.  
"""


class PublishClient(AndroidClient):
    def __init__(self, device: uiautomator2.Device):
        super().__init__(device)
