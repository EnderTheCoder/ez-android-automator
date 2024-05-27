from ez_android_automator.bilibili_task import BilibiliAccountTask
from ez_android_automator.client import create_usb_client

client = create_usb_client()  # 创建客户端
task = BilibiliAccountTask('/data/data/tv.danmaku.bili', '/app_account', 'abdSh.sh', "/sdcard/adbAccountTest",
                           'AccountData')  # 创建任务
client.set_task(task)  # 设置任务
client.run_current_task()  # 开始运行任务
