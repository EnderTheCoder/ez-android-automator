import uiautomator2

from ez_android_automator.client import PublishClient

from ez_android_automator.bilibili_task import OpenAppStage, BeforeLoginStage, PhoneAuthCodeStage

client = PublishClient(uiautomator2.connect_usb())
print(client.dump_xml())
exit()
# client.set_task(OpenAppStage(0))
# client.set_task(BeforeLoginStage(1, '13038005054'))
client.set_task(PhoneAuthCodeStage(2))
client.run_current_task()
