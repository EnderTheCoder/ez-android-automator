"""
@Time: 2024/5/22 17:00
@Auth: coin
@Email: 918731093@qq.com
@File: weibo_task.py
@IDE: PyCharm
@Motto：one coin
"""

from ez_android_automator.client import Stage, PublishClient, AndroidClient, PublishTask, DownloadMediaStage, \
    PhoneLoginTask, WaitCallBackStage


class OpenAppStage(Stage):
    def __init__(self, serial, clear_data: bool = False):
        self.clear_data = clear_data
        super().__init__(serial)

    def run(self, client: PublishClient):
        client.restart_app("com.sina.weibo", self.clear_data)
        if self.clear_data:
            client.wait_to_click({'text': '同意并继续'})


class BeforeLoginStage(Stage):
    def __init__(self, serial, phone: str):
        super().__init__(serial)
        self.phone = phone

    def run(self, client: AndroidClient):
        client.wait_to_click({"content-desc": "我"})
        client.wait_to_click({"text": "手机号"})
        client.device.send_keys(self.phone)
        client.wait_to_click({"text": "获取验证码"})


class PhoneAuthCodeStage(Stage):
    def __init__(self, serial):
        super().__init__(serial)
        self.code = None

    def run(self, client: AndroidClient):
        client.device.send_keys(self.code)
        client.wait_to_click({"text": "同意并登录"})
        client.wait_to_click({"text": "跳过"})
        client.wait_to_click({"text": "跳过"})

    def code_callback(self, code: str):
        self.code = code


class PressPublishButtonStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({"resource-id": "com.sina.weibo:id/rlredpacketSave"})
        client.wait_to_click({"text": "视频"})


class ChooseFirstVideoStage(Stage):
    def run(self, client: PublishClient):
        client.device.click(495, 270)
        client.wait_to_click({'text': '下一步(1)'})
        client.wait_to_click({'text': '下一步'})


class SetVideoOptionsStage(Stage):
    def __init__(self, serial, title: str, content: str):
        super().__init__(serial)
        self.title = title
        self.content = content

    def run(self, client: PublishClient):
        client.wait_to_click({"text": "分享新鲜事..."})
        client.device.send_keys(self.content)
        client.wait_to_click({"text": "原创"})
        client.wait_to_click({"text": "填写标题能获得更多关注"})
        client.device.send_keys(self.title)
        client.wait_to_click({"text": "发送"})


class WeiboPublishVideoTask(PublishTask):
    """
    Publish a video on Weibo.
    """

    def __init__(self, priority: int, title: str, content: str, video: str):
        super().__init__(priority, title, content, video, '')
        # self.stages.append(DownloadMediaStage(0, video))
        self.stages.append(OpenAppStage(1))
        self.stages.append(PressPublishButtonStage(2))
        self.stages.append(ChooseFirstVideoStage(3))
        self.stages.append(SetVideoOptionsStage(4, self.title, self.content))


class WeiboPhoneLoginTask(PhoneLoginTask):
    def __init__(self, phone: str):
        super().__init__(phone)
        self.stages.append(OpenAppStage(0, True))
        self.stages.append(BeforeLoginStage(1, phone))
        auth_stage = PhoneAuthCodeStage(3)
        self.stages.append(WaitCallBackStage(2, 60, self.get_code, auth_stage.code_callback))
        self.stages.append(auth_stage)
