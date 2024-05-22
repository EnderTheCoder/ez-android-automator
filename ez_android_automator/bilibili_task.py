import time

from ez_android_automator.client import Stage, PublishClient, AndroidClient, StatisticTask


class OpenAppStage(Stage):
    def __init__(self, serial, clear_data: bool = False):
        self.clear_data = clear_data
        super().__init__(serial)

    def run(self, client: PublishClient):
        client.restart_app("tv.danmaku.bili", self.clear_data)
        if self.clear_data:
            client.wait_to_click({'text': '同意并继续'})


class BeforeLoginStage(Stage):
    def __init__(self, serial, phone: str):
        super().__init__(serial)
        self.phone = phone

    def run(self, client: AndroidClient):
        client.wait_to_click({"content-desc": "登录，按钮"})
        client.wait_to_click({"text": "请输入手机号码"})
        client.device.send_keys(self.phone)
        client.wait_to_click({"text": "获取验证码"})


class PhoneAuthCodeStage(Stage):
    def __init__(self, serial):
        super().__init__(serial)
        self.code = None

    def run(self, client: AndroidClient):
        client.device.send_keys(self.code)
        client.wait_to_click({"text": "同意并登录"})

    def code_callback(self, code: str):
        self.code = code


class PressPublishButtonStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({"content-desc": "发布内容,5之3,标签"})


class ChooseFirstVideoStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({'text': '视频'})


class StatisticCenterStage(Stage):
    def run(self, client: AndroidClient):
        time.sleep(7)  # wait for ad to be finished
        client.wait_to_click({'text': '我的'})
        client.wait_to_click({'text': '稿件管理'})


class GetStatisticStage(Stage):
    def __init__(self, stage_serial: int, video_title: str, statistic_callback: callable):
        super().__init__(stage_serial)
        self.video_title = video_title
        self.statistic_callback = statistic_callback

    def run(self, client: AndroidClient):
        client.wait_until_found({'text': '数据'})  # wait for list to be loaded
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
            'coin': get_statistic_by_attr_name('投币'),
            'share': get_statistic_by_attr_name('分享')
        }
        self.statistic_callback(statistic)
        pass


class BilibiliStatisticTask(StatisticTask):
    def __init__(self, video_title):
        super().__init__()
        self.statistic = None
        self.append(OpenAppStage(0))
        self.append(StatisticCenterStage(1))
        self.append(GetStatisticStage(2, video_title, self.statistic_callback))

    def statistic_callback(self, statistic: dict):
        self.statistic = statistic
