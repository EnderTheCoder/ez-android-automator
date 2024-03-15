from ez_android_automator.client import *
from ez_android_automator.xhs_task import XhsPasswordLoginTask

cli = PublishClient(uiautomator2.connect())

cli.set_task(XhsPasswordLoginTask(input('输入手机号'), input('输入密码')))
cli.run_current_task()
