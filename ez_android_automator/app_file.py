"""
@Time: 2024/07/20 08:00
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: app_file.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.

Provide helper classes and functions for uploading or downloading app data files from android client.
"""
import json
import os
import tarfile

from ez_android_automator.client import AndroidClient


class AppFilePkg(object):
    def __init__(self, pkg_name: str, create_time: float, path_mappings: dict):
        self.pkg_name = pkg_name  # app package name
        self.create_time = create_time
        self.path_mappings = path_mappings  # arc_name --> remote_path
        self.base_remote_tmp_path = '/sdcard/tmp'

    def add_path_mapping(self, pkg_path, original_path):
        self.path_mappings[pkg_path] = original_path

    def to_json(self):
        return json.dumps({
            'pkg_name': self.pkg_name,
            'create_time': self.create_time,
            'path_mappings': self.path_mappings
        })

    def pull(self, local_dir, file_name, client: AndroidClient, save_storage: bool = True):
        """
        Pull file from client to server.
        :warning: the `file_name` param provided should not be duplicated. It is recommended to use random file name.
        :param local_dir: a local directory to pull file,
        :param file_name: data from client will be store as 2 file: <file_name>.json and <file_name>.tar.gz.
        :param client: client to execute this pull function.
        :param save_storage: whether to del tmp files in tend to save storage.
        """
        local_tmp_dir_path = str(os.path.join(local_dir, file_name))
        os.makedirs(local_tmp_dir_path, exist_ok=True)
        try:
            for local_path, remote_path in self.path_mappings:
                local_tmp_file_path = os.path.join(local_tmp_dir_path, local_path)
                client.device.pull(remote_path, local_tmp_file_path)
                with tarfile.open(os.path.join(local_dir, file_name) + '.tar.gz', mode='w:gz') as tar:
                    tar.add(local_tmp_file_path, arcname=local_path)
        except Exception as e:
            os.rmdir(local_tmp_dir_path)  # clear tmp file dir if the client failed to pull.
            raise e
        if save_storage:
            os.rmdir(local_tmp_dir_path)

    def push(self, local_dir, file_name, client: AndroidClient, save_storage: bool = True):
        """
        Push file from server to client.
        :param local_dir: a local directory to find files and extract them.
        :param file_name: data from client will be read from 2 file: <file_name>.json and <file_name>.tar.gz.
        :param client: client to execute this push function.
        :param save_storage: whether to del tmp files in tend to save storage.
        """
        local_tmp_dir_path = str(os.path.join(local_dir, file_name))
        if not os.path.exists(local_tmp_dir_path):
            with tarfile.open(f'{file_name}.tar.gz', mode='r:gz') as tar_ref:
                tar_ref.extractall(local_tmp_dir_path)
        remote_tmp_dir_path = str(os.path.join(self.base_remote_tmp_path, file_name))
        client.device.shell(f'mkdir {self.base_remote_tmp_path}')
        client.device.shell(f'mkdir {self.base_remote_tmp_path}/{file_name}')
        for arc_name, remote_path in self.path_mappings:
            client.device.push(os.path.join(local_tmp_dir_path, arc_name), os.path.join(remote_tmp_dir_path, arc_name))
            client.su_shell(f'mv {os.path.join(remote_tmp_dir_path, arc_name)} {remote_path}')
            client.su_shell(f'chmod 777 -R {remote_path}')
        client.device.shell(f'rm {remote_tmp_dir_path}')
        if save_storage:
            os.rmdir(local_tmp_dir_path)


def load_from_files(json_path, tar_path) -> AppFilePkg:
    if not os.path.exists(json_path):
        raise FileNotFoundError(json_path)
    if not os.path.exists(tar_path):
        raise FileNotFoundError(tar_path)
    with open(json_path, 'r') as f:
        json_data = json.load(f)
        return AppFilePkg(json_data['pkg_name'], json_data['create_time'], json_data['path_mappings'])
