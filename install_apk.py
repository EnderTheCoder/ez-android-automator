"""
@Time: 2024/1/3 18:36
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: install_apk.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import uiautomator2

from ez_android_automator.install_apk_task import InstallApk
from ez_android_automator.client import PublishClient

address = input('input address for your device:')
file = input('input file path for your apk file:')
package_name_to_verify = input('input package name to verify after installation, type in `skip` to skip verification:')
client = PublishClient(uiautomator2.connect(address))
client.set_task(InstallApk(file, package_name_to_verify))
client.run_current_task()
pass
