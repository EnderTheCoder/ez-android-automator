"""
@Time: 2024/6/16 16:30
@Auth: coin
@Email: 918731093@qq.com
@File: toutiao_task.py
@IDE: PyCharm
@Motto: one coin
"""
import time
from ez_android_automator.client import Stage, PublishClient, AndroidClient, PublishTask, \
    PhoneLoginTask, WaitCallBackStage, StatisticTask, PullDataTask, TaskAsStage
from ez_android_automator.idm_task import IDMPullTask


class OpenAppStage(Stage):
    def __init__(self, serial, clear_data: bool = False):
        self.clear_data = clear_data
        super().__init__(serial)

    def run(self, client: PublishClient):
        client.restart_app("com.ss.android.ugc.aweme.lite", self.clear_data)
        if self.clear_data:
            client.wait_to_click({'text': '同意'})


class BeforeLoginStage(Stage):
    def __init__(self, serial, phone: str):
        super().__init__(serial)
        self.phone = phone

    def run(self, client: AndroidClient):
        client.wait_to_click({"text": "我"})
        client.wait_to_click({"text": "以其他账号 登录"})
        client.device.send_keys(self.phone)
        client.wait_to_click({"text": "验证并登录"})
        client.wait_to_click({"text": "同意并登录"})


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
        client.wait_to_click({"content-desc": "拍摄"})
        client.wait_to_click({"text": "相册"})


class ChooseFirstVideoStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({'text': '视频'})
        time.sleep(1)
        client.device.click(160, 530)
        client.wait_to_click({'text': '下一步'})
        client.wait_to_click({'text': '下一步'})


class SetVideoOptionsStage(Stage):
    def __init__(self, serial, content: str, title=None):
        super().__init__(serial)
        self.content = content
        self.title = title

    def run(self, client: PublishClient):
        client.wait_to_click({"class": "android.widget.EditText"})
        client.device.send_keys(self.content)
        client.wait_to_click({"text": "发布"})


class DouyinjisuPublishVideoTask(PublishTask):
    """
    Publish a video on Douyinjisu.
    """

    def __init__(self, priority: int, title: str, content: str, video: str):
        super().__init__(priority, title, content, video, '')
        task = IDMPullTask(video)
        self.stages.append(TaskAsStage(0, task))
        self.stages.append(OpenAppStage(1))
        self.stages.append(PressPublishButtonStage(2))
        self.stages.append(ChooseFirstVideoStage(3))
        self.stages.append(SetVideoOptionsStage(4, self.content, self.title))


class DouyinjisuPhoneLoginTask(PhoneLoginTask):
    def __init__(self, phone: str):
        super().__init__(phone)
        self.stages.append(OpenAppStage(0, True))
        self.stages.append(BeforeLoginStage(1, phone))
        auth_stage = PhoneAuthCodeStage(3)
        self.stages.append(WaitCallBackStage(2, 60, self.get_code, auth_stage.code_callback))
        self.stages.append(auth_stage)
