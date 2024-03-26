import uiautomator2
from ez_android_automator.client import PublishClient
from ez_android_automator.xigua_task import XiguaPasswordLoginTask

cli = PublishClient(uiautomator2.connect())

cli.set_task(XiguaPasswordLoginTask('13038005054', 'zhf990414'))
cli.run_current_task()
