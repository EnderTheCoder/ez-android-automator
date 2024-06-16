from ez_android_automator.manager import Manager
from ez_android_automator.bilibili_task import BilibiliPhoneLoginTask

manager = Manager()
manager.push_task(BilibiliPhoneLoginTask('xxx'))
manager.push_task(BilibiliPhoneLoginTask('xxx'))
manager.run()