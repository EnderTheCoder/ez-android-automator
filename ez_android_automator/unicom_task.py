"""
@Time: 2023/11/21 下午6:59
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: unicom_task.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import time

from ez_android_automator.client import AndroidClient, ClientTask, Stage, ClientWaitTimeout


class OpenAppStage(Stage):
    def run(self, client: AndroidClient):
        client.restart_app('com.sinovatech.unicom.ui', True)


class CleanPopUpsStage(Stage):
    def run(self, client: AndroidClient):
        client.wait_to_click({'text': '同意'}, timeout=10, gap=0.5)
        client.wait_to_click({'text': '以后再说'})
        pass


class BeforeLoginStage(Stage):
    def run(self, client: AndroidClient):
        client.wait_to_click({'text': '我的'})
        client.wait_to_click({'text': '去登录'})
        client.wait_to_click({'resource-id': 'com.sinovatech.unicom.ui:id/login_type_rb_broadband'})
        client.wait_to_click({'text': '请输入身份证号码'})


class LoginStage(Stage):
    def __init__(self, serial, social_id, city_id):
        super().__init__(serial)
        self.social_id = social_id
        self.city_id = city_id

    def run(self, client: AndroidClient):
        client.device.send_keys(self.social_id)
        client.wait_to_click({'text': '请输入宽带所在地市'})
        client.device.send_keys(self.city_id)
        client.wait_to_click({'text': '*请务必确认该地市为宽带安装地市'})
        client.wait_to_click({'resource-id': 'com.sinovatech.unicom.ui:id/login_check_img'})
        client.wait_to_click({'text': '登 录'})


class VerifyArea:
    def __init__(self, addr_reminder, blanks):
        self.addr_reminder = addr_reminder
        self.blanks = blanks

    def guess_blank(self, full_addr) -> list:
        number_char_lst = []
        for c in full_addr:
            if '0' <= c <= '9':
                number_char_lst.append(c)
        return number_char_lst[len(number_char_lst) - len(self.blanks):]


class SlideVerifyStage(Stage):

    def run(self, client: AndroidClient):
        client.wait_until_found({'resource-id': 'nc_1_n1z'})
        slider = client.rs[0]
        rail = client.find_xml_by_attr({'resource-id': 'nc_1__scale_text'})[0]
        client.drag_node(slider, rail)


class AddressVerifyStage(Stage):
    def __init__(self, stage_serial, address):
        super().__init__(stage_serial)
        self.address = address

    def run(self, client: AndroidClient):
        client.wait_until_found({'class': 'android.widget.EditText'})
        parent_set = set()
        areas = []
        for blank in client.rs:
            parent_set.add(blank.parent)
        for parent in parent_set:
            pure_children = []
            for child in parent.children:
                if child != '\n':
                    pure_children.append(child)
            areas.append(VerifyArea(pure_children[0]['text'], pure_children[1:]))

        client.find_xml_by_attr({'text': '进入'})
        try:
            for i, area in enumerate(areas):
                client.click_xml_node(area.blanks[0])
                for c in area.guess_blank(self.address):
                    client.device.send_keys(c)
                    time.sleep(0.5)
                client.click_xml_node(client.rs[i])
                client.wait_to_click({'text': '我知道了'}, timeout=3)
                time.sleep(0.5)
        except ClientWaitTimeout:
            pass


class SignStage(Stage):
    def run(self, client: AndroidClient):
        client.wait_to_click({'text': '首页'})
        try:
            client.simple_click(1)
            client.wait_until_found({'text': '请使用联通手机号登录APP，参与本次活动'})
            client.key_back()
        except ClientWaitTimeout:
            pass
        client.simple_click(1)
        client.simple_click(0, 0.5)
        client.simple_click(0, 0.5)
        client.simple_click(0, 0.5)
        client.wait_to_click({'content-desc': '签到'})
        client.wait_until_found({'text': '签到签到'})


class UnicomSignTask(ClientTask):
    def __init__(self, social_id: str, address: str, city_id: str = '0352'):
        super().__init__()
        self.social_id = social_id
        self.address = address
        self.city_id = city_id
        self.stages.append(OpenAppStage(0))
        self.stages.append(CleanPopUpsStage(1))
        self.stages.append(BeforeLoginStage(2))
        self.stages.append(LoginStage(3, social_id, city_id))
        self.stages.append(SlideVerifyStage(4))
        self.stages.append(AddressVerifyStage(5, self.address))
        self.stages.append(SignStage(6))


class InstallStage(Stage):
    def run(self, client: AndroidClient):
        if 'com.sinovatech.unicom.ui' not in client.device.app_list():
            client.device.app_install('com.sinovatech.unicom.ui.apk')


class UnicomInstallTask(ClientTask):
    def __init__(self):
        super().__init__()
        self.stages.append(InstallStage(0))
