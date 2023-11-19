from client import PublishTask


class RedBookPublishVideoTask(PublishTask):
    """
    Publish a video on Xiaohongshu.
    """

    def __init__(self, title: str, content: str, video: str):
        super().__init__(title, content, video, '')


