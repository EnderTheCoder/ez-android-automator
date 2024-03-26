import uiautomator2
from ez_android_automator.client import PublishClient
from ez_android_automator.kuaishou_task import KuaishouPasswordLoginTask

cli = PublishClient(uiautomator2.connect())

cli.set_task(KuaishouPasswordLoginTask('13038005054', 'zhf990414'))
cli.run_current_task()
# 账号密码登录需要图片验证
