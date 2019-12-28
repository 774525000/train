# -*- coding:utf-8  -*-

import base64


def save_pic(url):
    try:
        with open('./static/pic.png', 'wb') as f:
            f.write(base64.b64decode(url.split(',')[1]))
    except Exception as e:
        print(f"保存图片失败:{e}")
        raise e


def get_pic():
    try:
        with open('./static/pic.png', 'rb') as f:
            im = f.read()
        return im
    except Exception as e:
        print(e)
        raise e
