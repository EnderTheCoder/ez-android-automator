import time

from ez_android_automator.client import create_usb_client
from ez_android_automator.app_file import AppFilePkg

client = create_usb_client()
pkg = AppFilePkg(None, time.time(), path_mappings={'DCIM': '/sdcard/test.txt'})
pkg.pull('/home/ender/PycharmProjects/ez-android-automator', 'test_download', client)
