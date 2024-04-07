"""
@Time: 2024/2/29 19:00
@Auth: coin
@Email: 918731093@qq.com
@File: xigua_task.py
@IDE: PyCharm
@Motto：one coin
"""
import time
from typing import Callable

from ez_android_automator.client import Stage, PublishTask, DownloadMediaStage, PublishClient, AndroidClient, \
    WaitCallBackStage, PhoneLoginTask, PasswordLoginTask


class OpenAppStage(Stage):
    def __init__(self, serial, clear_data: bool = False):
        self.clear_data = clear_data
        super().__init__(serial)

    def run(self, client: PublishClient):
        client.restart_app("com.ss.android.article.video", self.clear_data)
        if self.clear_data:
            time.sleep(1)
            client.wait_to_click({'text': '同意'})
            client.wait_to_click({'text': '取消'})
            client.wait_to_click({'text': '允许'})


class PressPublishButtonStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({'text': '发视频'})


class ChooseFirstVideoStage(Stage):
    def run(self, client: PublishClient):
        client.device.sleep(1)
        client.device.click(300, 500)
        client.wait_to_click({'text': '去发布'})


class SetVideoOptionsStage(Stage):
    def __init__(self, serial, content: str):
        super().__init__(serial)
        self.content = content

    def run(self, client: PublishClient):
        client.wait_to_click({'text': '输入标题 (必填）'})
        client.device.send_keys(self.content)
        client.device.keyevent('back')
        client.wait_to_click({'text': '发布'})


class BeforeLoginStage(Stage):
    def __init__(self, serial, phone: str):
        super().__init__(serial)
        self.phone = phone

    def run(self, client: AndroidClient):
        client.wait_to_click({'text': '我的'})
        client.wait_to_click({'text': '其他登录方式'})
        client.wait_to_click({'text': '输入手机号'})
        client.device.send_keys(self.phone)
        client.wait_to_click({'text': '登录'})
        client.wait_to_click({'text': '同意'})


class PasswordLoginStage(Stage):
    def __init__(self, serial, account, password):
        super().__init__(serial)
        self.account = account
        self.password = password

    def run(self, client: AndroidClient):
        client.wait_to_click({'text': '我的'})
        client.wait_to_click({'text': '其他登录方式'})
        client.wait_to_click({'text': '密码登录'})
        client.wait_to_click({'text': '输入手机号'})
        client.device.send_keys(self.account)
        client.wait_to_click({'text': '请输入密码'})
        client.device.send_keys(self.password)
        client.wait_to_click({'text': '登录'})
        client.wait_to_click({'text': '同意'})
        client.wait_to_click({'text': '下次再说'})


class PhoneAuthCodeStage(Stage):
    def __init__(self, serial):
        super().__init__(serial)
        self.code = None

    def run(self, client: AndroidClient):
        client.device.send_keys(self.code)

    def code_callback(self, code: str):
        self.code = code


class CompleteStage(Stage):
    def run(self, client: AndroidClient):
        client.wait_to_click({'text': '下次再说'})


class XiguaPublishVideoTask(PublishTask):
    """
    Publish a video on Xigua.
    """

    def __init__(self, priority: int, title: str, content: str, video: str):
        super().__init__(priority, title, content, video, '')
        self.stages.append(DownloadMediaStage(0, video))
        self.stages.append(OpenAppStage(1))
        self.stages.append(PressPublishButtonStage(2))
        self.stages.append(ChooseFirstVideoStage(3))
        self.stages.append(SetVideoOptionsStage(4, self.content))


class XiguaPhoneLoginTask(PhoneLoginTask):
    def __init__(self, phone: str, callback: Callable[[], str]):
        super().__init__(phone, callback)
        self.stages.append(OpenAppStage(0, True))
        self.stages.append(BeforeLoginStage(1, phone))
        auth_stage = PhoneAuthCodeStage(3)
        self.stages.append(WaitCallBackStage(2, 60, callback, auth_stage.code_callback))
        self.stages.append(auth_stage)
        self.stages.append(CompleteStage(4))


class XiguaPasswordLoginTask(PasswordLoginTask):
    def __init__(self, account: str, password: str):
        super().__init__(account, password)
        self.stages.append(OpenAppStage(0, True))
        self.stages.append(PasswordLoginStage(1, account, password))
