"""
@Time: 2024/7/27 7:19
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: test_damai.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import time

from ez_android_automator.client import ClientTask, AndroidClient, create_usb_client
from ez_android_automator.damai_task import DaMaiBuyTask, OutOfStockError

task = DaMaiBuyTask(
    [('祁佩璇', '152701199203060928')],
    "上海乐华",
    None,
    0,
    3)


def handle(_client: AndroidClient, _task: ClientTask, _exception):
    if isinstance(_exception, OutOfStockError):
        print(f'库存不足:{_exception.found}/{_exception.need}，重试中。')
        _client.device.keyevent('back')
        time.sleep(0.5)
        _task.reset_stage_to(5)
        return True
    return False


task.set_handler(handle)
client = create_usb_client()
client.set_task(
    task
)

client.run_current_task()
