"""
@Time: 2023/11/17 12:21
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: client.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.

This file contains ez_android_automator classes and helper functions relating Client, Task and Exception.
"""
import threading
from typing import Callable

import bs4
import uiautomator2
from bs4 import BeautifulSoup
import time


def create_network_client(addr):
    return AndroidClient(uiautomator2.connect(addr))


def create_usb_client(serial: str = None, init: bool = False):
    return AndroidClient(uiautomator2.connect_usb(serial, init))


def parse_coordinates(bounds: str):
    """
    Parse bounds string in xml attribute 'bounds' and make a set of coordinates indicates two point on screen.
    :param bounds: bounds string in xml attribute 'bounds', example:[162,36][192,79]
    :return: a set of coordinates indicates two point on screen
    """
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


class PhoneLoginException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class TaskCallback:
    """
    Executed when a task is completed. Use this to pass data back to main system.
    """

    def run(self, task):
        pass


class TaskExceptionHandler:
    """
    Base abstract class for handling exception in execution of tasks. Extend this class to do handling.
    """

    def __init__(self):
        pass

    def handle(self, _client, task):
        """
        Override this method to handle the exception.
        :param _client: the client that throws the exception
        :param task: current task in execution
        :return:
        """
        pass


class TestHandler(TaskExceptionHandler):
    def handle(self, _client, task):
        raise task.exception


class DebugHandler(TaskExceptionHandler):

    def handle(self, _client, task):
        _client.device.screenshot("latest_failure.jpg")


class AndroidClient:
    """
    Base client for controlling android devices
    """

    def __init__(self, device: uiautomator2.Device):
        self.exception_handler = None
        self.rs = None
        self.device = device
        self.xml = ''
        self.task = None
        self.task: ClientTask
        self.exception_handler: TaskExceptionHandler
        self.rs: bs4.ResultSet
        self.occupied = False

    def restart_app(self, package_name: str, clear_data=False):
        """
        Restart app by package name. This will reset app state to open state.
        Notice: some apps cannot be started by app_start, use adb shell am instead.
        :param package_name: package name of the app
        :param clear_data: clear app data before open
        :return: None
        """
        self.device.app_stop(package_name)
        if clear_data:
            self.device.app_clear(package_name)
        self.device.app_start(package_name)

    def start_app_am(self, package_name: str):
        """
        Start app using Activity Manager. Used only when app_start() failed to work.
        :param package_name: package name of the app
        :return: None
        """
        self.device.shell('am start -n {}/{}.main.MainActivity'.format(package_name, package_name))

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
            this loop. It accepts only one param in type of AndroidClient.
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

    def wait_to_click(self, attr: dict, timeout=5, gap=0):
        """
        Use given params to find the right node and click it. This method is used on the most common situations.
        An exception will be thrown if it finds nothing using the given attr param.
        :param gap: the gap time in secs between finding and clicking.
        :param timeout: Max time to wait in secs on this element.
        :param attr: the attribute used on finding xml nodes.
        :return: None
        """

        self.wait_until_found(attr, timeout)
        time.sleep(gap)
        self.click_xml_node(self.rs[0])

    def wait_until_found(self, attr: dict, timeout=10):
        def bool_lambda(client_: AndroidClient):
            return len(client_.find_xml_by_attr(attr)) > 0

        self.wait_until_finish(bool_lambda, timeout=timeout)

    def run_current_task(self, failure_callback: Callable = None):
        self.task.run(self)
        if self.task.is_exception() and failure_callback is not None:
            failure_callback(self)
        self.task = None

    def set_task(self, task):
        self.task = task

    def set_exception_handler(self, handler: TaskExceptionHandler):
        self.exception_handler = handler

    def drag(self, slider: (int, int, int, int), rail: (int, int, int, int)):
        self.device.drag((slider[0] + slider[1]) / 2,
                         (slider[2] + slider[3]) / 2,
                         rail[1],
                         (rail[2] + rail[1]) / 2)

    def drag_node(self, slider, rail):
        self.drag(parse_coordinates(slider['bounds']), parse_coordinates(rail['bounds']))

    def simple_click(self, wait_before=0, wait_after=0):
        w, h = self.device.window_size()
        time.sleep(wait_before)
        self.device.click(w / 2, h / 2)
        time.sleep(wait_after)

    def lock(self):
        self.occupied = True

    def unlock(self):
        self.occupied = False

    def is_usable(self):
        return self.task is None or self.task.is_finished() or self.task.is_exception() and not self.lock

    def alive(self):
        return self.device.alive() and self.device.agent_alive()


class PublishClient(AndroidClient):
    """
    Client for publishing content on social media.
    """

    def __init__(self, device: uiautomator2.Device):
        super().__init__(device)

    def copy_media_to_gallery(self, media_path):
        """
        Copy file to target's gallery.
        """

        gallery_path = "/sdcard/DCIM/Camera/"
        remote_path = gallery_path + media_path.split('/')[-1]
        self.device.push(media_path, remote_path)
        self.device.shell(f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{remote_path}')


class Stage:
    """
    Base abstract class for a single step in a task.
    """

    def __init__(self, stage_serial: int):
        self.stage_serial = stage_serial

    def run(self, client: AndroidClient):
        pass

    def get_serial(self):
        return self.stage_serial


class CallbackWaitTimeoutException(Exception):
    def __init__(self, stage_serial):
        super().__init__(f"Wait too long on this callback. Stage:{stage_serial}")


class ClientTask:
    def __init__(self):
        self.stages = list[Stage]()
        self.current_stage = -1
        self.exception = None
        self.finished = False
        self.exception: Exception
        self.callback = None
        self.callback: TaskCallback

    def run(self, client: AndroidClient):
        try:
            for i, stage in enumerate(self.stages):
                self.current_stage = i
                stage.run(client)
        except Exception as e:
            self.exception = e
            if client.exception_handler is not None:
                client.exception_handler.handle(client, self)
        self.finished = True
        if self.callback is not None:
            self.callback.run(self)

    def get_stage(self):
        return self.current_stage

    def is_going(self):
        return -1 < self.current_stage < len(self.stages) and not self.is_exception()

    def is_finished(self):
        return self.finished

    def is_exception(self):
        return self.exception is not None

    def append(self, stage: Stage):
        self.stages.append(stage)

    def set_callback(self, callback: TaskCallback):
        self.callback = callback


class PublishTask(ClientTask):
    """
    Base abstract class for a publishing-type task
    """

    def __init__(self, priority: int, title: str, content: str, video: str, photo: str):
        super().__init__()
        self.priority = priority
        self.title = title
        self.content = content
        self.video = video
        self.photo = photo

    def shift_down_priority(self):
        self.current_stage = -1
        self.exception = None
        self.finished = False
        self.exception: Exception
        self.priority += 1


class LoginTask(ClientTask):
    """
    Base abstract class for logining on apps.
    """
    pass


class PasswordLoginTask(LoginTask):
    """
    Base abstract class for using password to login on apps.
    """

    def __init__(self, account: str, password: str):
        """
        :param account: Can be username or phone number, depends on real situations.
        :param password: Password used to login on apps.
        """
        self.account = account
        self.password = password
        super().__init__()


class PhoneLoginTask(LoginTask):
    """
    Base abstract class for using phone verify-code to login on apps.
    """

    def __init__(self, phone: str, verify_callback: Callable[[], str]):
        """
        :param phone: User phone number
        :param verify_callback: A callback function, will be called after the phone verification code has been fired.
        """
        self.phone = phone
        self.verify_callback = verify_callback
        self.code = None
        super().__init__()




class DownloadMediaStage(Stage):
    def __init__(self, serial, url: str):
        super().__init__(serial)
        self.url = url

    def run(self, client: AndroidClient):
        client.restart_app('com.sec.android.app.sbrowser')
        client.wait_to_click({'resource-id': 'com.sec.android.app.sbrowser:id/location_bar_edit_text'})
        print("self.urlself.urlself.urlself.url", self.url)
        client.device.send_keys(self.url)
        client.device.send_action('go')
        time.sleep(5)
        # client.device.click(972, 1902)
        # time.sleep(1)
        # client.device.click(972, 1902)
        # time.sleep(1)
        # client.device.click(972, 1902)
        client.device.click(1014, 1325)
        time.sleep(1)
        client.device.click(1014, 1325)
        time.sleep(1)
        client.device.click(1014, 1325)
        client.wait_to_click({'text': '下载'})
        client.wait_to_click({'text': '下载'})
        client.wait_until_found({'text': '打开文件'}, timeout=600)


class WaitCallBackStage(Stage):
    def __init__(self, stage_serial: int, max_wait_time: float, callback: Callable[[], str],
                 task_callback: Callable[[str], None]):
        self.max_wait_time = max_wait_time
        self.callback = callback
        self.task_callback = task_callback
        self.res = None
        super().__init__(stage_serial)

    def get_code_wrapper(self):
        self.task_callback(self.callback())

    def run(self, client: AndroidClient):
        t = threading.Thread(target=self.get_code_wrapper)
        t.start()
        current_wait_time = 0.0
        while True:
            if not t.is_alive():
                break
            else:
                time.sleep(0.1)
                current_wait_time += 0.1
                if current_wait_time > self.max_wait_time:
                    raise CallbackWaitTimeoutException(self.stage_serial)
