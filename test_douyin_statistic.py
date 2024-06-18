from ez_android_automator.douyin_task import DouyinStatisticTask
from ez_android_automator.client import create_usb_client

client = create_usb_client()  # 创建客户端
task = DouyinStatisticTask('研究生公寓 这是简介')  # 创建任务

statistic = None


def print_statistic(e_task):  # 编写回调函数
    global statistic
    statistic = e_task.statistic  # 将获取到的数据赋值给全局变量statistic从而将数据从任务中“拿出来”。


task.set_callback(print_statistic)  # 设置回调函数
client.set_task(task)  # 设置任务
client.run_current_task()  # 开始运行任务

print("最终播放数据：", statistic)  # 打印获取到的数据

