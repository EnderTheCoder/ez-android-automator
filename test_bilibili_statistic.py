from ez_android_automator.bilibili_task import BilibiliStatisticTask
from ez_android_automator.client import create_usb_client

client = create_usb_client()
task = BilibiliStatisticTask('不能说的秘密')

statistic = None


def print_statistic(e_task):
    global statistic
    statistic = e_task.statistic


task.set_callback(print_statistic)
client.set_task(task)
client.run_current_task()

print("最终播放数据：", statistic)
