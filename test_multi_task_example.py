from ez_android_automator.client import create_usb_client, CombinedSequentialTask, PhoneLoginTask, PushAccountTask

client = create_usb_client()

task = CombinedSequentialTask(
    PhoneLoginTask('12345678'),
    PushAccountTask('', '', '', '', '', '')
)

client.set_task(task)
client.run_current_task()
