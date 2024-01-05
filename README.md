# EZ-ANDROID-AUTOMATOR

一个基于uiautomator2的安卓自动化项目，使用beautifulsoup来解析xml，并且提供外部可以调用的HTTP API

## adb证书

adbkey和adbkey.pub两个文件是adb证书，如果想要连接到机器上，需要把这两个文件替换到windows的`C://Users/用户名/.android/`目录下，或者linux的`/home/用户名/.android/`目录下

## 切换adb模式方法

adb在开机的时候默认运行在usb模式下，我们无法通过ip地址连接到机器，所以需要切换到tcpip模式下。
手动切换可以使用命令

```shell
adb -s 机器序列号 tcpip 端口号
```

其中端口号默认为5555

如果要查询机器的序列号，使用命令

```shell
adb devices
```

若要使用自动切换请按照以下步骤进行

1. 启动黑盒子
2. 连接黑盒子的usb到电脑上
3. 按下模式切换按钮（切换后指示灯为蓝色）
4. 运行自动切换脚本make_all_usb_devices_tcpip.py
5. 按下模式切换按钮（切换后指示灯为绿色）
6. 登陆路由器管理界面查看手机ip（默认为192.168.3.1，密码123456）
