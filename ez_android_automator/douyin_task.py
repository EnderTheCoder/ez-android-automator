"""
@Time: 2024/3/15 13:30
@Auth: coin
@Email: 918731093@qq.com
@File: douyin_task.py
@IDE: PyCharm
@Motto：one coin
"""
import time
from typing import Callable

from ez_android_automator.app_file import AppFilePkg
from ez_android_automator.client import Stage, PublishTask, PublishClient, AndroidClient, \
    PhoneLoginTask, WaitCallBackStage, TaskAsStage, StatisticTask
from ez_android_automator.idm_task import IDMPullTask


class PrepareStage(Stage):
    """
    Common stage for some unexpected pop-ups.
    """

    def run(self, client: PublishClient):
        client.intercept_to_click({'text': '关闭'})
        client.intercept_to_click({'text': '以后再说'})
        client.intercept_to_click({'text': '始终允许'})
        client.intercept_to_click({'text': '仅在使用中允许'})


class OpenAppStage(Stage):
    def __init__(self, serial, clear_data: bool = False):
        self.clear_data = clear_data
        super().__init__(serial)

    def run(self, client: PublishClient):
        client.device.app_stop('com.ss.android.ugc.aweme')
        if self.clear_data:
            client.device.app_clear('com.ss.android.ugc.aweme')
        client.device.shell('am start -n com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.main.MainActivity')
        if self.clear_data:
            client.wait_to_click({'text': '同意'})


class PressPublishButtonStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({'content-desc': '拍摄，按钮'})


class ChooseFirstVideoStage(Stage):
    def run(self, client: PublishClient):
        # client.wait_to_click({'resource-id': 'com.lbe.security.miui:id/permission_allow_foreground_only_button'})
        # client.wait_to_click({'resource-id': 'com.lbe.security.miui:id/permission_allow_foreground_only_button'})
        client.wait_to_click({'text': '相册'})
        # client.wait_to_click({"resource-id": "com.lbe.security.miui:id/permission_allow_button"})
        client.wait_to_click({'text': '视频'})
        time.sleep(2)
        client.device.click(200, 550)
        client.wait_to_click({'text': '下一步'})
        client.wait_to_click({'text': '下一步'})


class SetVideoOptionsStage(Stage):
    def __init__(self, serial, content: str):
        super().__init__(serial)
        self.content = content

    def run(self, client: PublishClient):
        client.wait_to_click({'text': '添加作品描述..'})
        client.device.send_keys(self.content)
        client.key_back()
        client.find_xml_by_attr({'content-desc': '发作品'})
        client.click_xml_node(client.rs[0])


class BeforeLoginStage(Stage):
    def __init__(self, serial, phone: str):
        super().__init__(serial)
        self.phone = phone

    def run(self, client: AndroidClient):
        client.wait_to_click({'text': '我'})
        client.wait_to_click({'text': '请输入手机号'})
        client.device.send_keys(self.phone)
        client.wait_to_click({'text': '验证并登录'})
        time.sleep(0.5)
        client.wait_to_click({'text': '同意并登录'})


class PhoneAuthCodeStage(Stage):
    def __init__(self, serial):
        super().__init__(serial)
        self.code = None

    def run(self, client: AndroidClient):
        client.device.send_keys(self.code)

    def code_callback(self, code: str):
        self.code = code


class StatisticCenterStage(Stage):
    def run(self, client: AndroidClient):
        time.sleep(7)  # wait for ad to be finished
        client.wait_to_click({'text': '我'})
        client.wait_to_click({'text': '查看更多'})
        client.wait_to_click({'text': '抖音创作者中心'})
        client.wait_to_click({'text': '更多作品'})


class GetStatisticStage(Stage):
    def __init__(self, stage_serial: int, video_title: str, statistic_callback: Callable):
        super().__init__(stage_serial)
        self.video_title = video_title
        self.statistic_callback = statistic_callback

    def run(self, client: AndroidClient):
        client.wait_until_found({'text': self.video_title})  # wait for list to be loaded


class DouyinStatisticTask(StatisticTask):
    def __init__(self, video_title):
        super().__init__()
        self.statistic = None
        self.append(OpenAppStage(0))
        self.append(StatisticCenterStage(1))
        self.append(GetStatisticStage(2, video_title, self.statistic_callback))

    def statistic_callback(self, statistic: dict):
        self.statistic = statistic


class DouyinVideoPublishTask(PublishTask):
    """
    Publish a video on Douyin.
    """

    def __init__(self, priority: int, title: str, content: str, video: str, download_timeout: int = 120):
        super().__init__(priority, title, content, video, '')
        task = IDMPullTask(video, download_timeout=download_timeout)
        self.stages.append(TaskAsStage(0, task))
        self.stages.append(OpenAppStage(1))
        self.stages.append(PressPublishButtonStage(2))
        self.stages.append(ChooseFirstVideoStage(3))
        self.stages.append(SetVideoOptionsStage(4, self.content))


class DouyinPhoneLoginTask(PhoneLoginTask):
    def __init__(self, phone: str):
        super().__init__(phone)
        self.stages.append(OpenAppStage(0, True))
        self.stages.append(BeforeLoginStage(1, phone))
        auth_stage = PhoneAuthCodeStage(3)
        self.stages.append(WaitCallBackStage(2, 60, self.get_code, auth_stage.code_callback))
        self.stages.append(auth_stage)


douyin_file_pkg = AppFilePkg('com.ss.android.ugc.aweme', time.time(),
                             ['app_accs', 'app_dex', 'app_librarian', 'app_pigeonShopInfoCache', 'app_sys-plat',
                              'app_textures', 'app_webview', 'app_webview_com.ss.android.ugc.aweme:push', 'cache',
                              'shared_prefs', 'code_cache', 'databases', 'awemeSplashCache', 'files', 'small_emoji_res'])
