"""
@Time: 2024/2/26 16:30
@Auth: coin
@Email: 918731093@qq.com
@File: douyin_task1.py
@IDE: PyCharm
@Motto：one coin
"""
import time

from ez_android_automator.client import Stage, PublishTask, DownloadMediaStage, PublishClient


class OpenAppStage(Stage):
    def run(self, client: PublishClient):
        client.device.app_stop('com.ss.android.ugc.aweme')
        client.device.shell('am start -n com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.main.MainActivity')


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
