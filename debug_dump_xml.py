import datetime
import time

import uiautomator2

from ez_android_automator.client import PublishClient

cli = PublishClient(uiautomator2.connect())
with open('sample/' + str(time.time()) + '.xml', 'w') as f:
    f.write(cli.dump_xml())