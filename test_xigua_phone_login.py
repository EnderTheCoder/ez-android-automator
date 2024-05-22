import uiautomator2
from ez_android_automator.client import PublishClient
from ez_android_automator.xigua_task import XiguaPhoneLoginTask

cli = PublishClient(uiautomator2.connect())

cli.set_task(XiguaPhoneLoginTask('13038005054'))
cli.run_current_task()
