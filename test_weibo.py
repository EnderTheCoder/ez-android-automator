"""
@Time: 2024/5/14 21:00
@Auth: coin
@Email: 918731093@qq.com
@File: test_weibo.py
@IDE: PyCharm
@Motto：one coin
"""
import uiautomator2
from ez_android_automator.client import PublishClient
from ez_android_automator.weibo_task import WeiboPhoneLoginTask, WeiboPublishVideoTask

client = PublishClient(uiautomator2.connect_usb())
# print(client.dump_xml())
# exit()

# task = WeiboPhoneLoginTask("13038005054")
# client.set_task(task)
# client.run_current_task_async()
# task.send_captcha(input("输入验证码"))

client.set_task(
    WeiboPublishVideoTask(5, '我总在', '忙忙碌碌寻宝藏', 'http://192.168.3.32:8000/media/video/17060924290060.mp4'))
client.run_current_task()
