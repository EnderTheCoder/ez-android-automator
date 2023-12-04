"""
@Time: 2023/11/30 18:04
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: unicom_http_api.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import adbutils
import requests
from ez_android_automator.client import AndroidClient
from ez_android_automator.unicom_task import UnicomSignTask
import socket
import uiautomator2
import threading


def scan_port(ip_address, port):
    try:
        s = socket.create_connection((ip_address, port), 0.1)
        s.shutdown(socket.SHUT_RDWR)
        return True
    except socket.error:
        return False


def scan_network(addr: str, port: int):
    mask = int(addr.split('/')[1])

    static_addr_parts = addr.split('.')[:int(mask / 8)]
    static_addr = ''
    for part in static_addr_parts:
        static_addr += part + '.'
    open_addr = []
    for i in range(1, 255):
        new_addr = static_addr + str(i)
        if scan_port(new_addr, port):
            open_addr.append(new_addr)
            print(f'{new_addr}:{port} open')
    return open_addr


class UnicomExecutorClient:
    def __init__(self, api_addr):
        self.addr = api_addr
        self.android_clients = list[AndroidClient]()
        if requests.get(api_addr).status_code != 200:
            raise requests.HTTPError('Invalid server addr.')

    def pick(self):
        response = requests.get(self.addr + '/executor/pick')
        data = response.json()
        if response.status_code >= 300 or data['code'] < 0:
            raise requests.HTTPError('Failed to pick profile due to a http failure.')
        elif data['code'] == 101:
            return None
        else:
            return data['data']

    def append_device(self, device: uiautomator2.Device):
        self.android_clients.append(AndroidClient(device))

    def report(self, task_id: int, message: str = 'success', is_successful: bool = True, is_kill_task: bool = False):
        response = requests.post(self.addr + '/executor/report', json={
            'task_id': task_id,
            'message': message,
            'is_successful': is_successful,
            'is_kill_task': is_kill_task
        })
        data = response.json()
        if response.status_code >= 300 or data['code'] < 0:
            raise requests.HTTPError('Failed to pick profile due to a http failure.')

    def import_devices_from_network(self, addr):
        print(f'importing devices from {addr}')
        ip_list = scan_network(addr, 5555)
        for i, ip in enumerate(ip_list):
            device = uiautomator2.connect(ip)
            self.android_clients.append(AndroidClient(device))
        print(f'scan complete, found {len(self.android_clients)} devices')

    def import_devices_from_usb(self):
        print('importing devices from usb')
        for device in adbutils.AdbClient().device_list():
            self.android_clients.append(AndroidClient(uiautomator2.connect_usb(device.serial)))
        print(f'found {len(self.android_clients)} devices')

    def thread_run(self, client: AndroidClient, server_task):
        client.set_task(UnicomSignTask(server_task['profile']['social_id'], server_task['profile']['addr']))
        client.run_current_task()
        if not client.task.is_exception():
            self.report(server_task['task_id'], 'success', client.task.is_finished())
            print('Success on task {}'.format(server_task['task_id']))
        else:
            self.report(server_task['task_id'],
                        f'Stopped at {client.task.current_stage}/{len(client.task.stages)}, reason: {str(client.task.exception)}',
                        client.task.is_finished())
            print('Fail on task {}'.format(server_task['task_id']))
        client.unlock()

    def start(self):
        print('start to run tasks on clients:')
        while True:
            server_task = self.pick()
            if server_task is not None:
                print('picked task:{} from server'.format(server_task['task_id']))
                while True:
                    found_client = False
                    for client in self.android_clients:
                        if client.is_usable():
                            client.lock()
                            found_client = True
                            thread = threading.Thread(target=self.thread_run, args=(client, server_task))
                            thread.start()
                            break
                    if found_client:
                        break
