"""
@Time: 2024/1/3 18:25
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: install_apk_task.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
from ez_android_automator.client import AndroidClient, ClientTask, Stage


class InstallFailException(BaseException):
    def __init__(self, package_name: str):
        super().__init__(f'Failed on installing package {package_name}')


class InstallStage(Stage):
    def __init__(self, stage_serial, apk_file_name: str):
        super().__init__(stage_serial)
        self.apk_file_name = apk_file_name

    def run(self, client: AndroidClient):
        client.device.app_install(self.apk_file_name)


class VerifyPackageName(Stage):
    def __init__(self, stage_serial, verify_package_name):
        super().__init__(stage_serial)
        self.verify_package_name = verify_package_name

    def run(self, client: AndroidClient):
        if self.verify_package_name not in client.device.app_list():
            raise InstallFailException(self.verify_package_name)


class InstallApk(ClientTask):
    def __init__(self, apk_file_name: str, verify_package_name: str):
        super().__init__()
        self.append(InstallStage(0, apk_file_name))
        self.append(VerifyPackageName(1, verify_package_name))
