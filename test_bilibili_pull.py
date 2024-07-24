from ez_android_automator.app_file import PullAccountTask
from ez_android_automator.bilibili_task import BilibiliFilePkg
from ez_android_automator.client import create_usb_client

client = create_usb_client()
client.set_task(PullAccountTask(BilibiliFilePkg(), '.', 'bilibili_test'))
client.run_current_task()
