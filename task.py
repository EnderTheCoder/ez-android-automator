from client import PublishClient


class Stage:
    def __init__(self, stage_serial):
        self.stage_serial = stage_serial

    def run(self, client: PublishClient):
        pass

    def get_serial(self):
        return self.stage_serial


class PublishTask:
    def __init__(self, title: str, content: str, video: str, photo: str):
        self.title = title
        self.content = content
        self.video = video
        self.photo = photo
        self.stages = list[Stage]
        self.current_stage = -1
        self.exception = None

    def run(self, client: PublishClient):
        try:
            for i, stage in enumerate(self.stages):
                self.current_stage = i
                stage.run(client)
        except Exception as e:
            self.exception = e

    def get_stage(self):
        return self.current_stage

    def is_going(self):
        return -1 < self.current_stage < len(self.stages) and not self.is_exception()

    def is_finished(self):
        return self.current_stage == len(self.stages)

    def is_exception(self):
        return self.exception is None
