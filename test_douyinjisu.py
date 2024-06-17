"""
@Time: 2024/6/16 17:50
@Auth: coin
@Email: 918731093@qq.com
@File: bilibili_task.py
@IDE: PyCharm
@Motto：one coin
"""
import uiautomator2
from ez_android_automator.client import PublishClient
from ez_android_automator.douyinjisu_task import DouyinjisuPublishVideoTask, DouyinjisuPhoneLoginTask

client = PublishClient(uiautomator2.connect_usb())
# print(client.dump_xml())
# exit()

# task = DouyinjisuPhoneLoginTask("13038005054")
# client.set_task(task)
# client.run_current_task_async()
# task.send_captcha(input("输入验证码"))

client.set_task(
    DouyinjisuPublishVideoTask(5, '', '忙忙碌碌寻宝藏', 'http://192.168.3.32:8000/media/video/17060924290060.mp4'))
client.run_current_task()
