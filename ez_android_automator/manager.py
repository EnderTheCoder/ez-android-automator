"""
@Time: 2024/1/15 16:19
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: manager.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import queue
import warnings
import client
import threading


class Manager:
    def __init__(self):
        self.clients = dict[str, client.AndroidClient]()  # serial to client object
        self.tasks = queue.PriorityQueue()
        self.max_priority = 7

    def add_client(self, _client: client.AndroidClient):
        self.clients[_client.device.address] = _client

    def push_task(self, task: client.PublishTask):
        self.tasks.put((task.priority, task))

    def set_max_priority(self, priority: int):
        self.max_priority = priority

    def run_with_block(self):
        while True:
            if self.tasks.empty():
                for _client in self.clients.values():
                    if _client.is_usable():
                        task = self.tasks.get()
                        _client.set_task(task)

                        def failure_callback(__client: client.AndroidClient):
                            __client.task.shift_down_priority()
                            if __client.task.priority > self.max_priority:
                                self.push_task(__client.task)

                        threading.Thread(target=_client.run_current_task, args=(_client, failure_callback)).start()
                    else:
                        self.idle_task()
                        pass

    def maintain_clients(self):
        for serial in self.clients.keys():
            if not self.clients[serial].alive():
                warnings.warn(f'Client {serial} disconnected.')
                del self.clients[serial]

    def maintain_app_login(self):
        pass

    def idle_task(self):
        self.maintain_clients()
        self.maintain_app_login()
        pass
