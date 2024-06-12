import uiautomator2

from ez_android_automator.client import *
from ez_android_automator.xhs_task import XhsPhoneLoginTask

cli = PublishClient(uiautomator2.connect())


def success_callback():
    print('登陆成功')


task = XhsPhoneLoginTask(input('输入手机号'))
task.set_callback(success_callback)
cli.set_task(task)
cli.run_current_task_async()
task.send_captcha(input("输入验证码"))
