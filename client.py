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


def parse_coordinates(bounds: str):
    coordinates = []
    temp = ""
    coordinate_flag = False
    for c in bounds:
        if '0' <= c <= '9':
            temp = temp + c
            coordinate_flag = True
        elif coordinate_flag:
            coordinate_flag = False
            coordinates.append(int(temp))
            temp = ""
    x1 = coordinates[0]
    y1 = coordinates[1]
    x2 = coordinates[2]
    y2 = coordinates[3]
    return x1, x2, y1, y2


class ClientWaitTimeout(Exception):
    def __init__(self):
        super().__init__("Client wait too long to do detection on this task.")


class AndroidClient:
    """
    Base client for controlling android device
    """

    def __init__(self, device: uiautomator2.Device):
        self.rs = None
        self.device = device
        self.xml = ''

    def dump_xml(self):
        return self.device.dump_hierarchy()

    def refresh_xml(self):
        self.xml = self.dump_xml()

    def find_xml_by_attr(self, attrs) -> bs4.ResultSet:
        parser = BeautifulSoup(self.xml, 'xml')
        self.rs = parser.find_all(attrs=attrs)
        return self.rs

    def wait_until_finish(self, bool_func, refresh_xml: bool = True, timeout=5):
        """
        Block current thread until this client reached its destination.
        Args:
            bool_func: Pass in a quick detection lambda function to check if the condition is fulfilled, which will end
            this loop.
            refresh_xml: Deside if this client's xml will be refreshed in every loop.
            timeout: Max time to wait on this blocking.
        """
        start_time = time.time()
        while True:
            if refresh_xml:
                self.refresh_xml()
            if bool_func(self):
                return
            current_time = time.time()
            if start_time + timeout < current_time:
                raise ClientWaitTimeout()
            time.sleep(0.1)

    def click_center(self, coordinates: (int, int, int, int)):
        """
            Click center on a set of coordinates, usually works on simple buttons.
            Args:
                coordinates: (x1, x2, y1, y2)
        """
        x = (coordinates[0] + coordinates[1]) / 2
        y = (coordinates[2] + coordinates[3]) / 2
        self.device.click(x, y)

    def click_xml_node(self, node):
        self.click_center(parse_coordinates(node['bounds']))


class PublishClient(AndroidClient):
    """
    Client for publishing content on social media.
    """

    def __init__(self, device: uiautomator2.Device):
        super().__init__(device)
        self.task = None

    def copy_media_to_gallery(self, media_path):
        """
        Copy file to target's gallery.
        """

        gallery_path = "/sdcard/DCIM/Camera/"
        self.device.push(media_path, gallery_path + media_path.split('/')[-1])

    def run_current_task(self):
        self.task.run(self)

    def set_task(self, task):
        self.task = task


class Stage:
    def __init__(self, stage_serial):
        self.stage_serial = stage_serial

    def run(self, client: PublishClient):
        pass

    def get_serial(self):
        return self.stage_serial


class PublishTask:
    def __init__(self, title: str, content: str, video: str, photo: str):
        self.title = title
        self.content = content
        self.video = video
        self.photo = photo
        self.stages = list[Stage]()
        self.current_stage = -1
        self.exception = None

    def run(self, client: PublishClient):
        try:
            for i, stage in enumerate(self.stages):
                self.current_stage = i
                stage.run(client)
        except Exception as e:
            self.exception = e

    def get_stage(self):
        return self.current_stage

    def is_going(self):
        return -1 < self.current_stage < len(self.stages) and not self.is_exception()

    def is_finished(self):
        return self.current_stage == len(self.stages)

    def is_exception(self):
        return self.exception is None


class OpenAppStage(Stage):
    """
    Use adb shell to start douyin.
    """

    def run(self, client: PublishClient):
        client.device.shell('am start -n com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.main.MainActivity')


class ClickPublishButtonStage(Stage):
    """
    Wait until the app is up and click the publish button to enter gallery.
    """

    def run(self, client: PublishClient):
        def wait_main_page(client_: PublishClient) -> bool:
            return len(client_.find_xml_by_attr({'content-desc': '拍摄，按钮'})) > 0

        def enter_gallery(client_: PublishClient) -> bool:
            return len(client_.find_xml_by_attr({'text': '相册'})) > 0

        client.wait_until_finish(wait_main_page)
        client.click_xml_node(client.rs[0])
        client.wait_until_finish(enter_gallery)
        client.click_xml_node(client.rs[0])


class CopyVideoToGalleryStage(Stage):
    def run(self, client: PublishClient):
        client.copy_media_to_gallery('test.mp4')


class DouyinVideoPublishTask(PublishTask):
    def __init__(self, title: str, content, video):
        super().__init__(title, content, video, '')
        self.stages.append(OpenAppStage(0))
        self.stages.append(CopyVideoToGalleryStage(1))
        self.stages.append(ClickPublishButtonStage(2))
