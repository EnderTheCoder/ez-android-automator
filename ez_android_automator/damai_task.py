"""
@Time: 2024/7/27 7:08
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: damai_task.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.

Auto ticket buying tasks for damai app.
"""

from ez_android_automator.client import ClientTask, StartAppStage, Stage, AndroidClient


class InterceptStage(Stage):
    def run(self, client: AndroidClient):
        client.intercept_to_click({'resource-id': 'cn.damai:id/new_person_dialog_top_close_iv'})
        client.intercept_to_click({'resource-id': 'cn.damai:id/homepage_popup_window_close_btn'})
        client.intercept_to_click({'resource-id': 'cn.damai:id/homepage_advert_pb'},
                                  {'resource-id': 'cn.damai:id/channel_search_text'})


class SearchStage(Stage):
    def __init__(self, search_text: str):
        super().__init__()
        self.search_text = search_text

    def run(self, client: AndroidClient):
        client.wait_to_click({'resource-id': 'cn.damai:id/channel_search_text'})
        client.device.send_keys(self.search_text)
        client.device.send_action("search")


class SelectCityStage(Stage):
    def __init__(self, city: str):
        super().__init__()
        self.city = city

    def run(self, client: AndroidClient):
        client.wait_until_found({'resource-id': 'cn.damai:id/tour_recyclerView'})
        bounded_cities = client.rs[0].find_all(attrs={'resource-id': 'cn.damai:id/tv_city'})
        for bounded_city in bounded_cities:
            if bounded_city['text'] == self.city:
                pass


class DaMaiBuyTask(ClientTask):
    def __init__(self, search_text: str, city: str):
        super().__init__()
        self.append(InterceptStage())
        self.append(StartAppStage(0, 'cn.damai'))
        self.append(SearchStage(search_text))
        self.append(SelectCityStage(city))
        self.auto_serial()
