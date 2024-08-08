"""
@Time: 2024/8/7 19:19
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: ym_helper.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import base64
from io import BytesIO
import requests


class YmClient:
    def __init__(self, token: str, c_type: str):
        self.c_type = c_type
        self.token = token

    def parse(self, image) -> int:
        """
        Parse captcha
        :param image: the captcha image
        :return: an int value representing a pixel where to stop the sliding
        """
        img_buffer = BytesIO()
        image.save(img_buffer, format='JPEG')
        byte_data = img_buffer.getvalue()
        response = requests.post('http://api.jfbym.com/api/YmServer/customApi', json={
            "token": self.token,
            "image": base64.b64encode(byte_data).decode(),
            "type": self.c_type
        }, headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            raise RuntimeError(
                f"YmServer response error, parse captcha failed. code {response.status_code}, msg {response.text}")
        return int(response.json()['data'])
