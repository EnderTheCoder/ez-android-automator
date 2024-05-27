from ez_android_automator.bilibili_task import BilibiliGetAccountTask
from ez_android_automator.client import create_usb_client

client = create_usb_client()  # 创建客户端
task = BilibiliGetAccountTask('/data/data/tv.danmaku.bili', '/app_account', 'abdSh.sh', "/sdcard/adbAccountTest",
                              'AccountData/', 'app_account.tar.gz')  # 创建任务
client.set_task(task)  # 设置任务
client.run_current_task()  # 开始运行任务
