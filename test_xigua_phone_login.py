import uiautomator2
from ez_android_automator.client import PublishClient
from ez_android_automator.xigua_task import XiguaPhoneLoginTask

cli = PublishClient(uiautomator2.connect())


def test_callback():
    return input('输入验证码')


cli.set_task(XiguaPhoneLoginTask('13038005054', test_callback))
cli.run_current_task()
