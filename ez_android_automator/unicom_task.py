"""
@Time: 2023/11/21 下午6:59
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: unicom_task.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
from ez_android_automator.client import AndroidClient, ClientTask, Stage
from ez_android_automator.client import PublishClient


class OpenAppStage(Stage):
    def run(self, client: PublishClient):
        client.restart_app('com.sinovatech.unicom.ui', True)


class CleanPopUpsStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({'text': '同意'}, timeout=10)
        client.wait_to_click({'text': '以后再说'})
        pass


class BeforeLoginStage(Stage):
    def run(self, client: PublishClient):
        client.wait_to_click({'text': '我的'})
        client.wait_to_click({'text': '去登录'})
        client.wait_to_click({'text': '宽带'})
        client.wait_to_click({'text': '请输入身份证号码'})


class UnicomSignTask(ClientTask):
    def __init__(self, social_id: str, address: str, city_id: str = '0532'):
        super().__init__()
        self.social_id = social_id
        self.address = address
        self.city_id = city_id
        self.stages.append(OpenAppStage(0))
        self.stages.append(CleanPopUpsStage(1))
        self.stages.append(BeforeLoginStage(2))
