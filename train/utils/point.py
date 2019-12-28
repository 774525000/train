# -*- coding:utf-8  -*-


def get_points(res):
    try:
        if res.get('pic_str'):
            pic_str = res['pic_str']
            return [item.split(',') for item in pic_str.split('|')]
    except Exception as e:
        print(e)
        raise e
