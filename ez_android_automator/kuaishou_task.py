"""
@Time: 2024/1/30 15:00
@Auth: coin
@Email: 918731093@qq.com
@File: kuaishou_task.py
@IDE: PyCharm
@Motto：one coin
"""

from ez_android_automator.client import Stage, PublishTask, DownloadMediaStage, PublishClient


class OpenAppStage(Stage):
    def run(self, client: PublishClient):
        client.restart_app("com.smile.gifmaker")


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


class KuaishouPublishVideoTask(PublishTask):
    """
    Publish a video on Kuaishou.
    """

    def __init__(self, priority: int, title: str, content: str, video: str):
        super().__init__(priority, title, content, video, '')
        self.stages.append(DownloadMediaStage(0, video))
        self.stages.append(OpenAppStage(1))
        self.stages.append(PressPublishButtonStage(2))
        self.stages.append(ChooseFirstVideoStage(3))
        self.stages.append(SetVideoOptionsStage(4, self.content))
