"""
@Time: 2023/11/17 12:21
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: client.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.

This file contains ez_android_automator classes and helper functions relating Client, Task and Exception.
"""
import os
import threading
import warnings
from typing import Callable, Any, Union

import bs4
import uiautomator2
from bs4 import BeautifulSoup
import time
from .util import posix_path_join


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


class ClientWaitTimeout(TimeoutError):
    def __init__(self):
        super().__init__("Client wait too long to do detection on this task.")


class PhoneLoginException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class AndroidClient:
    """
    Base client for controlling android devices
    """

    def __init__(self, device: uiautomator2.Device):
        self.rs = None
        self.device = device
        self.xml = ''
        self.task = None
        self.task: ClientTask
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
        Start app using Activity Manager. Used only when app_start() failed to function.
        :param package_name: package name of the app
        :return: None
        """
        self.device.shell('am start -n {}/{}.main.MainActivity'.format(package_name, package_name))

    def shell(self, cmd: Union[str, list[str]], su: bool = False, print_ret: bool = False):
        if su:
            ret = self.su_shell(cmd)
        else:
            ret = self.device.shell(cmd)
        if ret.exit_code != 0:
            raise RuntimeError('Shell exit code not zero: {}'.format(ret.exit_code))
        if print_ret:
            print(ret.output)
        return ret

    def su_shell(self, cmd: Union[str, list[str]]):
        """
        Execute command as root user. Use only on rooted clients.
        """
        if isinstance(cmd, str):
            return self.device.shell(f"su -c {cmd}")
        elif isinstance(cmd, list):
            return self.device.shell(['su', '-c'] + cmd)

    def is_symbolic_link(self, path: str, su: bool = False) -> bool:
        ret = self.shell(['file', path], su).output.strip()
        if ret == f'{path}: cannot open':
            raise FileNotFoundError(path)
        return ret == f'{path}: symbolic link'

    def mkdir(self, path: str, su: bool = False, exists_ok: bool = False):
        if self.exists(path):
            if not exists_ok:
                raise FileExistsError(path)
        else:
            self.shell(['mkdir', path], su)

    def rmdir(self, path: str, su: bool = False, force: bool = False):
        if not self.exists(path):
            raise FileNotFoundError(path)
        cmd_lst = ['rm', '-r', path]
        if force:
            cmd_lst.insert(1, '-f')
        self.shell(cmd_lst, su)

    def exists(self, path: str, su: bool = False):
        try:
            self.is_file(path, su)
            return True
        except FileNotFoundError:
            return False

    def is_file(self, path: str, su: bool = False) -> bool:
        """
        Test if a path is file.
        Args:
            path (str): path to be teste.d
            su: use superuser
        Returns:
             True if the path is file, False is directory.
        Raises:
            FileNotFoundError
        """
        ret = self.shell(['file', path], su).output.strip()
        if ret == f'{path}: cannot open':
            raise FileNotFoundError(path)
        if ret == f'{path}: symbolic link':
            next_path = self.shell(['readlink', path], su).output.strip()
            if next_path == path:
                raise RuntimeError(f'Recursive symbolic link detected on path {path}')
            return self.is_file(next_path)
        return ret != f'{path}: directory'

    def is_dir(self, path: str) -> bool:
        return not self.is_file(path)

    def ls(self, path: str, su: bool = False) -> list[str]:
        """
        List files in a directory.
        Raises:
            RuntimeError
        """
        if self.is_file(path, su):
            raise RuntimeError(f'Path {path} is a file.')
        res = []
        for output in self.shell(['ls', path], su).output.split('\n'):
            if output != '':
                res.append(output.strip())
        return res

    def pull(self, src: str, dst: str, su: bool = False, skip_not_found: bool = True) -> None:
        basename = os.path.basename(src)
        if self.is_file(src, su):
            print(src)
            try:
                self.device.pull(src, posix_path_join(dst, basename))
            except FileNotFoundError as e:
                if not skip_not_found:
                    raise e
        else:
            os.makedirs(posix_path_join(dst, basename), exist_ok=True)
            for file_name in self.ls(src, su):
                next_path = posix_path_join(src, file_name)
                self.pull(next_path, posix_path_join(dst, basename), su)

    def push(self, src: str, dst: str, su: bool = False) -> None:
        basename = os.path.basename(src)
        if os.path.isfile(src):
            print(src)
            self.device.push(src, posix_path_join(dst, basename))
        else:
            self.mkdir(posix_path_join(dst, basename), su, exists_ok=True)
            for file_name in os.listdir(src):
                next_path = posix_path_join(src, file_name)
                self.push(next_path, posix_path_join(dst, basename), su)

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

    def run_current_task(self, failure_callback: Callable = None, clear_task: bool = True):
        self.task.run(self)
        if not self.task.is_finished and failure_callback is not None:
            failure_callback(self)
        if clear_task:
            self.task = None

    def run_current_task_async(self, failure_callback: Callable = None, clear_task: bool = True):
        threading.Thread(target=self.run_current_task, args=(failure_callback, clear_task,)).start()

    def set_task(self, task):
        self.task = task

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


class CallbackWaitTimeoutException(TimeoutError):
    def __init__(self, stage_serial):
        super().__init__(f"Wait too long on this callback. Stage:{stage_serial}")


class InvalidStageSerialException(Exception):
    def __init__(self, stage):
        super().__init__(f"Invalid stage serial for stage '{type(stage).__name__}'."
                         "Using a wrong stage serial can cause unexpected execution sequence for stages in a task."
                         "Assign valid stage serial in [0, n-1]")


class ClientTask:
    def __init__(self, priority: int = 3):
        self.callback = None
        self.stages = list[Stage]()
        self.current_stage = -1
        self.exception = None
        self.finished = False
        self.exception: Exception
        self.callback: Callable
        self.handler = None
        self.handler: Callable
        self.priority = priority
        self.sub_task = False

    def run(self, client: AndroidClient):
        if self.handler is None and not self.sub_task:
            warnings.warn(f'Handler for task {type(self).__name__} has not been implemented yet.'
                          'This may cause a crash when using manager to dispatch tasks.')
        for i, stage in enumerate(self.stages):
            self.current_stage = i
            try:
                stage.run(client)
            except Exception as e:
                self.exception = e
                if self.handler is not None:
                    if not self.handler(client, self, e):
                        break
                else:
                    raise e
        self.finished = True
        if self.callback is not None:
            self.callback(client, self)

    def __lt__(self, other):
        return self.priority < other.priority

    def get_stage(self):
        return self.current_stage

    def is_going(self):
        return -1 < self.current_stage < len(self.stages) and not self.is_exception()

    def is_finished(self):
        return self.finished

    def is_exception(self):
        return self.exception is not None

    def append(self, stage: Stage):
        if len(self.stages) != stage.stage_serial:
            raise InvalidStageSerialException(stage)
        self.stages.append(stage)

    def set_callback(self, callback: Callable[[AndroidClient, Any], None]):
        """
        This method set callback for the task, it will be called when a task is finished successfully.
        Implement a function with sign [(AndroidClient, ClientTask) -> None] to accept callback.
        """
        self.callback = callback

    def set_handler(self, handler: Callable[[AndroidClient, Any, Exception], bool]):
        """
        This method set callback for the task, it will be called when a task is interrupted by an exception.
        Implement a function with sign [(AndroidClient, ClientTask, Exception) -> bool] to handle exception.
        """
        self.handler = handler

    def shift_down_priority(self):
        self.current_stage = -1
        self.exception = None
        self.finished = False
        self.priority += 1

    def auto_serial(self):
        for i, stage in enumerate(self.stages):
            stage.stage_serial = i


class PublishTask(ClientTask):
    """
    Base abstract class for a publishing-type task
    """

    def __init__(self, priority: int, title: str, content: str, video: str, photo: str):
        super().__init__(priority)
        self.title = title
        self.content = content
        self.video = video
        self.photo = photo


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
        :param password: Password used to log in on apps.
        """
        self.account = account
        self.password = password
        super().__init__()


class PhoneLoginTask(LoginTask):
    """
    Base abstract class for using phone verify-code to login on apps.
    """

    def __init__(self, phone: str):
        """
        :param phone: User phone number
        """
        self.phone = phone
        self.code = None
        super().__init__()

    def get_code(self) -> str:
        return self.code

    def send_captcha(self, captcha):
        self.code = captcha
        pass


class StatisticTask(ClientTask):
    def __init__(self):
        super().__init__()
        self.statistic = None

    def statistic_callback(self, statistic: dict):
        self.statistic = statistic


class WaitCallBackStage(Stage):
    def __init__(self, stage_serial: int, max_wait_time: float, callback: Callable[[], str],
                 task_callback: Callable[[str], None]):
        self.max_wait_time = max_wait_time
        self.callback = callback
        self.task_callback = task_callback
        self.res = None
        super().__init__(stage_serial)
        self.signal_terminate = False

    def get_code_wrapper(self):
        c = None
        while c is None:
            c = self.callback()
            time.sleep(0.05)
            if self.signal_terminate:
                return
        self.task_callback(c)

    def terminate(self):
        self.signal_terminate = True

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
                    self.terminate()
                    raise CallbackWaitTimeoutException(self.stage_serial)


class StatisticFetcher(ClientTask):
    def __init__(self):
        super().__init__()
        pass


class TaskAsStage(Stage):
    """
    Use task as a stage. With this, you can combine tasks dependent on each others together.
    """

    def __init__(self, stage_serial: int, task: ClientTask):
        super().__init__(stage_serial)
        self.task = task
        self.task.sub_task = True

    def run(self, client: AndroidClient):
        self.task.run(client)
        if self.task.is_exception():
            raise self.task.exception


class CombinedSequentialTask(ClientTask):
    """
    Now you can execute sequential tasks dependent on each other together using this combined task.
    This is to assure that multiple tasks can be executed sequentially on same device when using manager.
    :example:  task = CombinedSequentialTask(TaskA(), TaskB(), TaskC())
    """

    def __init__(self, *args):
        super().__init__()
        for i, task in enumerate(args):
            self.append(TaskAsStage(i, task))


class StopAppStage(Stage):
    def __init__(self, stage_serial: int, pkg_name: str):
        super().__init__(stage_serial)
        self.pkg_name = pkg_name

    def run(self, client: AndroidClient):
        client.device.app_stop(self.pkg_name)


class StartAppStage(Stage):
    def __init__(self, stage_serial: int, pkg_name: str):
        super().__init__(stage_serial)
        self.pkg_name = pkg_name

    def run(self, client: AndroidClient):
        client.device.app_start(self.pkg_name)


class ClearAppStage(Stage):
    def __init__(self, stage_serial: int, pkg_name: str):
        super().__init__(stage_serial)
        self.pkg_name = pkg_name

    def run(self, client: AndroidClient):
        client.device.app_clear(self.pkg_name)
