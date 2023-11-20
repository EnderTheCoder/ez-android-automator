"""
@Time: 2023/11/20 15:57
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: xhs_task.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""

from client import PublishTask, Stage, PublishClient
from douyin_task import CopyVideoToGalleryStage


class OpenAppStage(Stage):
    def run(self, client: PublishClient):
        client.restart_app('com.xingin.xhs')


class PressPublishButtonStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({'content-desc': '发布'})


class ChooseFirstVideoStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({'resource-id': 'com.xingin.xhs:id/j17'}, gap=1)
        client.wait_to_click({'resource-id': 'com.xingin.xhs:id/dcy'})
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
        client.device.keyevent('back')
        client.wait_to_click({'text': '发布笔记'})


class XhsPublishVideoTask(PublishTask):
    """
    Publish a video on Xiaohongshu.
    """

    def __init__(self, title: str, content: str, video: str):
        super().__init__(title, content, video, '')
        self.stages.append(OpenAppStage(0))
        self.stages.append(CopyVideoToGalleryStage(1, self.video))
        self.stages.append(PressPublishButtonStage(2))
        self.stages.append(ChooseFirstVideoStage(3))
        self.stages.append(SetVideoOptionsStage(4, self.title, self.content))
