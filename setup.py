"""
@Time: 2023/11/20 21:39
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: setup.py.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
from setuptools import setup, find_packages

setup(
    name="ez-android-automator",
    version="0.1.0",
    description="Simple project based on ui-automator-2, used for controlling android devices",
    author="EnderTheCoder",
    author_email="ggameinvader@gmail.com",
    url="https://git.ender.cool/EnderTheCoder/ez-android-automator",
    packages=find_packages(),
    python_requires=">=3.10",
)
