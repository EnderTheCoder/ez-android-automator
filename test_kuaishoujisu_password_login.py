import uiautomator2
from ez_android_automator.client import PublishClient
from ez_android_automator.kauishoujisu_task import KuaishoujisuPasswordLoginTask

cli = PublishClient(uiautomator2.connect())

cli.set_task(KuaishoujisuPasswordLoginTask('13038005054', 'zhf990414'))
cli.run_current_task()
