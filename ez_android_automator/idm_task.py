import time

from .client import PublishClient, ClientTask, Stage, AndroidClient, CallbackWaitTimeoutException, ClientWaitTimeout


class OpenAppStage(Stage):
    def run(self, client: PublishClient):
        client.restart_app("idm.internet.download.manager.plus")


class InputStage(Stage):
    def __init__(self, serial, url: str):
        super().__init__(serial)
        self.url = url

    def run(self, client: PublishClient):
        client.wait_to_click({'resource-id': 'idm.internet.download.manager.plus:id/fab_expand_menu_button'}, gap=1)
        client.wait_to_click({'text': '添加链接'})
        client.wait_to_click({'text': '下载链接'})
        client.device.send_keys(self.url)
        client.wait_to_click({'text': '连接'})
        client.wait_to_click({'text': '开始'})
        try:
            client.wait_to_click({'text': '确认'})
        except ClientWaitTimeout:
            pass


class WaitFinishStage(Stage):
    def __init__(self, serial, timeout: float):
        super().__init__(serial)
        self.timeout = timeout

    def run(self, client: AndroidClient):
        time_start = time.time()

        single = None
        while single is None:
            client.refresh_xml()
            lst = client.find_xml_by_attr({'resource-id': 'idm.internet.download.manager.plus:id/progressView'})
            if len(lst) == 0:
                raise Exception(
                    'No download progress view found in list. '
                    'This is probably caused by download task is not successfully created.'
                )
            single = lst[0].find(attrs={'text': '完成'})
            if time.time() - time_start > self.timeout:
                raise ClientWaitTimeout()
            time.sleep(0.1)


class IDMPullTask(ClientTask):
    def __init__(self, res_url: str, download_timeout: float = 0):
        super().__init__()
        self.url = res_url
        self.timeout = download_timeout
        self.stages.append(OpenAppStage(0))
        self.stages.append(InputStage(1, self.url))
        self.stages.append(WaitFinishStage(2, self.timeout))
