"""
@Time: 2024/1/15 18:22
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: example.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""

from ez_android_automator.client import create_network_client
from ez_android_automator.manager import Manager
from ez_android_automator.xhs_task import XhsPublishVideoTask


# extend class to create your own callback. create callback class for each task class.
# bind callback to your task.
def success():
    print("we did it.")


def fail():
    print("we failed.")


# extend handler to create your own handler.
# bind handler to your client.


# Create clients
client1 = create_network_client('192.168.3.52:5555')
# client2 = create_network_client('192.168.1.2:5555')

# set exception handler
client1.set_exception_handler(fail)

# create task and callback
task = XhsPublishVideoTask(5, '我的世界模组开发', '自己做的，测试', 'https://127.0.0.1/test4.mp4')
task.set_callback(success)

# initialize manager
manager = Manager()
manager.add_client(client1)
# manager.add_client(client2)

# push task
manager.push_task(task)
# start manager
manager.run()
# unreachable code here. push task on another thread
# manager.push_task(task)
