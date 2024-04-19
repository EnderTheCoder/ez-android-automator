"""
@Time: 2024/3/6 11:00
@Auth: coin
@Email: 918731093@qq.com
@File: kuaishoujisu_task.py
@IDE: PyCharm
@Motto：one coin
"""

from ez_android_automator.client import Stage, PublishTask, DownloadMediaStage, PublishClient


class OpenAppStage(Stage):
    def run(self, client: PublishClient):
        client.restart_app("com.kuaishou.nebula")


class PressPublishButtonStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({'resource-id': 'com.kuaishou.nebula:id/btn_shoot_skin'})



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




class KuaishoujisuPublishVideoTask(PublishTask):
    """
    Publish a video on Kuaishoujisu.
    """

    def __init__(self, priority: int, title: str, content: str, video: str):
        super().__init__(priority, title, content, video, '')
        # self.stages.append(DownloadMediaStage(0, video))
        self.stages.append(OpenAppStage(1))
        self.stages.append(PressPublishButtonStage(2))
        self.stages.append(ChooseFirstVideoStage(3))
        self.stages.append(SetVideoOptionsStage(4, self.content))