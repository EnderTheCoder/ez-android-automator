"""
@Time: 2024/2/29 19:00
@Auth: coin
@Email: 918731093@qq.com
@File: xigua_task.py
@IDE: PyCharm
@Motto：one coin
"""

from ez_android_automator.client import Stage, PublishTask, DownloadMediaStage, PublishClient


class OpenAppStage(Stage):
    def run(self, client: PublishClient):
        client.restart_app("com.ss.android.article.video")


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


class XiguaPublishVideoTask(PublishTask):
    """
    Publish a video on Xigua.
    """

    def __init__(self, priority: int, title: str, content: str, video: str):
        super().__init__(priority, title, content, video, '')
        # self.stages.append(DownloadMediaStage(0, video))
        self.stages.append(OpenAppStage(1))
        self.stages.append(PressPublishButtonStage(2))
        self.stages.append(ChooseFirstVideoStage(3))
        self.stages.append(SetVideoOptionsStage(4, self.content))
