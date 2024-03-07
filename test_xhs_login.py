import uiautomator2

from ez_android_automator.client import *
from ez_android_automator.xhs_task import XhsPhoneLoginTask

cli = PublishClient(uiautomator2.connect())


def test():
    return input('输入验证码')


cli.set_task(XhsPhoneLoginTask(input('输入手机号'), test))
cli.run_current_task()
