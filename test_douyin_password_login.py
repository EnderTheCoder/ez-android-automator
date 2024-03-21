import uiautomator2
from ez_android_automator.client import PublishClient
from ez_android_automator.douyin_task import DouyinPasswordLoginTask

cli = PublishClient(uiautomator2.connect())

cli.set_task(DouyinPasswordLoginTask('13038005054', '990414'))
cli.run_current_task()
# 账号密码登录需要验证码
