"""
@Time: 2024/7/27 7:08
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: damai_task.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.

Auto ticket buying tasks for damai app.
"""
import time
from typing import Optional

from ez_android_automator.client import ClientTask, StartAppStage, Stage, AndroidClient, ClientWaitTimeout


class InterceptStage(Stage):
    def run(self, client: AndroidClient):
        client.intercept_to_click({'resource-id': 'cn.damai:id/new_person_dialog_top_close_iv'})
        client.intercept_to_click({'resource-id': 'cn.damai:id/homepage_popup_window_close_btn'})
        client.intercept_to_click({'resource-id': 'cn.damai:id/homepage_advert_pb'},
                                  {'resource-id': 'cn.damai:id/channel_search_text'})
        client.intercept_to_click({'resource-id': 'cn.damai:id/damai_theme_dialog_cancel_btn'})
        client.intercept_to_click({'resource-id': 'cn.damai:id/state_view_refresh_btn'})
        client.intercept_to_click({'resource-id': 'cn.damai:id/damai_theme_dialog_confirm_btn'})
        client.intercept_to_click({'text': '知道了'})
        client.intercept_to_click({'text': '下次再说'})
        client.intercept_to_click({'text': '确认并知悉'})
        client.intercept_to_click({'text': '不开启'})
        client.intercept_to_click({'text': ''})


class SearchStage(Stage):
    def __init__(self, search_text: str):
        super().__init__()
        self.search_text = search_text

    def run(self, client: AndroidClient):
        client.wait_to_click({'resource-id': 'cn.damai:id/channel_search_text'})
        client.device.send_keys(self.search_text)
        client.device.send_action("search")
        client.wait_to_click({'text': '演出'})


class EnterFirstSearchResultStage(Stage):
    def run(self, client: AndroidClient):
        time.sleep(0.5)
        client.wait_to_click({'resource-id': 'cn.damai:id/ll_search_item'})
        client.wait_until_found({'resource-id': 'cn.damai:id/trade_project_detail_purchase_status_bar_container_fl'},
                                trigger_interceptors=False)


class SelectCityStage(Stage):
    def __init__(self, city: str):
        super().__init__()
        self.city = city

    def run(self, client: AndroidClient):
        client.wait_until_found({'resource-id': 'cn.damai:id/tour_recyclerView'})
        city = client.rs[0].find(attrs={'resource-id': 'cn.damai:id/tv_city', 'text': self.city})
        if city is not None:
            client.click_xml_node(city)


class CheckFareStage(Stage):
    def run(self, client: AndroidClient):
        rs = ['']
        while len(rs) != 0:
            client.refresh_xml()
            rs = client.find_xml_by_attr(
                {'resource-id': 'cn.damai:id/id_new_project_normal_count_down_layout'})
        client.wait_to_click({'resource-id': 'cn.damai:id/trade_project_detail_purchase_status_bar_container_fl'},
                             refresh_xml=False, trigger_interceptors=False)


class OutOfStockError(RuntimeError):
    def __init__(self, need: int, found: int):
        self.need = need
        self.found = found
        super().__init__(f"Out of stock! Need {need}, found {found}")


class SelectDateStage(Stage):
    def __init__(self, date_idx: int, level_idx: int, amount: int):
        super().__init__()
        self.date_idx = date_idx
        self.level_idx = level_idx
        self.amount = amount

    def run(self, client: AndroidClient):
        client.wait_until_found({'resource-id': 'cn.damai:id/project_detail_perform_flowlayout'})
        rs_project = client.find_xml_by_attr({'resource-id': 'cn.damai:id/project_detail_perform_flowlayout'})
        rs_0 = rs_project[0].find_all_next(attrs={'resource-id': 'cn.damai:id/ll_perform_item'})
        self.date_idx = min(len(rs_0) - 1, self.date_idx)
        client.click_xml_node(rs_0[self.date_idx])
        client.wait_until_found({'text': '预约想看票档'})
        rs_price = client.find_xml_by_attr({'resource-id': 'cn.damai:id/layout_price'})
        rs_1 = rs_price[0].find_all(attrs={'resource-id': 'cn.damai:id/ll_perform_item'})
        self.level_idx = min(len(rs_1) - 1, self.level_idx)
        lack_tag = rs_1[self.level_idx].find(attrs={'text': '缺货登记'})
        if lack_tag is not None:
            raise OutOfStockError(self.amount, 0)
        client.click_xml_node(rs_1[self.level_idx])
        client.wait_until_found({'resource-id': 'cn.damai:id/img_jia'})
        for i in range(self.amount - 1):
            client.click_xml_node(client.rs[0])
        time.sleep(0.5)
        client.refresh_xml()
        client.find_xml_by_attr({'resource-id': 'cn.damai:id/tv_num'})
        found = int(str(client.rs[0]['text']).removesuffix("张"))
        if found != self.amount:
            raise OutOfStockError(self.amount, found)
        client.wait_to_click({'resource-id': 'cn.damai:id/btn_buy_view'})


class FireStage(Stage):
    def run(self, client: AndroidClient):
        client.wait_to_click({'resource-id': 'cn.damai:id/checkbox'}, click_all=True)
        client.wait_to_click({'text': '提交订单'}, refresh_xml=False)


class ResetAudienceStage(Stage):
    def __init__(self, audiences: list[tuple[str, str]]):
        super().__init__()
        self.audiences = audiences

    def run(self, client: AndroidClient):
        client.wait_to_click({'text': '我的'})
        client.wait_to_click({'text': '观演人'})
        client.wait_until_found({'text': '常用观演人'})
        time.sleep(1)
        try:
            while True:
                client.wait_to_click({'resource-id': 'cn.damai:id/custom_delete'}, timeout=1, gap=2)
                client.wait_to_click({'resource-id': 'cn.damai:id/damai_dialog_confirm_btn'})
                time.sleep(2)
        except ClientWaitTimeout:
            pass
        for audience in self.audiences:
            client.wait_to_click({'resource-id': 'cn.damai:id/add_customer_btn'})
            client.wait_until_found({'text': '请填写观演人姓名'})
            time.sleep(1)
            client.wait_to_click({'resource-id': 'cn.damai:id/add_contacts_name'})
            client.device.send_keys(audience[0])
            client.device.send_action("next")
            client.device.send_keys(audience[1])
            client.device.xpath.click('//android.widget.CheckBox')
            client.wait_to_click({'resource-id': 'cn.damai:id/add_contacts_save_btn'})
            client.wait_until_found({'text': '常用观演人'})
        client.device.keyevent('back')
        client.device.keyevent('back')


class DaMaiBuyTask(ClientTask):
    def __init__(self, audiences: list[tuple[str, str]], search_text: str, city: Optional[str], date_idx, level_idx):
        super().__init__()
        self.append(InterceptStage())
        self.append(StartAppStage(0, 'cn.damai'))
        self.append(ResetAudienceStage(audiences))
        self.append(SearchStage(search_text))
        self.append(EnterFirstSearchResultStage())
        self.append(CheckFareStage())
        if city is not None:
            self.append(SelectCityStage(city))
        self.append(SelectDateStage(date_idx, level_idx, len(audiences)))
        self.append(FireStage())
        self.auto_serial()
