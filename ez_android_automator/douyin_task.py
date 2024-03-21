"""
@Time: 2024/3/15 13:30
@Auth: coin
@Email: 918731093@qq.com
@File: douyin_task.py
@IDE: PyCharm
@Motto：one coin
"""
import time
from typing import Callable
from ez_android_automator.client import Stage, PublishTask, DownloadMediaStage, PublishClient, AndroidClient, \
    PhoneLoginTask, WaitCallBackStage, PasswordLoginTask, ClientWaitTimeout


class OpenAppStage(Stage):
    def __init__(self, serial, clear_data: bool = False):
        self.clear_data = clear_data
        super().__init__(serial)

    def run(self, client: PublishClient):
        client.device.app_stop('com.ss.android.ugc.aweme')
        if self.clear_data:
            client.device.app_clear('com.ss.android.ugc.aweme')
        client.device.shell('am start -n com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.main.MainActivity')
        if self.clear_data:
            client.wait_to_click({'text': '同意'})


class PressPublishButtonStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({'content-desc': '拍摄，按钮'})


class ChooseFirstVideoStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({'text': '相册'})
        client.wait_until_found({'text': '视频'})
        client.wait_to_click({'text': '视频'})
        time.sleep(2)
        client.device.click(200, 550)
        client.wait_to_click({'text': '下一步'})


class SetVideoOptionsStage(Stage):
    def __init__(self, serial, content: str):
        super().__init__(serial)
        self.content = content

    def run(self, client: PublishClient):
        client.wait_to_click({'text': '添加作品描述..'})
        client.device.send_keys(self.content)
        client.device.keyevent('back')
        client.find_xml_by_attr({'text': '发布'})
        client.click_xml_node(client.rs[0])


class BeforeLoginStage(Stage):
    def __init__(self, serial, phone: str):
        super().__init__(serial)
        self.phone = phone

    def run(self, client: AndroidClient):
        client.wait_to_click({'text': '我'})
        client.wait_to_click({'text': '请输入手机号'})
        client.device.send_keys(self.phone)
        client.wait_to_click({'text': '验证并登录'})
        time.sleep(0.5)
        client.wait_to_click({'text': '同意并登录'})


class PhoneAuthCodeStage(Stage):
    def __init__(self, serial):
        super().__init__(serial)
        self.code = None

    def run(self, client: AndroidClient):
        client.device.send_keys(self.code)
        client.wait_to_click({'text': '完成'})

    def code_callback(self, code: str):
        self.code = code


class PasswordLoginStage(Stage):
    def __init__(self, serial, account, password):
        super().__init__(serial)
        self.account = account
        self.password = password

    def run(self, client: AndroidClient):
        client.wait_to_click({'text': '我'})
        client.wait_to_click({'text': '密码登录'})
        client.device.send_keys(self.account)
        try:
            client.wait_to_click({'text': '请先勾选，同意后再进行登录'})
            client.wait_to_click({'text': '请输入密码'})
            client.device.send_keys(self.password)
        except ClientWaitTimeout as e:
            client.wait_to_click({'text': '请输入密码'})
            client.device.send_keys(self.password)
            client.wait_to_click({'text': '同意'})
        client.wait_to_click({'text': '登录'})


class DouyinVideoPublishTask(PublishTask):
    """
    Publish a video on Douyin.
    """

    def __init__(self, priority: int, title: str, content: str, video: str):
        super().__init__(priority, title, content, video, '')
        self.stages.append(DownloadMediaStage(0, video))
        self.stages.append(OpenAppStage(1))
        self.stages.append(PressPublishButtonStage(2))
        self.stages.append(ChooseFirstVideoStage(3))
        self.stages.append(SetVideoOptionsStage(4, self.content))


class DouyinPhoneLoginTask(PhoneLoginTask):
    def __init__(self, phone: str, callback: Callable[[], str]):
        super().__init__(phone, callback)
        self.stages.append(OpenAppStage(0, True))
        self.stages.append(BeforeLoginStage(1, phone))
        auth_stage = PhoneAuthCodeStage(3)
        self.stages.append(WaitCallBackStage(2, 60, callback, auth_stage.code_callback))
        self.stages.append(auth_stage)


class DouyinPasswordLoginTask(PasswordLoginTask):
    def __init__(self, account: str, password: str, callback: Callable[[], str]):
        super().__init__(account, password)
        self.stages.append(OpenAppStage(0, True))
        self.stages.append(PasswordLoginStage(1, account, password))
        auth_stage = PhoneAuthCodeStage(3)
        self.stages.append(WaitCallBackStage(2, 60, callback, auth_stage.code_callback))
        self.stages.append(auth_stage)
