import os
import subprocess

def pull_file_from_device(device_path, local_path):
    command = f"adb pull {device_path} {local_path}"
    subprocess.run(command, shell=True)

device_path = "/sdcard/adbAccountTest/app_account.tar.gz"  # 设备上的文件路径
local_path = "AccountData"  # 电脑上的保存路径

pull_file_from_device(device_path, local_path)
