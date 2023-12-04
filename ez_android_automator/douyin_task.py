from ez_android_automator.client import Stage, PublishClient, PublishTask


class OpenAppStage(Stage):
    """
    Use adb shell command to start douyin.
    """

    def run(self, client: PublishClient):
        client.device.app_stop('com.ss.android.ugc.aweme')
        client.device.shell('am start -n com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.main.MainActivity')


class ClickPublishButtonStage(Stage):
    """
    Wait until the app is up and click the publish button to enter gallery.
    """

    def run(self, client: PublishClient):
        def wait_main_page(client_: PublishClient) -> bool:
            return len(client_.find_xml_by_attr({'content-desc': '拍摄，按钮'})) > 0

        def enter_gallery(client_: PublishClient) -> bool:
            return len(client_.find_xml_by_attr({'text': '相册'})) > 0

        client.wait_until_finish(wait_main_page)
        client.click_xml_node(client.rs[0])
        client.wait_until_finish(enter_gallery)
        client.click_xml_node(client.rs[0])


class CopyVideoToGalleryStage(Stage):
    """
    Copy a media file to gallery path.
    """

    def __init__(self, stage_serial, video):
        super().__init__(stage_serial)
        self.video = video

    def run(self, client: PublishClient):
        client.copy_media_to_gallery(self.video)


class SelectVideoStage(Stage):
    """
    Choose the first video in gallery and press 'next' button.
    """

    def run(self, client: PublishClient):
        def is_video_tag(client_: PublishClient):
            return len(client_.find_xml_by_attr({'text': '视频'})) > 0

        client.wait_until_finish(is_video_tag)
        client.click_xml_node(client.rs[0])

        def is_first_img(client_: PublishClient):
            return len(
                client_.find_xml_by_attr({'resource-id': 'com.ss.android.ugc.aweme:id/no0', 'index': '0'})) > 0

        client.wait_until_finish(is_first_img)
        client.click_xml_node(client.rs[0])

        def is_next_button(client_: PublishClient):
            return len(client_.find_xml_by_attr({'text': '下一步'}))

        client.wait_until_finish(is_next_button)
        client.click_xml_node(client.rs[0])


class SetVideoOptions(Stage):
    def __init__(self, stage_serial, title: str):
        super().__init__(stage_serial)
        self.title = title

    def run(self, client: PublishClient):
        def is_title_blank(client_: PublishClient):
            return len(client_.find_xml_by_attr({'text': '添加作品描述..'}))

        client.wait_until_finish(is_title_blank)
        client.click_xml_node(client.rs[0])
        client.device.send_keys(self.title)
        client.device.keyevent('back')
        client.find_xml_by_attr({'text': '发布'})
        client.click_xml_node(client.rs[0])
        pass


class DouyinVideoPublishTask(PublishTask):
    """
    Publish a video on douyin.
    """

    def __init__(self, title: str, content: str, video: str):
        super().__init__(title, content, video, '')
        self.stages.append(OpenAppStage(0))
        self.stages.append(CopyVideoToGalleryStage(1, video))
        self.stages.append(ClickPublishButtonStage(2))
        self.stages.append(SelectVideoStage(3))
        self.stages.append(SetVideoOptions(4, title))
