from ez_android_automator.client import create_usb_client

client = create_usb_client()
client.push('./DCIM', '/sdcard/test')
