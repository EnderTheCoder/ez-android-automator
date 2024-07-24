"""
@Time: 2024/07/20 08:00
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: app_file.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.

Provide helper classes and functions for uploading or downloading app data files from android client.
Remember to use rooted devices to upload/download app data files in /data/data dir.
"""
import json
import os
import shutil
import tarfile
from typing import Union

from .client import AndroidClient, ClientTask, Stage, StopAppStage, ClearAppStage
from .util import posix_path_join


class AppFilePkg(object):
    def __init__(self, pkg_name: Union[str, None], create_time: float, path_mappings: Union[list[str], dict[str, str]]):
        self.pkg_name = pkg_name  # app package name
        self.create_time = create_time
        if isinstance(path_mappings, dict):
            self.path_mappings = path_mappings  # arc_name --> remote_path
        elif isinstance(path_mappings, list):
            self.path_mappings = {}
            for path_mapping in path_mappings:
                self.path_mappings[path_mapping] = posix_path_join('/data/data', pkg_name, path_mapping)
        self.base_remote_tmp_path = '/sdcard/tmp'

    def add_path_mapping(self, pkg_path, original_path):
        self.path_mappings[pkg_path] = original_path

    def dict(self) -> dict:
        return {
            'pkg_name': self.pkg_name,
            'create_time': self.create_time,
            'path_mappings': self.path_mappings
        }

    def pull(self, root_dir, file_name, client: AndroidClient, save_storage: bool = False):
        """
        Pull file from client to server.
        :warning: the `file_name` param provided should not be duplicated. It is recommended to use random file name.
        :param root_dir: a local directory to pull file,
        :param file_name: data from client will be store as 2 file: <file_name>.json and <file_name>.tar.gz.
        :param client: client to execute this pull function.
        :param save_storage: whether to del tmp files in tend to save storage.
        """
        local_tmp_dir_path = str(posix_path_join(root_dir, file_name))
        remote_tmp_dir_path = str(posix_path_join(self.base_remote_tmp_path, file_name))
        try:
            if os.path.exists(local_tmp_dir_path):
                shutil.rmtree(local_tmp_dir_path)
            os.makedirs(local_tmp_dir_path, exist_ok=False)
            if not client.exists(remote_tmp_dir_path):
                client.mkdir(remote_tmp_dir_path)
            json_exported = False
            for arc_name, remote_path in self.path_mappings.items():
                arc_name = os.path.basename(arc_name)
                local_tmp_file_path = posix_path_join(local_tmp_dir_path, arc_name)
                client.su_shell(['cp', '-r', remote_path, posix_path_join(remote_tmp_dir_path, arc_name)])
                client.su_shell(['chmod', '777', '-R', posix_path_join(remote_tmp_dir_path, arc_name)])
                client.pull(posix_path_join(remote_tmp_dir_path, arc_name), local_tmp_dir_path, True, True)
                with tarfile.open(posix_path_join(root_dir, file_name) + '.tar.gz', mode='w:gz') as tar:
                    tar.add(local_tmp_file_path, arcname=arc_name)
                    if not json_exported:
                        json_exported = True
                        json_path = posix_path_join(local_tmp_dir_path, '.package_info.json')
                        with open(json_path, 'w') as json_f:
                            json.dump(self.dict(), json_f)
                            tar.add(json_path)
            if save_storage:
                shutil.rmtree(local_tmp_dir_path)
            if client.exists(remote_tmp_dir_path):
                client.rmdir(remote_tmp_dir_path)
        except Exception as e:
            shutil.rmtree(local_tmp_dir_path)  # clear tmp file dir if the client failed to pull.
            if client.exists(remote_tmp_dir_path):
                client.rmdir(remote_tmp_dir_path)
            raise e

    def push(self, root_dir, file_name, client: AndroidClient, save_storage: bool = False):
        """
        Push file from server to client.
        :param root_dir: a local directory to find files and extract them.
        :param file_name: data from client will be read from 2 file: <file_name>.json and <file_name>.tar.gz.
        :param client: client to execute this push function.
        :param save_storage: whether to del tmp files in tend to save storage.
        """
        local_tmp_dir_path = str(posix_path_join(root_dir, file_name))
        remote_tmp_dir_path = str(posix_path_join(self.base_remote_tmp_path, file_name))
        try:
            if not os.path.exists(local_tmp_dir_path):
                with tarfile.open(f'{file_name}.tar.gz', mode='r:gz') as tar_ref:
                    tar_ref.extractall(local_tmp_dir_path)
            if not client.exists(self.base_remote_tmp_path):
                client.mkdir(self.base_remote_tmp_path)
            client.mkdir(posix_path_join(self.base_remote_tmp_path, file_name), exists_ok=True)
            for arc_name, remote_path in self.path_mappings.items():
                arc_name = os.path.basename(arc_name)
                client.push(posix_path_join(local_tmp_dir_path, arc_name), remote_tmp_dir_path)
                if client.exists(remote_path):
                    client.rmdir(remote_path, True, True)
                client.shell(f'mv {posix_path_join(remote_tmp_dir_path, arc_name)} {remote_path}', su=True,
                             print_ret=True)
                client.shell(f'chmod 777 -R {remote_path}', su=True, print_ret=True)
            client.rmdir(remote_tmp_dir_path)
            if save_storage:
                shutil.rmtree(local_tmp_dir_path)
            if client.exists(remote_tmp_dir_path):
                client.rmdir(remote_tmp_dir_path)
        except Exception as e:
            if client.exists(remote_tmp_dir_path):  # clear tmp file dir if the client failed to push.
                client.rmdir(remote_tmp_dir_path)
            raise e


class PullStage(Stage):
    def __init__(self, stage_serial: int, pkg: AppFilePkg, root_dir: str, file_name: str, save_storage: bool = False):
        super().__init__(stage_serial)
        self.app_pkg = pkg
        self.root_dir = root_dir
        self.save_storage = save_storage
        self.file_name = file_name

    def run(self, client: AndroidClient):
        self.app_pkg.pull(self.root_dir, self.file_name, client, self.save_storage)


class PullAccountTask(ClientTask):
    """
    Pull account data files from client to server. Use only on rooted devices.
    """

    def __init__(self,
                 pkg: AppFilePkg,
                 root_dir: str,
                 file_name: str,
                 save_storage: bool = False,
                 stop_before_push: bool = True):
        super().__init__()
        if stop_before_push:
            self.append(StopAppStage(0, pkg.pkg_name))
        self.append(PullStage(1, pkg, root_dir, file_name, save_storage))
        self.auto_serial()


class PushStage(Stage):
    def __init__(self, stage_serial: int, pkg: AppFilePkg, root_dir: str, file_name: str, save_storage: bool = False):
        super().__init__(stage_serial)
        self.app_pkg = pkg
        self.root_dir = root_dir
        self.save_storage = save_storage
        self.file_name = file_name

    def run(self, client: AndroidClient):
        self.app_pkg.push(self.root_dir, self.file_name, client, self.save_storage)


class PushAccountTask(ClientTask):
    """
    Push account data files from server to client. Use only on rooted devices.
    """

    def __init__(self,
                 pkg: AppFilePkg,
                 root_dir: str,
                 file_name: str,
                 save_storage: bool = False,
                 stop_before_push: bool = True):
        super().__init__()
        if stop_before_push:
            self.append(StopAppStage(0, pkg.pkg_name))
        self.append(ClearAppStage(1, pkg.pkg_name))
        self.append(PushStage(2, pkg, root_dir, file_name, save_storage))
        self.auto_serial()


def load_from_files(dir_path) -> AppFilePkg:
    """
    Load pkg using this function when try to upload an app pkg that already exists.
    """
    json_path = posix_path_join(dir_path, '.package_info.json')
    if not os.path.exists(dir_path):
        raise FileNotFoundError(dir_path)
    if not os.path.exists(json_path):
        raise FileNotFoundError(json_path)
    with open(json_path, 'r') as f:
        json_data = json.load(f)
        return AppFilePkg(json_data['pkg_name'], json_data['create_time'], json_data['path_mappings'])
