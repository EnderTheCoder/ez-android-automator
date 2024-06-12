"""
@Time: 2024/1/30 15:00
@Auth: coin
@Email: 918731093@qq.com
@File: kuaishou_task.py
@IDE: PyCharm
@Motto：one coin
"""
import time
from typing import Callable
from ez_android_automator.client import Stage, PublishTask, PublishClient, AndroidClient, \
    PhoneLoginTask, WaitCallBackStage, ClientWaitTimeout, PasswordLoginTask, TaskAsStage
from ez_android_automator.idm_task import IDMPullTask


class OpenAppStage(Stage):
    def __init__(self, serial, clear_data: bool = False):
        self.clear_data = clear_data
        super().__init__(serial)

    def run(self, client: PublishClient):
        client.restart_app("com.smile.gifmaker", self.clear_data)
        if self.clear_data:
            client.wait_to_click({'text': '不同意'})
            time.sleep(1)
            client.wait_to_click({'text': '同意并继续'})


class PressPublishButtonStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({'resource-id': 'com.smile.gifmaker:id/shoot_container'}, gap=3)


class ChooseFirstVideoStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({'text': '相册'})
        client.wait_until_found({'text': '视频'})
        client.wait_to_click({'text': '视频'})
        client.wait_until_found({'text': '视频'})
        client.device.click(300, 440)
        client.wait_to_click({'text': '下一步(1)'})
        client.wait_until_found({'text': '下一步'})
        client.wait_to_click({'text': '下一步'})


class SetVideoOptionsStage(Stage):
    def __init__(self, serial, content: str):
        super().__init__(serial)
        self.content = content

    def run(self, client: PublishClient):
        client.wait_to_click({'text': '添加合适的话题和描述，作品能获得更多推荐'})
        client.device.send_keys(self.content)
        client.wait_to_click({'text': '发布'})


class BeforeLoginStage(Stage):
    def __init__(self, serial, phone: str):
        super().__init__(serial)
        self.phone = phone

    def run(self, client: AndroidClient):
        client.wait_to_click({'text': '我'})
        client.wait_to_click({'text': '请输入手机号'})
        client.device.send_keys(self.phone)
        client.wait_to_click({'text': '获取验证码'})
        try:
            client.wait_to_click({'text': '同意'})
        except ClientWaitTimeout as e:
            pass


class PhoneAuthCodeStage(Stage):
    def __init__(self, serial):
        super().__init__(serial)
        self.code = None

    def run(self, client: AndroidClient):
        client.device.send_keys(self.code)
        client.wait_to_click({'text': '登录'})
        try:
            client.wait_to_click({'text': '同意并登录'})
        except ClientWaitTimeout as e:
            pass

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
        client.wait_to_click({'text': '请输入密码'})
        client.device.send_keys(self.password)
        client.wait_to_click({'text': '登录'})
        time.sleep(0.5)
        client.wait_to_click({'text': '同意并登录'})


class KuaishouPublishVideoTask(PublishTask):
    """
    Publish a video on Kuaishou.
    """

    def __init__(self, priority: int, title: str, content: str, video: str):
        super().__init__(priority, title, content, video, '')
        task = IDMPullTask(video)
        self.stages.append(TaskAsStage(0, task))
        self.stages.append(OpenAppStage(1))
        self.stages.append(PressPublishButtonStage(2))
        self.stages.append(ChooseFirstVideoStage(3))
        self.stages.append(SetVideoOptionsStage(4, self.content))


class KuaishouPhoneLoginTask(PhoneLoginTask):
    def __init__(self, phone: str):
        super().__init__(phone)
        self.stages.append(OpenAppStage(0, True))
        self.stages.append(BeforeLoginStage(1, phone))
        auth_stage = PhoneAuthCodeStage(3)
        self.stages.append(WaitCallBackStage(2, 60, self.get_code, auth_stage.code_callback))
        self.stages.append(auth_stage)


class KuaishouPasswordLoginTask(PasswordLoginTask):
    def __init__(self, account: str, password: str):
        super().__init__(account, password)
        self.stages.append(OpenAppStage(0, True))
        self.stages.append(PasswordLoginStage(1, account, password))
