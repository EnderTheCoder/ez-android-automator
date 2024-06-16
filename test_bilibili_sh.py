from ez_android_automator.bilibili_task import BilibiliGetAccountTask, BilibiliTranAccountTask
from ez_android_automator.client import create_usb_client

client = create_usb_client()  # 创建客户端
task = BilibiliGetAccountTask('/data/data/tv.danmaku.bili', 'app_account', 'abdSh.sh', "/sdcard/adbAccountTest",
                              'AccountData', 'app_account')  # 创建任务
client.set_task(task)  # 设置任务
# client.run_current_task()  # 开始运行任务
# task2 = BilibiliTranAccountTask('/data/data/tv.danmaku.bili', 'Datas', 'abdTransSh.sh', "/sdcard/adbAccountTest",
#                               'AccountData', 'app_account')
#
# client.set_task(task2)  # 设置任务
client.run_current_task()  # 开始运行任务
