"""
@Time: 2024/6/16 14:30
@Auth: coin
@Email: 918731093@qq.com
@File: toutiao_task.py
@IDE: PyCharm
@Motto: one coin
"""
import time
from ez_android_automator.client import Stage, PublishClient, AndroidClient, PublishTask, \
    PhoneLoginTask, WaitCallBackStage, StatisticTask, PushAccountTask, TaskAsStage
from ez_android_automator.idm_task import IDMPullTask


class OpenAppStage(Stage):
    def __init__(self, serial, clear_data: bool = False):
        self.clear_data = clear_data
        super().__init__(serial)

    def run(self, client: PublishClient):
        client.restart_app("com.ss.android.article.news", self.clear_data)
        if self.clear_data:
            client.wait_to_click({'text': '同意'})
            client.wait_to_click({'text': '关闭'})


class BeforeLoginStage(Stage):
    def __init__(self, serial, phone: str):
        super().__init__(serial)
        self.phone = phone

    def run(self, client: AndroidClient):
        client.wait_to_click({"text": "我的"})
        client.wait_to_click({"text": "其他登录方式"})
        client.wait_to_click({"text": "手机登录"})
        client.device.send_keys(self.phone)
        client.wait_to_click({"text": "获取验证码"})
        client.wait_to_click({"text": "同意并继续"})


class PhoneAuthCodeStage(Stage):
    def __init__(self, serial):
        super().__init__(serial)
        self.code = None

    def run(self, client: AndroidClient):
        client.device.send_keys(self.code)

    def code_callback(self, code: str):
        self.code = code


class PressPublishButtonStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({"text": "发布"})


class ChooseFirstVideoStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({'content-desc': '添加图片'})
        time.sleep(1)
        client.device.click(390, 380)
        client.wait_to_click({'text': '完成'})


class SetVideoOptionsStage(Stage):
    def __init__(self, serial, content: str, title=None):
        super().__init__(serial)
        self.content = content
        self.title = title

    def run(self, client: PublishClient):
        client.wait_to_click({"text": "说点什么…"})
        client.device.send_keys(self.content)
        client.wait_to_click({"text": "添加标题"})
        client.device.send_keys(self.title)
        client.wait_to_click({"text": "发布"})


class ToutiaoPublishVideoTask(PublishTask):
    """
    Publish a video on Toutiao.
    """

    def __init__(self, priority: int, title: str, content: str, video: str):
        super().__init__(priority, title, content, video, '')
        task = IDMPullTask(video)
        self.stages.append(TaskAsStage(0, task))
        self.stages.append(OpenAppStage(1))
        self.stages.append(PressPublishButtonStage(2))
        self.stages.append(ChooseFirstVideoStage(3))
        self.stages.append(SetVideoOptionsStage(4, self.content, self.title))


class ToutiaoPhoneLoginTask(PhoneLoginTask):
    def __init__(self, phone: str):
        super().__init__(phone)
        self.stages.append(OpenAppStage(0, True))
        self.stages.append(BeforeLoginStage(1, phone))
        auth_stage = PhoneAuthCodeStage(3)
        self.stages.append(WaitCallBackStage(2, 60, self.get_code, auth_stage.code_callback))
        self.stages.append(auth_stage)
