"""
@Time: 2024/7/27 7:08
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: damai_task.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.

Auto ticket buying tasks for damai app.
"""
import random
import time
from typing import Optional

from ez_android_automator.client import ClientTask, StartAppStage, Stage, AndroidClient, ClientWaitTimeout, \
    parse_node_xyxy
from ez_android_automator.ym_helper import SliderSolver, CaptchaSolveError


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
        client.intercept_to_click({'resource-id': 'cn.damai:id/homepage_eva_cancel'})


class SearchStage(Stage):
    def __init__(self, search_text: str):
        super().__init__()
        self.search_text = search_text

    def run(self, client: AndroidClient):
        client.wait_to_click({'resource-id': 'cn.damai:id/channel_search_text'})
        time.sleep(0.5)
        client.device.send_keys(self.search_text)
        client.wait_until_found({'text': self.search_text, 'resource-id': 'cn.damai:id/header_search_v2_input'})
        client.key_enter()
        client.wait_to_click({'text': '演出'})


class EnterFirstSearchResultStage(Stage):
    def run(self, client: AndroidClient):
        time.sleep(0.5)
        client.wait_to_click({'resource-id': 'cn.damai:id/ll_search_item'})
        client.wait_until_found({'resource-id': 'cn.damai:id/trade_project_detail_purchase_status_bar_container_fl'},
                                timeout=10)


class SelectCityStage(Stage):
    def __init__(self, city: str):
        super().__init__()
        self.city = city

    def run(self, client: AndroidClient):
        try:
            client.wait_until_found({'resource-id': 'cn.damai:id/tour_recyclerView'})
            client.wait_to_click({'resource-id': 'cn.damai:id/tv_city', 'text': self.city})
        except ClientWaitTimeout:
            print("City identified not found, fallback to first search result.")
            client.wait_to_click({'resource-id': 'cn.damai:id/ll_search_item'})


class CheckFareStage(Stage):
    def __init__(self):
        super().__init__()
        self.count_down_checked = False
        self.purchase_node = None
        self.audience_pre_set = False

    def run(self, client: AndroidClient):
        client.refresh_xml(intercept=False)
        while len(client.find_xml_by_attr({'text': '购票须知'})) > 0:
            client.click_xml_node(client.rs[0])
            client.refresh_xml()
        client.wait_until_found({'resource-id': 'cn.damai:id/trade_project_detail_purchase_status_bar_container_fl'})
        if not self.audience_pre_set:
            try:
                client.wait_to_click({'resource-id': 'cn.damai:id/goto_setinfo_btn_text'})
                client.wait_until_found({'text': '预选本次实名观演人'})
                time.sleep(0.5)
                client.wait_to_click({'text': '去预选'})
                client.wait_to_click({'checked': 'false', 'checkable': 'true'}, click_all=True, timeout=10)
                client.wait_to_click({'text': '确定'})
                client.key_back()
                client.wait_until_found(
                    {'resource-id': 'cn.damai:id/trade_project_detail_purchase_status_bar_container_fl'},
                    timeout=20)
                self.audience_pre_set = True
            except ClientWaitTimeout:
                self.audience_pre_set = True
                if len(client.find_xml_by_attr({'text': '已预选'})) > 0:
                    client.key_back()
                    client.wait_until_found(
                        {'resource-id': 'cn.damai:id/trade_project_detail_purchase_status_bar_container_fl'}
                    )
        if not self.count_down_checked:
            rs_0 = ['']
            rs_1 = ['']
            rs_2 = ['']
            while len(rs_0) != 0 or len(rs_1) != 0 or len(rs_2) != 0:
                client.refresh_xml()
                rs_0 = client.find_xml_by_attr(
                    {'resource-id': 'cn.damai:id/id_new_project_normal_count_down_layout'})
                rs_1 = client.find_xml_by_attr({'resource-id': 'cn.damai:id/project_timer_layout'})
                rs_2 = client.find_xml_by_attr({'resource-id': 'cn.damai:id/member_normal_start_sale_layout'})
            self.count_down_checked = True
        if self.purchase_node is None:
            self.purchase_node = \
                client.find_xml_by_attr(
                    {'resource-id': 'cn.damai:id/trade_project_detail_purchase_status_bar_container_fl'})[0]
        while True:
            client.click_xml_node(self.purchase_node)
            client.refresh_xml(intercept=False)
            if len(client.find_xml_by_attr({'text': '场次'})) > 0:
                break


class OutOfStockError(RuntimeError):
    def __init__(self, need: int, found: int):
        self.need = need
        self.found = found
        super().__init__(f"Out of stock! Need {need}, found {found}")


class SelectDateStage(Stage):
    def __init__(self, date_idx: list[int], level_idx: list[int], amount: int, ignore_num: bool = False):
        super().__init__()
        self.date_idx = date_idx
        self.level_idx = level_idx
        self.amount = amount
        self.ignore_num = ignore_num

    def run(self, client: AndroidClient):
        client.wait_until_found({'resource-id': 'cn.damai:id/layout_perform_view'},
                                intercept=False)
        rs_project = client.rs[0]
        rs_0 = rs_project.find_all(attrs={'resource-id': 'cn.damai:id/ll_perform_item'})
        chosen_date_idx = -1
        try:
            for idx in self.date_idx:
                if rs_0[idx].find(attrs={'text': '无票'}) is None:
                    chosen_date_idx = idx
                    break
                if idx == self.date_idx[-1]:
                    raise OutOfStockError(self.amount, 0)
        except OutOfStockError as e:
            # if len(rs_0) <= 1:
            raise e
            # else:
            #     while True:
            #         for idx, r_elem in enumerate(rs_0):
            #             if idx not in self.date_idx:

        client.click_xml_node(rs_0[chosen_date_idx])
        while True:
            client.refresh_xml(intercept=False)
            rs_price = client.find_xml_by_attr({'resource-id': 'cn.damai:id/layout_price'})
            if len(rs_price) == 0:
                client.click_xml_node(rs_0[chosen_date_idx])
            else:
                break
        rs_1 = rs_price[0].find_all(attrs={'resource-id': 'cn.damai:id/ll_perform_item'})
        chosen_level_idx = -1
        for idx in self.level_idx:
            if rs_1[idx].find(attrs={'text': '缺货登记'}) is None:
                chosen_level_idx = idx
                break
            if idx == self.level_idx[-1]:
                raise OutOfStockError(self.amount, 0)
        client.click_xml_node(rs_1[chosen_level_idx])
        client.wait_until_found({'resource-id': 'cn.damai:id/img_jia'}, intercept=False)
        for i in range(self.amount - 1):
            client.click_xml_node(client.rs[0])
        if not self.ignore_num:
            client.refresh_xml()
            client.find_xml_by_attr({'resource-id': 'cn.damai:id/tv_num'})
            found = int(str(client.rs[0]['text']).removesuffix("张"))
            if found != self.amount:
                raise OutOfStockError(self.amount, found)
        client.wait_to_click({'resource-id': 'cn.damai:id/btn_buy_view'}, refresh_xml=self.ignore_num)


class FireStage(Stage):
    def __init__(self, need: int, ym_token: Optional[str]):
        super().__init__()
        self.need = need
        if ym_token is not None:
            self.captcha_parser = SliderSolver(ym_token)

    def run(self, client: AndroidClient):
        client.refresh_xml(intercept=False)
        if len(client.find_xml_by_attr({'text': '我知道了'})) > 0:
            raise OutOfStockError(self.need, 0)

        client.wait_until_found({'text': '确认订单'},
                                intercept=False, timeout=10)
        while client.device.app_current()['package'] == 'cn.damai':
            print('current app:', client.device.app_current()['package'])
            if len(client.find_xml_by_attr({'text': '提交订单'})) > 0:
                submit_rs = client.rs
                if len(client.find_xml_by_attr(
                        {'checked': 'false', 'checkable': 'true', 'resource-id': 'cn.damai:id/checkbox'})) > 0:
                    for x in client.rs:
                        print('Unchecked audience detected')
                        client.click_xml_node(x)
                print('Submitting order')
                client.click_xml_node(submit_rs[0])
            client.refresh_xml()
            if len(client.find_xml_by_attr({'text': '亲，请按照说明进行验证哦'})) > 0:
                print('captcha triggered')
                if self.captcha_parser is None:
                    while True:
                        client.refresh_xml()
                        if len(client.find_xml_by_attr({'text': '亲，请按照说明进行验证哦'})) == 0:
                            print('captcha out')
                            break
                else:
                    if len(client.find_xml_by_attr({'text': '在在加载验证码信息，请稍等'})) > 0:
                        print('awaiting captcha to be loaded')
                        continue
                    if len(client.find_xml_by_attr({'text': '请稍等片刻再点击刷新哦'})) > 0:
                        print('captcha failed too many times')
                        raise RuntimeError('failed to solve captcha in time.')
                    slider_node = client.find_xml_by_attr({'resource-id': 'scratch-captcha-btn'})[0]
                    rail_node = slider_node.parent
                    captcha_node = client.find_xml_by_attr({'resource-id': 'scratch-captcha-question-container'})[
                        0].parent

                    slider_xyxy = parse_node_xyxy(slider_node)
                    rail_xyxy = parse_node_xyxy(rail_node)

                    client.device.touch.down((slider_xyxy[0] + slider_xyxy[2]) / 2,
                                             (slider_xyxy[1] + slider_xyxy[3]) / 2)

                    slider_center_cur = [(slider_xyxy[0] + slider_xyxy[2]) / 2, (slider_xyxy[1] + slider_xyxy[3]) / 2]

                    t1 = time.time()
                    captcha_try_cnt = 0
                    while True:
                        captcha_try_cnt += 1
                        slider_center_cur[0] += 50
                        slider_center_cur[1] = (slider_xyxy[1] + slider_xyxy[3]) / 2 + random.randrange(-2, 2)

                        if slider_center_cur[0] > rail_xyxy[2]:
                            print('Captcha FAIL')
                            client.device.touch.up(0, 0)
                            client.device.xpath.click('//android.view.View[@text=""]')
                            break

                        client.device.touch.move(slider_center_cur[0], slider_center_cur[1])

                        captcha_img = client.shot_xml(captcha_node)
                        try:
                            right_x = self.captcha_parser.solve(captcha_img)
                            client.device.touch.up(right_x, slider_center_cur[1])
                            print('Solve SUCCESS')
                            break
                        except CaptchaSolveError:
                            print(f'Captcha Solve attempt failed on[{captcha_try_cnt}]')
                            pass
                    t2 = time.time()
                    print(f'Captcha solve elapsed {t2 - t1:.2f} seconds')
            if len(client.find_xml_by_attr(attrs={'text': '继续尝试'})) > 0:
                client.click_xml_node(client.rs[0])

            if len(client.find_xml_by_attr(attrs={'text': '我知道了'})) > 0:
                client.click_xml_node(client.rs[0])
                raise OutOfStockError(self.need, 0)


class ResetAudienceStage(Stage):
    def __init__(self, audiences: list[tuple[str, str]]):
        super().__init__()
        self.audiences = audiences

    def run(self, client: AndroidClient):
        if self.audiences is None or self.audiences == []:
            return
        client.wait_to_click({'text': '我的'}, timeout=10)
        client.wait_to_click({'text': '观演人'})
        client.wait_until_found({'text': '常用观演人'})
        time.sleep(1)
        try:
            while True:
                client.wait_to_click({'resource-id': 'cn.damai:id/custom_delete'}, timeout=1, gap=2)
                client.wait_to_click({'resource-id': 'cn.damai:id/damai_dialog_confirm_btn'})
                time.sleep(0.5)
        except ClientWaitTimeout:
            pass
        for audience in self.audiences:
            client.wait_to_click({'resource-id': 'cn.damai:id/add_customer_btn'})
            client.wait_until_found({'text': '请填写观演人姓名'})
            time.sleep(1)
            client.wait_to_click({'resource-id': 'cn.damai:id/add_contacts_name'})
            client.device.send_keys(audience[0])
            client.wait_to_click({'resource-id': 'cn.damai:id/add_contacts_idcard_number'})
            client.device.send_keys(audience[1])
            client.key_back()
            client.device.xpath.click('//android.widget.CheckBox')
            client.wait_to_click({'resource-id': 'cn.damai:id/add_contacts_save_btn'})
            client.wait_until_found({'text': '常用观演人'})
        client.key_back()
        client.key_back()


class DaMaiBuyTask(ClientTask):

    def __init__(self, audiences: list[tuple[str, str]], search_text: str, city: Optional[str], date_idx: list[int],
                 level_idx: list[int], ym_token: str):
        super().__init__()
        self.append(InterceptStage())
        self.append(StartAppStage(0, 'cn.damai'))
        self.append(ResetAudienceStage(audiences))
        self.append(SearchStage(search_text))
        if city is not None:
            self.append(SelectCityStage(city))
        else:
            self.append(EnterFirstSearchResultStage())
        self.append(CheckFareStage())
        self.append(SelectDateStage(date_idx, level_idx, len(audiences)))
        self.append(FireStage(len(audiences), ym_token))
        self.auto_serial()
        self.handler = damai_handler


def damai_handler(_client: AndroidClient, _task: DaMaiBuyTask, _exception):
    if isinstance(_exception, OutOfStockError):
        print(f'库存不足:{_exception.found}/{_exception.need}，重试中。')
        if isinstance(_task.current_stage(), FireStage):
            _task.reset_stage_to(_task.current_stage_idx - 1)
            return True
        if isinstance(_task.current_stage(), SelectDateStage):
            _client.key_back()
            _task.reset_stage_to(5)
            return True
    raise _exception


def damai_handler_non_except(_client: AndroidClient, _task: DaMaiBuyTask, _exception):
    if isinstance(_exception, OutOfStockError):
        print(f'库存不足:{_exception.found}/{_exception.need}，重试中。')
        if isinstance(_task.current_stage(), FireStage):
            _task.reset_stage_to(_task.current_stage_idx - 1)
            return True
        if isinstance(_task.current_stage(), SelectDateStage):
            _client.key_back()
            _task.reset_stage_to(5)
            return True
    print('Giving up task')
    return False
