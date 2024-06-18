from ez_android_automator.bilibili_task import BilibiliPushAccountTask, BilibiliStatisticTask
from ez_android_automator.client import create_usb_client, CombinedSequentialTask

client = create_usb_client()

task = CombinedSequentialTask(
    BilibiliPushAccountTask(from_packagename="", from_path="", sh_name="", to_path="", server_to_path="", tar_name=""),
    BilibiliStatisticTask(video_title="")
)

client.set_task(task)
client.run_current_task()
