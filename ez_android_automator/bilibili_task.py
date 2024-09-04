"""
@Time: 2024/5/14 19:00
@Auth: coin
@Email: 918731093@qq.com
@File: bilibili_task.py
@IDE: PyCharm
@Motto: one coin
"""
import time
from typing import Callable

from .client import Stage, PublishClient, AndroidClient, PublishTask, \
    PhoneLoginTask, WaitCallBackStage, StatisticTask, TaskAsStage, ClientWaitTimeout
from .idm_task import IDMPullTask
from .app_file import AppFilePkg


class OpenAppStage(Stage):
    def __init__(self, clear_data: bool = False):
        self.clear_data = clear_data
        super().__init__()

    def run(self, client: PublishClient):
        client.restart_app("tv.danmaku.bili", self.clear_data)


class PrepareStage(Stage):
    """
    Common stage for some unexpected pop-ups.
    """
    def run(self, client: PublishClient):
        client.intercept_to_click({'text': '始终允许'})
        client.intercept_to_click({"text": "同意并继续"})
        client.intercept_to_click({'resource-id': 'tv.danmaku.bili:id/count_down'})


class BeforeLoginStage(Stage):
    def __init__(self, serial, phone: str):
        super().__init__(serial)
        self.phone = phone

    def run(self, client: AndroidClient):
        client.wait_to_click({"resource-id": "tv.danmaku.bili:id/avatar_layout"})
        client.wait_to_click({"resource-id": "tv.danmaku.bili:id/et_phone_number"})
        client.device.send_keys(self.phone)
        client.wait_to_click({"resource-id": "tv.danmaku.bili:id/get_auth_code"})
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
        client.wait_to_click({"content-desc": "发布内容,5之3,标签"}, gap=1)


class ChooseFirstVideoStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({'text': '视频'}, timeout=10)
        client.wait_to_click({'text': '视频'}, timeout=10)
        client.wait_to_click({'resource-id': 'tv.danmaku.bili:id/sdv_cover'})
        client.wait_to_click({'text': '发布'})


class SetVideoOptionsStage(Stage):
    def __init__(self, serial, content: str):
        super().__init__(serial)
        self.content = content

    def run(self, client: PublishClient):
        client.wait_to_click({"resource-id": "tv.danmaku.bili:id/et_title"})
        client.device.send_keys(self.content)
        client.wait_to_click({"resource-id": "tv.danmaku.bili:id/tv_upper_publish"})


class StatisticCenterStage(Stage):
    def run(self, client: AndroidClient):
        try:
            client.wait_until_disappear({'resource-id': 'tv.danmaku.bili:id/splash_interact_view'})
        except ClientWaitTimeout:
            pass
        client.wait_to_click({'text': '我的'})
        client.wait_to_click({'text': '稿件管理'})


class GetStatisticStage(Stage):
    def __init__(self, video_title: str, statistic_callback: Callable):
        super().__init__()
        self.video_title = video_title
        self.statistic_callback = statistic_callback

    def run(self, client: AndroidClient):
        client.wait_to_click({'resource-id': 'tv.danmaku.bili:id/upper_search_et'}, gap=1)
        client.wait_to_click({'resource-id': 'tv.danmaku.bili:id/upper_search_et'})
        client.wait_until_found({'resource-id': 'tv.danmaku.bili:id/upper_search_cancel_tv'})
        client.wait_to_click({'resource-id': 'tv.danmaku.bili:id/upper_search_et'})
        time.sleep(1)
        client.device.send_keys(self.video_title)
        client.wait_until_found({'text': self.video_title, 'resource-id': 'tv.danmaku.bili:id/upper_search_et'})
        client.key_enter()
        client.wait_until_found({'resource-id': 'tv.danmaku.bili:id/video_layout'})
        client.wait_until_found({'text': self.video_title})
        parser = client.find_xml_by_attr({'text': self.video_title})
        parser = parser[0]
        parent = parser.parent.parent.parent
        last = parent.contents[-2]
        statistic_btn = last.find('node', {'text': '数据'})
        client.click_xml_node(statistic_btn)
        client.wait_until_found({'text': '播放量'})
        time.sleep(2)
        client.refresh_xml()

        def get_statistic_by_attr_name(name):
            label_node = client.find_xml_by_attr({'text': name})[0]
            data_node = label_node.next.next
            return int(data_node['text'])

        statistic = {
            'view': get_statistic_by_attr_name('播放量'),
            'like': get_statistic_by_attr_name('点赞'),
            'comment': get_statistic_by_attr_name('评论'),
            'collect': get_statistic_by_attr_name('收藏'),
            'share': get_statistic_by_attr_name('分享')
        }
        self.statistic_callback(statistic)


class BilibiliStatisticTask(StatisticTask):
    def __init__(self, video_title):
        super().__init__()
        self.statistic = None
        self.append(PrepareStage())
        self.append(OpenAppStage())
        self.append(StatisticCenterStage())
        self.append(GetStatisticStage(video_title, self.statistic_callback))
        self.auto_serial()

    def statistic_callback(self, statistic: dict):
        self.statistic = statistic


class BilibiliPublishVideoTask(PublishTask):
    """
    Publish a video on Bilibili.
    """

    def __init__(self, priority: int, title: str, content: str, video: str, download_timeout: int = 120):
        super().__init__(priority, title, content, video, '')
        task = IDMPullTask(video, download_timeout=download_timeout)
        self.stages.append(TaskAsStage(0, task))
        self.stages.append(OpenAppStage())
        self.stages.append(PressPublishButtonStage(2))
        self.stages.append(ChooseFirstVideoStage(3))
        self.stages.append(SetVideoOptionsStage(4, self.content))
        self.auto_serial()


class BilibiliPhoneLoginTask(PhoneLoginTask):
    def __init__(self, phone: str):
        super().__init__(phone)
        self.stages.append(OpenAppStage(True))
        self.stages.append(BeforeLoginStage(1, phone))
        auth_stage = PhoneAuthCodeStage(3)
        self.stages.append(WaitCallBackStage(2, 60, self.get_code, auth_stage.code_callback))
        self.stages.append(auth_stage)
        self.auto_serial()


class BilibiliFilePkg(AppFilePkg):
    def __init__(self):
        super().__init__('tv.danmaku.bili', time.time(), [
            'shared_prefs', 'app_blkv', 'files', 'cache', 'app_device_settings', 'databases', 'app_account'
        ])


bilibili_file_pkg = BilibiliFilePkg()
