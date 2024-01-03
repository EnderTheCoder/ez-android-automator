"""
@Time: 2024/1/3 21:03
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: make_all_usb_devices_tcpip.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""

import adbutils

cnt = 0

for device in adbutils.AdbClient().device_list():
    device.tcpip(5555)
    cnt += 1

print(f'Restarted {cnt} devices in tcpip mode.')
