import uiautomator2

from ez_android_automator.client import *
from ez_android_automator.xhs_task import XhsPhoneLoginTask

cli = PublishClient(uiautomator2.connect())


task = XhsPhoneLoginTask(input('输入手机号'))
cli.set_task(task)
cli.run_current_task_async()
task.send_captcha(input("输入验证码"))

