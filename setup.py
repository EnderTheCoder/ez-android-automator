"""
@Time: 2023/11/20 21:39
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: setup.py.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
from setuptools import setup

setup(
    name="ez_android_automator",
    version="1.1.4",
    description="Simple project based on ui-automator-2, used for controlling android devices",
    author="EnderTheCoder",
    author_email="ggameinvader@gmail.com",
    url="https://git.ender.cool/EnderTheCoder/ez-android-automator",
    packages=['ez_android_automator'],
    py_modules=['ez_android_automator'],
    python_requires=">=3.10",
    install_requires=["adbutils>=2.7.2", "beautifulsoup4>=4.12.2", "requests>=2.31.0", "uiautomator2>=3.2.2"]
)
