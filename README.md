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
