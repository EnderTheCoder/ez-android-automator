"""
@Time: 2023/11/20 15:57
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: xhs_task.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import time
from ez_android_automator.client import PublishTask, Stage, PublishClient, PhoneLoginTask, \
    PasswordLoginTask, AndroidClient, WaitCallBackStage, TaskAsStage
from ez_android_automator.idm_task import IDMPullTask


class OpenAppStage(Stage):

    def __init__(self, serial, clear_data: bool = False):
        self.clear_data = clear_data
        super().__init__(serial)

    def run(self, client: PublishClient):
        client.restart_app('com.xingin.xhs', self.clear_data)
        if self.clear_data:
            client.wait_to_click({'text': '同意'})


class PressPublishButtonStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({'content-desc': '发布'})


class ChooseFirstVideoStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({'text': '视频'}, gap=1)
        client.wait_until_found({'text': '视频'})
        client.device.click(310, 445)
        client.wait_to_click({'content-desc': '下一步'})
        client.wait_to_click({'text': '下一步'})


class SetVideoOptionsStage(Stage):
    def __init__(self, serial, title: str, content: str):
        super().__init__(serial)
        self.title = title
        self.content = content

    def run(self, client: PublishClient):
        client.wait_to_click({'text': '填写标题会有更多赞哦～'})
        client.device.send_keys(self.title)
        client.wait_to_click({'text': '添加正文'})
        client.device.send_keys(self.content)
        client.key_back()
        client.wait_to_click({'text': '发布笔记'})


class BeforeLoginStage(Stage):
    def __init__(self, serial, phone: str):
        super().__init__(serial)
        self.phone = phone

    def run(self, client: AndroidClient):
        client.wait_to_click({'text': '手机号登录'})
        client.wait_to_click({'text': '请输入手机号码'})
        client.device.send_keys(self.phone)
        client.wait_to_click({'text': '验证并登录'})
        time.sleep(0.5)
        client.wait_to_click({'text': '同意并继续'})


class PhoneAuthCodeStage(Stage):
    def __init__(self, serial):
        super().__init__(serial)
        self.code = None

    def run(self, client: AndroidClient):
        client.wait_to_click({'text': '输入验证码'})
        client.device.send_keys(self.code)

    def code_callback(self, code: str):
        self.code = code


class PasswordLoginStage(Stage):
    def __init__(self, serial, account, password):
        super().__init__(serial)
        self.account = account
        self.password = password

    def run(self, client: AndroidClient):
        client.wait_to_click({'text': '手机号登录'})
        client.wait_to_click({'text': '密码登录'})
        client.device.send_keys(self.account)
        client.wait_to_click({'text': '输入密码'})
        client.device.send_keys(self.password)
        client.wait_to_click({'text': '登录'})
        time.sleep(0.5)
        client.wait_to_click({'text': '同意并继续'})


class XhsPublishVideoTask(PublishTask):
    """
    Publish a video on Xiaohongshu.
    """

    def __init__(self, priority: int, title: str, content: str, video: str):
        super().__init__(priority, title, content, video, '')
        task = IDMPullTask(video)
        self.stages.append(TaskAsStage(0, task))
        self.stages.append(OpenAppStage(1))
        self.stages.append(PressPublishButtonStage(2))
        self.stages.append(ChooseFirstVideoStage(3))
        self.stages.append(SetVideoOptionsStage(4, self.title, self.content))


class XhsPhoneLoginTask(PhoneLoginTask):
    def __init__(self, phone: str):
        super().__init__(phone)
        self.stages.append(OpenAppStage(0, True))
        self.stages.append(BeforeLoginStage(1, phone))
        auth_stage = PhoneAuthCodeStage(3)
        self.stages.append(WaitCallBackStage(2, 60, self.get_code, auth_stage.code_callback))
        self.stages.append(auth_stage)


class XhsPasswordLoginTask(PasswordLoginTask):
    def __init__(self, account: str, password: str):
        super().__init__(account, password)
        self.stages.append(OpenAppStage(0, True))
        self.stages.append(PasswordLoginStage(1, account, password))
