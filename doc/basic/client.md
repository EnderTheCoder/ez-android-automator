# 客户端Client

## 创建

客户端（Client）在该系统中代表一台实际的手机，你可以使用两种方式来创建客户端：

- USB
- TCP/IP

### USB连接

使用USB创建客户端的实例：

```python
from ez_android_automator.client import create_usb_client

client = create_usb_client()
```

在有多个USB设备连接时，需要指定连接设备的serial序列号：

```python
from ez_android_automator.client import create_usb_client

client = create_usb_client('abc123')
```

### TCP/IP连接

使用TCP/IP地址创建客户端的实例：

```python
from ez_android_automator.client import create_network_client

client = create_network_client('192.168.3.52:5555')
```

需要注意的是，在使用TCP/IP创建客户端时需要指定端口，在大部分情况下是5555.

并且，使用该方式进行连接还需要安装目标设备的adbkey，这是一个用于认证控制设备的密钥文件。

adbkey和adbkey.pub两个文件是adb证书，如果想要连接到机器上，需要把这两个文件替换到windows的`C://Users/用户名/.android/`
目录下，或者linux的`/home/用户名/.android/`目录下
