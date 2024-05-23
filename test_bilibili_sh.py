from ez_android_automator.bilibili_task import BilibiliStatisticTask
from ez_android_automator.client import create_usb_client

client = create_usb_client()  # 创建客户端
task = BilibiliStatisticTask('不能说的秘密')  # 创建任务
client.set_task(task)  # 设置任务
client.run_current_task()  # 开始运行任务